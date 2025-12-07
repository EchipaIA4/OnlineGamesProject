from entities.item import Item

class MemoryChip(Item):
    def __init__(self, name = "Memory chip", description = "Can fill up ram!", path = "assets/sprites/memory_chip.png", slot_size = None):
        super().__init__(name, description, path, slot_size)
