from entities.inventory.item import Item

class SystemCore(Item):
    def __init__(self, name = "System core", description = "Soul of the OS!", path = "assets/sprites/items/system_core.png", slot_size = None):
        super().__init__(name, description, path, slot_size)
