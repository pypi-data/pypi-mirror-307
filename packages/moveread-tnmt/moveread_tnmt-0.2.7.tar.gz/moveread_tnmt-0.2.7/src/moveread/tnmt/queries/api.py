from dataclasses import dataclass
from sqlmodel import Session
from moveread.tnmt import Tournament, Round, SheetModel, queries, Upload

@dataclass
class Select:
  session: Session

  def tnmt(self, tournId: str):
    return self.session.get(Tournament, tournId)
  
  def round(self, tournId: str, group: str, round: str):
    return self.session.get(Round, (tournId, group, round))
  
  def game(self, tournId: str, group: str, round: str, board: str):
    return self.session.exec(queries.select_game(tournId, group, round, board)).first()
  
  def game_uploads(self):
    return self.session.exec(queries.game_uploads()).all()
  
  def model(self, tournId: str):
    if (obj := self.session.get(SheetModel, tournId)):
      return obj.model

@dataclass
class API:
  session: Session

  @property
  def select(self):
    return Select(self.session)