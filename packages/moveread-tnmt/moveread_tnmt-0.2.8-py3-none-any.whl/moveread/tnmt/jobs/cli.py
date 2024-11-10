import asyncio
import typer
from sqlmodel import create_engine, Session
from moveread.tnmt import jobs

main = typer.Typer()

pairings = typer.Typer()
main.add_typer(pairings, name='pairings')

@pairings.command()
def current(
  sql: str = typer.Option(help='SQL connection string', envvar='SQL_CONN_STR')
):
  engine = create_engine(sql)
  with Session(engine) as session:
    asyncio.run(jobs.scrape_current_pairings(session))

@pairings.command()
def all(
  sql: str = typer.Option(help='SQL connection string', envvar='SQL_CONN_STR')
):
  engine = create_engine(sql)
  with Session(engine) as session:
    asyncio.run(jobs.scrape_all_pairings(session))