from typing import TypeVar, Generic, Callable, Iterable
import os
from time import time
from fastapi import UploadFile, Request, HTTPException, Depends
from dslog import Logger
import pure_cv as vc
from chess_pairings import GameId

def token(req: Request) -> str:
  auth = req.headers.get('Authorization') or ''
  if (parts := auth.split(' ')) and len(parts) == 2:
    return parts[1]
  raise HTTPException(status_code=401)

Bearer: str = Depends(token)

async def notify(gameId: GameId, logger: Logger):
  endpoint = os.getenv('NOTIFY_ENDPOINT')
  token = os.getenv('NOTIFY_TOKEN')
  try:
    if endpoint is None:
      raise ValueError('No NOTIFY_ENDPOINT environment variable')
    import aiohttp
    async with aiohttp.ClientSession() as session:
      async with session.post(endpoint, json=gameId, headers=[('Authorization', f'Bearer {token}')]) as r: # type: ignore
        if r.status == 200:
          logger(f'Notified "{endpoint}" of game {gameId}', level='DEBUG')
        else:
          logger(f'Failed to notify "{endpoint}" of game {gameId}: {r.status}. Content:', await r.text(), level='ERROR')
  except Exception as e:
    logger(f'Exception notifying "{endpoint}" of game {gameId}:', e, level='ERROR')


def safe_extension(file: UploadFile) -> str | None:
  if file.filename and len(parts := file.filename.split('.')) == 2:
    return parts[1]
  
def descale2jpg(img: bytes, height: int):
  mat = vc.decode(img)
  return vc.encode(vc.descale_h(mat, height), format='.jpg')

K = TypeVar('K')
T = TypeVar('T')

class TimedIterableCache(Generic[K, T]):
  def __init__(self, get: Callable[[K], Iterable[T]], *, ttl_secs: float, max_entries: int):
    self._get = get
    self.ttl_secs = ttl_secs
    self._cache: dict[K, tuple[list[T], float]] = {}
    self.max_entries = max_entries

  def insert(self, k: K, access_time: float | None = None) -> Iterable[T]:
    access_time = access_time or time()
    if len(self._cache) >= self.max_entries:
      older_client = min(self._cache.keys(), key=self._cache.__getitem__)
      del self._cache[older_client]
    
    def gen():
      stored = []
      for x in self._get(k):
        stored.append(x)
        yield x
      self._cache[k] = stored, access_time

    yield from gen()


  def __getitem__(self, key: K) -> Iterable[T]:
    now = time()
    if key not in self._cache or now - self._cache[key][1] > self.ttl_secs:
      yield from self.insert(key, now)
    else:
      yield from self._cache[key][0]