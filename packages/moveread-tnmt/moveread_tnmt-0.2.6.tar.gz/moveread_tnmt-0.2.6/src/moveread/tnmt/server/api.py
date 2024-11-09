from typing import Literal
import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI, Response, UploadFile
from fastapi.responses import StreamingResponse
from kv import LocatableKV
from dslog import Logger
from dslog.uvicorn import setup_loggers_lifespan, DEFAULT_FORMATTER, ACCESS_FORMATTER
import chess_pairings as cp
from moveread.tnmt import Tournament, Group, FrontendGame, FrontendPGN
from .sdk import SDK
from .util import notify, Bearer

def fastapi(
  sdk: SDK, images: LocatableKV[bytes], *,
  logger: Logger = Logger.click().prefix('[TNMT API]'),
):

  app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
    lifespan=setup_loggers_lifespan(
      access=logger.format(ACCESS_FORMATTER),
      uvicorn=logger.format(DEFAULT_FORMATTER),
    )
  )

  @app.get('/authorize/{tournId}', responses={ 401: {}, 200: {} })
  def authorize(tournId: str, token: str = Bearer):
    authed = sdk.authorize(token, tournId)
    return Response(status_code=200 if authed else 401)

  @app.get('/')
  def get_tournaments(skip: int = 0, take: int = 10) -> list[Tournament]:
    return list(sdk.get_tnmts(skip, take))

  @app.get('/{tournId}', responses={ 404: {}, 200: { 'model': Tournament }})
  def get_tournament(tournId: str, resp: Response) -> Tournament | None:
    tnmt = sdk.get_tnmt(tournId)
    if tnmt is None:
      resp.status_code = 404
    return tnmt

  @app.get('/{tournId}/{group}.pgn', response_model=str)
  def get_group_pgn(tournId: str, group: str, skip: int = 0, take: int | None = None, no_cache: bool = False):
    pgn = sdk.get_group_pgn(**cp.groupId(tournId, group), skip=skip, take=take, no_cache=no_cache)
    return StreamingResponse(content=pgn, media_type='application/x-chess-pgn', headers={
      'Content-Disposition': f'attachment; filename={tournId}_{group}.pgn'
    })

  @app.get('/{tournId}/{group}/', responses={ 404: {}, 200: { 'model': Group }})
  def get_group(tournId: str, group: str, r: Response) -> Group | None:
    grp = sdk.get_group(tournId, group)
    if grp is None:
      r.status_code = 404
    return grp

  @app.get('/{tournId}/{group}/{round}.pgn', response_model=str)
  def get_round_pgn(tournId: str, group: str, round: str, skip: int = 0, take: int | None = None, no_cache: bool = False):
    pgn = sdk.get_round_pgn(**cp.roundId(tournId, group, round), skip=skip, take=take, no_cache=no_cache)
    return StreamingResponse(content=pgn, media_type='application/x-chess-pgn', headers={
      'Content-Disposition': f'attachment; filename={tournId}_{group}_{round}.pgn'
    })
  
  @app.get('/{tournId}/{group}/{round}')
  def get_round(tournId: str, group: str, round: str) -> list[FrontendGame]:
    return list(sdk.get_round(**cp.roundId(tournId, group, round)))

  @app.get('/{tournId}/{group}/{round}/{board}/pgn')
  def get_pgn(tournId: str, group: str, round: str, board: str, resp: Response) -> FrontendPGN | None:
    pgn = sdk.get_pgn(**cp.gameId(tournId, group, round, board))
    # if pgn is None:
      # resp.status_code = 404
    return pgn

  @app.get('/{tournId}/{group}/{round}/{board}/images', responses={ 404: {}, 200: { 'model': list[str] }})
  def get_images(tournId: str, group: str, round: str, board: str, resp: Response) -> list[str] | None:
    urls = sdk.get_images(**cp.gameId(tournId, group, round, board))
    if urls is None or len(urls) == 0:
      resp.status_code = 404
      return None
    
    expiry = datetime.now() + timedelta(hours=1)
    return [images.url(url, expiry=expiry) for url in urls]

  # @app.post('/{tournId}/{group}/{round}/{board}/move', responses={
  #   401: dict(model=Literal['UNAUTHORIZED']),
  #   200: dict(model=Literal['OK']),
  #   500: dict(model=Literal['ERROR'])
  # })
  # def move_game(
  #   tournId: str, group: str, round: str, board: str,
  #   new_board: str, resp: Response, token: str = Bearer,
  # ) -> Literal['OK', 'UNAUTHORIZED', 'ERROR']:
  #   if not sdk.authorize(token, tournId):
  #     resp.status_code = 401
  #     return 'UNAUTHORIZED'
    
  #   from_id = cp.gameId(tournId, group, round, board)
  #   to_id = cp.gameId(tournId, group, round, new_board)
  #   try:
  #     post = sdk.move_game(from_id, to_id)
  #     asyncio.create_task(post)
  #     return 'OK'
  #   except Exception as e:
  #     logger(f'Error moving "{cp.stringifyId(**from_id)}" -> "{cp.stringifyId(**to_id)}":', e, level='ERROR')
  #     resp.status_code = 500
  #     return 'ERROR'


  @app.post('/{tournId}/{group}/{round}/{board}/pgn', responses={
    401: dict(model=Literal['UNAUTHORIZED']),
    200: dict(model=Literal['OK']),
    500: dict(model=Literal['ERROR'])
  })
  async def post_pgn(
    tournId: str, group: str, round: str, board: str,
    pgn: list[str], r: Response, token: str = Bearer
  ) -> Literal['OK', 'UNAUTHORIZED', 'ERROR']:
    
    if not sdk.authorize(token, tournId):
      r.status_code = 401
      return 'UNAUTHORIZED'
    
    gid = cp.gameId(tournId, group, round, board)
    try:
      sdk.post_pgn(pgn, **gid)
      return 'OK'
    except Exception as e:
      logger(f'Error posting PGN "{cp.stringifyId(**gid)}":', e, level='ERROR')
      r.status_code = 500
      return 'ERROR'

  @app.post('/{tournId}/{group}/{round}/{board}', responses={
    401: dict(model=Literal['UNAUTHORIZED']),
    200: dict(model=Literal['OK']),
    500: dict(model=Literal['ERROR'])
  })
  async def post_game(
    tournId: str, group: str, round: str, board: str,
    images: list[UploadFile], r: Response, token: str = Bearer
  ) -> Literal['OK', 'UNAUTHORIZED', 'ERROR']:
  
    if not sdk.authorize(token, tournId):
      r.status_code = 401
      return 'UNAUTHORIZED'
    
    gid = cp.gameId(tournId, group, round, board)
    res, coro = await sdk.post_game(images, **gid)

    async def post_task():
      r = await coro
      logger('Post task finished, returning:', r)
    asyncio.create_task(post_task())
    
    if res.tag == 'left':
      logger(f'Error posting game "{cp.stringifyId(**gid)}":', res.value, level='ERROR')
      r.status_code = 500
      return 'ERROR'
    
    asyncio.create_task(notify(gid, logger))
    return 'OK' 

  # @app.delete('/{tournId}/{group}/{round}/{board}', responses={
  #   401: dict(model=Literal['UNAUTHORIZED']),
  #   500: dict(model=Literal['ERROR']),
  #   200: dict(model=Literal['OK']),
  # })
  # def delete_game(
  #   tournId: str, group: str, round: str, board: str,
  #   resp: Response, token: str = Bearer
  # ):
  #   if not sdk.authorize(token, tournId):
  #     resp.status_code = 401
  #     return 'UNAUTHORIZED'
    
  #   gid = cp.gameId(tournId, group, round, board)
  #   try:
  #     post = sdk.delete_game(**gid)
  #     asyncio.create_task(post)
  #     return 'OK'
  #   except Exception as e:
  #     logger(f'Error deleting game "{cp.stringifyId(**gid)}":', e, level='ERROR')
  #     resp.status_code = 500
  #     return 'ERROR'

  return app