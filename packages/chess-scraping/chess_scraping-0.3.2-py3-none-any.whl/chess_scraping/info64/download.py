import httpx
from bs4 import BeautifulSoup
from haskellian import Left, Right
from chess_scraping import DownloadError

INFO64 = 'https://info64.org'
def main_slug(id: str, *, team: bool = False):
  base = '/team' if team else ''
  return base + '/' + id.strip('/')

def round_slug(id: str, round: str | int, *, team: bool = False):
  id = id.lstrip('/')
  if team:
    return f'/team/{id}/board/{round}'
  else:
    return f'/{id}/{round}'

async def download(slug: str, params = dict(hl='en'), *, base: str = INFO64):
  try:
    async with httpx.AsyncClient(base_url=base, follow_redirects=True) as client:
      res = await client.get(slug, params=params)
      res.raise_for_status()
      return Right(BeautifulSoup(res.text, 'html.parser'))
  except httpx.HTTPError as e:
    return Left(DownloadError(str(e)))
  
async def download_round(id: str, round: str | int, *, team: bool = False):
  return await download(round_slug(id, round, team=team))

async def download_main(id: str, *, team: bool = False):
  return await download(main_slug(id, team=team))