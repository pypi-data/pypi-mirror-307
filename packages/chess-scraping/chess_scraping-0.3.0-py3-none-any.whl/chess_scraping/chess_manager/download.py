import httpx
from bs4 import BeautifulSoup
from haskellian import Either, Left, Right
from chess_scraping import DownloadError

CHESS_MANAGER = 'https://www.chessmanager.com'

def main_slug(id: int | str):
  return f'/en/tournaments/{id}'

def round_slug(id: int | str, round: str | int):
  return f'/en/tournaments/{id}/rounds/{round}'

async def download(slug: str, *, base: str = CHESS_MANAGER):
  try:
    async with httpx.AsyncClient(base_url=base, follow_redirects=True) as client:
      res = await client.get(slug)
      res.raise_for_status()
      return Right(BeautifulSoup(res.text, 'html.parser'))
  except httpx.HTTPError as e:
    return Left(DownloadError(str(e)))
  

async def download_main(id: int | str, *, base: str = CHESS_MANAGER):
  return await download(main_slug(id), base=base)

async def download_round(id: int | str, round: str | int, *, base: str = CHESS_MANAGER):
  return await download(round_slug(id, round), base=base)