import re
from dataclasses import KW_ONLY, dataclass
from datetime import date, datetime

from busy.util.date_util import absolute_date
from busy.util.date_util import relative_date
from busy.util import date_util


class ItemStateError(Exception):
    pass


START_TIME_FORMAT = '%Y%m%d%H%M'


@dataclass
class Item:

    description: str
    _: KW_ONLY
    state: str = 'todo'
    done_date: date = None
    plan_date: date = None

    def __str__(self):
        """Represent the item as its simple form"""
        return self.simple

    def restricted(*allowed_states):
        """Restrict a method to a specific set of states"""
        def wrapper(method):
            def replacement(self, *args, **kwargs):
                if self.state in allowed_states:
                    return method(self, *args, **kwargs)
                else:
                    raise ItemStateError
            return replacement
        return wrapper

    # Older versions of Busy supported an elaborate "followon" mechanism

    FOLLOW_SPLIT = re.compile(r'\s*\-*\>\s*')
    LEGACY_REPEAT = re.compile(r'^\s*repeat(?:\s+[io]n)?\s+(.+)\s*$', re.I)

    def __setattr__(self, name, value):
        if self.__annotations__[name] == date:
            value = absolute_date(value)
        super().__setattr__(name, value)

    @property
    def _words(self):
        return self.body.split()

    def _marked(self, mark):
        return [w[1:] for w in self._words if w.startswith(mark)]

    # ---- Interface for use by integrations ----

    @property
    def tags(self):
        """Set of all words starting with #"""
        return {m.lower() for m in self._marked('#')}

    @property
    def url(self):
        """The first word starting with @"""
        return (self._marked('@') + ['']).pop(0)

    def data_value(self, key: str):
        """Value of word starting with % and the provided key"""
        return next((m[1:] for m in self._marked("%") if m[0] == key), None)

    @property
    def elapsed(self):
        if 'e' in self.timing_data:
            return int(self.timing_data['e'])
        else:
            return 0

    @property
    def base(self):
        """body description with no tags, resource, or data"""
        wins = [w for w in self._words if w[0] not in '#@!%']
        return " ".join(wins)

    # ----

    @property
    def timing_data(self):
        """Dict of words starting with !"""
        return {m[0]: m[1:] for m in self._marked("!")}

    @property
    def start_time(self):
        if 's' in self.timing_data:
            return datetime.strptime(self.timing_data['s'], START_TIME_FORMAT)

    @property
    def simple(self):
        """Base plus tags"""
        wins = [w for w in self._words if w[0] not in '@!']
        return " ".join(wins)

    @property
    def listable(self):
        """Simple plus repeat"""
        if self.repeat_text:
            return f"{self.simple} > {self.repeat_text}"
        else:
            return self.simple

    @property
    def nodata(self):
        """Everything but the bang data"""
        wins = [w for w in self._words if w[0] not in '!']
        return " ".join(wins)

    @property
    def repeat_text(self):
        """Second and successive segments, all but body"""
        split = self.FOLLOW_SPLIT.split(self.description, maxsplit=1)
        if len(split) > 1:
            next = split[1]
            # Legacy "repeat" text
            match = self.LEGACY_REPEAT.match(next)
            if match:
                return match.group(1)
            else:
                return next
        else:
            return ""

    @property
    def body(self):
        """Without the repeat followon"""
        split = self.FOLLOW_SPLIT.split(self.description, maxsplit=1)
        if split:
            return split[0]
        else:
            return ""

    @property
    def repeat_date(self):
        text = self.repeat_text
        if text:
            return relative_date(text)

    @restricted('todo')
    def done(self, done_date: date, plan_date: date = None):
        """Updates the item to done and returns a copy as a plan for the
        plan_date if provided"""
        self.state = 'done'
        self.done_date = done_date
        plan_description = self.nodata
        if self.repeat_text:
            plan_description += f" > {self.repeat_text}"
        self.description = self.body
        if plan_date:
            return Item(plan_description, state='plan', plan_date=plan_date)

    @restricted('done')
    def undone(self):
        self.state = 'todo'

    @restricted('todo')
    def plan(self, plan_date: date):
        self.state = 'plan'
        self.plan_date = plan_date

    @restricted('plan')
    def unplan(self):
        self.state = 'todo'

    @restricted('todo')
    def update_time(self):
        """Update elapsed time based on start time"""
        if self.start_time and self.base:
            prev = self.elapsed
            new = (date_util.now() - self.start_time).seconds // 60
            elapsed = new + prev
            changed = f"{self.nodata} !e{elapsed}"
            if self.repeat_text:
                changed += f" > {self.repeat_text}"
            self.description = changed

    @restricted('todo')
    def start_timer(self):
        if self.base and not self.start_time:
            start = date_util.now().strftime(START_TIME_FORMAT)
            elapsed = self.elapsed
            changed = f"{self.nodata} !s{start}"
            if elapsed:
                changed += f" !e{elapsed}"
            if self.repeat_text:
                changed += f" > {self.repeat_text}"
            self.description = changed

    # ---- named filers ----

    def filter_donemin(self, min_date):
        if self.done_date:
            return self.done_date >= absolute_date(min_date)

    def filter_donemax(self, max_date):
        if self.done_date:
            return self.done_date <= absolute_date(max_date)

    def filter_planmin(self, min_date):
        if self.plan_date:
            return self.plan_date >= absolute_date(min_date)

    def filter_planmax(self, max_date):
        if self.plan_date:
            return self.plan_date <= absolute_date(max_date)
