from bs4 import Tag, BeautifulSoup
from haskellian import Either, Left, Right, either as E
from chess_pairings import Result, Paired, Unpaired, Pairing, RoundPairings
from chess_scraping import ParsingError

def parse_result(result) -> Result | None:
  if not isinstance(result, str) or len(result) < 2:
    return None
  w, *_, b = result
  match w+b:
    case '10':
      return '1-0'
    case '01':
      return '0-1'
    case '½½':
      return '1/2-1/2'
    case '+-':
      return '+-'
    case '-+':
      return '-+'
    
def safe_int(s) -> int | None:
  try:
    return int(s)
  except:
    ...
    
def parse_row(tr: Tag, board: str) -> Either[ParsingError, Pairing]:
  try:
    cols = tr.find_all('td')
    # board_num = cols[0].text.strip().strip('.')
    white_player = cols[3].a.text.strip()
    white_elo = safe_int(cols[4].text.strip())
    result = cols[6].text.strip()
    black_player = cols[9].a.text.strip()
    black_elo = safe_int(cols[10].text.strip())
    
    if black_player == "No Opponent":
      return Right(Unpaired(player=white_player, board=board, reason='No Opponent'))
    else:
      return Right(Paired(
        white=white_player, black=black_player,
        white_elo=white_elo, black_elo=black_elo,
        result=parse_result(result), board=board
      ))
  except Exception as e:
    return Left(ParsingError(f'Error parsing row: {e}'))
  

@E.do[ParsingError]()
def parse_round(soup: BeautifulSoup) -> RoundPairings:
  if not (table := soup.find('tbody')):
    return Left('No table found').unsafe()
  if not (rows := table.find_all('tr')): # type: ignore
    return Left('No rows found').unsafe()
  pairs = list(E.filter([parse_row(r, board=str(i+1)) for i, r in enumerate(rows)]))
  if not pairs:
    return Left('No valid rows found').unsafe()
  return pairs


def paired_rounds(round_page: BeautifulSoup) -> list[str] | None:
  """Finds the tournament rounds from the navigation bar"""
  try:
    rounds = round_page.find(string='Round:').parent.find_next_siblings() # type: ignore
    return [r.text.strip() for r in rounds]
  except:
    ...