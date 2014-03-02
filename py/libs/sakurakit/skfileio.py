# coding: utf8
# skfileio.py
# 11/10/2012 jichi
import os
import skstr
from skdebug import dprint, dwarn

## Parsing file names ##

_repl_escape = skstr.multireplacer({
  #"'": '', # remove
  '"': '', # remove
  '?': u'？',
  '*': u'＊',
  ':': u'：',
  '<': u'＜',
  '>': u'＞',
  '/': u'／',
  '|': '-',
  '\\': '-',
  '\t': ' ',
}) #, escape=True
def escape(name):
  """
  @param  name  unicode
  @return  unicode
  """
  return _repl_escape(name).strip() if name else ''

# http://stackoverflow.com/questions/7287996/python-get-relative-path-from-comparing-two-absolute-paths
def relpaths(paths): # [unicode] -> [unicode]
  path = map(os.path.abspath, paths)
  prefix = os.path.commonprefix(paths)
  return [os.path.relpath(path, prefix) for path in paths]

def realpath(path, prefix): # unicode, unicode -> unicode
  return os.path.relpath(os.path.abspath(path), os.path.abspath(prefix))

## Read and write ##

def readfile(path, mode='r'):
  """
  @param  path  str
  @param  mode  str  'r' or 'rb'
  @return  unicode or ""
  """
  try:
    with open(path, mode) as f:
      return f.read()
  except IOError: pass
  except UnicodeDecodeError, e: dwarn(e)
  except Exception, e: dwarn(e)
  return ""

def readdata(path): return readfile(path, mode='rb')

def writefile(path, data, mode='w'):
  """
  @param  path  str
  @param  data  str
  @param  mode  str  'w' or 'wb'
  @return  bool
  """
  try:
    with open(path, mode) as f:
      f.write(data)
    return True
  except IOError: pass
  except UnicodeEncodeError, e: dwarn(e)
  except Exception, e: dwarn(e)
  return False

def iterwritefile(path, iterdata, mode='w', flush=True):
  """
  @param  path  str
  @param  iterdata [str]
  @param  mode  str  'w' or 'wb'
  @return  bool
  """
  try:
    with open(path, mode) as f:
      for it in iterdata:
        f.write(it)
        if flush:
          f.flush()
    return True
  except IOError: pass
  except UnicodeEncodeError, e: dwarn(e)
  except Exception, e: dwarn(e)
  return False

def writedata(path, data, **kwargs): return writefile(path, data, mode='wb', **kwargs)
def iterwritedata(path, iterdata, **kwargs): return iterwritefile(path, terdata, mode='wb', **kwargs)

def removefile(path):
  """
  @param  path  str
  @return  bool
  """
  dprint(path)
  try: os.remove(path); return True
  except: return False

def removetree(path): # remove the whole directory recursively
  """
  @param  path  str
  @return  bool
  """
  dprint(path)
  try:
    import shutil
    shutil.rmtree(path)
    return True
  except: return False

def trashfile(path):
  """
  @param  path  str or unicode
  @return  bool  if succeed
  """
  from sakurakit import skos
  if skos.WIN:
    from sakurakit import skwin
    # The send2trash is broken for windows. Use my own version instead
    return skwin.trash_file(path)
  else:
    from send2trash import send2trash
    try:
      send2trash(path)
      return True
    except OSError, e:
      dwarn("failed to delete file %s, exception:" % path, e)
      return False

def touchfile(path):
  """
  @param  path
  @return  bool
  """
  try:
    if not os.path.exists(path):
      open(path, 'w+').close()
    return True
  except: return False

def rename(src, dst):
  """
  @param  src  str
  @param  dst  str
  @return  bool
  """
  try: os.rename(src, dst); return True
  except: return False

def filecreatetime(path):
  """
  @return  long
  """
  try: return os.path.getctime(path)
  except: return 0

def fileupdatetime(path):
  """
  @return  long
  """
  try: return os.path.getmtime(path)
  except: return 0

def filesize(path):
  """
  @return  int
  """
  try: return os.stat(path).st_size
  except: return 0

def fileempty(path):
  """
  @return  bool
  """
  return filesize(path) == 0

# Directory navigation

# http://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
def getfirstchildfile(path): # unicode -> unicode or None
  try:
    parent, dirs, files = os.walk(path).next()
    return os.path.join(parent, files[0])
  except Exception, e:
    dwarn(e)

# http://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
def getfirstchilddir(path): # unicode -> unicode or None
  try:
    parent, dirs, files = os.walk(path).next()
    return os.path.join(parent, dirs[0])
  except Exception, e:
    dwarn(e)

# Compression

# http://docs.python.org/2/library/tarfile.html
# mode: r, r:gz, r:bz2
def extracttar(path, location, mode='r'): # unicode, unicode -> bool
  import tarfile
  try:
    #with tarfile.TarFile(path) as z: # without extraction
    with tarfile.open(path, mode) as z:
      z.extractall(location)
      return True
  except Exception, e:
    dwarn(e)
  return False

# http://stackoverflow.com/questions/17217073/how-to-decompress-a-xz-file-which-has-multiple-folders-files-inside-in-a-singl
# Only needed by Python2. tar.xz is supported by Python3 by default.
def extracttarxz(path, location): # unicode, unicode -> bool
  import tarfile
  try:
    with contextlib.closing(lzma.LZMAFile(path)) as xz:
      with tarfile.open(fileobj=xz) as f:
        f.extractall(location)
        return True
  except Exception, e:
    dwarn(e)
  return False

# http://stackoverflow.com/questions/9431918/extracting-zip-file-contents-to-specific-directory-in-python-2-7
def extractzip(path, location): # unicode, unicode -> bool
  import zipfile
  try:
    with zipfile.ZipFile(path, 'r') as z:
      z.extractall(location)
      return True
  except Exception, e:
    dwarn(e)
  return False

# http://stackoverflow.com/questions/11466572/python-how-to-compress-with-7zip-instead-of-zip-code-changing
# Only needed by Python2. 7zip is supported by Python3 by default.
# Note: This require pylzma to be installed first
def extract7z(path, location): # unicode, unicode -> bool
  import py7zlib # could be found in pylzma from pip
  try:
    with py7zlib.Archive7z(path, 'r') as z:
      z.extractall(location)
      return True
  except Exception, e:
    dwarn(e)
  return False

# EOF
