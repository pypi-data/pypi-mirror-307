from argparse import ArgumentParser
import os

DEFAULT_ORIGINS = [
  'http://localhost:5173',
  'http://localhost:4713',
  'http://localhost:5000',
  'https://moveread.com',
  'https://dfy.moveread.com',
  'https://tnmt.moveread.com',
]

def env(variable: str, *, default = None, required: bool = True) -> dict:
  if (value := os.getenv(variable, default)) is not None:
    return dict(default=value)
  return dict(required=required)

def main():
  parser = ArgumentParser()
  parser.add_argument('--blob', type=str, **env('BLOB_CONN_STR'), help='Blobs KV connection string  ')
  parser.add_argument('--sql', type=str, **env('SQL_CONN_STR'), help='SQL connection string')
  parser.add_argument('--url', type=str, help='URL of the API')
  parser.add_argument('--ttl', type=float, default=60*5, help='PGN Cache TTL (seconds)')
  parser.add_argument('--max-entries', type=int, default=1000, help='PGN Cache max entries')

  parser.add_argument('-p', '--port', type=int, default=80)
  parser.add_argument('--host', type=str, default='0.0.0.0')
  parser.add_argument('--cors', default=DEFAULT_ORIGINS, nargs='*', type=str, help='CORS allowed origins')

  args = parser.parse_args()

  from dslog import Logger, formatters
  logger = Logger.stderr().format(formatters.click)
  logger('Starting API...')
  logger('- Cache TTL: ', args.ttl)
  logger('- Cache Max Entries: ', args.max_entries)
  logger('- CORS allowed origins: ', args.cors)

  from kv import KV, LocatableKV, FilesystemKV, ServerKV
  blobs = locatable_blobs = KV.of(args.blob)
  if isinstance(blobs, FilesystemKV) and args.url:
    locatable_blobs = blobs.served(args.url.rstrip('/') + '/images')
  elif not isinstance(blobs, LocatableKV):
    raise ValueError('Either blobs must be a LocatableKV, or --url be provided')

  from sqlmodel import create_engine
  engine = create_engine(args.sql)

  from moveread.tnmt import server
  from fastapi.middleware.cors import CORSMiddleware
  import uvicorn

  sdk = server.SDK(blobs, engine, cache_ttl=args.ttl, cache_max_entries=args.max_entries)
  api = server.fastapi(sdk, images=locatable_blobs, logger=logger) # type: ignore
  api.add_middleware(CORSMiddleware, allow_origins=args.cors, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
  api.mount('/images', ServerKV(blobs))

  uvicorn.run(api, host=args.host, port=args.port)