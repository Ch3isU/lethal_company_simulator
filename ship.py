from utility import log_warning
class Ship:
    def __init__(self) -> None:
        self.loot = []

    def add_item_list(self, item_list):
        if len(item_list) == 0:
            return
        for item in item_list:
            try:
                if len(item) == 2:
                    self.add_item(item[0], item[1])
                else:
                    log_warning("I fucked up when adding list of items to ship (len != 2)")
            except:
                log_warning("I fucked up when adding list of items to ship (no list? idk)")
                continue
    def add_item(self, name, value):
        if value < 0:
            value = 0
        self.loot.append((name, value))

    def get_total(self):
        if len(self.loot) == 0:
            return 0
        sum = 0
        for item in self.loot:
            sum += item[1]
        return sum
    
    def sell_item(self, index):
        try:
            val = self.loot[index][1]
            self.loot.pop(index)
        except IndexError as e:
            log_warning("i fucked up when selling an item..")
            return 0
        return val