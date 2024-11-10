from typing import Sequence, Mapping
from haskellian import Either, Left, Right
import httpx
from chess_scraping import DownloadError
from bs4 import BeautifulSoup 

def slug(db_key: int | str) -> str:
  return f"/tnr{db_key}.aspx"

CHESS_RESULTS = 'https://chess-results.com/'
ARCHIVE_CHESS_RESULTS = 'https://archive.chess-results.com/'
BASES = [CHESS_RESULTS, ARCHIVE_CHESS_RESULTS]
BLOCKED_MESSAGE = "Note: To reduce the server load by daily scanning of all links (daily 100.000 sites and more) by search engines like Google, Yahoo and Co, all links for tournaments older than 5 days (end-date) are shown after clicking the following button:"

async def download(
  slug: str, params: Mapping = {}, *,
  base = CHESS_RESULTS, blocked_message = BLOCKED_MESSAGE
) -> Either[DownloadError, BeautifulSoup]:
  try:
    async with httpx.AsyncClient(base_url=base) as client:
      res = await client.get(slug, params=params)
      res.raise_for_status()
      soup = BeautifulSoup(res.text, 'html.parser')
      if soup.find(string=blocked_message) is None:
        return Right(soup)
      else:
        input_tag = soup.find(id="__VIEWSTATE")
        if input_tag is None:
          return Left(DownloadError('VIEWSTATE not found'))
        try:
          viewstate = input_tag['value'] # type: ignore
        except:
          return Left(DownloadError('VIEWSTATE found but does not have "value" attribute'))
        res2 = await client.post(slug, params=params, data={
          "__VIEWSTATE": viewstate,
          "cb_alleDetails": "Show+tournament+details"
        })
        return Right(BeautifulSoup(res2.text, 'html.parser'))
  except httpx.HTTPError as e:
    return Left(DownloadError(detail=str(e)))
  
async def fallbacked_download(
  slug: str, params: Mapping = {}, *,
  bases: Sequence[str] = [CHESS_RESULTS, ARCHIVE_CHESS_RESULTS],
  blocked_message = BLOCKED_MESSAGE
):
  errs = []
  for base in bases:
    result = await download(slug, params, base=base, blocked_message=blocked_message)
    if result.tag == 'right':
      return result
    else:
      errs.append(result.value)
  return Left(DownloadError(detail=','.join(errs)))

async def download_main(db_key: int | str, *, bases = BASES):
  """Main page of a tournament"""
  url = slug(db_key)
  params = dict(lan=1)
  return await fallbacked_download(url, params, bases=bases)

async def download_pairings(db_key: int | str, *, bases = BASES):
  params = dict(lan=1, rd=0, art=2, turdet='YES', zeilen=99999)
  url = slug(db_key)
  return await fallbacked_download(url, params, bases=bases)

async def download_round(db_key: int | str, round: int | str, *, bases = BASES):
  params = dict(lan=1, rd=round, art=2, turdet='YES', zeilen=99999)
  url = slug(db_key)
  return await fallbacked_download(url, params, bases=bases)

async def download_schedule(db_key: int | str, *, bases = BASES):
  params = dict(lan=1, art=14, turdet='YES')
  url = slug(db_key)
  return await fallbacked_download(url, params, bases=bases)