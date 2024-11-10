from haskellian import either as E
from chess_pairings import GroupPairings, RoundPairings
from chess_scraping import ScrapingError
from .download import download_round
from .parse import paired_rounds, parse_round, parse_team_round

@E.do[ScrapingError]()
async def scrape_round(id: str, round: int | str, *, team: bool = False) -> RoundPairings:
  soup = (await download_round(id, round, team=team)).unsafe()
  parse = parse_team_round if team else parse_round
  return parse(soup).unsafe()

@E.do[ScrapingError]()
async def scrape_group(id: str, team: bool = False) -> GroupPairings:
  """Scrape all rounds of the group, by:
  1. Scrapes the first round -> pairings and #rounds
  2. Scrapes subsequent rounds
  """
  first_round = (await download_round(id, 1, team=team)).unsafe()
  parse = parse_team_round if team else parse_round
  first_pairings = parse(first_round).unsafe()
  rounds = E.maybe(paired_rounds(first_round)).unsafe()
  other_pairings = []
  for i in rounds[1:]:
    r = (await scrape_round(id, i, team=team)).unsafe()
    other_pairings.append(r)
  return { str(i+1): p for i, p in enumerate([first_pairings] + other_pairings) }