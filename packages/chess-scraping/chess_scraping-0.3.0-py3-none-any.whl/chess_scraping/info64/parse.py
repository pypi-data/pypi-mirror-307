from bs4 import BeautifulSoup, Tag
from haskellian import Either, Left, Right, either as E
from chess_pairings import Result, Paired, Unpaired, TeamHeader, Pairing, RoundPairings
from chess_scraping import ParsingError

def rounds_dropdown(soup: BeautifulSoup) -> Tag | None:
  """Find the dropdown menu with the rounds"""
  try:
    return soup.find(string='Pairings and results').parent.find_next('li').parent # type: ignore
  except:
    ...

def paired_rounds(soup: BeautifulSoup) -> list[str] | None:
  """Finds the group's paired rounds from the navigation bar"""
  try:
    rounds = []
    dropdown = rounds_dropdown(soup)
    for anchor in dropdown.find_all('a'): # type: ignore
      round_n = anchor.text.strip()
      rounds.append(round_n.split(' ')[-1])
      # there's a little check icon to indicate a round is finished
      # so, we want up to the first unchecked round
      if not anchor.find('span'): 
        break
    return rounds
  except:
    ...

def safe_int(s) -> int | None:
  try:
    return int(s)
  except:
    return None
  
def parse_result(result) -> Result | None:
  match result:
    case '1-0' | '0-1':
      return result
    case '½-½':
      return '1/2-1/2'
    case '+--':
      return '+-'
    case '--+':
      return '-+'
    
def parse_team_result(result) -> Result | None:
  """Yes, they decided to format them differently... XD"""
  match result:
    case '1 - 0':
      return '1-0'
    case '0 - 1':
      return '0-1'
    case '0.5 - 0.5':
      return '1/2-1/2'
    case '+ - -': # actually never seen this one, so it's a guess
      return '+-'
    case '- - +': # id.
      return '-+'

def parse_row(tr: BeautifulSoup, board: str) -> Either[ParsingError, Pairing]:
  try:
    cols = tr.find_all('td')
    white_player = cols[1].text.strip()
    white_no = safe_int(cols[2].text.strip())
    white_elo = safe_int(cols[4].text.strip())
    if len(cols) > 10:
      result = cols[6].text.strip()
      black_player = cols[7].text.strip()
      black_no = safe_int(cols[8].text.strip())
      black_elo = safe_int(cols[10].text.strip())
      
      return Right(Paired(
        white=white_player, black=black_player, 
        white_no=white_no, white_elo=white_elo,
        black_no=black_no, black_elo=black_elo,
        result=parse_result(result), board=board
      ))
    else:
      return Right(Unpaired(player=white_player, board=board, reason='Unpaired'))
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

def is_header_row(tr: BeautifulSoup) -> bool:
  """Whether a table row is a team header. Based on it having a 'team-pairings' class"""
  return 'team-pairing' in tr.get('class', []) # type: ignore

def parse_team_row(tr: BeautifulSoup, board: str) -> Either[ParsingError, Pairing]:
  try:
    cols = tr.find_all('td')
    white_player = cols[1].text.strip()
    white_elo = safe_int(cols[3].text.strip())
    if len(cols) >= 8:
      result = cols[5].text.strip()
      black_player = cols[6].text.strip()
      black_elo = safe_int(cols[8].text.strip())
      
      return Right(Paired(
        white=white_player, black=black_player, 
        white_elo=white_elo, black_elo=black_elo,
        result=parse_team_result(result), board=board,
      ))
    else:
      return Right(Unpaired(player=white_player, board=board, reason='Unpaired'))
  except Exception as e:
    return Left(ParsingError(f'Error parsing row: {e}'))

@E.do[ParsingError]()
def parse_team_round(soup: BeautifulSoup) -> RoundPairings:
  if not (table := soup.find('tbody')):
    return Left('No table found').unsafe()
  if not (rows := table.find_all('tr')): # type: ignore
    return Left('No rows found').unsafe()
  
  pairs: list[Pairing] = []
  team_board = 0
  player_board = 1

  for row in rows:
    if is_header_row(row):
      team_board += 1
      player_board = 1
      # TODO: pairs.append(TeamHeader(white=...))
      continue
    pair = parse_team_row(row, board=f'{team_board}.{player_board}')
    if pair.tag == 'left':
      continue
    player_board += 1

  return pairs