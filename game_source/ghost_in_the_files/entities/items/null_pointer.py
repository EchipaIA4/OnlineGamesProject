from entities.inventory.item import Item

class NullPointer(Item):
    def __init__(self, name = "Null pointer", description = "A glitchy symbol item!", path = "assets/sprites/items/null_pointer.png", slot_size = None):
        super().__init__(name, description, path, slot_size)
