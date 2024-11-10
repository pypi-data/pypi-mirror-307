from typing import Sequence, ClassVar, Literal
from dataclasses import dataclass
from datetime import date, datetime
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import String
from sqltypes import SpaceDelimitedList, ValidatedJSON
from chess_pairings import GameId, gameId, Result
from chess_scraping import Source

class SheetModel(SQLModel, table=True):
  tournId: str = Field(primary_key=True, foreign_key='tournament.tournId')
  model: str

class Tournament(SQLModel, table=True):
  tournId: str = Field(primary_key=True)
  name: str
  site: str | None = None
  start_date: date
  end_date: date
  groups: Sequence[str] = Field(sa_type=SpaceDelimitedList)

  def __repr__(self):
    import json
    dct = dict(self)
    dct['start_date'] = self.start_date.strftime('%d/%m/%Y')
    dct['end_date'] = self.end_date.strftime('%d/%m/%Y')
    return 'Tournament(' + json.dumps(dct, indent=2) + ')'
  __str__ = __repr__
  

class Pairings(SQLModel, table=True):
  tournId: str = Field(foreign_key='tournament.tournId', primary_key=True)
  group: str = Field(primary_key=True)
  pairings: Source = Field(sa_type=ValidatedJSON(Source))

@dataclass
class Group:
  tournId: str
  name: str
  rounds: Sequence[str]

class Round(SQLModel, table=True):
  tournId: str = Field(primary_key=True, foreign_key='tournament.tournId')
  group: str = Field(primary_key=True)
  name: str = Field(primary_key=True)
  start_dtime: datetime
  
class Image(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  url: str
  descaled_url: str
  uploadId: str = Field(default=None, foreign_key='upload.id')

class FrontendPGN(SQLModel):
  moves: Sequence[str] = Field(sa_type=SpaceDelimitedList)
  early: bool | None = None

class PGN(FrontendPGN, table=True):
  uploadId: str = Field(default=None, primary_key=True, foreign_key='upload.id')

@dataclass
class Paired:
  white: str
  black: str
  result: Result | None = None


@dataclass
class FrontendGame:
  board: str
  pairing: Paired
  status: 'GameStatus | None' = None

  @classmethod
  def of(cls, game: 'Game'):
    return cls(game.board, Paired(white=game.white, black=game.black, result=game.result), game.status)

class Upload(SQLModel, table=True):
  id: str = Field(primary_key=True)
  imgs: list[Image] = Relationship()
  pgn: PGN | None = Relationship()
  games: list['Game'] = Relationship(back_populates='upload')
  status: 'GameStatus | None' = Field(default=None, sa_type=String)

GameStatus = Literal['uploaded', 'doing', 'done', 'header']
"""header: the game is not a real game but a header for team tournaments"""

class Game(SQLModel, table=True):
  Status: ClassVar = GameStatus
  id: int | None = Field(default=None, primary_key=True)
  tournId: str = Field(foreign_key='tournament.tournId')
  uploadId: str | None = Field(default=None, foreign_key='upload.id')
  group: str
  round: str
  board: str
  index: int
  """Boards may have out of whack names (e.g. in team tournaments "1.3"). This is the order you'd see in chess-results"""
  white: str
  black: str
  result: Result | None = Field(sa_type=String)
  upload: Upload | None = Relationship(back_populates='games')

  @property
  def status(self) -> GameStatus | None:
    return self.upload and self.upload.status

  def gameId(self) -> GameId:
    return gameId(self.tournId, self.group, self.round, self.board)
  
class Token(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  token: str
  tournId: str = Field(foreign_key='tournament.tournId')
  
__all__ = [
  'Game', 'GameId', 'Image', 'Tournament', 'PGN', 'Paired', 'Token'
]