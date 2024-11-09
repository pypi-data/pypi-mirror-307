from typing_extensions import Iterable, Unpack, Sequence, Coroutine, Any
from dataclasses import dataclass
import asyncio
from uuid import uuid4
from sqlalchemy import Engine
from sqlmodel import Session, select
from fastapi import UploadFile
from haskellian import either as E, Left, Either, promise as P, Iter
from kv import KV, InexistentItem
import chess_pairings as cp
from moveread.tnmt import Token, Tournament, Group, FrontendGame, queries, Game, FrontendPGN, \
  Image, PGN, Upload
from .util import TimedIterableCache, safe_extension, descale2jpg
from .pgns import export_all


@dataclass
class SDK:
  images: KV[bytes]
  engine: Engine
  cache_ttl: float = 30
  cache_max_entries: int = 1000

  def __post_init__(self):
    self.pgns_cache = TimedIterableCache(self.gen_round_pgn, ttl_secs=self.cache_ttl, max_entries=self.cache_max_entries)

  def authorize(self, token: str, tournId: str) -> bool:
    with Session(self.engine) as ses:
      results = ses.exec(select(Token).where(Token.token == token, Token.tournId == tournId))
      return results.first() is not None
    
  def get_tnmts(self, skip: int = 0, take: int = 10) -> Iterable[Tournament]:
    with Session(self.engine) as ses:
      ord: Any = Tournament.start_date.desc() # type: ignore (yeah)
      stmt = select(Tournament).order_by(ord) \
        .offset(skip).limit(take)
      return ses.exec(stmt).all()

  def get_tnmt(self, tournId: str) -> Tournament | None:
    with Session(self.engine) as ses:
      return ses.get(Tournament, tournId)
    
  def get_group(self, tournId: str, group: str) -> Group | None:
    with Session(self.engine) as ses:
      rounds = ses.exec(queries.select_paired_rounds(tournId, group)).all()
      return Group(tournId=tournId, name=group, rounds=rounds)
  
  def get_round(self, **roundId: Unpack[cp.RoundId]) -> Iterable[FrontendGame]:
    with Session(self.engine) as ses:
      stmt = select(Game).where(*queries.round_games(**roundId)).order_by(Game.index) # type: ignore
      for g in ses.exec(stmt):
        yield FrontendGame.of(g)

  def gen_round_pgn(self, roundId: tuple[str, str, str]):
    rid = cp.roundId(*roundId)
    with Session(self.engine) as ses:
      round = ses.exec(queries.select_round(**rid)).first()
      stmt = select(Game).where(*queries.round_games(**rid)).order_by(Game.index) # type: ignore
      games = ses.exec(stmt).all()
      tnmt = ses.exec(queries.select_tnmt(rid['tournId'])).first()
      yield from export_all(games, tnmt, round)
    
  def get_round_pgn(self, *, skip: int = 0, take: int | None = None, tournId: str, group: str, round: str, no_cache: bool = False) -> Iterable[str]:
    id = (tournId, group, round)
    iter = self.pgns_cache[id] if not no_cache else self.pgns_cache.insert(id)
    iter = Iter(iter).skip(skip)
    return iter.take(take) if take is not None else iter
  
  def get_group_pgn(self, *, skip: int = 0, take: int | None = None, no_cache: bool = False, **groupId: Unpack[cp.GroupId]) -> Iterable[str]:
    with Session(self.engine) as ses:
      rounds = ses.exec(queries.select_paired_rounds(**groupId)).all()
      for round in rounds:
        yield from self.get_round_pgn(skip=skip, take=take, **groupId, round=round, no_cache=no_cache)
  
  def get_pgn(self, **gameId: Unpack[cp.GameId]) -> FrontendPGN | None:
    with Session(self.engine) as ses:
      game = ses.exec(queries.select_game(**gameId)).first()
      if game and game.upload and game.upload.pgn:
        return game.upload.pgn
      
  def post_pgn(self, pgn: Sequence[str], **gameId: Unpack[cp.GameId]):
    with Session(self.engine) as ses:
      if (game := ses.exec(queries.select_game(**gameId)).first()):
        game.upload = Upload(
          id=f'{cp.stringifyId(**gameId)}_{uuid4()}',
          pgn=PGN(moves=pgn), status='done'
        )
        ses.add(game)
        ses.commit()
      
  def get_images(self, **gameId: Unpack[cp.GameId]) -> list[str] | None:
    with Session(self.engine) as ses:
      game = ses.exec(queries.select_game(**gameId)).first()
      if game and game.upload:
        return [img.descaled_url for img in game.upload.imgs]
      
  async def _upload(self, image: UploadFile, url: str):
    return await self.images.insert(url, await image.read())
  
  async def _descale_imgs(self, imgs: Sequence[tuple[str, bytes]], target_height: int):
    """Descales and uploads the images. Expects `(url, img)` tuples"""
    descaled = [descale2jpg(img, target_height) for _, img in imgs]
    uploads = [self.images.insert(url, img) for (url, _), img in zip(imgs, descaled)]
    return await asyncio.gather(*uploads)

  async def post_game(
    self, images: Sequence[UploadFile],
    descaled_height: int = 768, **gameId: Unpack[cp.GameId]
  ) -> tuple[Either, Coroutine]:
    """ - Runs tasks that must happen before responding to the client.
    - Returns the result + a coroutine that must run after responding (independent of the result)
    """
    img_urls = []
    descaled_urls = []
    delete_urls = []
    imgs = []

    try:
      with Session(self.engine) as ses:
        game = ses.exec(queries.select_game(**gameId)).first()
        if game is None:
          return Left(InexistentItem(detail=f'Game {gameId} not found in DB')), P.of(None).run()
        
        uuid = f'{cp.stringifyId(**gameId)}_{uuid4()}'
        img_urls = [f'{uuid}/{i}.' + (safe_extension(img) or 'jpg') for i, img in enumerate(images)]
        descaled_urls = [f'{uuid}/{i}-{descaled_height}.jpg' for i in range(len(images))]

        imgs = await asyncio.gather(*[img.read() for img in images])
        original_uploads = [self.images.insert(url, img) for url, img in zip(img_urls, imgs)]
        res = E.sequence(await asyncio.gather(*original_uploads))

        if (upl := game.upload):
          delete_urls = [img.url for img in upl.imgs] + [img.descaled_url for img in upl.imgs]
          [ses.delete(img) for img in upl.imgs]

        upload = Upload(
          id=uuid, status='uploaded',
          imgs=[Image(url=url, descaled_url=url) for url in img_urls]
        )
        game.upload = upload
        ses.add(upload)
        ses.add(game)
        ses.commit()

    except Exception as e:
      res = Left(e)

    if res.tag == 'right':
      async def post_tasks():
        deletions = [self.images.delete(url) for url in delete_urls]
        descaled_uploads = self._descale_imgs(list(zip(descaled_urls, imgs)), descaled_height)
        await asyncio.gather(*deletions, descaled_uploads)

        with Session(self.engine) as ses:
          if (game := ses.exec(queries.select_game(**gameId)).first()) and game.upload:
            for img, descaled_url in zip(game.upload.imgs, descaled_urls):
              img.descaled_url = descaled_url
              ses.add(img)
            ses.commit()

    else:
      async def post_tasks():
        await asyncio.gather(*[self.images.delete(url) for url in img_urls]) # not to leak storage

    return res, post_tasks()
