from typing_extensions import Literal, Mapping, TypedDict, Sequence
from dataclasses import dataclass

Result = Literal['1-0', '1/2-1/2', '0-1', '+-', '-+']

@dataclass
class TeamHeader:
  white: str
  black: str
  board: str
  result: str | None = None
  tag: Literal['team'] = 'team'

@dataclass
class Paired:
  white: str
  black: str
  board: str
  white_no: int | None = None
  white_elo: int | None = None
  black_no: int | None = None
  black_elo: int | None = None
  result: Result | None = None
  tag: Literal['paired'] = 'paired'

@dataclass
class Unpaired:
  player: str
  board: str
  reason: str
  tag: Literal['unpaired'] = 'unpaired'
  
Pairing = Paired | Unpaired | TeamHeader
RoundPairings = Sequence[Pairing]
GroupPairings = Mapping[str, RoundPairings]
TournamentPairings = Mapping[str, GroupPairings]
"""Group -> Round -> Board -> Pairing"""

class GroupId(TypedDict):
  tournId: str
  group: str

class RoundId(GroupId):
  round: str

class GameId(RoundId):
  board: str

def gameId(tournId: str, group: str, round: str, board: str) -> GameId:
  return GameId(tournId=tournId, group=group, round=round, board=board)

def stringifyId(tournId: str, group: str, round: str, board: str) -> str:
  return f'{tournId}/{group}/{round}/{board}'

def roundId(tournId: str, group: str, round: str) -> RoundId:
  return RoundId(tournId=tournId, group=group, round=round)

def groupId(tournId: str, group: str) -> GroupId:
  return GroupId(tournId=tournId, group=group)
