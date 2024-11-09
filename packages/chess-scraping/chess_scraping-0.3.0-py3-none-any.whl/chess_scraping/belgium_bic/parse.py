from bs4 import Tag, BeautifulSoup
from haskellian import Either, Left, Right, either as E
from chess_pairings import Result, Paired, Unpaired, TeamHeader, Pairing, RoundPairings
from chess_scraping import ParsingError
    
def parse_header(table: Tag) -> Either[ParsingError, TeamHeader]:
  try:
    header = table.find('thead').find('tr') # type: ignore
    fields = header.find_all('th') # type: ignore
    section = fields[0].get_text(strip=True) # 1A, 1B, 2A, etc.
    team_white = fields[2].get_text(strip=True)
    result = fields[3].get_text(strip=True)
    team_black = fields[5].get_text(strip=True)
    return Right(TeamHeader(white=team_white, black=team_black, result=result, board=section))
  except Exception as e:
    return Left(ParsingError(f'Error parsing header: {e}'))

def find_tables(soup: BeautifulSoup, *, group: str) -> Either[ParsingError, list[tuple[Tag, TeamHeader]]]:
  """Find table of pairings for a given group. (e.g. `group = '4B'`)"""
  tables = soup.find_all('table')
  errors = []
  outputs: list[tuple[Tag, TeamHeader]] = []
  
  for table in tables:
    header = parse_header(table)
    if header.tag == 'left':
      errors.append(header.value)
    elif header.value.board == group:
      outputs.append((table, header.value))
  
  if outputs:
    return Right(outputs)
  elif errors:
    return Left(ParsingError(f'Errors parsing headers: {errors}'))
  else:
    return Left(ParsingError(f'Could not find table for group {group}'))
  
def parse_row(row: Tag, board: str):
  fields = row.find_all('td')
  white = fields[2].get_text(strip=True)
  result = fields[3].get_text(strip=True)
  black = fields[5].get_text(strip=True)
  return Paired(white=white, black=black, result=result, board=board)

def parse_table(table: Tag) -> Either[ParsingError, list[Paired]]:
  body = table.find('tbody')
  if not isinstance(body, Tag):
    return Left(ParsingError('Could not find table body'))
  entries = body.find_all('tr')
  pairs = [parse_row(row, board=str(i+1)) for i, row in enumerate(entries)]
  return Right(pairs)

@E.do[ParsingError]()
def parse_round(soup: BeautifulSoup, *, group: str) -> RoundPairings:
  pairs: RoundPairings = []
  for table, heading in find_tables(soup, group=group).unwrap():
    pairs.extend([heading] + parse_table(table).unwrap())

  return pairs

def find_rounds(soup: BeautifulSoup) -> Either[ParsingError, list[str]]:
  """Find all round names"""
  group = soup.find('mat-button-toggle-group')
  if not isinstance(group, Tag):
    return Left(ParsingError('Could not find button group'))
  buttons = group.find_all('mat-button-toggle')
  return Right([btn.get_text(strip=True) for btn in buttons])