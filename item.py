
class item:
    def __init__(self, name, cost, description=None) -> None:
        self.name = name
        self.cost = cost
        if description is not None:
            self.description = description 
        else: self.description = f"An item that might come in handy later"

class Items:
    # id, name, cost
    WALKY_TALKY = item("walky talky", 10, "Used to communicate over a long distance")
    FLASHLIGHT = item("flashlight", 15, "Brightens up even the darkest places")
    SHOVEL = item("shovel", 30, "Used for digging. Or to hit others.")
    SHOWBOOTS = item("snowboots", 50, "Enable easy travelling even in the deepest snow")

    def get_items():
        return [Items.WALKY_TALKY, Items.FLASHLIGHT, Items.SHOVEL, Items.SHOWBOOTS]
