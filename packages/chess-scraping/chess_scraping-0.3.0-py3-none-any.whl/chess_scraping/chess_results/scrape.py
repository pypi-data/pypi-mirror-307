from haskellian import Either, either as E
from chess_pairings import GroupPairings, RoundPairings
from chess_scraping import ScrapingError
from .download import download_pairings, download_round
from .parse import parse_rounds, parse_round

async def scrape_group(db_key: int | str) -> Either[ScrapingError, GroupPairings]:
  soup = await download_pairings(db_key)
  return soup.bind(parse_rounds)

@E.do[ScrapingError]()
async def scrape_round(db_key: int | str, round: int | str) -> RoundPairings:
  soup = (await download_round(db_key, round)).unsafe()
  return parse_round(soup, str(round)).unsafe()