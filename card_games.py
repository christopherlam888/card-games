from blackjack import Blackjack
from baccarat import Baccarat

import pyfiglet

GAMES = [Blackjack, Baccarat]


def get_num_decks(default):
    try:
        num_decks = int(input(f"How many decks? ({default}) "))
        if num_decks < 1:
            raise ValueError
    except ValueError:
        num_decks = default
    return num_decks


def main():
    print(pyfiglet.figlet_format("Card Games"))

    while True:
        user_game = input(
            f"What game would you like to play? ({', '.join(game.name for game in GAMES)}) "
        ).lower()

        for game in GAMES:
            if user_game == game.id:
                instance = game(get_num_decks(game.default_num_decks))
                instance.play()
                break


if __name__ == "__main__":
    main()
