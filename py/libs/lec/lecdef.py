# coding: utf8
# lecdef.py
# 1/20/2015 jichi

DLL_BUFFER_SIZE = 0x2000 # output buffer size

LEC_LANGUAGES = frozenset((
  'ja',
  'en',
  'zh',
  'ko',
  'id',
  'ar',
  'de',
  'es',
  'fr',
  'it',
  'nl',
  'pl',
  'pt',
  'ru',
  #'ms',
  #'th',
  #'vi',
  'he', # Hebrew
  'fa', # Persian
  'tl', # Tagalog in Philippine
  'tr', # Turkish
  'uk', # Ukrainian
  'ps', # Pashto in Afghanistan
))

POWERTRANS_LANGUAGES = ( # [(str fr, str to)]
  ('ja', 'en'),
  ('en', 'ru'),
  ('ja', 'ru'),
)
POWERTRANS_SOURCE_LANGUAGES = 'en', 'ja'
POWERTRANS_TARGET_LANGUAGES = 'en', 'ru'

def mt_lang_test(to=None, fr=None, online=True):
  """
  @param* to  str
  @param* fr  str
  @param* online  bool
  @return  bool
  """
  if online:
    return (not fr or fr[:2] in MT_LANGUAGES) and (not to or to[:2] in LEC_LANGUAGES)
  else: # Offline
    return ((fr, to) in POWERTRANS_LANGUAGES if fr and to else
        fr in POWERTRANS_SOURCE_LANGUAGES or
        to in POWERTRANS_TARGET_LANGUAGES)

# EOF
