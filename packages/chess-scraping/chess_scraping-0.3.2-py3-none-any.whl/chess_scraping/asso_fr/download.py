import httpx
from haskellian import Left, Right
from bs4 import BeautifulSoup
from chess_scraping import DownloadError

ASSO_FR = 'http://echecs.asso.fr'

async def download(slug: str, params = {}, *, base: str | None = None):
  base = base or ASSO_FR
  try:
    # accept http and https
    async with httpx.AsyncClient(base_url=base, follow_redirects=True) as client:
      res = await client.get(slug, params=params)
      res.raise_for_status()
      return Right(BeautifulSoup(res.text, 'html.parser'))
  except httpx.HTTPError as e:
    return Left(DownloadError(str(e)))
  
async def download_main(id: str, *, base: str | None = None):
  slug = f'/FicheTournoi.aspx?Ref={id}'
  return await download(slug, base=base)

async def download_round(id: str, round: int | str, *, base: str | None = None):
  slug = f'Resultats.aspx?URL=Tournois/Id/{id}/{id}&Action={round:02}'
  return await download(slug, base=base)