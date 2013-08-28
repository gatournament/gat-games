# coding: utf-8
import sys

VERSION = '0.0.2'

if sys.version_info[0] == 2:
    from gat_games.games.truco import *
    from gat_games.games.truco_clean_deck import *
else:
    from .games.truco import *
    from .games.truco_clean_deck import *

SUPPORTED_GAMES = [Truco, TrucoCleanDeck]
