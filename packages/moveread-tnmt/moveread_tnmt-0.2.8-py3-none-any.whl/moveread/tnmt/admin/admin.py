from typing import Mapping
from datetime import datetime
from sqlmodel import Session, select
from dslog import Logger
import chess_scraping as cs
from moveread.tnmt import Tournament, Round, SheetModel, queries, Token, Pairings

def upsert_tnmt(session: Session, tnmt: Tournament, *, logger: Logger = Logger.click()):
  if (curr := session.exec(queries.select_tnmt(tnmt.tournId)).first()):
    logger('Deleting existing entry:', curr, level='DEBUG')
    session.delete(curr)
  logger('Inserting new entry:', tnmt)
  session.add(tnmt)

def upsert_round(
  session: Session, tournId: str, group: str, round: str, *,
  logger: Logger = Logger.click(), start: datetime
):
  if not (rnd := session.exec(queries.select_round(tournId, group, round)).first()):
    rnd = Round(tournId=tournId, group=group, name=round, start_dtime=start)
    logger(f'Inserting new round: "{tournId}/{group}/{round}:"', start.strftime('%d/%m/%Y %H:%M:%S'))
    session.add(rnd)
  elif rnd.start_dtime == start:
    logger('Round start time already set to', start)
  else:
    logger('Updating round start time:', rnd.start_dtime, '->', start)
    rnd.start_dtime = start
    session.add(rnd)

def upsert_model(session: Session, tournId: str, model: str, *, logger: Logger = Logger.click()):
  if (curr := session.exec(queries.select_model(tournId)).first()):
    if curr.model == model:
      logger(f'Model "{model}" already set for "{tournId}"')
    else:
      logger(f'Updating model for "{tournId}": "{curr.model}" -> "{model}"')
      curr.model = model
      session.add(curr)
  else:
    logger(f'Inserting new model for "{tournId}": "{model}"')
    session.add(SheetModel(tournId=tournId, model=model))

def upsert_pairings(session: Session, tournId: str, group: str, pairings: cs.Source, *, logger: Logger):
  if (obj := session.get(Pairings, (tournId, group))):
    if obj.pairings.tag == pairings.tag and obj.pairings.id == pairings.id:
      logger(f'Pairings for "{group}" are already up to date')
    else:
      logger(f'Current: {obj.pairings.tag} ({obj.pairings.id}), New: {pairings.tag} ({pairings.id})')
      obj.pairings = pairings
      session.add(obj)
      logger(f'Updated pairings entry for "{group}"')
  else:
    session.add(Pairings(tournId=tournId, group=group, pairings=pairings))
    logger(f'Created pairings entry for "{group}"')


def list_tokens(session: Session, tournId: str):
  stmt = select(Token.token).where(Token.tournId == tournId)
  return session.exec(stmt).all()

def add_token(session: Session, tournId: str, token: str, *, logger: Logger = Logger.click()):
  if session.exec(select(Token).where(Token.tournId == tournId, Token.token == token)).first():
    logger(f'Token "{token}" already exists for "{tournId}"')
  else:
    logger(f'Adding token "{token}" for "{tournId}"')
    session.add(Token(tournId=tournId, token=token))

def revoke_token(session: Session, tournId: str, token: str, *, logger: Logger = Logger.click()):
  stmt = select(Token).where(Token.tournId == tournId, Token.token == token)
  if (tok := session.exec(stmt).first()):
    logger(f'Revoking token "{token}" for "{tournId}"')
    session.delete(tok)
  else:
    logger(f'Token "{token}" not found for "{tournId}"')

class API:
  def __init__(self, session: Session, logger: Logger = Logger.click()):
    self.session = session
    self.logger = logger

  def list_tnmts(self):
    return self.session.exec(select(Tournament.tournId)).all()

  def upsert_tnmt(self, tnmt: Tournament):
    upsert_tnmt(self.session, tnmt, logger=self.logger)

  def upsert_model(self, tournId: str, model: str):
    upsert_model(self.session, tournId, model, logger=self.logger)

  def upsert_round(self, tournId: str, group: str, round: str, start: datetime):
    upsert_round(self.session, tournId, group, round, start=start, logger=self.logger)

  def upsert_pairings(self, tournId: str, group: str, pairings: cs.Source):
    upsert_pairings(self.session, tournId, group, pairings, logger=self.logger)

  def list_tokens(self, tournId: str):
    return list_tokens(self.session, tournId)
  
  def add_token(self, tournId: str, token: str):
    add_token(self.session, tournId, token, logger=self.logger)

  def revoke_token(self, tournId: str, token: str):
    revoke_token(self.session, tournId, token, logger=self.logger)

  def upsert_details(self, tnmt: Tournament, rounds: Mapping[str, Mapping[str, datetime]]):
    self.upsert_tnmt(tnmt)
    for group, rnds in rounds.items():
      for rnd, start in rnds.items():
        self.upsert_round(tnmt.tournId, group, rnd, start)
