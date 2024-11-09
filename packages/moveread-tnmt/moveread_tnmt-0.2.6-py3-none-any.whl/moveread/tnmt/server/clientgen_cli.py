import os
from argparse import ArgumentParser
from openapi_ts import generate_client
from moveread.tnmt.server import fastapi

def main():

  parser = ArgumentParser()
  parser.add_argument('-o', '--output', required=True)
  args = parser.parse_args()

  app = fastapi({}, {}) # type: ignore
  spec = app.openapi()
  generate_client(spec, args.output, args={
    '--client': '@hey-api/client-fetch',
    '--services': '{ asClass: false }',
    '--schemas': 'false'
  })

if __name__ == '__main__':
  main()