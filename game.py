from ship import Ship
from moon import Moon, Experimentation, Rend, weathers, CompanyBuilding
from player import Player
from item import Items
import random
from utility import read_bool

class Game:
    def __init__(self, players: list[Player], money=25) -> None:
        self.ship = Ship()
        self.despair = 50
        self.money = money
        self.days_till_quota = 3
        self.quota_amount = 130
        self.quota_count = 1
        self.players = players
        self.moon = Experimentation(self)
        self.moon.current_weather = weathers.SUNNY
        self.moons = [self.moon, Rend(self), CompanyBuilding(self)]
        self.alive_players = players[:]
        self.owned_items = []

    def introduction():
        print("You are a contracted worker for the Company. Your job is to coordinate your crew members to collect scrap from abandoned, industrialized moons to meet the Company's profit quota.\n"
              "You can use the cash you earn to travel to new moons with higher risks and buy items that help your crew on your journey.\n"
              "You control everything from the ships computer. To start the game type 'land' to see other options type 'help'")
        

    def handle_input(self):
        ip = input("\n")
        possible_commands = ["help", "moons", "land", "route", "debug", "quota", "store", "quit", "buy"]
        while True:
            parts = ip.split()
            command = parts[0].lower()
            args = parts[1:]

            if command not in possible_commands:
                print("There was no action supplied with that word. To see other options type 'help'")
                ip = input("\n")
            else:
                break

        if command == "help":
            print("'help' shows possible options.")
            print("'moons' shows a list of accessible moons you can fly to.")
            print("'store' shows the companies store selection.")
            print("'route <moon>' selects <moon> as the desired moon to fly to when landing.")
            print("'buy <item>' buy an item from the company store.")
            print("'land' lands the shop on the selected moon.")
            print("'quota' shows you further accountabilities regarding your teams quota.")
            print("'quit' quits the game. However there is no saving.")
        elif command == "moons":
            print("Welcome to the Moon selection. To change the selected moon and route to another moon type 'route <moon>'")
            print("-------------------")
            for moon in self.moons:
                print(f"* {moon.name} ({weathers.as_string(moon.current_weather)}) | cost {moon.cost}")
        elif command == "quota":
            print(f"you have {self.days_till_quota} days left to sell items worth {self.quota_amount}")
        elif command == "quit":
            return True
        elif command == "store":
            print("Welcome to the Company store. To buy an item type 'buy <item>'")
            print("-------------------")
            for elem in Items.get_items():
                print(f"{elem.name}: {elem.description} | {elem.cost}")

        elif command == "buy":
            if len(args) == 0:
                print("Please specify an item after 'buy'.")
            else:
                selected_item = " ".join(args).lower()
                found = False
                for buyable in Items.get_items():
                    if buyable.name.startswith(selected_item):
                        found = True
                        if read_bool(f"do you want to buy the item {buyable.name} for {buyable.cost} credits?\n"):
                            if buyable.cost > self.money:
                                print("Not enough money available.")
                            else:
                                self.money -= buyable.cost
                                self.owned_items.append(buyable)
                                print(f"your new credit balance is {self.money}.")
                        else:
                            print(f"Process was cancelled.")
                if not found:
                    print(f"the selected item {selected_item} was not found in the list of available items.\n To show a list of buyable items type >store<.")

        elif command == "route":
            if len(args) == 0:
                print("Please specify a moon after 'route'.")
            else:
                selected_moon = " ".join(args).capitalize()
                found = False
                for moon in self.moons:
                    if moon.name.startswith(selected_moon):
                        found = True
                        if read_bool(f"do you want to redirect the ship to {moon.name} for {moon.cost} credits?\n"):
                            if moon.cost > self.money:
                                print("Not enough money available.")
                            else:
                                self.money -= moon.cost
                                self.moon = moon
                                print(f"your new credit balance is {self.money}.")
                                print(f"the ship is heading towards {self.moon.name}.")
                        else:
                            print(f"Process was cancelled. The ship is still on course to {self.moon.name}")
                if not found:
                    print(f"the selected moon {selected_moon} was not found in the list of available moons.\n To show a list of accessible moons type >moons<")
                
        elif command == "debug":
            print(f"money: {self.money}")
            print(f"despair: {self.despair}")
            print(f"ship.loot: {self.ship.loot}")
            print(f"players: {[p.name for p in self.players]}")
            print(f"alive players: {[p.name for p in self.alive_players]}")
            print(f"current selected moon: {self.moon}")
        
        elif command == "land":
            print(f"You are landing on {self.moon.name}. Your Crew leaves.")
            items_found = self.moon.run_simulation()
            print(f"The day is over. {[p.name for p in self.alive_players]} return to the ship.")
            print(f"They have brought: {items_found}.")
            self.ship.add_item_list(item_list=items_found)
            print(f"Your new ship total comes to {self.ship.get_total()}")
            self.alive_players = self.players[:]
            if self.days_till_quota <= 0:
                print("the time to reach the quota is up.")
                if self.quota_amount > 0:
                    print(f"you did not fullfill the required amount for quota no. {self.quota_count} within the deathline. You missed the quota by {self.quota_amount} credits. As a consequence you have to leave the companies ship. Good Luck in Space.")
                    return True
                else:
                    print("Congratulations on achieving the required quota.")
                    self.quota_count += 1
                    self.quota_amount = int(130 + 100 *  (1 + self.quota_count ** 2 / 16) * (random.random() + 1))
                    self.days_till_quota = 3
                    print(f"your new quota is set at {self.quota_amount}. You have {self.days_till_quota} days left to fullfill the quota.")
            else:
                self.days_till_quota -= 1
                
            if self.days_till_quota == 0:
                print("you have ZERO days left to sell your items at the company building. To redirect the ship type 'route Company'.")
            

            self.days_till_quota -= 0

        return False

    def run(self):
        Game.introduction()
        quit = False
        while(not quit):
            quit = self.handle_input()
