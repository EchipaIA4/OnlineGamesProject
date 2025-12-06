from entities.item import Item

class Key(Item):
    def __init__(self, name = "Key", description = "Can unlock things!", path = "assets/sprites/key.png", slot_size = None):
        super().__init__(name, description, path, slot_size)
