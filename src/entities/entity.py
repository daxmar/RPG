import uuid

class Entity:
    def __init__(self, name="Unknown"):
        self.id = uuid.uuid4()
        self.components = {}

    def add_component(self, component):
        self.components[type(component)] = component
        return self

    def get_component(self, component_type):
        return self.components.get(component_type)

    def has_component(self, component_type):
        return component_type in self.components