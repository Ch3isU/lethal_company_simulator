from utility import read_bool
from game import Game
import random

class roundbased:
    def __init__(self, game:Game, final_pos, max_rounds) -> None:
        self.game = game
        self.final_pos = final_pos
        self.max_rounds = max_rounds
        self.current_pos = 0
        self.pattern = {}
        self.narrate = {}
    
    def get_player_input(self, round):
        return True
    
    def bad_ending(self, round):
        pass

    def good_ending(self, round):
        pass

    def out_of_turns(self):
        pass

    def update_pos(self, player_input):
        if player_input:
            return self.current_pos + 1
        else:
            return self.current_pos


    def check_finished(self):
        return self.current_pos >= self.final_pos

    def run(self):
        for round in range(self.max_rounds):
            # narrate the situaltion
            if self.narrate.get(round) is not None:
                self.narrate.get(round)()
            
            # get player input
            p_input = self.get_player_input(round)

            # play round based on player input
            if self.pattern.get(round) is not None:
                alive = self.pattern.get(round)(self.current_pos, p_input)
            else:
                alive = True

            if not alive:
                return self.bad_ending(round)
                
            
            self.current_pos = self.update_pos(p_input)

            if self.check_finished():
                return self.good_ending(round)
            
        return self.out_of_turns()
    
class Avalanche(roundbased):
    def __init__(self) -> None:
        super().__init__(final_pos=4, max_rounds=9)
        # narrating functions
        def a():
            print("Snow starts to fall from the Mountain. An Avalanche forms behind you and starts sliding down the Mountain.\n")
        def b():
            print("Snow starts to fall from the Mountain. An Avalanche forms in front of you and starts sliding down the Mountain.\n")

        # check if dead functions
        def f3(pos, p_input):
            print("the Avalanche covers the last part of the route in front of your crew. \n")
            if (pos == 3) and p_input == True:
                return False
            else: 
                return True
        
        def f12(pos, p_input):
            print("the Avalanche reaches the middle part of the route. \n")
            if (pos == 1 or pos == 2) and p_input == True:
                return False
            else: 
                return True

        def f0(pos, p_input):
            print("the Avalanche covers the first part of the route behind your crew. \n")
            if pos == 0 and p_input == True:
                return False
            else: 
                return True

        possible_check_alive = [
            {1: f0, 2: f12, 3:f3},  {2: f0, 3: f12, 4:f3}, {2: f0, 3: f12, 4:f3}, {1: f3, 2: f12, 3: f0}, {2: f3, 3: f12, 4: f0}, {2: f3, 3: f12, 4: f0}
        ]
        possible_narrate = [
            {0: a}, {0: a}, {1: a}, {1: b}, {1: b}, {2: b}
        ]

        index = random.randint(0, len(possible_check_alive)-1)
        self.pattern = possible_check_alive[index]
        self.narrate = possible_narrate[index]

    def get_player_input(self, round):
        
        if self.current_pos == 2:
            print("Your crew is wandering through the snow looking for a safe place.\n")
            if round > 7:
                print("Your crew can`t handle the cold any longer. You need to get to safety as quick as possible.\n")
            elif round > 4:
                print("Your crew starts to freeze. You should hurry.\n")
            selection = True

        elif self.current_pos == 0:
            print("Your crew is currently safe. The way to the next safe point should not be too far away. \n")
            if round > 7:
                print("Your crew can`t handle the cold any longer. You need to get to safety as quick as possible.\n")
            elif round > 4:
                print("Your crew starts to freeze. You should hurry.\n")
            selection = read_bool("do you want to leave and go?\n")

        elif self.current_pos == 1:
            print("Your crew has already completed a quarter of the route. The way to the next safe point is far away.\n")
            if round > 7:
                print("Your crew can`t handle the cold any longer. You need to get to safety as quick as possible. \n")
            elif round > 4:
                print("Your crew starts to freeze. You should hurry. \n")
            selection = read_bool("do you want to leave and go?\n")

        elif self.current_pos == 3:
            print("Your crew has almost reached its destination.\n")
            if round > 7:
                print("Your crew can`t handle the cold any longer. You need to get to safety as quick as possible. \n")
            elif round > 4:
                print("Your crew starts to freeze. You should hurry. \n")
            selection = read_bool("do you want to leave and go now?\n")

        return selection

    def bad_ending(self, round):
        print("Your crew was swept away by the avalanche. There are no survivors and all collected loot is lost. \n")
        return 0, self.game.alive_players

    def good_ending(self, round):
        print("Your crew got out!")
        if round > 5:
            print("However they have suffered from the cold.\n")
        return 0, []
        

    def out_of_turns(self):
        print("Your crew stayed out in the cold for too long and froze to death. \n")
        return 0, self.game.alive_players

