from haskellian import either as E
from chess_pairings import GroupPairings, RoundPairings
from chess_scraping import ScrapingError
from .download import download_round
from .parse import paired_rounds, parse_round

@E.do[ScrapingError]()
async def scrape_round(id: int | str, round: int | str) -> RoundPairings:
  soup = (await download_round(id, round)).unsafe()
  return parse_round(soup).unsafe()

@E.do[ScrapingError]()
async def scrape_group(id: int | str) -> GroupPairings:
  """Scrape all rounds of the group, by:
  1. Scrapes the first round -> pairings and #rounds
  2. Scrapes subsequent rounds
  """
  first_round = (await download_round(id, 1)).unsafe()
  first_pairings = parse_round(first_round).unsafe()
  rounds = E.maybe(paired_rounds(first_round)).unsafe()
  other_pairings = []
  for i in rounds[1:]:
    r = (await scrape_round(id, i)).unsafe()
    other_pairings.append(r)
  return { str(i+1): p for i, p in enumerate([first_pairings] + other_pairings) }