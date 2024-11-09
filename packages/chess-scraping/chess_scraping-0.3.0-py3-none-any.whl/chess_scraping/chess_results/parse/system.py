from typing import Literal, get_args
from bs4 import BeautifulSoup
from chess_scraping import PairingSystem

CRSystem = Literal['Swiss-System', 'Round robin']
CR_SYSTEMS = get_args(CRSystem)

def parse(cr_system: CRSystem) -> PairingSystem:
  if cr_system == 'Swiss-System':
    return 'swiss'
  else:
    return 'round-robin'

def find_system(soup: BeautifulSoup) -> PairingSystem | None:
  try:
    system = soup.find(string='Tournament type').find_next().get_text() # type: ignore
    if system in CR_SYSTEMS:
      return parse(system) # type: ignore
  except:
    ...