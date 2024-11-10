from haskellian import Left, Right, Either
from bs4 import BeautifulSoup
import chess_pairings as cp
import chess_scraping as cs

def parse_result(r: str) -> 'cp.Result | None':
  if r == '1 - 0':
    return '1-0'
  elif r == '0 - 1':
    return '0-1'
  elif r == 'X - X':
    return '1/2-1/2'
  elif r == '1 - F':
    return '+-'
  elif r == 'F - 1':
    return '+-'
  
def parse_round(soup: BeautifulSoup) -> 'Either[cs.ParsingError, cp.RoundPairings]':
  try:
    rows = soup.find_all('tr', class_=['papi_liste_f', 'papi_liste_c'])
    out: cp.RoundPairings = []
    
    for i, row in enumerate(rows):
      cells = row.find_all('td')
      result = parse_result(cells[4].text.strip())
      white = cells[2].text.strip()
      black = cells[5].text.strip()
      out.append(cp.Paired(white=white, result=result, black=black, board=str(i+1)))

    return Right(out)
  
  except Exception as e:
    return Left(cs.ParsingError(str(e)))