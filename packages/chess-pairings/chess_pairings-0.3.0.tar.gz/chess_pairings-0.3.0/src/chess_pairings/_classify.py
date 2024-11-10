from typing import Callable, Mapping, Sequence, Iterable, Literal, overload
import chess.pgn
from chess_pairings import GamesMapping, gameId

@overload
def classify(
  games: Iterable[chess.pgn.Game], *,
  headers2tournId: Callable[[Mapping[str, str]], str] = lambda x: x['Event'],
  headers2group: Callable[[Mapping[str, str]], str],
  headers2round: Callable[[Mapping[str, str]], str] = lambda x: x['Round'].split('.')[0],
  headers2board: Callable[[Mapping[str, str]], str] = lambda x: x['Round'].split('.')[1],
  return_unclassified: Literal[True],
) -> tuple[GamesMapping[chess.pgn.Game], Sequence[chess.pgn.Game]]:
  ...

@overload
def classify(
  games: Iterable[chess.pgn.Game], *,
  headers2tournId: Callable[[Mapping[str, str]], str] = lambda x: x['Event'],
  headers2group: Callable[[Mapping[str, str]], str],
  headers2round: Callable[[Mapping[str, str]], str] = lambda x: x['Round'].split('.')[0],
  headers2board: Callable[[Mapping[str, str]], str] = lambda x: x['Round'].split('.')[1],
  return_unclassified: Literal[False] = False,
) -> GamesMapping[chess.pgn.Game]:
  ...
  
def classify( # type: ignore
  games: Iterable[chess.pgn.Game], *,
  headers2tournId: Callable[[Mapping[str, str]], str] = lambda x: x['Event'],
  headers2group: Callable[[Mapping[str, str]], str],
  headers2round: Callable[[Mapping[str, str]], str] = lambda x: x['Round'].split('.')[0],
  headers2board: Callable[[Mapping[str, str]], str] = lambda x: x['Round'].split('.')[1],
  return_unclassified: bool = False,
):
  
  classified_games = GamesMapping[chess.pgn.Game]()
  unclassified_games = []
  
  for game in games:
    hdrs = game.headers
    try:
      tournId = headers2tournId(hdrs)
      group = headers2group(hdrs)
      round = headers2round(hdrs)
      board = headers2board(hdrs)
      classified_games[gameId(tournId, group, round, board)] = game
    except:
      unclassified_games.append(game)
  if return_unclassified:
    return classified_games, unclassified_games
  else:
    return classified_games