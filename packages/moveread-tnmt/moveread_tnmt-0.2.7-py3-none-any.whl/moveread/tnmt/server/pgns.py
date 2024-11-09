from typing import Iterable
from chess_utils import PGNHeaders, export_pgn
from .._types import Game, Tournament, Round

def export(game: Game, tnmt: Tournament | None = None, round: Round | None = None) -> str | None:
  site = tnmt and tnmt.site
  event = tnmt and tnmt.name
  dtime = round and round.start_dtime
  headers = PGNHeaders(
    Event=event, Site=site, White=game.white, Black=game.black,
    Round=f'{game.round}.{game.board}', Result=game.result,
    Date=dtime and dtime.strftime('%Y.%m.%d')
  )
  upl = game.upload
  if upl and upl.pgn:
    comment = '[...]' if upl.pgn.early else None
    return export_pgn(upl.pgn.moves, headers, comment)
  else:
    return export_pgn([], headers)

def export_all(games: Iterable[Game], tnmt: Tournament | None = None, round: Round | None = None) -> Iterable[str]:
  for game in games:
    if (pgn := export(game, tnmt, round)) is not None:
      yield pgn + '\n\n'