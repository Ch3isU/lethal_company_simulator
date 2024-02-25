import time
from utility import log_warning, read_bool, read_items_from_file
from player import Player
from monster import Monsters
import random
from random import normalvariate


def items_with_value(init_total_value):
    total_value = init_total_value
    if total_value <= 0:
        return []
    epsilon = 40
    items = read_items_from_file()
    idx = list(range(len(items)))
    random_values = [normalvariate(elem[1], elem[1]/10) for elem in items]
    inital_weights = [elem[2] if random_value < total_value else 0 for random_value, elem in zip(random_values, items)]
    panic_break = 10000
    # loot found = [name, value]
    loot_found = []
    while total_value > epsilon and panic_break > 0:
        selected_idx = random.choices(idx, weights=inital_weights, k=1)[0]
        if random_values[selected_idx] > total_value:
            inital_weights[selected_idx] = 0
            continue
        loot_found.append([items[selected_idx][0], random_values[selected_idx]])
        total_value -= random_values[selected_idx]
        inital_weights[selected_idx] -= 1
        random_values[selected_idx] = normalvariate(items[selected_idx][1], items[selected_idx][1]/10)
        if sum(inital_weights) <= 0:
            inital_weights = [elem[2] if random_value < total_value else 0 for random_value, elem in zip(random_values, items)]
        panic_break -= 1
    
    if len(loot_found) == 0:
        min_dist = abs(total_value - random_values[0])
        min_idx = 0
        for i, val in enumerate(random_values):
            dist = abs(val - total_value)
            if dist < min_dist:
                min_dist = dist
                min_idx = i
        return [[items[min_idx][0], int(total_value)]]
    need_to_add = total_value / len(loot_found)
    total_found = 0
    for loot in loot_found:
        loot[1] = round(loot[1] + need_to_add)
        total_found += loot[1]

    loot_found[0][1] += init_total_value - total_found
    return loot_found

def reduce_item_len(items, new_len):
    need_to_remove = len(items) - new_len
    if need_to_remove <= 0 or new_len < 1:    
        return items
    
    items.sort(key=lambda x: x[1])
    need_to_add = sum(e[1] for e in items[:need_to_remove+1])
    items = items[need_to_remove+1:]
    all_items = read_items_from_file()
    random_values = [normalvariate(elem[1], elem[1]/10) for elem in all_items]
    min_dist = abs(need_to_add - random_values[0])
    min_idx = 0
    for i, val in enumerate(random_values):
        dist = abs(val - need_to_add)
        if dist < min_dist:
            min_dist = dist
            min_idx = i
    items.append([all_items[min_idx][0], int(need_to_add)])
    random.shuffle(items)
    return items





class weathers:
    SUNNY = 1
    RAIN = 2
    STORMY = 3
    FOGGY = 4
    ECLIPSED = 5
    FLOODED = 6
    SNOWY = 7
    def as_string(weather):
        if weather == weathers.SUNNY:
            return "sunny"
        if weather == weathers.RAIN:
            return "rainy"
        if weathers == weathers.STORMY:
            return "stormy"
        if weather == weathers.FOGGY:
            return "foggy"
        if weather == weathers.ECLIPSED:
            return "eclipsed"
        if weather == weathers.FLOODED:
            return "flooded"
        if weather == weathers.SNOWY:
            return "snowy"
        log_warning(f"there is no name for weather no. {weather}")
        return "varies"


class Moon:
    def __init__(self, name, cost, dificulty, game, possible_weathers=[(weathers.SUNNY, 10)]) -> None:
        self.name = name
        self.cost = cost
        self.dificulty = dificulty
        self.game = game
        self.possible_weathers = possible_weathers
        self.current_weather = self.determin_weather()
    
    def determin_weather(self):
        weather_list = []
        weight_list = []

        for weather, weight in self.possible_weathers:
            weather_list.append(weather)
            weight_list.append(weight)

        return random.choices(weather_list, weights=weight_list, k=1)[0]
    
    def get_Monsters(self):
        return [Monsters.BRACKEN, Monsters.SPIDER, Monsters.THUMPER, Monsters.SNAREFLEE,  Monsters.EYELESS_DOG]

    def get_possible_events(self):
        """returns a list with all possible event numbers and a dificulty for said event"""
        possible_events = [(0, 1), (1, 2)]
        # todo add other events
        return possible_events

    def determin_event(self):
        """determins which event will be run"""
        event_ids = []
        event_frequencies = []
        for event in self.get_possible_events():
            event_ids.append(event[0])
            event_frequencies.append(event[1])

        return random.choices(event_ids, weights=event_frequencies, k=1)[0]


    def event(self, num):
        """runs event with associated with number num
        returns number of loot gained/lost
        """
        if num == 0:
            # clumsiest player dies due to monster
            try:
                clumsiest = self.game.alive_players[0]
                for player in self.game.alive_players:
                    if player.clumsiness > clumsiest.clumsiness:
                        clumsiest = player
            except Exception as e:
                log_warning(f"player list of game does not work as intended\n {e} \n")
                clumsiest = Player(name="Steve", weappon_strength=0, clumsiness=10)

            monster = random.choice(self.get_Monsters())
            lost_loot = int(random.normalvariate(2.5*clumsiest.clumsiness, self.dificulty+1))
            print(f"{monster.death_message(clumsiest.name)} He lost items worth {lost_loot} credits")
            return -lost_loot, [clumsiest]
        
        if num == 1:
            try:
                selected_player = random.choice(self.game.alive_players)
            except Exception as e:
                log_warning("player list of game does not work as intended (might be empty)\n")
                selected_player = Player(name="Steve", weappon_strength=0, clumsiness=10)

            print(f"{selected_player.name} has found a present. There might be a valueable Item inside. But it could be everything.")
            value = round(random.normalvariate(20 + self.dificulty * 10, 5 + self.dificulty))
            if value < 0:
                value = 0
            monster_kills = random.randint(1, 100) > 45 + selected_player.current_disadvantage*2
            if read_bool(f"Should {selected_player.name} open it?"):
                if monster_kills:
                    monster = random.choice(self.get_Monsters())
                    print(f"After opening the present a {monster.name} jumps out of the box. {selected_player.name} did not survive.")
                    return 0, [selected_player]
                else:
                    print(f"{selected_player.name} opens the present. Inside was loot worth {value} credits.")
                    return value, []
            else:
                if monster_kills:
                    print("The present remains sealed. Your crew is very grateful, as the gift looks very ominous.")
                else:
                    if value > 20 + self.dificulty * 10: 
                        print("The present remains sealed. Your crew thinks the content might have been valueable.")
                        return 0, []
                    else: 
                        print("The present remains sealed. Your crew thinks the content would not have been that valueable anyway.")
                        return 0, []


            


    def run_simulation(self):
        extra_loot_today = 0
        events_today = 3
        for i in range(events_today):
            selected_event_id =  self.determin_event()
            print(selected_event_id, " is beeing played")
            try:
                stuff, players_killed = self.event(selected_event_id)
                if players_killed is None:
                    players_killed = []
                killed_player_names = [player.name for player in players_killed]

                for i, player in enumerate(self.game.alive_players):
                    if player.name in killed_player_names:
                        self.game.alive_players.pop(i)
                extra_loot_today += stuff   
                print(f"players: {[p.name for p in self.game.players]}")
                print(f"alive players: {[p.name for p in self.game.alive_players]}")
            except Exception as e:
                log_warning(f"Well i dont know something fucked something up when doing the event no. {selected_event_id} {e}")

        alive = self.game.alive_players
        total_disadvantage = 0
        for player in alive:
            total_disadvantage += player.current_disadvantage
        if len(self.game.alive_players) == 0:
            return []
        mu = len(alive) * (25 + (10 * (1 + self.dificulty)) - (total_disadvantage * 3))
        var = len(alive) * (1 + self.dificulty) 
        base_loot_found = round(normalvariate(mu, var))
        total_value_found = base_loot_found + extra_loot_today
        needed_loot = self.game.quota_amount - self.game.ship.get_total()
        if self.game.days_till_quota == 1 and 0 < needed_loot < self.game.despair:
            total_value_found += needed_loot
            self.game.despair -= needed_loot

        return items_with_value(total_value_found)


class Experimentation(Moon):
    def __init__(self, game) -> None:
        super().__init__(name="Experimentation", cost=0, dificulty=0, game=game)

class Rend(Moon):
    def __init__(self, game) -> None:
        super().__init__(name="Rend", cost=550, dificulty=9, game=game, possible_weathers=[(weathers.SUNNY, 1), (weathers.RAIN, 1), (weathers.STORMY, 1), (weathers.FLOODED, 1), (weathers.FOGGY, 1), (weathers.ECLIPSED, 1), (weathers.SNOWY, 1)])

class CompanyBuilding(Moon):
    def __init__(self, game) -> None:
        super().__init__(name="Company", cost=0, dificulty=0, game=game, possible_weathers=[(weathers.SUNNY, 1)])
        self.confirm = True
    def run_simulation(self):
        print("Welcome to the Company Building. Here you can sell your scrap.")

        print(f"Loot in your ship totals at {self.game.ship.get_total()}.")

        while True:    
            print(f"to sell an item type 'sell <item number>' or 'sell all' to sort the list type 'sort'. Type 'skipconfirm' to skip/enable confirmation when selling an item. Type 'quota' to see details about your current quota.")
            print(f"When you are done selling items type 'leave'")
            print(f"Here are your items.")
            for i, elem in enumerate(self.game.ship.loot):
                print(f"{i}, {elem[0]}, {elem[1]}")

            player_input = input("\n")
            possible_commands = ["sell", "sort", "skipconfirm", "leave", "quota"]
            parts = player_input.split()
            command = parts[0].lower()
            args = parts[1:]
            if command not in possible_commands:
                print(f"There was no action supplied with command {command}")
                continue
            if command == "leave":
                return []
            if command == "sell":
                if args[0] == "all":
                    if self.confirm:
                        if not read_bool(f"do you want to sell all items for {self.game.ship.get_total()} credits?"):
                            print("no item was sold.")
                            continue
                    self.game.money += self.game.ship.get_total()
                    self.game.quota_amount -= self.game.ship.get_total()
                    if self.game.quota_amount < 0:
                        self.game.quota_amount = 0
                    self.game.ship.loot = []
                    print("all items sold")
                    continue
                try:
                    index = int(args[0])
                    selected_item = self.game.ship.loot[index]
                    if self.confirm:
                        if not read_bool(f"do you want to sell {selected_item[0]} for {selected_item[1]} credits?"):
                            print("no item was sold.")
                            continue
                    
                    earned_money = self.game.ship.sell_item(index)
                    self.game.money += earned_money
                    self.game.quota_amount -= earned_money
                    if self.game.quota_amount < 0:
                        self.game.quota_amount = 0
                    
                    print("item sold")
                except Exception as e:
                    print(f"there was no item with the given item number {args[0]}")

            if command == "sort":
                self.game.ship.loot.sort(key=lambda x: x[1])
                continue

            if command == "skipconfirm":
                self.confirm = not self.confirm

            if command == "quota":
                print(f"you have {self.game.days_till_quota} days left to sell items worth {self.game.quota_amount}")

    