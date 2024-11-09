from typing import Iterable
from dataclasses import dataclass
from haskellian import either as E, iter as I, Left
from chess_pairings import Result, Paired, Unpaired, Pairing
from bs4 import BeautifulSoup, Tag
from chess_scraping import ParsingError

@dataclass
class Columns:
  white: int
  black: int
  result: int
  white_no: int | None = None
  white_elo: int | None = None
  black_no: int | None = None
  black_elo: int | None = None

@dataclass
class Row:
  white: str
  black: str
  result: str
  white_no: str | None = None
  white_elo: str | None = None
  black_no: str | None = None
  black_elo: str | None = None

def parse_result(result: str) -> Result | None:
  """Parse result string from chessresults page
  - `'1 - 0' -->` white victory
  - `'0 - 1' -->` black victory
  - `'"½ - ½"' -->` 1/2-1/2
  - `'+ - -' -->` white victory by forfeit
  - `'- - +' -->` black victory by forfeit
  - any other --> None
  """
  match result:
    case "1 - 0":
      return "1-0"
    case "0 - 1":
      return "0-1"
    case "½ - ½":
      return "1/2-1/2"
    case "+ - -":
      return "+-"
    case "- - +":
      return "-+"
    
def safe_int(s) -> int | None:
  try:
    return int(s)
  except:
    ...

def parse_row(row: Row, board: str) -> Pairing:
  if row.black_no == '' or row.black_no == '-1': # happends in round robin for byes, idk
    return Unpaired(player=row.white, reason=row.black, board=board)
  else:
    return Paired(
      result=parse_result(row.result), white=row.white, black=row.black,
      white_no=safe_int(row.white_no), white_elo=safe_int(row.white_elo),
      black_no=safe_int(row.black_no), black_elo=safe_int(row.black_elo),
      board=board
    )
  
@E.do[ParsingError]()
def parse_columns(soup: BeautifulSoup) -> Columns:
  for row in soup.find_all('tr'):
    headers = [th.get_text(strip=True) for th in row.find_all(["th", "td"], recursive=False)]
    if headers != []:
      white = I.find_idx(lambda x: x == "White", headers)
      black = I.find_last_idx(lambda x: x == "Black", headers)
      result = I.find_idx(lambda x: x == "Result", headers)
      white_no = I.find_idx(lambda x: x == "No.", headers)
      white_elo = I.find_idx(lambda x: x == "Rtg", headers)
      black_no = I.find_last_idx(lambda x: x == "No.", headers)
      black_elo = I.find_last_idx(lambda x: x == "Rtg", headers)
      if white is not None and black is not None and result is not None:
        return Columns(white, black, result, white_no, white_elo, black_no, black_elo)
        
  return Left(ParsingError('Unable to find headers')).unsafe()

PAIRING_CLASSES = ["CRng1", "CRng2", "CRg1", "CRg2"]
"""Only rows with pairings have these classes, idk"""

def pairings_row(row: Tag) -> bool:
  return any(cls in row.get("class", []) for cls in PAIRING_CLASSES) # type: ignore

@I.lift
def extract_round(rows: Iterable[Tag], columns: Columns) -> Iterable[Row]:
  for row in rows:
    if not pairings_row(row):
      continue
    try:
      cols = list(row.find_all("td"))
      col_text = lambda i: cols[i].get_text(strip=True)
      yield Row(
        white=col_text(columns.white), black=col_text(columns.black), result=col_text(columns.result),
        white_no=col_text(columns.white_no) if columns.white_no is not None else None,
        white_elo=col_text(columns.white_elo) if columns.white_elo is not None else None,
        black_no=col_text(columns.black_no) if columns.black_no is not None else None,
        black_elo=col_text(columns.black_elo) if columns.black_elo is not None else None,
      )
    except:
      ...