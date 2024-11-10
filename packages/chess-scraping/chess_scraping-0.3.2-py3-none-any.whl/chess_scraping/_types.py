from typing import Literal
from dataclasses import dataclass
from datetime import date

PairingSystem = Literal['swiss', 'round-robin', 'team-swiss', 'team-round-robin']

@dataclass
class Details:
  name: str
  site: str
  start_date: date
  end_date: date
  pairing_system: PairingSystem

ScrapingSource = Literal['chess-results', 'chess-manager', 'info64', 'asso-france', 'info64-team', 'belgium-bic']

@dataclass
class Source:
  """Source of pairings for a tournament group"""
  tag: ScrapingSource
  id: str
  """Unique identifier for the tournament
  - Chess Results: 6-digit DB key
  - Chess Manager: 16-digit id
  - Info64: string slug, e.g. 'xviii-super-tournament' or 'team/xvii-super-tournament'
  - Belgium BIC: f'{year}:{group}', e.g. '2024:4D'
  """

@dataclass
class DownloadError:
  detail: str | None = None
  reason: Literal['download-error'] = 'download-error'

@dataclass
class ParsingError:
  detail: str | None = None
  reason: Literal['parsing-error'] = 'parsing-error'

ScrapingError = DownloadError | ParsingError