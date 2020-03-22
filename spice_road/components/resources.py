from playtest.components import Component


class Resource(Component):
    def to_data(self):
        pass

    def reset(self):
        pass


class Caravan(Resource):
    """A set of resources, with a 10 item limit."""

    def discard_to(self, down_to: int):
        raise NotImplementedError()
