from haskellian import Either, Left
from chess_pairings import GroupPairings, RoundPairings
from chess_scraping import Source, ScrapingError, ParsingError, \
  chess_results as cr, chess_manager as cm, info64, asso_fr, \
  belgium_bic as bic

async def scrape_group(src: Source) -> Either[ScrapingError, GroupPairings]:
  if src.tag == 'chess-results':
    return await cr.scrape_group(src.id)
  elif src.tag == 'chess-manager':
    return await cm.scrape_group(src.id)
  elif src.tag == 'info64' or src.tag == 'info64-team':
    return await info64.scrape_group(src.id, team=src.tag == 'info64-team')
  elif src.tag == 'asso-france':
    return await asso_fr.scrape_group(src.id)
  elif src.tag == 'belgium-bic':
    year, group = src.id.split(':')
    return await bic.scrape_group(year=year, group=group)
  else:
    return Left(ParsingError(f'Unknown scraping source: {src.tag}'))
  
async def scrape_round(src: Source, round: str | int) -> Either[ScrapingError, RoundPairings]:
  if src.tag == 'chess-results':
    return await cr.scrape_round(src.id, round)
  elif src.tag == 'chess-manager':
    return await cm.scrape_round(src.id, round)
  elif src.tag == 'info64' or src.tag == 'info64-team':
    return await info64.scrape_round(src.id, round, team=src.tag == 'info64-team')
  elif src.tag == 'asso-france':
    return await asso_fr.scrape_round(src.id, round)
  elif src.tag == 'belgium-bic':
    year, group = src.id.split(':')
    return await bic.scrape_round(year=year, group=group, round=round)
  else:
    return Left(ParsingError(f'Unknown scraping source: {src.tag}'))