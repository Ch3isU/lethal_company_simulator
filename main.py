import random
from player import Player
from game import Game
from utility import log_warning

def read_player_numbers():
    premium_player_count = -1
    while(premium_player_count < 0):
        try:
            premium_player_count = int(input("Select amount of premium players:"))
        except:
            continue
    other_player_count = -1
    while(other_player_count < 0):
        try:
            other_player_count = int(input("Select amount of other players:"))
        except:
            continue
    return premium_player_count, other_player_count

def read_players_from_file(filename):
    playername_file = open(filename, 'r')
    players = []
    for line in playername_file:
        if line.startswith("#"):
            continue
        elems = line.split(" ")
        if len(elems) != 3:
            log_warning(f"a line containing playerinformation in file {filename} is not formatted correctly")
            continue
        try:
            players.append(Player(elems[0], int(elems[1]), int(elems[2])))
        except:
            log_warning(f"a line containing playerinformation in file {filename} is not formatted correctly")
    return players



def read_bool(question):
    answer = ""
    while answer != "yes" and answer != "no":
        answer = input(question)
    if answer == "yes":
        return True
    elif answer == "no":
        return False
    else:
        log_warning("I fucked up somehow (yes or no is maybe)")
        return False

def main():
    print("Welcome to Lethal Company Simulator")
    print()
    
    premium_player_count = 0
    other_player_count = 0

    while premium_player_count + other_player_count <= 0:
        premium_player_count, other_player_count = read_player_numbers()


    premium_players = read_players_from_file('src/premium_crew.txt')

    if premium_player_count > len(premium_players):
        print(f"could only provide {len(premium_players)} premium players")
        premium_player_count = len(premium_players)

    selected_premium_players = random.sample(premium_players, premium_player_count)
    

    other_players = read_players_from_file('src/crew_names.txt')

    if other_player_count > len(other_players):
        print(f"could only provide {len(other_players)} players")
        other_player_count = len(other_players)

    print()
    selected_base_players = random.sample(other_players, other_player_count)

    selected_player_names = [elem.name for elem in selected_premium_players + selected_base_players]
    print()
    print(f"your crew consists of {selected_player_names}")


    game = Game(players = selected_premium_players + selected_base_players, money=2500)
    game.run()




if __name__ == "__main__":
    main()

