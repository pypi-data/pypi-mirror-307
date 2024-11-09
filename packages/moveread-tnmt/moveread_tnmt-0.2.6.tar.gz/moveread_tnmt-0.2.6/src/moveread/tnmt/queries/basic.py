from typing import Any
from sqlmodel import select
from moveread.tnmt import Game, Upload, Tournament, Round, SheetModel

def group_games(tournId: str, group: str):
  return Game.tournId == tournId, Game.group == group

def group_rounds(tournId: str, group: str):
  return Round.tournId == tournId, Round.group == group

def round_games(tournId: str, group: str, round: str):
  return Game.tournId == tournId, Game.group == group, Game.round == round

def exact_game(tournId: str, group: str, round: str, board: str):
  return Game.tournId == tournId, Game.group == group, Game.round == round, Game.board == board

def exact_round(tournId: str, group: str, round: str):
  return Round.tournId == tournId, Round.group == group, Round.name == round

def select_game(tournId: str, group: str, round: str, board: str):
  return select(Game).where(*exact_game(tournId, group, round, board))

def select_group_games(tournId: str, group: str):
  return select(Game).where(*group_games(tournId, group))

def select_round_games(tournId: str, group: str, round: str):
  return select(Game).where(*round_games(tournId, group, round))

def select_tnmt(tournId: str):
  return select(Tournament).where(Tournament.tournId == tournId)

def select_tnmt_rounds(tournId: str):
  return select(Round).where(Round.tournId == tournId)

def select_round(tournId: str, group: str, round: str):
  return select(Round).where(*exact_round(tournId, group, round))

def select_rounds(tournId: str, group: str):
  """All tournament's rounds, sorted by start dtime"""
  return select(Round).where(Round.tournId == tournId, Round.group == group) \
    .order_by(Round.start_dtime) # type: ignore

def select_model(tournId: str):
  return select(SheetModel).where(SheetModel.tournId == tournId)

def game_uploads():
  eq: Any = Game.uploadId == Upload.id # join has bad types idk
  return select(Game, Upload).join(Upload, eq).where(Upload.status == 'uploaded')