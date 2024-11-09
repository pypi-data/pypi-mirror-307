from typing import Sequence
from datetime import datetime, timedelta
from sqlmodel import select, Session
from haskellian import iter as I, Left, Right
import chess_pairings as cp
from moveread.tnmt import Round, Pairings, Game, Tournament, queries

def current_pairings(session: Session, now: datetime | None = None) -> Sequence[tuple[Tournament, Pairings]]:
  """Ongoing tournaments with available pairings"""
  now = now or datetime.now()
  tomorrow = now + timedelta(days=1)
  yesterday = now - timedelta(days=1)
  stmt = select(Tournament, Pairings) \
    .where(Tournament.start_date < tomorrow, yesterday < Tournament.end_date) \
    .join(Pairings, Tournament.tournId == Pairings.tournId) # type: ignore
  return session.exec(stmt).all()

def round_paired(session: Session, tournId: str, group: str, round: str) -> bool:
  """Does the round have pairings?"""
  stmt = queries.select_round_games(tournId, group, round)
  return session.exec(stmt).first() is not None

def round_finished(session: Session, tournId: str, group: str, round: str) -> bool:
  """Does the round have all results? (WARNING: will return true if unpaired! - by vacuity)"""
  stmt = queries.select_round_games(tournId, group, round).where(Game.result == None)
  return session.exec(stmt).first() is None

def select_paired_rounds(tournId: str, group: str):
  """Select all rounds with pairings"""
  subquery = (
    select(Game.round, Round.start_dtime)
    .where(Game.tournId == tournId, Game.group == group)
    .join(Round, (Game.tournId == Round.tournId) & (Game.group == Round.group) & (Game.round == Round.name)) # type: ignore
    .order_by(Round.start_dtime) # type: ignore
    .distinct()
    .subquery()
  )
  s: str = subquery.c.round # type: ignore
  return select(s)

def current_round(
  session: Session, tournId: str, group: str, *, now: datetime | None = None,
  round_paired = round_paired, round_finished = round_finished
):
  """Determine the current round (whose pairings should be polled)"""
  now = now or datetime.now()
  if not (rounds := session.exec(queries.select_rounds(tournId, group)).all()):
    return Left(f'No rounds found for group "{tournId}/{group}"')
  
  if (prev := I.find_last_idx(lambda r: r.start_dtime < now, rounds)) is None:
    return Right(rounds[0].name)
  
  # if next round (which hasn't yet started) is paired, nothing to do
  if prev+1 < len(rounds) and round_paired(session, **cp.roundId(tournId, group, rounds[prev+1].name)):
    return Right(None)
  
  # if current round is finished, poll the next round if it exists
  if round_finished(session, **cp.roundId(tournId, group, rounds[prev].name)):
    if prev+1 < len(rounds):
      return Right(rounds[prev+1].name)
    else:
      return Right(None)
  
  # otherwise, poll the current round
  return Right(rounds[prev].name)