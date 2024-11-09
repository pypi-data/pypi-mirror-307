from haskellian import either as E, iter as I
from chess_pairings import GroupPairings, RoundPairings
from chess_scraping import ScrapingError
from .download import download_round
from .parse import parse_round

@E.do[ScrapingError]()
async def scrape_round(id: str, round: int | str) -> RoundPairings:
  soup = (await download_round(id, round)).unsafe()
  return parse_round(soup).unsafe()

@E.do[ScrapingError]()
async def scrape_group(id: str) -> GroupPairings:
  """Scrape all rounds of the group, by scraping in succession until no more rounds are found."""
  out: GroupPairings = {}
  for i in I.range(1):
    e = await scrape_round(id, i)
    if e.tag == 'left' or not e.value:
      break
    out[str(i)] = e.value

  return out