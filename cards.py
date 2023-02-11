from collections import namedtuple
from itertools import product
from random import shuffle
from typing import List

Card = namedtuple("Card", ("rank", "suit"))


class Deck:
    card_ranks = []
    card_suits = []

    def __init__(self, num):
        self.cards = []
        for _ in range(num):
            self.add_deck()
        self.shuffle()

    def add_deck(self):
        self.cards.extend(
            [
                Card(rank, suit)
                for rank, suit in product(self.card_ranks, self.card_suits)
            ]
        )

    def shuffle(self):
        shuffle(self.cards)

    def draw_card(self) -> Card:
        return self.cards.pop()


class FrenchDeck(Deck):
    card_ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    card_suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
