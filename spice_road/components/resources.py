from playtest.components import Component


class Resources(Component):
    def to_data(self):
        pass

    def reset(self):
        pass


class Caravan(Resources):
    """A set of resources, with a 10 item limit."""
    pass
