# coding: utf8
# youtube.py
# 10/27/2013 jichi

if __name__ == '__main__':
  import sys
  reload(sys)
  sys.setdefaultencoding('utf-8')
  import initrc
  initrc.initenv()

import os
from sakurakit.skdebug import dprint, dwarn
from google.googletrans import translate

USAGE = "to.ts from.ts"

def getcfg(fname): # unicode -> unicode
  return os.path.join(os.path.dirname(__file__), '../../tr/%s' % fname)

def loadcfg(name): # unicode -> {unicode:unicode}
  ret = {}
  with open(name, 'r') as f:
    for line in f:
      t = line.strip()
      if t and t[0] != '#':
        fr , delim, to = t.partition('=')
        ret[fr.rstrip()] = to.lstrip()
  return ret

CORRECTIONS = {
  'enko': loadcfg(getcfg('ko_KR.cfg')),
}

ESCAPE = frozenset((
  'en',
  'ja',
  'zh', 'zht', 'zhs',
  'ko',
  'vi',
  'th',
  'id',
  'de',
  'es',
  'fr',
  'it',
  'nl',
  'pl',
  'pt',
  'ru',

  'UI',
  'Asc', 'Desc',
  'Python', 'BBCode', 'Javascript',
))
def tr(text, escape=ESCAPE, corrections=CORRECTIONS, fr='', to=''):
  """
  @param  tr  function
  @param  text  unicode  text
  @param* to  str  language
  @param* fr  str  language
  @return  unicode or None
  """
  d = corrections.get(fr+to)
  if d:
    t = d.get(text)
    if t:
      return t
  if text in escape:
    return text
  return translate(text,  fr=fr, to=to)

def locale2lang(t):
  """
  @param  t  str
  @return  str
  """
  if t == 'zh_CN':
    return 'zhs'
  if t == 'zh_TW':
    return 'zht'
  return t[:2]

def translatefile(fout, fin):
  """
  @param  fout  ts path
  @param  fin  ts path
  @return  bool
  """
  import os
  dprint("enter")
  flocale = os.path.basename(fin).split('.')[0]
  tlocale = os.path.basename(fout).split('.')[0]
  dprint("processing: %s < %s" % (tlocale, flocale))
  from trio import trts
  ok = trts.trfile(tr, fout, fin, locale=tlocale)
  dprint("leave: ok = %s" % ok)
  return ok

def main(argv):
  """
  @param  argv  [unicode]
  @return  int
  """
  dprint("enter")
  ret = 0
  try:
    if len(argv) != 2:
      dwarn("usage: %s" % USAGE)
    else:
      ok = translatefile(fout=argv[0], fin=argv[1])
      ret = 0 if ok else 1
  except Exception, e:
    dwarn(e)
    ret = 1
  dprint("leave: ret = %s" % ret)
  return ret

if __name__ == '__main__':
  import sys
  ret = main(sys.argv[1:])
  sys.exit(ret)

# EOF
