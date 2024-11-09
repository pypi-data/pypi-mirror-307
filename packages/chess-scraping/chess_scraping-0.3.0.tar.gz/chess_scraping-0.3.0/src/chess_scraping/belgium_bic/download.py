from haskellian import Either, Left, Right
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from chess_scraping import DownloadError
from chess_scraping.util import urljoin

INTERCLUBS = 'https://interclub.web.app/'

async def scrape(url: str, *, timeout_ms=3*60*1e3) -> str:
  """Scrape rendered HTML, waiting for network requests to finish."""
  async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page()
    await page.goto(url)
    # await page.wait_for_load_state('networkidle', timeout=3*60*1e3)
    await page.wait_for_selector('.mat-spinner', state='detached', timeout=timeout_ms)
    html = await page.content()
    await browser.close()
    return html

def round_slug(*, year: int | str, round: str | int):
  return f'/round/{round}?year={year}'

async def download(slug: str, *, base: str = INTERCLUBS):
  try:
    html = await scrape(urljoin(base, slug))
    return Right(BeautifulSoup(html, 'html.parser'))
  except Exception as e:
    return Left(DownloadError(str(e)))

async def download_round(*, year: int | str, round: str | int, base: str = INTERCLUBS):
  return await download(round_slug(year=year, round=round), base=base)