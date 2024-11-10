from typing import Iterator, MutableMapping, Mapping, Generic, TypeVar, Iterable
from haskellian import iter as I
from chess_pairings import GameId, GroupId, RoundId, gameId, groupId, roundId

T = TypeVar('T')

class GamesMapping(Mapping[GameId, T], Generic[T]):

  @classmethod
  def from_pairs(cls, pairs: Iterable[tuple[GameId, T]]) -> 'GamesMapping[T]':
    mapping = cls()
    for key, value in pairs:
      mapping[key] = value
    return mapping

  def __init__(self, init: Mapping[str, dict[str, dict[str, dict[str, T]]]] = {}):
    """Mapping tnmtId -> group -> round -> board -> T"""
    self.dict: dict[str, dict[str, dict[str, dict[str, T]]]] = dict(init)

  def _getitem(self, *, tournId: str, group: str, round: str, board: str) -> T:
    return self.dict[tournId][group][round][board]
  
  def __getitem__(self, key: GameId) -> T:
    return self._getitem(**key)

  def _setitem(self, *, tournId: str, group: str, round: str, board: str, value: T) -> None:
    if tournId not in self.dict:
      self.dict[tournId] = {}
    if group not in self.dict[tournId]:
      self.dict[tournId][group] = {}
    if round not in self.dict[tournId][group]:
      self.dict[tournId][group][round] = {}
    self.dict[tournId][group][round][board] = value

  def __setitem__(self, key: GameId, value: T) -> None:
    self._setitem(**key, value=value)

  def __delitem__(self, *, tournId: str, group: str, round: str, board: str) -> None:
    del self.dict[tournId][group][round][board]
    if not self.dict[tournId][group][round]:
      del self.dict[tournId][group][round]
    if not self.dict[tournId][group]:
      del self.dict[tournId][group]
    if not self.dict[tournId]:
      del self.dict[tournId]

  def __len__(self) -> int:
    return len(list(self.gameIds()))
  
  def __repr__(self) -> str:
    return f'GamesMapping({repr(self.dict)})'
  
  @I.lift
  def tournIds(self) -> Iterable[str]:
    return self.dict.keys()
  
  @I.lift
  def groupIds(self) -> Iterable[GroupId]:
    for tournId, groups in self.dict.items():
      for group in groups:
        yield groupId(tournId, group)

  @I.lift
  def roundIds(self) -> Iterable[RoundId]:
    for tournId, groups in self.dict.items():
      for group, rounds in groups.items():
        for round in rounds:
          yield roundId(tournId, group, round)

  @I.lift
  def gameIds(self) -> Iterable[GameId]:
    for tournId, groups in self.dict.items():
      for group, rounds in groups.items():
        for round, boards in rounds.items():
          for board in boards:
            yield gameId(tournId, group, round, board)

  def __iter__(self) -> Iterator[GameId]:
    return self.gameIds()
