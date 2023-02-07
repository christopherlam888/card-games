import cards
from cards import Deck
from cards import FrenchDeck

import pyfiglet

class Baccarat:
    
    # default constructor
    def __init__(self, num):
        self.num_decks = num
        self.deck = FrenchDeck(self.num_decks)
        self.deck.shuffle()
        self.player_score = 1000
        self.strategy_score = 1000

    # calculate a hand value
    def hand_value(self, hand):
        value = 0
        for card in hand:
            if card.rank in ['J', 'Q', 'K']:
                value += 0
            elif card.rank == 'A':
                value += 1
            else:
                value += int(card.rank)
        value = value%10
        return value

    # print the player hand
    def print_player_hand(self, player_hand):
        print("Player:", *[card.rank for card in player_hand])
        print()
    
    # print the banker hand
    def print_banker_hand(self, banker_hand):
        print("Banker:", *[card.rank for card in banker_hand])
        print()

    # determine player move
    def player_move(self, hand):
        return

    # determine banker move
    def banker_move(self, hand):
        return

    # determine result
    def determine_result(self, player_hand, banker_hand, bet, strategy_bet):
        if self.hand_value(player_hand) == self.hand_value(banker_hand):
            if bet[1] == 't':
                self.player_score += bet[0]*8
                print("Win")
            else:
                print("Tie")
            self.strategy_score -= strategy_bet[0]
        elif self.hand_value(player_hand) > self.hand_value(banker_hand):
            if bet[1] == 'p':
                self.player_score += bet[0]
                print("Win")
            else:
                self.player_score -= bet[0]
                print("Lose")
            self.strategy_score -= strategy_bet[0]
        else:
            if bet[1] == 'b':
                self.player_score += bet[0]
                print("Win")
            else:
                self.player_score -= bet[0]
                print("Lose")
            self.strategy_score += strategy_bet[0]

    # play a hand
    def play_hand(self):

        player_hand = []
        banker_hand = []

        # prompt for bet
        print("Score: ", self.player_score)
        bet = []
        bet_amount = input("Place your bet (5): ")
        if bet_amount.isdigit() and int(bet_amount)%5 == 0:
            bet.append(int(bet_amount))
        else:
            bet.append(5)
        bet_type = input("Place your bet (Player P, Banker B, Tie T): ").lower()
        if bet_type in ['p', 'b', 't']:
            bet.append(bet_type)
        else:
            bet.append('p')
        strategy_bet = [5, 'b']
        print()

        #deal starting hands
        player_hand = ([self.deck.draw_card(), self.deck.draw_card()])
        banker_hand = ([self.deck.draw_card(), self.deck.draw_card()])

        self.print_player_hand(player_hand)
        self.print_banker_hand(banker_hand)

        # check for natural win
        if self.hand_value(player_hand) in [8, 9] or self.hand_value(banker_hand) in [8, 9]:
            self.determine_result(player_hand, banker_hand, bet, strategy_bet)
        
        # deal third card
        else:
            if self.hand_value(player_hand) <= 5:
                player_hand.append(self.deck.draw_card())
                if player_hand[2].rank == '8':
                    if self.hand_value(banker_hand) <= 2:
                        banker_hand.append(self.deck.draw_card())
                elif player_hand[2].rank in ['6', '7']:
                    if self.hand_value(banker_hand) <= 6:
                        banker_hand.append(self.deck.draw_card())
                elif player_hand[2].rank in ['4', '5']:
                    if self.hand_value(banker_hand) <= 5:
                        banker_hand.append(self.deck.draw_card())
                elif player_hand[2].rank in ['2', '3']:
                    if self.hand_value(banker_hand) <= 4:
                        banker_hand.append(self.deck.draw_card())
                else: 
                    if self.hand_value(banker_hand) <= 3:
                        banker_hand.append(self.deck.draw_card())
            else:
                if self.hand_value(banker_hand) <= 5:
                    banker_hand.append(self.deck.draw_card())

            self.print_player_hand(player_hand)
            self.print_banker_hand(banker_hand)

            self.determine_result(player_hand, banker_hand, bet, strategy_bet)

        print()

        # print scores
        print("Player Score: ", self.player_score)
        print("Strategy Score: ", self.strategy_score)
        print()

    # play the game
    def play(self):
        print(pyfiglet.figlet_format("Baccarat"))
        while(input("Play hand? (y/N) ").lower() == 'y'):
            print()
            self.play_hand()
            # new deck if less than one deck's number of cards remain
            if len(self.deck.cards) < 52:
                self.deck = FrenchDeck(self.num_decks)
