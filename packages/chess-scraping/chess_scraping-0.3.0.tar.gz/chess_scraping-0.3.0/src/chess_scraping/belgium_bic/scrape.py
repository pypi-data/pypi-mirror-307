from haskellian import either as E
from chess_pairings import GroupPairings, RoundPairings
from chess_scraping import ScrapingError
from .download import download_round
from .parse import find_rounds, parse_round

@E.do[ScrapingError]()
async def scrape_round(*, year: int | str, group: str, round: int | str) -> RoundPairings:
  soup = (await download_round(year=year, round=round)).unwrap()
  return parse_round(soup, group=group).unwrap()

@E.do[ScrapingError]()
async def scrape_group(*, year: int | str, group: str) -> GroupPairings:
  """Scrape all rounds of the group, by:
  1. Scrapes the first round -> pairings and find rounds
  2. Scrapes subsequent rounds until an empty round is hit
  """
  print('Scraping first round...')
  first_round = (await download_round(year=year, round=1)).unwrap()
  first_pairings = parse_round(first_round, group=group).unwrap()
  rounds = find_rounds(first_round).unwrap()
  pairings = [first_pairings]
  for rnd in rounds[1:]:
    print(f'Scraping round {rnd}...')
    round = (await scrape_round(year=year, group=group, round=rnd)).unwrap()
    if all(pair.tag != 'paired' for pair in round):
      break
    pairings.append(round)
  
  return dict(zip(rounds, pairings))