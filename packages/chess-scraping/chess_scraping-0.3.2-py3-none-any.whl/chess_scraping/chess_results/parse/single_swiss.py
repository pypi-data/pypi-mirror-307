import re
from bs4 import BeautifulSoup
from haskellian import Left, either as E
from chess_pairings import Paired, Pairing, GroupPairings
from .common import parse_row, parse_columns, extract_round


@E.do()
def parse_single_swiss(soup: BeautifulSoup) -> GroupPairings:
  rounds: dict[str, list[Pairing]] = {}
  columns = parse_columns(soup).unsafe()
  headings = soup.find_all(string=re.compile(r'^Round \d+'))

  for h in headings:
    rnd = h.get_text(strip=True).split(" ")[1]
    table = h.find_next("table")
    if table is None:
      Left(f'Unable to find table for heading {h}').unsafe()
    
    pairs = [
      parse_row(pair, board=str(i+1))
      for i, pair in enumerate(extract_round(table.find_all('tr'), columns))
    ]

    # some rounds may have byes in advance. So, check wether any pair is actually paired
    if any(isinstance(p, Paired) for p in pairs):
      rounds[rnd] = pairs

  return rounds
