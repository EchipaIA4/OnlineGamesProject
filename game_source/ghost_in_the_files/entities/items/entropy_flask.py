from entities.inventory.item import Item

class EntropyFlask(Item):
    def __init__(self, name = "Entropy flask", description = "A weird liquid-like digital container.", path = "assets/sprites/items/entropy_flask.png", slot_size = None):
        super().__init__(name, description, path, slot_size)
