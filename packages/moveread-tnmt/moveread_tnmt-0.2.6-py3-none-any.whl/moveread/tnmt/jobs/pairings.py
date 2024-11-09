from datetime import datetime
from sqlmodel import Session
import chess_pairings as cp 
import chess_scraping as cs
from moveread.tnmt import Game, queries
from dslog import Logger

def update_round_pairings(session: Session, *, tournId: str, group: str, round: str, pairings: cp.RoundPairings):
  """Insert/update pairings of a round"""
  round_games = session.exec(queries.select_round_games(**cp.roundId(tournId, group, round))).all()
  games_idx = cp.GamesMapping[Game].from_pairs([(g.gameId(), g) for g in round_games])
  added: list[cp.GameId] = []
  updated: list[cp.GameId] = []

  for board, pair in pairings.items():
    if pair.tag != 'paired':
      continue
    gid = cp.gameId(tournId, group, round, board)
    if gid in games_idx:
      game = games_idx[gid]
      if game.white != pair.white or game.black != pair.black or game.result != pair.result:
        game.white = pair.white; game.black = pair.black; game.result = pair.result
        updated.append(gid)
    else:
      game = Game(
        tournId=tournId, group=group, round=round, board=board, index=int(board)-1,
        white=pair.white, black=pair.black, result=pair.result
      )
      added.append(gid)
    session.add(game)
  
  session.commit()
  return added, updated

def index(board: str):
  if len(parts := board.split('.')) == 2:
    team, player = int(parts[0]), int(parts[1])
    return 1000*team + player # surely no team has more than 1000 players!
  return int(board)-1
  
  
def update_group_pairings(session: Session, *, tournId: str, group: str, pairings: cp.GroupPairings):
    """Insert/update pairings of a group"""
    group_games = session.exec(queries.select_group_games(tournId, group)).all()
    games_idx = cp.GamesMapping[Game].from_pairs([(g.gameId(), g) for g in group_games])
    added: list[cp.GameId] = []
    updated: list[cp.GameId] = []

    for round, rnd_pairings in pairings.items():
      for board, pair in rnd_pairings.items():
        if pair.tag != 'paired':
          continue
        gid = cp.gameId(tournId, group, round, board)
        if gid in games_idx:
          game = games_idx[gid]
          if game.white != pair.white or game.black != pair.black or game.result != pair.result:
            game.white = pair.white; game.black = pair.black; game.result = pair.result
            updated.append(gid)
        else:
          game = Game(
            tournId=tournId, group=group, round=round, board=board, index=index(board),
            white=pair.white, black=pair.black, result=pair.result
          )
          added.append(gid)
        session.add(game)
    session.commit()
    return added, updated


async def scrape_all_pairings(
  session: Session, *, now: datetime | None = None, logger: Logger = Logger.click(),
  scrape_group = cs.scrape_group
):
  """Updates pairings for all ongoing tournaments"""
  pairing_sources = queries.current_pairings(session, now)
  current_tnmts = [tnmt.tournId for tnmt, _ in pairing_sources]
  logger(f'Updating current tournaments: {", ".join(current_tnmts)}')
  for tnmt, src in pairing_sources:
    e = await scrape_group(src.pairings)
    if e.tag == 'left':
      logger(f'Error fetching pairings for "{tnmt.tournId}/{src.group}"', e.value, level='ERROR')
      continue
    added, updated = update_group_pairings(session, tournId=tnmt.tournId, group=src.group, pairings=e.value)
    logger(f'Updated pairings for "{tnmt.tournId}/{src.group}", added {len(added)} and updated {len(updated)} games', level='DEBUG')


async def scrape_current_pairings(
  session: Session, *, now: datetime | None = None, logger: Logger = Logger.click(),
  scrape_round = cs.scrape_round
):
  pairing_sources = queries.current_pairings(session, now)
  current_tnmts = [tnmt.tournId for tnmt, _ in pairing_sources]
  logger(f'Updating current tournaments: {", ".join(current_tnmts)}')
  for tnmt, src in pairing_sources:
    e = queries.current_round(session, tnmt.tournId, src.group, now=now)
    if e.tag == 'left':
      logger(f'Error finding current round for "{tnmt.tournId}/{src.group}":', e.value, level='ERROR')
      continue
    if (rnd := e.value) is None:
      logger(f'No round to poll for "{tnmt.tournId}/{src.group}"')
      continue

    logger(f'Updating current round for {tnmt.tournId} {src.group}: {rnd}')
    e = await scrape_round(src.pairings, rnd)
    if e.tag == 'left':
      logger(f'Error scraping pairings for "{tnmt.tournId}/{src.group}":', e.value, level='WARNING')
      continue
    
    added, updated = update_round_pairings(session, tournId=tnmt.tournId, group=src.group, round=rnd, pairings=e.value)
    logger(f'Updated pairings for "{tnmt.tournId}/{src.group}", added {len(added)} and updated {len(updated)} games', level='DEBUG')