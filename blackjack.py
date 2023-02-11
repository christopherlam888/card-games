from cards import FrenchDeck

import pyfiglet


class Blackjack:
    id = "blackjack"
    name = "Blackjack"
    default_num_decks = 6

    # default constructor
    def __init__(self, num):
        self.num_decks = num
        self.deck = FrenchDeck(self.num_decks)
        self.deck.shuffle()
        self.player_score = 1000
        self.basic_score = 1000

    # calculate a hand value
    def get_hand_value(self, hand):
        value = 0
        soft = 0
        is_soft = False
        for card in hand:
            if card.rank in ["J", "Q", "K"]:
                value += 10
            elif card.rank == "A":
                value += 11
                soft += 1
            else:
                value += int(card.rank)
        if soft != 0:
            while soft > 0 and value > 21:
                value -= 10
                soft -= 1
        if soft > 0:
            is_soft = True
        return [value, is_soft]

    # print the dealer hand
    def print_dealer_hand(self, dealer_hand):
        print(f"Dealer: {dealer_hand[0].rank} ?")
        print()

    # reveal the dealer hand
    def reveal_dealer_hand(self, dealer_hand):
        print("Dealer:", *[card.rank for card in dealer_hand])
        print()

    # print a single player hand
    def print_player_hand(self, num, player_hands):
        print("Player:", *[card.rank for card in player_hands[num]])

    # print a single basic hand
    def print_basic_hand(self, num, basic_hands):
        print("Basic:", *[card.rank for card in basic_hands[num]])

    # determine a move based on basic strategy
    def basic_move(self, hand, basic_hands, rank):
        # split
        if len(basic_hands) <= 3 and len(hand) == 2 and hand[0].rank == hand[1].rank:
            if hand[0].rank in ["2", "3", "6", "7", "9"] and rank in [
                "2",
                "3",
                "4",
                "5",
                "6",
            ]:
                return "sp"
            elif hand[0].rank == 4 and rank in ["5", "6"]:
                return "sp"
            elif hand[0].rank in ["8", "A"]:
                return "sp"
            elif hand[0].rank in ["2", "3", "7"] and rank == 7:
                return "sp"
            elif hand[0].rank == 9 and rank in ["8", "9"]:
                return "sp"

        # soft
        if self.get_hand_value(hand)[1]:
            if self.get_hand_value(hand)[0] == 20:
                return "s"
            elif self.get_hand_value(hand)[0] == 19 and rank != "6":
                return "s"
            elif self.get_hand_value(hand)[0] == 19 and rank == "6":
                if len(hand) == 2:
                    return "d"
                else:
                    return "h"
            elif self.get_hand_value(hand)[0] == 18 and rank in [
                "2",
                "3",
                "4",
                "5",
                "6",
            ]:
                if len(hand) == 2:
                    return "d"
                else:
                    return "h"
            elif self.get_hand_value(hand)[0] == 18 and rank in ["7", "8"]:
                return "s"
            elif rank in ["5", "6"]:
                if len(hand) == 2:
                    return "d"
                else:
                    return "h"
            elif self.get_hand_value(hand)[0] >= 15 and rank in ["4"]:
                if len(hand) == 2:
                    return "d"
                else:
                    return "h"
            elif self.get_hand_value(hand)[0] == 17 and rank in ["3"]:
                if len(hand) == 2:
                    return "d"
                else:
                    return "h"
            else:
                return "h"

        # hard
        else:
            if self.get_hand_value(hand)[0] >= 17:
                return "s"
            elif self.get_hand_value(hand)[0] >= 13 and rank in [
                "2",
                "3",
                "4",
                "5",
                "6",
            ]:
                return "s"
            elif self.get_hand_value(hand)[0] == 12 and rank in ["4", "5", "6"]:
                return "s"
            elif self.get_hand_value(hand)[0] in [10, 11] and rank in [
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
            ]:
                if len(hand) == 2:
                    return "d"
                else:
                    return "h"
            elif self.get_hand_value(hand)[0] == 11 and rank in [
                "10",
                "J",
                "Q",
                "K",
                "A",
            ]:
                if len(hand) == 2:
                    return "d"
                else:
                    return "h"
            elif self.get_hand_value(hand)[0] == 9 and rank in ["3", "4", "5", "6"]:
                if len(hand) == 2:
                    return "d"
                else:
                    return "h"
            else:
                return "h"

    # draw a card from the deck for basic
    def basic_draw_card(self, cards_drawn, basic_cards_drawn):
        if len(cards_drawn) != 0:
            return cards_drawn.pop(0)
        else:
            card = self.deck.draw_card()
            basic_cards_drawn.append(card)
            return card

    # play a hand
    def play_hand(self):
        player_hands = []
        basic_hands = []
        dealer_hand = []

        # prompt for bet
        print("Score: ", self.player_score)
        bets = []
        try:
            bet = int(input("Place your bet (5): "))
            bets.append(bet if bet % 5 == 0 else 5)
        except ValueError:
            bets.append(5)
        basic_bets = [5]
        print()

        # deal starting hands
        player_hands.append([self.deck.draw_card(), self.deck.draw_card()])
        basic_hands.append([player_hands[0][0], player_hands[0][1]])
        dealer_hand = [self.deck.draw_card(), self.deck.draw_card()]

        # check for blackjack
        if (
            self.get_hand_value(dealer_hand)[0] == 21
            or self.get_hand_value(player_hands[0])[0] == 21
        ):
            if (
                self.get_hand_value(dealer_hand)[0] == 21
                and self.get_hand_value(player_hands[0])[0] == 21
            ):
                self.reveal_dealer_hand(dealer_hand)
                self.print_player_hand(0, player_hands)
                print("Push")
            elif (
                self.get_hand_value(dealer_hand)[0] != 21
                and self.get_hand_value(player_hands[0])[0] == 21
            ):
                self.reveal_dealer_hand(dealer_hand)
                self.print_player_hand(0, player_hands)
                print("Win")
                self.player_score += bets[0] * 1.5
                self.basic_score += basic_bets[0] * 1.5
            else:
                self.reveal_dealer_hand(dealer_hand)
                self.print_player_hand(0, player_hands)
                print("Lose")
                self.player_score -= bets[0]
                self.basic_score -= basic_bets[0]
            print()

        # not blackjack
        else:
            self.print_dealer_hand(dealer_hand)
            cards_drawn = []
            basic_cards_drawn = []

            # player move
            count = 0
            while count < len(player_hands):
                self.print_player_hand(count, player_hands)
                if self.get_hand_value(player_hands[count])[0] < 21:
                    move = input("Hit (H), Stand (S), Double (D), Split (Sp): ").lower()
                    while (
                        move == "h"
                        or (move == "d" and len(player_hands[count]) == 2)
                        or (move == "sp" and len(player_hands) <= 3)
                        and player_hands[count][0].rank == player_hands[count][1].rank
                        and len(player_hands[count]) == 2
                    ):
                        if move == "h":
                            card = self.deck.draw_card()
                            cards_drawn.append(card)
                            player_hands[count].append(card)
                            self.print_player_hand(count, player_hands)
                            if self.get_hand_value(player_hands[count])[0] < 21:
                                move = input(
                                    "Hit (H), Stand (S), Double (D), Split (Sp): "
                                ).lower()
                            else:
                                move = ""
                        elif move == "d":
                            bets[count] *= 2
                            card = self.deck.draw_card()
                            cards_drawn.append(card)
                            player_hands[count].append(card)
                            self.print_player_hand(count, player_hands)
                            move = ""
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
                            if self.get_hand_value(player_hands[count])[0] < 21:
                                move = input(
                                    "Hit (H), Stand (S), Double (D), Split (Sp): "
                                ).lower()
                            else:
                                move = ""
                count += 1
                print()

            # basic move
            count = 0
            while count < len(basic_hands):
                if self.get_hand_value(basic_hands[count])[0] < 21:
                    move = self.basic_move(
                        basic_hands[count], basic_hands, dealer_hand[0].rank
                    )
                    while move in ["h", "d", "sp"]:
                        if move == "h":
                            basic_hands[count].append(
                                self.basic_draw_card(cards_drawn, basic_cards_drawn)
                            )
                            if self.get_hand_value(basic_hands[count])[0] < 21:
                                move = self.basic_move(
                                    basic_hands[count], basic_hands, dealer_hand[0].rank
                                )
                            else:
                                move = ""
                        elif move == "d":
                            basic_bets[count] *= 2
                            basic_hands[count].append(
                                self.basic_draw_card(cards_drawn, basic_cards_drawn)
                            )
                            move = ""
                        elif move == "sp":
                            basic_bets.append(bets[count])
                            basic_hands.append(
                                [
                                    basic_hands[count].pop(),
                                    self.basic_draw_card(
                                        cards_drawn, basic_cards_drawn
                                    ),
                                ]
                            )
                            basic_hands[count].append(
                                self.basic_draw_card(cards_drawn, basic_cards_drawn)
                            )
                            if self.get_hand_value(basic_hands[count])[0] < 21:
                                move = self.basic_move(
                                    basic_hands[count], basic_hands, dealer_hand[0].rank
                                )
                            else:
                                move = ""
                count += 1
            self.deck.cards.extend(basic_cards_drawn)

            # dealer move
            while self.get_hand_value(dealer_hand)[0] < 17:
                dealer_hand.append(self.deck.draw_card())
            self.reveal_dealer_hand(dealer_hand)

            # determine results for each player hand
            for count in range(len(player_hands)):
                self.print_player_hand(count, player_hands)
                if (
                    self.get_hand_value(player_hands[count])[0]
                    == self.get_hand_value(dealer_hand)[0]
                    and self.get_hand_value(player_hands[count])[0] <= 21
                ):
                    print("Player Push")
                elif (
                    self.get_hand_value(player_hands[count])[0]
                    > self.get_hand_value(dealer_hand)[0]
                    or self.get_hand_value(dealer_hand)[0] > 21
                ) and self.get_hand_value(player_hands[count])[0] <= 21:
                    print("Player Win")
                    self.player_score += bets[count]
                else:
                    print("Player Lose")
                    self.player_score -= bets[count]
                print()

            # determine results for each basic hand
            for count in range(len(basic_hands)):
                self.print_basic_hand(count, basic_hands)
                if (
                    self.get_hand_value(basic_hands[count])[0]
                    == self.get_hand_value(dealer_hand)[0]
                    and self.get_hand_value(basic_hands[count])[0] <= 21
                ):
                    print("Basic Push")
                elif (
                    self.get_hand_value(basic_hands[count])[0]
                    > self.get_hand_value(dealer_hand)[0]
                    or self.get_hand_value(dealer_hand)[0] > 21
                ) and self.get_hand_value(basic_hands[count])[0] <= 21:
                    print("Basic Win")
                    self.basic_score += basic_bets[count]
                else:
                    print("Basic Lose")
                    self.basic_score -= basic_bets[count]
                print()

        # print scores
        print("Player Score: ", self.player_score)
        print("Basic Score: ", self.basic_score)
        print()

    # play the game
    def play(self):
        print(pyfiglet.figlet_format("Blackjack"))
        while input("Play hand? (y/N) ").lower() == "y":
            print()
            self.play_hand()
            # new deck if less than one deck's number of cards remain
            if len(self.deck.cards) < 52:
                self.deck = FrenchDeck(self.num_decks)
