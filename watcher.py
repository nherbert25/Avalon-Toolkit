class Watcher:
    """ A simple class, set to watch its variable. """

    def __init__(self, value):
        self.variable = value

    def set_value(self, new_value):
        if self.variable != new_value:
            self.pre_change()
            self.variable = new_value
            self.post_change()

    def pre_change(self):
        # do stuff before variable is about to be changed
        pass

    def post_change(self):
        # do stuff right after variable has changed
        pass
