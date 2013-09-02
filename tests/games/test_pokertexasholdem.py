# coding: utf-8
import unittest
from nose.tools import raises

from gat_games.games.poker_texasholdem import *


class PokerTests(unittest.TestCase):
    def setUp(self):
        self.p1 = PokerPlayer()
        self.p2 = PokerPlayer()
        self.poker = Poker(1, [self.p1, self.p2])

    def test_game_attributes(self):
        self.assertEquals(1000, self.poker.initial_chips)
        self.assertEquals(10, self.poker.ante_price)
        self.assertEquals(None, self.poker.last_dealer)
        self.assertEquals({str(self.p1):0, str(self.p2):0}, self.poker.chips)

    def test_poker_initial_chips_and_ante_price_can_be_customizable(self):
        self.poker = Poker(1, [], initial_chips=2000, ante_price=20)
        self.assertEquals(2000, self.poker.initial_chips)
        self.assertEquals(20, self.poker.ante_price)

    def test_start_game_distribute_chips_to_each_player(self):
        self.assertEquals(0, self.poker.amount_of_chips(self.p1))
        self.assertEquals(0, self.poker.amount_of_chips(self.p2))
        self.poker.execute_command(StartGameCommand())
        self.assertEquals(1000, self.poker.amount_of_chips(self.p1))
        self.assertEquals(1000, self.poker.amount_of_chips(self.p2))

    def test_end_game_decide_the_winners_based_on_the_chips(self):
        self.poker.execute_command(StartGameCommand())
        self.poker.add_chips(self.p1, -1000)
        self.poker.add_chips(self.p2, 1000)
        self.poker.execute_command(EndGameCommand())
        self.assertEquals([self.p2], self.poker.winners)
        self.assertEquals([self.p1], self.poker.losers)

    def test_context(self):
        ctx = self.poker.get_context(self.p1)
        self.assertEquals(1000, ctx['initial_chips'])
        self.assertEquals(10, ctx['ante_price'])
        self.assertEquals(None, ctx['last_dealer'])
        self.assertEquals({str(self.p1):0, str(self.p2):0}, ctx['chips'])


class PokerRoundTests(unittest.TestCase):
    def setUp(self):
        self.p1 = PokerPlayer()
        self.p2 = PokerPlayer()
        self.poker_game = Poker(1, [self.p1, self.p2])
        self.poker_game.execute_command(StartGameCommand())
        self.poker = PokerRound(1, [self.p1, self.p2])
        self.poker.parent = self.poker_game

    def test_game_attributes(self):
        self.assertEquals(0, self.poker.pot_total)
        self.assertEquals({str(self.p1):0, str(self.p2):0}, self.poker.pot)
        self.assertEquals(None, self.poker.dealer)
        self.assertEquals(Deck(), self.poker.community_cards)

    def test_start_round_take_player_chips_to_the_pot(self):
        self.poker.execute_command(StartRoundCommand())
        self.assertEquals(20, self.poker.pot_total)
        self.assertEquals(990, self.poker_game.amount_of_chips(self.p1))
        self.assertEquals(990, self.poker_game.amount_of_chips(self.p2))

    def test_start_round_decide_the_next_dealer(self):
        self.assertEquals(None, self.poker.dealer)
        self.assertEquals(None, self.poker_game.last_dealer)
        d1 = StartRoundCommand().next_dealer(self.poker)
        d2 = self.poker.players[(self.poker.players.index(d1) + 1) % len(self.poker.players)]

        self.poker.execute_command(StartRoundCommand())
        self.assertEquals(d1, self.poker.dealer)
        self.poker_game.last_dealer = d1

        self.poker.execute_command(StartRoundCommand())
        self.assertEquals(d2, self.poker.dealer)
        self.poker_game.last_dealer = d2

        self.poker.execute_command(StartRoundCommand())
        self.assertEquals(d1, self.poker.dealer)

    def test_end_round_update_the_last_dealer(self):
        self.assertEquals(None, self.poker_game.last_dealer)

        self.poker.execute_command(StartRoundCommand())
        self.poker.execute_command(EndRoundCommand())
        self.assertEquals(self.poker.dealer, self.poker_game.last_dealer)

    def test_deal_distribute_two_cards_for_each_player(self):
        self.poker.execute_command(StartRoundCommand())
        self.poker.execute_command(DealCardsCommand())
        self.assertEquals(2, len(self.poker.hand(self.p1)))
        self.assertEquals(2, len(self.poker.hand(self.p2)))

    def test_flop_face_up_three_cards_to_the_board(self):
        self.poker.execute_command(StartRoundCommand())
        self.poker.execute_command(FlopCommand())
        self.assertEquals(3, len(self.poker.community_cards))

    def test_turn_round_face_up_one_more_card_to_the_board(self):
        self.poker.execute_command(StartRoundCommand())
        self.poker.execute_command(FlopCommand())
        self.poker.execute_command(TurnCommand())
        self.assertEquals(4, len(self.poker.community_cards))

    def test_river_round_face_up_last_card_to_the_board(self):
        self.poker.execute_command(StartRoundCommand())
        self.poker.execute_command(FlopCommand())
        self.poker.execute_command(TurnCommand())
        self.poker.execute_command(RiverCommand())
        self.assertEquals(5, len(self.poker.community_cards))

    def test_context(self):
        ctx = self.poker.get_context(self.p1)
        self.assertEquals(0, ctx['pot_total'])
        self.assertEquals({str(self.p1):0, str(self.p2):0}, ctx['pot'])
        self.assertEquals(None, ctx['dealer'])
        self.assertEquals(Deck(), ctx['community_cards'])


class PokerTestBase(unittest.TestCase):
    def setUp(self):
        self.p1 = PokerPlayer()
        self.p2 = PokerPlayer()
        self.poker_game = Poker(1, [self.p1, self.p2])
        self.poker_game.execute_command(StartGameCommand())
        self.poker = PokerRound(1, [self.p1, self.p2])
        self.poker.parent = self.poker_game
        self.poker.execute_command(StartRoundCommand())
        self.poker.play()
        self.poker.player_in_turn = self.p1


class PassTests(PokerTestBase):
    def test_validate(self):
        pass
    def test_execute(self):
        self.poker.execute_command(Pass(self.p1))


class PayTests(PokerTestBase):
    def test_validate(self):
        pass
    def test_execute(self):
        self.poker.execute_command(Pay(self.p1))


class IncreaseBetTests(PokerTestBase):
    def test_validate(self):
        pass
    def test_execute(self):
        self.poker.execute_command(IncreaseBet(self.p1))


class GiveUpTests(PokerTestBase):
    def test_validate(self):
        pass

    @raises(EndGame)
    def test_execute(self):
        self.poker.execute_command(GiveUp(self.p1))
