# coding: utf8
# features.py
# 12/24/2012 jichi
# Cached settings

from sakurakit.skdebug import dprint
import settings

def underwine():
  """
  @return  bool
  """
  import os
  from sakurakit import skpaths
  try: return os.path.exists(os.path.join(skpaths.SYSTEM32, 'winecfg.exe'))
  except Exception, e:
    from sakurakit.skdebug import dwarn
    dwarn(e)
    return False
WINE = underwine()

def isadmin():
  """
  @return  bool or None
  """
  from sakurakit import skos
  if not skos.WIN or WINE:
    return
  from sakurakit import skwinsec
  return skwinsec.is_elevated()
ADMIN = isadmin()

INTERNET_CONNECTION = settings.global_().internetConnection()
MACHINE_TRANSLATION = settings.global_().allowsMachineTranslation()
USER_COMMENT = settings.global_().allowsUserComment()
TEXT_TO_SPEECH = settings.global_().allowsTextToSpeech()
MAINLAND_CHINA = False

def setInternetConnection(v): global INTERNET_CONNECTION; INTERNET_CONNECTION = v
def setMachineTranslation(v): global MACHINE_TRANSLATION; MACHINE_TRANSLATION = v
def setUserComment(v): global USER_COMMENT; USER_COMMENT = v
def setTextToSpeech(v): global TEXT_TO_SPEECH; TEXT_TO_SPEECH = v

def setMainlandChina(value):
  global MAINLAND_CHINA
  if MAINLAND_CHINA != value:
    dprint(value)
    MAINLAND_CHINA = value

    from google import googletts, googletrans
    import erogamescape.api
    import getchu.search, getchu.soft
    import dlsite.search
    import dmm.game
    if not value:
      for it in googletts, googletrans:
        it.seturl(it.defaulturl())
      for it in  getchu.soft, getchu.search, dlsite.search, dmm.game, erogamescape.api:
        it.resethost()
    else:
      import config
      googletts.seturl(config.PROXY_GOOGLE_TTS)
      googletrans.seturl(config.PROXY_GOOGLE_TRANS)
      erogamescape.api.sethost(config.PROXY_EROGAMESCAPE)
      dmm.game.sethost(config.PROXY_DMM)
      dlsite.search.sethost(config.PROXY_DLSITE)
      for it in getchu.soft, getchu.search:
        it.sethost(config.PROXY_GETCHU)

def init():
  ss = settings.global_()
  ss.internetConnectionChanged.connect(setInternetConnection)
  ss.allowsMachineTranslationChanged.connect(setMachineTranslation)
  ss.allowsUserCommentChanged.connect(setUserComment)
  ss.allowsTextToSpeechChanged.connect(setTextToSpeech)

  ss.mainlandChinaChanged.connect(setMainlandChina)
  if ss.isMainlandChina():
    setMainlandChina(True)

init()

# EOF
