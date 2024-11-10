import markdown

class ReleaseNotes:
  
  DIR = 'templates/status/partials'
  FILE = 'release_notes.md'

  def __init__(self, dir=None):
    self._dir = dir if dir else self.DIR
    self._text = ""
    self._read()

  def notes(self):
    return markdown.markdown(self._text)

  def _read(self):
    path = f'{self._dir}/{self.FILE}'
    with open(path, "r") as f:
      self._text = f.read()
