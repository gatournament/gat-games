# coding: utf-8
from itertools import combinations
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
        if game.player_in_turn != self.player:
            raise InvalidCommandError('Player can not pass right now')
        # player has enough chips
        # another player increase the bet

    def execute(self, game):
        pass

class Pay(PlayerGameCommand):
    def validate(self, game, context):
        if game.player_in_turn != self.player:
            raise InvalidCommandError('Player can not pass right now')
        # player has enough chips

    def execute(self, game):
        pass

class IncreaseBet(PlayerGameCommand):
    def validate(self, game, context):
        if game.player_in_turn != self.player:
            raise InvalidCommandError('Player can not pass right now')
        # player has enough chips

    def execute(self, game):
        pass

class GiveUp(PlayerGameCommand):
    def validate(self, game, context):
        if game.player_in_turn != self.player:
            raise InvalidCommandError('Player can not give up right now')

    def execute(self, game):
        game.remove_player(self.player)
        if len(game.players) == 1:
            raise EndGame()


class StartGameCommand(StartGameCommand):
    def execute(self, game):
        for player in game.players:
            game.add_chips(player, game.initial_chips)

    def read_context(self, game):
        for p in game.players:
            pass
            # game.chips(p) = 1000


class EndGameCommand(EndGameCommand):
    def execute(self, game):
        max_chips = 0
        for player in game.players:
            total = game.amount_of_chips(player)
            max_chips = max(max_chips, total)
        for player in game.players:
            total = game.amount_of_chips(player)
            if total == max_chips:
                game.winners.append(player)
            else:
                game.losers.append(player)

    def read_context(self, game):
        for p in game.players:
            pass
            # game.chips(p) = 1000


class StartRoundCommand(StartRoundCommand):
    def execute(self, game):
        for player in game.players: # Ante
            game.parent.add_chips(player, -game.parent.ante_price)
            game.add_player_bet(player, game.parent.ante_price)
            game.pot_total += game.parent.ante_price
        game.dealer = self.next_dealer(game)

    def next_dealer(self, game):
        if game.parent.last_dealer:
            index = game.players.index(game.parent.last_dealer) + 1
            index %= len(game.players)
            return game.players[index]
        else:
            # return game.random.choice(game.players)
            return game.players[0]

    def read_context(self, game):
        pass


class EndRoundCommand(EndRoundCommand):
    def read_context(self, game):
        pass

    def execute(self, game):
        game.parent.last_dealer = game.dealer


class DealCardsCommand(GameCommand):
    def execute(self, game):
        game.distribute_cards_to_each_player(2)


class FlopCommand(GameCommand):
    def execute(self, game):
        game.deck.distribute([game.community_cards], 3)


class TurnCommand(GameCommand):
    def execute(self, game):
        game.deck.distribute([game.community_cards], 1)


class RiverCommand(GameCommand):
    def execute(self, game):
        game.deck.distribute([game.community_cards], 1)


class PokerRound(CardGameRound):
    Deck = PokerDeck
    StartGameCommand = StartRoundCommand

    # def play(self):
    #     self.player_in_turn = self.next_player()
    #     self.player_play(self.player_in_turn, action='blind_bet')

    def prepare(self):
        self.pot_total = 0
        self.pot = {}
        for player in self.players:
            self.pot[str(player)] = 0
        self.dealer = None
        self.community_cards = Deck()

    def add_player_bet(self, player, amount):
        self.pot[str(player)] += amount

    def get_context(self, player):
        ctx = super(PokerRound, self).get_context(player)
        ctx['pot_total'] = self.pot_total
        ctx['pot'] = self.pot
        ctx['dealer'] = self.dealer
        ctx['community_cards'] = self.community_cards
        return ctx

    def showdown(self):
        for player in self.players:
            self.best_player_combination(player)

    def best_player_combination(self, player):
        deck = self.community_cards.clone()
        hand = self.hand(player)
        deck.push(hand.get_cards())
        combs = combinations(deck.get_cards(), 5)
        combs = [PokerCombination(cards) for cards in combs]
        combs.sort()
        return combs[-1]

    def before_play(self): pass
    def start_new_cycle(self): pass
    def before_player_play(self, player, context): pass
    def after_player_play(self, player, context, response=None): pass
    def after_play(self): pass
    def is_the_end(self):
        return len(self.players) == 1
    def the_end(self): pass
    def summary(self): return super(PokerRound, self).summary()

    def start_round(self): pass


class Poker(CardGame):
    Round = PokerRound
    StartGameCommand = StartGameCommand
    EndGameCommand = EndGameCommand
    RandomStrategy = RandomPokerPlayer
    Player = PokerPlayer

    def prepare(self):
        self.initial_chips = self.kwargs.get('initial_chips', 1000)
        self.ante_price = self.kwargs.get('ante_price', 10)
        self.chips = {}
        for player in self.players:
            self.chips[str(player)] = 0
        self.last_dealer = None

    def amount_of_chips(self, player):
        return self.chips[str(player)]

    def add_chips(self, player, amount):
        self.chips[str(player)] += amount

    def new_round(self):
        players = []
        for player in self.players:
            if self.amount_of_chips(player) >= self.ante_price:
                players.append(player)
        round_game = self.Round(self.random.randint(1, 999999), players, **self.kwargs)
        # self.games.append(round_game)
        return round_game

    def get_context(self, player):
        ctx = super(Poker, self).get_context(player)
        ctx['initial_chips'] = self.initial_chips
        ctx['ante_price'] = self.ante_price
        ctx['last_dealer'] = self.last_dealer
        ctx['chips'] = self.chips
        return ctx

    def before_play(self): pass
    # def play(self): pass
    def before_start_round(self, round_game): pass
    def after_end_round(self, round_game): pass
    def after_play(self): pass
    def is_the_end(self): return False
    def the_end(self): pass
    def summary(self): return super(Poker, self).summary()
