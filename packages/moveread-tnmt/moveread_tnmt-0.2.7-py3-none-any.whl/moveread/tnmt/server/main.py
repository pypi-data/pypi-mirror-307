import os

DEFAULT_ORIGINS = [
  'http://localhost:5173',
  'http://localhost:4713',
  'https://localhost',
  'https://moveread.com',
  'https://dfy.moveread.com',
  'https://tnmt.moveread.com',
]

def get_env(variable: str, default=None, required=True):
  value = os.getenv(variable, default)
  if value is None and required:
      raise ValueError(f"Environment variable {variable} is required.")
  return value

# Check environment variables first
if get_env('LOAD_DOTENV', required=False):
  from dotenv import load_dotenv
  load_dotenv()
   
blob_conn_str = get_env('BLOB_CONN_STR')
sql_conn_str = get_env('SQL_CONN_STR')
images_path = get_env('IMAGES_PATH', default=None, required=False)
cache_ttl = float(get_env('CACHE_TTL', default=60*5)) # type: ignore
cache_max_entries = int(get_env('CACHE_MAX_ENTRIES', default=1000)) # type: ignore
port = int(get_env('PORT', default=80)) # type: ignore
host = get_env('HOST', default='0.0.0.0')
cors_origins = get_env('CORS_ORIGINS', default=",".join(DEFAULT_ORIGINS)).split(",") # type: ignore

# Import other modules after checking environment variables
from dslog import Logger, formatters
from kv import KV, LocatableKV
from sqlmodel import create_engine
from fastapi.middleware.cors import CORSMiddleware
from moveread.tnmt import server

logger = Logger.stderr().format(formatters.click)
logger('Starting API...')
logger('- Cache TTL: ', cache_ttl)
logger('- Cache Max Entries: ', cache_max_entries)
logger('- CORS allowed origins: ', cors_origins)

blobs = KV.of(blob_conn_str) # type: ignore
assert isinstance(blobs, LocatableKV)

engine = create_engine(sql_conn_str) # type: ignore

sdk = server.SDK(blobs, engine, cache_ttl=cache_ttl, cache_max_entries=cache_max_entries)
app = server.fastapi(sdk, images=blobs, logger=logger)
app.add_middleware(CORSMiddleware, allow_origins=cors_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
