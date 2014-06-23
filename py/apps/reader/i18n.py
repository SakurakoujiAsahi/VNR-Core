# coding: utf8
# i18n.py
# 12/14/2012 jichi

from datetime import datetime
from sakurakit.sktr import tr_
from mytr import my
import config, defs

## Names ##

LANGUAGE_NAMES = {
  'ja': tr_("Japanese"),
  'en': tr_("English"),
  'zh': tr_("Chinese"), # normalized
  'zht': tr_("Chinese"),
  'zhs': tr_("Simplified Chinese"),
  'ko': tr_("Korean"),
  'th': tr_("Thai"),
  'vi': tr_("Vietnamese"),
  'ms': tr_("Malaysian"),
  'id': tr_("Indonesian"),
  'de': tr_("German"),
  'fr': tr_("French"),
  'it': tr_("Italian"),
  'es': tr_("Spanish"),
  'nl': tr_("Dutch"),
  'pl': tr_("Polish"),
  'pt': tr_("Portuguese"),
  'ru': tr_("Russian"),
}
def language_name(lang):
  """
  @param  lang  str
  @return  unicode
  """
  return LANGUAGE_NAMES.get(lang) or tr_("English")

def language_name2(lang):
  """
  @param  lang  str
  @return  unicode
  """
  if isinstance(lang, str):
    return tr_(lang)
  if isinstance(lang, unicode):
    return tr_(lang.encode('utf8', errors='ignore'))
  return ''

def font_family(lang):
  return config.FONTS.get(lang) or ''

GENDER_NAMES = {
  'm': tr_("Male"),
  'f': tr_("Female"),
  '':  tr_("Not specified"),
}
def gender_name(g): return GENDER_NAMES.get(g) or ''

SITE_NAMES = {
  'amazon': "Amazon", #u"アマゾン",
  'digiket': "DiGiket",
  'dmm': "DMM",
  'getchu': "Getchu", #u"げっちゅ屋",
  'gyutto': "Gyutto", #u"ギュット!",
  'dlsite': "DLsite",
  'trailers': "Trailers",
  'tokuten': "特典", #u"エロゲーム特典",
  'scape': u"批評空間",
  'erogamescape': u"批評空間",
  'holyseal': u"聖封",
  'homepage': u"公式HP",
  'wiki': tr_("Wiki"), #u"ウィキ"
}
def site_name(t): return SITE_NAMES.get(t) or ''

KEY_NAMES = {
  'mouse left': tr_("Left-click"),
  'mouse middle': tr_("Middle-click"),
  'mouse right': tr_("Right-click"),
  'Space': tr_("Space"),
  'Back': u'←', # ひだり
  'Left': u'←', # ひだり
  'Right': u'→', # みぎ
  'Up': u'↑', # うえ
  'Down': u'↓', # した
  'Prior': 'PageUp',
  'Next': 'PageDown',
  'Capital': 'Cap', #'CapsLock',
  'Escape': 'Esc',
}
def key_name(t): # str -> unicode
  return KEY_NAMES.get(t) or t

def combined_key_name(t, delim='+'): # str -> unicode
  from hkman import unpackhotkey
  return delim.join(map(key_name, unpackhotkey(t)))

#def key_from_name(t): # unicode -> str
#  for k,v in KEY_NAMES.iteritems():
#    if v == t:
#      return k
#  return t

#INV_LANGUAGE_NAMES = {v:k for k, v in LANGUAGE_NAMES.iteritems()}
#
#def language_from_name(name):
#  return INV_LANGUAGE_NAMES.get(name) or ""

def language_compatible_to(termLanguage, language):
  """
  @param  termLanguage  str  lang
  @param  language  str  lang
  """
  if termLanguage == 'ja':
    return True
  if termLanguage[:2] == language[:2]:
    return True
  if termLanguage == 'en' and config.is_latin_language(language):
    return True
  return False

## Date time ##

WEEK_NAMES = [
  u"日",
  u"月",
  u"火",
  u"水",
  u"木",
  u"金",
  u"土",
]

def unparsedatetime(d):
  #return d.strftime("%m/%d/%Y {0} %H:%M").format(
  #    WEEK_NAMES[d.weekday()]).lstrip('0')
  return "%s/%s/%s %s %s:%s" % (
      d.month, d.day, d.year,
      WEEK_NAMES[d.weekday()],
      d.hour, d.minute)

def unparsedate(d):
  """
  @param  sec  long
  @return  str
  """
  return "%s/%s/%s %s" % (
      d.month, d.day, d.year,
      WEEK_NAMES[d.weekday()])

def timestamp2datetime(sec):
  """
  @param  sec  long
  @return  str
  """
  return unparsedatetime(datetime.fromtimestamp(sec))

def timestamp2date(sec):
  """
  @param  sec  long
  @return  str
  """
  return unparsedate(datetime.fromtimestamp(sec))

## Threads ##

THREAD_TIPS = {
  defs.HOOK_THREAD_TYPE: my.tr("Text thread from user-defined H-code"),
  defs.CUI_THREAD_TYPE: my.tr("Text thread from Windows Non-GUI function"),
  defs.GUI_THREAD_TYPE: my.tr("Text thread from Windows GUI function"),
  defs.ENGINE_THREAD_TYPE: my.tr("Text thread from game-specific engine"),
}
def threadtip(tt):
  """
  @param  tt  int  thread type
  @return  unicode not None
  """
  return THREAD_TIPS.get(tt) or ''

## Keywords ##

TIPS = {
  u"アドベンチャー": "Adventure",
  u"シミュレーション": "Simulation",
  u"デジタルノベル": "Digital Novel",
  u"アクション": "Action",
  u"バトル": "Battle",
  u"ファンタジー": "Fantasy",
  u"ラブコメ": "Love Comedy",
  u"コメディ": "Comedy",
  u"レズ": "Lesbian",
  u"ハーレム": "Harem",
  u"ショタ": "Shota",
  u"アニメ": "Anime",
  u"アニメーション": "Animation",
  u"アンドロイド": "Android",
  u"アンソロジー": "Anthology",
  u"ウェイトレス": "Waitress",
  u"チャイナドレス": "China Dress",
  u"アイドル": "Idol",
  u"アクセサリー": "Accessories",
  u"スポーツ": "Sports",
  u"動画・アニメーション": "Animation",
  u"ミステリー": "Mystery",
  u"オリジナル": "Original",
  u"ボーイズラブ": "Boys Love",
  u"コスプレ": "Cosplay",
  u"ダンジョン": "Dungeon",
  u"ホラー": "Horror",
  u"サスペンス": "Suspense",
  u"寝取り・寝取られ": "NTR",
  u"イチオシ作品": u"一番のお勧め",
  u"けもの娘": u"獣人娘",
  u"ふたなり": u"両性具有",
}
def tip(t):
  """
  @param  t  unicode
  @return  unicode
  """
  return TIPS.get(t) #or t.replace(u"コミケ", "Comiket")

TAGS = {
  "director":   u"企画・監督",
  "writer":     u"脚本", #u"シナリオ"
  "artist":     u"原画",
  "sdartist":   u"SD原画",
  "musician":   u"音楽",
  "singer":     u"うた",
  "lyrics":     u"作詞",
  "composer":   u"作曲",
  "arranger":   u"編曲",
}
def tag(t):
  """
  @param  t  unicode
  @return  unicode
  """
  return TAGS.get(t) or t

# EOF

## Translations ##
#
#TR_TITLES_EN = {
#  '' : '', # default item
#
#  u"さん" : "-san",
#  u"さぁん" : "-san",
#  u"さーん" : "-san",
#  u"さ～ん" : "-san",
#
#  u"様" : "-sama",
#  u"さま" : "-sama",
#  u"さーま" : "-sama",
#  u"さーまー" : "-sama",
#  u"さ～ま" : "-sama",
#
#  u"殿" : "-dono",
#
#  u"君" : "-kun",
#  u"くん" : "-kun",
#  u"くーん" : "-kun",
#  u"く～ん" : "-kun",
#
#  u"ちゃん" : "-chan",
#  u"ちゃーん" : "-chan",
#  u"ちゃ～ん" : "-chan",
#
#  u"ん" : "-chan",
#
#  u"しゃん" : "-shan",
#  u"ちん" : "-chin",
#  u"ち" : "-chi",
#  u"っち" : "-chi",
#
#  u"たん" : "-tan",
#  u"たぁん" : "-tan",
#  u"たーん" : "-tan",
#  u"た～ん" : "-tan",
#
#  u"先生" : "-sensei",
#  u"せんせい" : "-sensei",
#  u"せんせ" : "-sensei",
#  u"せんせー" : "-sensei",
#  u"せんせ～" : "-sensei",
#  u"センセイ" : "-sensei",
#  u"センセ" : "-sensei",
#  u"センセー" : "-sensei",
#  u"センセ～" : "-sensei",
#
#  u"先輩" : "-senpai",
#  u"せんぱい" : "-senpai",
#  #u"せんぱーい" : "-senpai",
#  #u"せんぱ～い" : "-senpai",
#  u"センパイ" : "-senpai",
#  #u"センパーイ" : "-senpai",
#  #u"センパ～イ" : "-senpai",
#
#  u"兄" : "-nii",
#  u"にい" : "-nii",
#  u"兄ちゃん" : "-niichan",
#  u"兄様" : "-niisama",
#  u"兄さま" : "-niisama",
#  u"兄さん" : "-niisan",
#
#  u"兄貴" : "-aniki",
#  u"の兄貴" : "-aniki",
#
#  u"姉" : "-nee",
#  u"ねえ" : "-nee",
#  u"姉ちゃん" : "-neechan",
#  u"姉様" : "-neesama",
#  u"姉さま" : "-neesama",
#  u"姉さん" : "-neesan",
#  u"お姉さま" : "-oneesama",
#  u"お姉さん" : "-oneesan",
#
#  u"お嬢様" : "-sama",
#  u"お嬢さま" : "-sama",
#}
#
#TR_TITLES_ZH = {
#  '' : '', # default item
#
#  u"さん" : u"桑",
#  u"さぁん" : u"桑",
#  u"さーん" : u"桑",
#  u"さ～ん" : u"桑",
#
#  u"様" : u"撒嘛",
#  u"さま" : u"撒嘛",
#  u"さーま" : u"撒嘛",
#  u"さーまー" : u"撒嘛",
#  u"さ～ま" : u"撒嘛",
#
#  u"殿" : u"殿下",
#
#  u"君" : u"君",
#  u"くん" : u"君",
#  u"くーん" : u"君",
#  u"く～ん" : u"君",
#
#  u"ちゃん" : u"酱",
#  u"ちゃーん" : u"酱",
#  u"ちゃ～ん" : u"酱",
#
#  u"ん" : u"酱",
#
#  u"しゃん" : u"香",
#  u"ちん" : u"亲",
#  u"ち" : u"亲",
#  u"っち" : u"亲",
#
#  u"たん" : u"糖",
#  u"たぁん" : u"糖",
#  u"たーん" : u"糖",
#  u"た～ん" : u"糖",
#
#  u"先生" : u"森賽",
#  u"せんせい" : u"森賽",
#  u"せんせ" : u"森賽",
#  u"せんせー" : u"森賽",
#  u"せんせ～" : u"森賽",
#  u"センセイ" : u"森賽",
#  u"センセ" : u"森賽",
#  u"センセー" : u"森賽",
#  u"センセ～" : u"森賽",
#
#  u"先輩" : u"先輩",
#  u"せんぱい" : u"先輩",
#  #u"せんぱーい" : u"先輩",
#  #u"せんぱ～い" : u"先輩",
#  u"センパイ" : u"先輩",
#  #u"センパーイ" : u"先輩",
#  #u"センパ～イ" : u"先輩",
#
#  u"兄" : u"哥哥",
#  u"にい" : u"哥哥",
#  u"兄ちゃん" : u"泥酱",
#  u"兄さん" : u"泥桑",
#  u"兄様" : u"泥撒嘛",
#  u"兄さま" : u"泥撒嘛",
#
#  u"兄貴" : u"大哥",
#  u"の兄貴" : u"大哥",
#
#  u"姉" : u"姐",
#  u"姉ちゃん" : u"捏酱",
#  u"姉さん" :  u"捏桑",
#  u"姉様" :  u"捏撒嘛",
#  u"姉さま" : u"捏撒嘛",
#  u"お姉様" :  u"哦捏撒嘛",
#  u"お姉さま" : u"哦捏撒嘛",
#
#  u"お嬢様" : u"大小姐",
#  u"お嬢さま" : u"大小姐",
#}
#
#def tr_titles(lang):
#  if lang and lang.startswith('zh'):
#    return TR_TITLES_ZH
#  else:
#    return TR_TITLES_EN
#
