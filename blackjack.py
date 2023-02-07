import cards
from cards import Deck
from cards import FrenchDeck

import pyfiglet

class Blackjack:
    def __init__(self, num) -> None:
        self.num_decks = num
        self.deck = FrenchDeck(self.num_decks)
        self.deck.shuffle()
        self.player_score = 1000
        self.basic_score = 1000

    def hand_value(self, hand):
        value = 0
        soft = 0
        is_soft = False
        for card in hand:
            if card.rank in ['J', 'Q', 'K']:
                value += 10
            elif card.rank == 'A':
                value += 11
                soft += 1
            else:
                value += int(card.rank)
        if soft != 0:
            while(soft > 0 and value > 21):
                value -= 10
                soft -= 1
        if soft > 0:
            is_soft = True
        return [value, is_soft]

    def print_dealer_hand(self, dealer_hand) -> None:
        print(f"Dealer: {dealer_hand[0].rank} ?")
        print()

    def reveal_dealer_hand(self, dealer_hand) -> None:
        print("Dealer:", *[card.rank for card in dealer_hand])
        print()

    def print_player_hand(self, num, player_hands) -> None:
        print("Player:", *[card.rank for card in player_hands[num]])

    def print_basic_hand(self, num, basic_hands) -> None:
        print("Basic:", *[card.rank for card in basic_hands[num]])
        
    def basic_move(self, hand, rank):
        if len(hand) == 2 and hand[0].rank == hand[1].rank:
            if hand[0].rank in ['2', '3', '6', '7', '9'] and rank in ['2', '3', '4', '5', '6']:
                return 'sp'
            elif hand[0].rank == 4 and rank in ['5', '6']:
                return 'sp'
            elif hand[0].rank in ['8', 'A']:
                return 'sp'
            elif hand[0].rank in ['2', '3', '7'] and rank == 7:
                return 'sp'
            elif hand[0].rank == 9 and rank in ['8', '9']:
                return 'sp'
        if self.hand_value(hand)[1]:
            if self.hand_value(hand)[0] == 20:
                return 's'
            elif self.hand_value(hand)[0] == 19 and rank != '6':
                return 's'
            elif self.hand_value(hand)[0] == 19 and rank == '6':
                return 'd'
            elif self.hand_value(hand)[0] == 18 and rank in ['2', '3', '4', '5', '6']:
                return d
            elif self.hand_value(hand)[0] == 18 and rank in ['7', '8']:
                return 's'
            elif rank in ['5', '6']:
                return 'd'
            elif self.hand_value(hand)[0] >= 15 and rank in ['4']:
                return 'd'
            elif self.hand_value(hand)[0] == 17 and rank in ['3']:
                return 'd'
            else: 
                return 'h'
        else:
            if self.hand_value(hand)[0] >= 17:
                return 's'
            elif self.hand_value(hand)[0] >= 13 and rank in ['2', '3', '4', '5', '6']:
                return 's'
            elif self.hand_value(hand)[0] == 12 and rank in ['4', '5', '6']:
                return 's'
            elif self.hand_value(hand)[0] in [10, 11] and rank in ['2', '3', '4', '5', '6', '7', '8', '9']:
                return 'd'
            elif self.hand_value(hand)[0] == 11 and rank in ['10', 'J', 'Q', 'K', 'A']:
                return 'd'
            elif self.hand_value(hand)[0] == 9 and rank in ['3', '4', '5', '6']:
                return 'd'
            else:
                return 'h'

    def basic_draw_card(self, cards_drawn, basic_cards_drawn):
        if len(cards_drawn) != 0:
            return cards_drawn.pop(0)
        else: 
            card = self.deck.draw_card()
            basic_cards_drawn.append(card)
            return card

    def play_hand(self) -> None:
    
        player_hands = []
        basic_hands = []
        dealer_hand = []
    
        print("Score: ", self.player_score)
        bets = []
        bet = input("Place your bet (5): ")
        if bet.isdigit() and int(bet)%5 == 0:
            bets.append(int(bet))
        else:
            bets.append(5)
        basic_bets = [5]
        print()

        player_hands.append([self.deck.draw_card(), self.deck.draw_card()])
        basic_hands.append([player_hands[0][0], player_hands[0][1]])
        dealer_hand = ([self.deck.draw_card(), self.deck.draw_card()])

        if self.hand_value(dealer_hand)[0] == 21 or self.hand_value(player_hands[0])[0] == 21:
            if self.hand_value(dealer_hand)[0] == 21 and self.hand_value(player_hands[0])[0] == 21:
                self.reveal_dealer_hand(dealer_hand)
                self.print_player_hand(0, player_hands)
                print("Push")        
            elif self.hand_value(dealer_hand)[0] != 21 and self.hand_value(player_hands[0])[0] == 21:
                self.reveal_dealer_hand(dealer_hand)
                self.print_player_hand(0, player_hands)
                print("Win")
                self.player_score += bets[0]
                self.basic_score += basic_bets[0]
            else:
                self.reveal_dealer_hand(dealer_hand)
                self.print_player_hand(0, player_hands)
                print("Lose")
                self.player_score -= bets[0]
                self.basic_score -= basic_bets[0]
            print()
        else: 
            self.print_dealer_hand(dealer_hand)
            cards_drawn = []
            basic_cards_drawn = []
            count = 0
            while(count < len(player_hands)):
                self.print_player_hand(count, player_hands)
                if self.hand_value(player_hands[count])[0] < 21:
                    move = input("Hit (H), Stand (S), Double (D), Split (Sp): ").lower() 
                    while(move == 'h' or (move == 'd' and len(player_hands[count]) == 2) or (move == 'sp' and len(player_hands) <= 3) and player_hands[count][0].rank == player_hands[count][1].rank and len(player_hands[count]) == 2):
                        if move == 'h':
                            card = self.deck.draw_card()
                            cards_drawn.append(card)
                            player_hands[count].append(card)
                            self.print_player_hand(count, player_hands)
                            if self.hand_value(player_hands[count])[0] < 21:
                                move = input("Hit (H), Stand (S), Double (D), Split (Sp): ").lower() 
                            else:
                                move = ''
                        elif move == 'd':
                            bets[count] *= 2
                            card = self.deck.draw_card()
                            cards_drawn.append(card)
                            player_hands[count].append(card)
                            self.print_player_hand(count, player_hands)
                            move = ''
                        else:
                            bets.append(bets[count])
                            card = self.deck.draw_card()
                            cards_drawn.append(card)
                            player_hands.append([player_hands[count].pop(), card])
                            card = self.deck.draw_card()
                            cards_drawn.append(card)
                            player_hands[count].append(card)
                            print()
                            self.print_player_hand(count, player_hands)
                            if self.hand_value(player_hands[count])[0] < 21:
                                move = input("Hit (H), Stand (S), Double (D), Split (Sp): ").lower() 
                            else:
                                move = ''
                count += 1
                print()

            count = 0
            while(count < len(basic_hands)):
                if self.hand_value(basic_hands[count])[0] < 21:
                    move = self.basic_move(basic_hands[count], dealer_hand[0].rank)
                    while(move in ['h', 'd', 'sp']): 
                        if move == 'h':
                            basic_hands[count].append(self.basic_draw_card(cards_drawn, basic_cards_drawn))
                            if self.hand_value(basic_hands[count])[0] < 21:
                                move = self.basic_move(basic_hands[count], dealer_hand[0].rank)
                            else:
                                move = ''
                        elif move == 'd':
                            bets[count] *= 2
                            basic_hands[count].append(self.basic_draw_card(cards_drawn, basic_cards_drawn))
                            move = ''
                        elif move == 'sp':
                            bets.append(bets[count])
                            basic_hands.append([basic_hands[count].pop(), self.basic_draw_card(cards_drawn, basic_cards_drawn)])
                            basic_hands[count].append(self.basic_draw_card(cards_drawn, basic_cards_drawn))
                            if self.hand_value(basic_hands[count])[0] < 21:
                                move = self.basic_move(basic_hands[count], dealer_hand[0].rank)
                            else:
                                move = ''
                count += 1            
            self.deck.cards.extend(basic_cards_drawn)
            
            while(self.hand_value(dealer_hand)[0] < 17):
                dealer_hand.append(self.deck.draw_card())
            self.reveal_dealer_hand(dealer_hand)

            for count in range(len(player_hands)):
                self.print_player_hand(count, player_hands)
                if self.hand_value(player_hands[count])[0] == self.hand_value(dealer_hand)[0] and self.hand_value(player_hands[count])[0] <= 21:
                    print("Player Push")
                elif (self.hand_value(player_hands[count])[0] > self.hand_value(dealer_hand)[0] or self.hand_value(dealer_hand)[0] > 21) and self.hand_value(player_hands[count])[0] <= 21:
                    print("Player Win")
                    self.player_score += bets[count]
                else:
                    print("Player Lose")
                    self.player_score -= bets[count]
                print()

            for count in range(len(basic_hands)):
                self.print_basic_hand(count, basic_hands)
                if self.hand_value(basic_hands[count])[0] == self.hand_value(dealer_hand)[0] and self.hand_value(basic_hands[count])[0] <= 21:
                    print("Basic Push")
                elif (self.hand_value(basic_hands[count])[0] > self.hand_value(dealer_hand)[0] or self.hand_value(dealer_hand)[0] > 21) and self.hand_value(basic_hands[count])[0] <= 21:
                    print("Basic Win")
                    self.basic_score += basic_bets[count]
                else:
                    print("Basic Lose")
                    self.basic_score -= basic_bets[count]
                print()
        
        print("Player Score: ", self.player_score)
        print("Basic Score: ", self.basic_score)
        print()

    def play(self) -> None:
        print(pyfiglet.figlet_format("Blackjack"))
        while(input("Play hand? (y/N) ").lower() == 'y'):
            print()
            self.play_hand()
            if len(self.deck.cards) < 52:
                self.deck = FrenchDeck(self.num_decks)

