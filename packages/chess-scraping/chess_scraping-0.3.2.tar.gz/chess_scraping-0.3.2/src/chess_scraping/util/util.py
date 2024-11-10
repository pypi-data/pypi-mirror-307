
def urljoin(*args) -> str:
  return '/'.join(map(lambda x: str(x).strip('/'), args))

def parse_int(s: str) -> int | None:
  try:
    return int(s)
  except:
    ...