from blackjack import Blackjack
from baccarat import Baccarat

import pyfiglet

def main():
    print(pyfiglet.figlet_format("Card Games"))

    playing = True
    while(playing):
        user_game = input("What game would you like to play? (Blackjack, Baccarat) ").lower()

        #blackjack
        if user_game == "blackjack":
            num_decks = 6
            user_num_decks = input("How many decks? (6) ")
            if user_num_decks.isdigit() and int(user_num_decks) >= 1:
                num_decks = int(user_num_decks)
            game = Blackjack(num_decks)
            game.play()

        # baccarat
        elif user_game == "baccarat":
            num_decks = 8
            user_num_decks = input("How many decks? (8) ")
            if user_num_decks.isdigit() and int(user_num_decks) >= 1:
                num_decks = int(user_num_decks)
            game = Baccarat(num_decks)
            game.play()

        else:
            playing = False

if __name__ == "__main__":
    main()
