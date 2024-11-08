from random import choice

from busy.command import QueueCommand


class DropCommand(QueueCommand):
    """Move items to the end of the todo collection of a queue"""

    name = 'drop'
    default_filter = [1]

    @QueueCommand.wrap
    def execute(self):
        collection = self.app.storage.get_collection(self.queue)
        if self.selection:
            lolist, hilist = self.collection.split(self.selection)
            self.collection.data = hilist + lolist
        self.set_next_item_status()


class PopCommand(QueueCommand):
    """Move items to the beginning of the collection"""

    name = 'pop'
    default_filter = ['-']

    @QueueCommand.wrap
    def execute(self):
        collection = self.app.storage.get_collection(self.queue)
        if self.selection:
            hilist, lolist = self.collection.split(self.selection)
            self.collection.data = hilist + lolist
        self.set_next_item_status()


class PickCommand(QueueCommand):
    """Move a random item to the beginning of the collection"""

    name = 'pick'
    default_filter = ['1-']

    @QueueCommand.wrap
    def execute(self):
        if self.selection:
            index = choice(self.selection)
            item = self.collection[index]
            hilist, lolist = self.collection.split([index])
            self.collection.data = hilist + lolist
        self.set_next_item_status()
