# coding: utf-8

# https://github.com/paulocheque/python-cardgameengine/blob/master/cardgames/pokertexasholdem/__init__.py
# https://github.com/paulocheque/python-cardgameengine/blob/master/cardgames/simplepokertexasholdem/__init__.py

# coding: utf-8
import random

from gat_games.game_engine.engine import *
from gat_games.game_engine.cardgame import *


class PokerPlayer(Player):
    def play(self, context, **kwargs):
        if kwargs.get('action', 'play') == 'x':
            self.blind_bet(context)

    def blind_bet(self, context):
        self.game.execute_command(BlindBet(self, chips=10))

    def bet_pre_flop(self, context): pass
    def bet_pos_flop(self, context): pass
    def bet_pos_4_card(self, context): pass
    def bet_pos_5_card(self, context): pass

    def can_increase_the_bet(self, context):
        return context['round_can_increase_the_bet']


class RandomPokerPlayer(PokerPlayer):
    pass


class PokerCard(Card):
    ranks = (AS, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, AS)


class PokerDeck(Deck):
    Card = PokerCard


class Pass(PlayerGameCommand):
    def validate(self, game, context):
        can_pass
        pass
    def execute(self, game):
        pass

class Pay(PlayerGameCommand):
    def validate(self, game, context):
        pass
    def execute(self, game):
        pass

class IncreaseBet(PlayerGameCommand):
    def validate(self, game, context):
        can_increase
        pass
    def execute(self, game):
        pass

class GiveUp(PlayerGameCommand):
    def validate(self, game, context):
        pass
    def execute(self, game):
        pass


class FlopCommand(GameCommand):
    def execute(self, game):
        pass


class StartGameCommand(StartGameCommand):
    def read_context(self, game):
        for p in game.players:
            game.chips(p) = 1000


class StartRoundCommand(StartRoundCommand):
    def read_context(self, game):
        for p in game.players: # Ante
            if round.game.playersChips[player.name] < round.game.configurations.roundsPrice:
                round.game.removePlayer(player)
            else:
                round.game.playersChips[player.name] -= round.game.configurations.roundsPrice
                round.pot += round.game.configurations.roundsPrice
        game.distribute_cards_to_each_player(2)


class FlopCommand(GameCommand):
    def execute(self, game):
        pass

class TurnCommand(GameCommand):
    def execute(self, game):
        pass

class RiverCommand(GameCommand):
    def execute(self, game):
        pass

class EndRoundCommand(EndRoundCommand):
    def read_context(self, game):
        pass


class PokerRound(CardGameRound):
    Deck = PokerDeck
    StartGameCommand = StartRoundCommand

    # def play(self):
    #     self.player_in_turn = self.next_player()
    #     self.player_play(self.player_in_turn, action='blind_bet')

    def prepare(self): pass
    def get_context(self, player): return super(Game, self).get_context(player)
    def before_play(self): pass
    def start_new_cycle(self): pass
    def before_player_play(self, player, context): pass
    def after_player_play(self, player, context, response=None): pass
    def after_play(self): pass
    def is_the_end(self): return True
    def the_end(self): pass
    def summary(self): return super(Game, self).summary()

    def start_round(self): pass


class Poker(CardGame):
    Round = PokerRound
    RandomStrategy = RandomPokerPlayer
    Player = PokerPlayer

    def prepare(self): pass
    def get_context(self, player): return super(Game, self).get_context(player)
    def before_play(self): pass
    def play(self): pass
    def before_start_round(self, round_game): pass
    def after_end_round(self, round_game): pass
    def after_play(self): pass
    def is_the_end(self): return True
    def the_end(self): pass
    def summary(self): return super(Game, self).summary()
