import typer
from sqlmodel import create_engine, Session
from moveread.tnmt import jobs

main = typer.Typer()

pairings = typer.Typer()
main.add_typer(pairings, name='pairings')

@pairings.command()
async def current(
  sql: str = typer.Option(help='SQL connection string', envvar='SQL_CONN_STR')
):
  engine = create_engine(sql)
  with Session(engine) as session:
    await jobs.scrape_current_pairings(session)

@pairings.command()
async def all(
  sql: str = typer.Option(help='SQL connection string', envvar='SQL_CONN_STR')
):
  engine = create_engine(sql)
  with Session(engine) as session:
    await jobs.scrape_all_pairings(session)