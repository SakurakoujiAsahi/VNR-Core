# coding: utf8
# 2/9/2015

MT_SOURCE_LANGUAGES = 'ja',
MT_TARGET_LANGUAGES = 'zhs', 'zht'

def mt_s_langs(online=False): return MT_SOURCE_LANGUAGES
def mt_t_langs(online=False): return MT_TARGET_LANGUAGES

def mt_test_lang(to=None, fr=None, online=False):
  """
  @param* to  str  language
  @param* fr  str  language
  @param* online  bool  ignored
  @return  bool
  """
  return (not fr or fr == 'ja') and (not to or to.startswith('zh'))

# EOF
