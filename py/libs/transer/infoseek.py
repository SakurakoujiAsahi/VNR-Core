# coding: utf8
# infoseek.py
# 10/12/2012 jichi
#
# See: http://transer.com/sdk/rest_api_function.html
# See (auth): http://translation.infoseek.ne.jp/js/translation-text.js
# See (lang): http://translation.infoseek.ne.jp/js/userinfo.js

if __name__ == '__main__':
  import sys
  sys.path.append('..')

import requests
from sakurakit import skstr
from sakurakit.skdebug import dwarn, derror
from sakurakit.sknetio import GZIP_HEADERS

session = requests # global session

# See: http://docs.python-requests.org/en/latest/user/advanced/#keep-alive
# See: http://stackoverflow.com/questions/10115126/python-requests-close-http-connection
#session = requests.Session(config={'keep_alive': False})

# See: http://transer.com/sdk/rest_api_function.html
#   key=LICENCE 	オプション 	サービスのユーザーライセンスを提供します。HTTPリクエストヘッダもしくはHTTP認証のいずれかを使用してユーザーライセンスが提供される場合、URLを指定する必要はありません。
#   e=ENGINE 	必須 	使用する翻訳エンジンを指定します。翻訳エンジンは/clsoap/userへリクエストして返されたユーザー情報のエンジンIDの内、一つでなければなりません。
#   p=PROFILE 	オプション 	翻訳で使用するエンジンプロパティのプロファイルを指定します。指定しない場合、エンジンプロパティはデフォルトプロファイルを使用します。
#   t=TEXT 	必須 	翻訳されたテキストもしくはHTMLを指定します。複数エントリの指定が可能で、それぞれのファイルは別のブロックとして翻訳されます。指定の順番通りに翻訳結果が別々に返されます。
#   format=TYPE 	オプション 	"t"パラメータのデータをフォーマットを指定します。"text"はテキストデータ、"html"はhtmlデータとして使用してください。これらのパラメータが指定されない場合は、テキストデータがデフォルトとして使用されます。
#   sent=true 	オプション 	センテンスセグメント情報が翻訳されたテキストとして返すようリクエストします。
#   equiv=true 	オプション 	equiv情報が翻訳されたテキストとして返すようリクエストします。
#
# translation-text.js:
#  tran_exec: (a, c) ->
#    $("#mstranslator-logo").hide()
#    if a.length <= 0
#      $("#rep-layer").html ""
#      return
#    $("#rep-clipboard").hide()
#    $("#rep-layer").html "<img src=\"" + tran.loading + "\" />"
#    a = a.substr(0, tran.max)  if a.length > tran.max
#    a = tran.br(a)
#    b = {}
#    b.e = tran.key
#    b.t = a
#    b.equiv = "true"
#    $.ajax
#      url: "/clsoap/translate"
#      type: "post"
#      dataType: "json"
#      timeout: 30000
#      data: b
#      beforeSend: (d) ->
#        d.setRequestHeader "Cross-Licence", "infoseek/main e3f33620ae053e48cdba30a16b1084b5d69a3a6c"
#
# In my API, equiv is not enabled, as I don't need that information
INFOSEEK_API = ("http://translation.infoseek.ne.jp/clsoap/translate?"
                "&key=infoseek/main+e3f33620ae053e48cdba30a16b1084b5d69a3a6c")

INFOSEEK_QUERY_LANG = "e"
INFOSEEK_QUERY_TEXT = "t"

# According to userinfo.js:
# ja-zhs => JC
# zhs-ja => CJ
# ja-zht => JCT
# zht-ja => CJT, not CTJ!
#INFOSEEK_LCODE = {
#  'en' : 'E',
#  'ja' : 'J',
#  'zht': 'CT',
#  'zhs': 'C',
#  'ko' : 'K',
#  'fr' : 'F',
#  'de' : 'G',
#  'it' : 'I',
#  'es' : 'S',
#  'pt' : 'P',
#  'th' : 'ATHMS',   # thai
#  'vi' : 'AVIMS',   # vietnam
#  'id' : 'AIDMS',   # indonesia
#
#  'ru' : 'E', # Russia is not supported, use English instead
#}
#
#def _lang(to, fr):
#  """
#  @param  to  unicode
#  @param  fr  unicode
#  @return  unicode
#  """
#  return (
#      INFOSEEK_LCODE[fr] + INFOSEEK_LCODE[to] if fr != 'zht' else
#      'C%sT' % INFOSEEK_LCODE[to])

INFOSEEK_LCODE = {
  'jade': 'JG',
  'jaen': 'JE',
  'jaes': 'JS',
  'jafr': 'JF',
  'jait': 'JI',
  'jako': 'JK',
  'japt': 'JP',
  'jazhs': 'JC',
  'jazht': 'JCT',

  'jath': 'JATHMS',
  'javi': 'JAVIMS',
  'jaid': 'JAIDMS',
  'thja': 'THJAMS',
  'vija': 'VIJAMS',
  'idja': 'IDJAMS',

  'deen': 'GE',
  'dees': 'GS',
  'defr': 'GF',
  'deit': 'GI',
  'deja': 'GJ',
  'deko': 'GK',
  'dept': 'GP',
  'dezhs': 'GC',
  'dezht': 'GCT',

  'ende': 'EG',
  'enes': 'ES',
  'enfr': 'EF',
  'enit': 'EI',
  'enja': 'EJ',
  'enko': 'EK',
  'enpt': 'EP',
  'enzhs': 'EC',
  'enzht': 'ECT',

  'esde': 'SG',
  'esen': 'SE',
  'esfr': 'SF',
  'esit': 'SI',
  'esja': 'SJ',
  'esko': 'SK',
  'espt': 'SP',
  'eszhs': 'SC',
  'eszht': 'SCT',

  'frde': 'FG',
  'fren': 'FE',
  'fres': 'FS',
  'frit': 'FI',
  'frja': 'FJ',
  'frko': 'FK',
  'frpt': 'FP',
  'frzhs': 'FC',
  'frzht': 'FCT',

  'itde': 'IG',
  'iten': 'IE',
  'ites': 'IS',
  'itfr': 'IF',
  'itja': 'IJ',
  'itko': 'IK',
  'itpt': 'IP',
  'itzhs': 'IC',
  'itzht': 'ICT',

  'kode': 'KG',
  'koen': 'KE',
  'koes': 'KS',
  'kofr': 'KF',
  'koit': 'KI',
  'koja': 'KJ',
  'kopt': 'KP',
  'kozhs': 'KC',
  'kozht': 'KCT',

  'ptde': 'PG',
  'pten': 'PE',
  'ptes': 'PS',
  'ptfr': 'PF',
  'ptit': 'PI',
  'ptja': 'PJ',
  'ptko': 'PK',
  'ptzhs': 'PC',
  'ptzht': 'PCT',

  'zhsde': 'CG',
  'zhsen': 'CE',
  'zhses': 'CS',
  'zhsfr': 'CF',
  'zhsit': 'CI',
  'zhsja': 'CJ',
  'zhsko': 'CK',
  'zhspt': 'CP',

  'zhtde': 'CGT',
  'zhten': 'CET',
  'zhtes': 'CST',
  'zhtfr': 'CFT',
  'zhtit': 'CIT',
  'zhtja': 'CJT',
  'zhtko': 'CKT',
  'zhtpt': 'CPT',
}
def _lang(to, fr):
  """
  @param  to  unicode
  @param  fr  unicode
  @return  unicode
  """
  return INFOSEEK_LCODE.get(fr + to) or 'JE' # from 'ja' to 'en'

__repl = skstr.multireplacer({
  r'\u0022': '"',
  r'\u0026': '&',
  r'\u0027': "'",
  r'\u003C': '<',
  r'\u003E': '>',
  r'\n':     '\n',
})
def translate(text, to='en', fr='ja'):
  """Return translated text, which is NOT in unicode format
  @param  text  unicode not None
  @param  fr  unicode not None, must be valid language code
  @param  to  unicode not None, must be valid language code
  @return  unicode or None

  Returned text is not decoded, as its encoding can be guessed.
  """
  try:
    r = session.get(INFOSEEK_API,
      headers=GZIP_HEADERS,
      params={
        INFOSEEK_QUERY_LANG: _lang(to, fr),
        INFOSEEK_QUERY_TEXT: text,
      }
    )

    #print r.headers['Content-Type']
    ret = r.content

    # return error message if not r.ok
    # example response: {"t":[{"text":"hello"}]}
    if r.ok and len(ret) > 15 + 4:
      # Unicode char, see: http://schneide.wordpress.com/2009/05/18/the-perils-of-u0027/
      ret = __repl(ret[15:-4])
      return ret

  #except socket.error, e:
  #  dwarn("socket error", e.args)
  except requests.ConnectionError, e:
    dwarn("connection error", e.args)
  except requests.HTTPError, e:
    dwarn("http error", e.args)
  #except KeyError, e:
  #  dwarn("invalid response header", e.args)
  except Exception, e:
    derror(e)

  dwarn("failed")

  try: dwarn(r.url)
  except: pass

if __name__ == '__main__':
  #t = translate(u"あのね  すもももももももものうち", 'en')
  #print type(t), t
  #t = translate(u"你好", 'en', 'zhs')
  #print type(t), t
  #t = translate(u"你好", 'en', 'zht')
  #print type(t), t
  #t = translate(u"こんにちは", 'vi', 'ja')
  #print type(t), t.decode('sjis', errors='ignore')

  def test():
    global session

    #s = u"オープニングやエンディングのアニメーションは単純に主人公を入れ替えた程度の物ではなく、タイトルロゴはもちろん金時や定春の行動や表情、登場する道具（万事屋の面々が乗る車のデザインなど）やクレジット文字など、細部に渡って変更がなされた。更に、坂田金時が『銀魂'』を最終回に追い込み新しいアニメ『まんたま』を始めようとした時にはエンディングや提供表示の煽りコメントが最終回を思わせる演出となり、『まんたま』でも専用のタイトルロゴとオープニングアニメーション（スタッフクレジット付き）が新造され、偽物の提供クレジットまで表示されるなど随所に至るまで徹底的な演出が行われた。また、テレビ欄では金魂篇終了回は『金魂'』最終回として、その翌週は新番組「銀魂'」として案内された。"
    s = "test"
    fr = "ja"
    to = "zhs"

    #s = u"What are you doing?"
    #fr = "en"

    from sakurakit.skprof import SkProfiler

    from qtrequests import qtrequests
    from PySide.QtNetwork import QNetworkAccessManager
    session = qtrequests.Session(QNetworkAccessManager())
    with SkProfiler():
      for i in range(10):
        t = translate(s, to=to, fr=fr)
    print t

    session = requests.Session()
    with SkProfiler():
      for i in range(10):
        t = translate(s, to=to, fr=fr)
    print t

    #session = requests
    #with SkProfiler():
    #  for i in range(10):
    #    t = translate(s, to=to, fr=fr)
    #print t

    app.quit()

  from PySide.QtCore import QCoreApplication, QTimer
  app = QCoreApplication(sys.argv)
  QTimer.singleShot(0, test)
  app.exec_()

# EOF
#
# See (lang): http://translation.infoseek.ne.jp/js/userinfo.js
# Reverse engineered by js2coffee.org:
#callback
#  user:
#    userid: "infoseek"
#    username: "Infoseek Translate"
#    apiAllowed: "TestEcho GetEngineInfo Recode SplitSentences UpdateEngineProfile TranslateText TranslateTextUpdate TranslateTextSimple TranslateHtml TranslateXml Translate TranslateMulti LookupFormatted CreateDictionary UpdateDictionaryInfo CopyDictionary DeleteDictionary DictionaryImport ChangeDictionaryOwner DictionaryExport AddDictionaryEntry GetDictionaryEntry DeleteDictionaryEntry ChangePassword CreateUser GetUser UpdateUser DeleteUser GetUserList CreateSession EndSession"
#    timezone: "Japan"
#
#  engines:
#    GE:
#      from: "de"
#      to: "en"
#      reverse: "EG"
#      display: "ドイツ語 - 英語"
#
#    GS:
#      from: "de"
#      to: "es"
#      reverse: "SG"
#      display: "ドイツ語 - スペイン語 {経由: 英語}"
#
#    GF:
#      from: "de"
#      to: "fr"
#      reverse: "FG"
#      display: "ドイツ語 - フランス語 {経由: 英語}"
#
#    GI:
#      from: "de"
#      to: "it"
#      reverse: "IG"
#      display: "ドイツ語 - イタリア語 {経由: 英語}"
#
#    GJ:
#      from: "de"
#      to: "ja"
#      reverse: "JG"
#      display: "ドイツ語 - 日本語 {経由: 英語}"
#
#    GK:
#      from: "de"
#      to: "ko"
#      reverse: "KG"
#      display: "ドイツ語 - 韓国語 {経由: 英語}"
#
#    GP:
#      from: "de"
#      to: "pt"
#      reverse: "PG"
#      display: "ドイツ語 - ポルトガル語 {経由: 英語}"
#
#    GC:
#      from: "de"
#      to: "zh-hans"
#      reverse: "CG"
#      display: "ドイツ語 - 中国語 (簡体) {経由: 英語}"
#
#    GCT:
#      from: "de"
#      to: "zh-hant"
#      reverse: "CGT"
#      display: "ドイツ語 - 中国語 (繁体) {経由: 英語}"
#
#    EG:
#      from: "en"
#      to: "de"
#      reverse: "GE"
#      display: "英語 - ドイツ語"
#
#    ES:
#      from: "en"
#      to: "es"
#      reverse: "SE"
#      display: "英語 - スペイン語"
#
#    EF:
#      from: "en"
#      to: "fr"
#      reverse: "FE"
#      display: "英語 - フランス語"
#
#    EI:
#      from: "en"
#      to: "it"
#      reverse: "IE"
#      display: "英語 - イタリア語"
#
#    EJ:
#      from: "en"
#      to: "ja"
#      reverse: "JE"
#      display: "英語 - 日本語"
#
#    EK:
#      from: "en"
#      to: "ko"
#      reverse: "KE"
#      display: "英語 - 韓国語 {経由: 日本語}"
#
#    EP:
#      from: "en"
#      to: "pt"
#      reverse: "PE"
#      display: "英語 - ポルトガル語"
#
#    EC:
#      from: "en"
#      to: "zh-hans"
#      reverse: "CE"
#      display: "英語 - 中国語 (簡体) {経由: 日本語}"
#
#    ECT:
#      from: "en"
#      to: "zh-hant"
#      reverse: "CET"
#      display: "英語 - 中国語 (繁体) {経由: 日本語}"
#
#    SG:
#      from: "es"
#      to: "de"
#      reverse: "GS"
#      display: "スペイン語 - ドイツ語 {経由: 英語}"
#
#    SE:
#      from: "es"
#      to: "en"
#      reverse: "ES"
#      display: "スペイン語 - 英語"
#
#    SF:
#      from: "es"
#      to: "fr"
#      reverse: "FS"
#      display: "スペイン語 - フランス語 {経由: 英語}"
#
#    SI:
#      from: "es"
#      to: "it"
#      reverse: "IS"
#      display: "スペイン語 - イタリア語 {経由: 英語}"
#
#    SJ:
#      from: "es"
#      to: "ja"
#      reverse: "JS"
#      display: "スペイン語 - 日本語 {経由: 英語}"
#
#    SK:
#      from: "es"
#      to: "ko"
#      reverse: "KS"
#      display: "スペイン語 - 韓国語 {経由: 英語}"
#
#    SP:
#      from: "es"
#      to: "pt"
#      reverse: "PS"
#      display: "スペイン語 - ポルトガル語 {経由: 英語}"
#
#    SC:
#      from: "es"
#      to: "zh-hans"
#      reverse: "CS"
#      display: "スペイン語 - 中国語 (簡体) {経由: 英語}"
#
#    SCT:
#      from: "es"
#      to: "zh-hant"
#      reverse: "CST"
#      display: "スペイン語 - 中国語 (繁体) {経由: 英語}"
#
#    FG:
#      from: "fr"
#      to: "de"
#      reverse: "GF"
#      display: "フランス語 - ドイツ語 {経由: 英語}"
#
#    FE:
#      from: "fr"
#      to: "en"
#      reverse: "EF"
#      display: "フランス語 - 英語"
#
#    FS:
#      from: "fr"
#      to: "es"
#      reverse: "SF"
#      display: "フランス語 - スペイン語 {経由: 英語}"
#
#    FI:
#      from: "fr"
#      to: "it"
#      reverse: "IF"
#      display: "フランス語 - イタリア語 {経由: 英語}"
#
#    FJ:
#      from: "fr"
#      to: "ja"
#      reverse: "JF"
#      display: "フランス語 - 日本語 {経由: 英語}"
#
#    FK:
#      from: "fr"
#      to: "ko"
#      reverse: "KF"
#      display: "フランス語 - 韓国語 {経由: 英語}"
#
#    FP:
#      from: "fr"
#      to: "pt"
#      reverse: "PF"
#      display: "フランス語 - ポルトガル語 {経由: 英語}"
#
#    FC:
#      from: "fr"
#      to: "zh-hans"
#      reverse: "CF"
#      display: "フランス語 - 中国語 (簡体) {経由: 英語}"
#
#    FCT:
#      from: "fr"
#      to: "zh-hant"
#      reverse: "CFT"
#      display: "フランス語 - 中国語 (繁体) {経由: 英語}"
#
#    IG:
#      from: "it"
#      to: "de"
#      reverse: "GI"
#      display: "イタリア語 - ドイツ語 {経由: 英語}"
#
#    IE:
#      from: "it"
#      to: "en"
#      reverse: "EI"
#      display: "イタリア語 - 英語"
#
#    IS:
#      from: "it"
#      to: "es"
#      reverse: "SI"
#      display: "イタリア語 - スペイン語 {経由: 英語}"
#
#    IF:
#      from: "it"
#      to: "fr"
#      reverse: "FI"
#      display: "イタリア語 - フランス語 {経由: 英語}"
#
#    IJ:
#      from: "it"
#      to: "ja"
#      reverse: "JI"
#      display: "イタリア語 - 日本語 {経由: 英語}"
#
#    IK:
#      from: "it"
#      to: "ko"
#      reverse: "KI"
#      display: "イタリア語 - 韓国語 {経由: 英語}"
#
#    IP:
#      from: "it"
#      to: "pt"
#      reverse: "PI"
#      display: "イタリア語 - ポルトガル語 {経由: 英語}"
#
#    IC:
#      from: "it"
#      to: "zh-hans"
#      reverse: "CI"
#      display: "イタリア語 - 中国語 (簡体) {経由: 英語}"
#
#    ICT:
#      from: "it"
#      to: "zh-hant"
#      reverse: "CIT"
#      display: "イタリア語 - 中国語 (繁体) {経由: 英語}"
#
#    JG:
#      from: "ja"
#      to: "de"
#      reverse: "GJ"
#      display: "日本語 - ドイツ語 {経由: 英語}"
#
#    JE:
#      from: "ja"
#      to: "en"
#      reverse: "EJ"
#      display: "日本語 - 英語"
#
#    JS:
#      from: "ja"
#      to: "es"
#      reverse: "SJ"
#      display: "日本語 - スペイン語 {経由: 英語}"
#
#    JF:
#      from: "ja"
#      to: "fr"
#      reverse: "FJ"
#      display: "日本語 - フランス語 {経由: 英語}"
#
#    JI:
#      from: "ja"
#      to: "it"
#      reverse: "IJ"
#      display: "日本語 - イタリア語 {経由: 英語}"
#
#    JK:
#      from: "ja"
#      to: "ko"
#      reverse: "KJ"
#      display: "日本語 - 韓国語"
#
#    JP:
#      from: "ja"
#      to: "pt"
#      reverse: "PJ"
#      display: "日本語 - ポルトガル語 {経由: 英語}"
#
#    JC:
#      from: "ja"
#      to: "zh-hans"
#      reverse: "CJ"
#      display: "日本語 - 中国語 (簡体)"
#
#    JCT:
#      from: "ja"
#      to: "zh-hant"
#      reverse: "CJT"
#      display: "日本語 - 中国語 (繁体)"
#
#    JATHMS:
#      from: "ja"
#      to: "thms"
#      reverse: "THJAMS"
#      display: "日本語 - タイ語"
#      target: "text"
#
#    JAVIMS:
#      from: "ja"
#      to: "vims"
#      reverse: "VIJAMS"
#      display: "日本語 - ベトナム語"
#      target: "text"
#
#    JAIDMS:
#      from: "ja"
#      to: "idms"
#      reverse: "IDJAMS"
#      display: "日本語 - インドネシア語"
#      target: "text"
#
#    THJAMS:
#      from: "thms"
#      to: "ja"
#      reverse: "JATHMS"
#      display: "タイ語 - 日本語"
#      target: "text"
#
#    VIJAMS:
#      from: "vims"
#      to: "ja"
#      reverse: "JAVIMS"
#      display: "ベトナム語 - 日本語"
#      target: "text"
#
#    IDJAMS:
#      from: "idms"
#      to: "ja"
#      reverse: "JAIDMS"
#      display: "インドネシア語 - 日本語"
#      target: "text"
#
#    KG:
#      from: "ko"
#      to: "de"
#      reverse: "GK"
#      display: "韓国語 - ドイツ語 {経由: 英語}"
#
#    KE:
#      from: "ko"
#      to: "en"
#      reverse: "EK"
#      display: "韓国語 - 英語 {経由: 日本語}"
#
#    KS:
#      from: "ko"
#      to: "es"
#      reverse: "SK"
#      display: "韓国語 - スペイン語 {経由: 英語}"
#
#    KF:
#      from: "ko"
#      to: "fr"
#      reverse: "FK"
#      display: "韓国語 - フランス語 {経由: 英語}"
#
#    KI:
#      from: "ko"
#      to: "it"
#      reverse: "IK"
#      display: "韓国語 - イタリア語 {経由: 英語}"
#
#    KJ:
#      from: "ko"
#      to: "ja"
#      reverse: "JK"
#      display: "韓国語 - 日本語"
#
#    KP:
#      from: "ko"
#      to: "pt"
#      reverse: "PK"
#      display: "韓国語 - ポルトガル語 {経由: 英語}"
#
#    KC:
#      from: "ko"
#      to: "zh-hans"
#      reverse: "CK"
#      display: "韓国語 - 中国語 (簡体) {経由: 日本語}"
#
#    KCT:
#      from: "ko"
#      to: "zh-hant"
#      reverse: "CKT"
#      display: "韓国語 - 中国語 (繁体) {経由: 日本語}"
#
#    PG:
#      from: "pt"
#      to: "de"
#      reverse: "GP"
#      display: "ポルトガル語 - ドイツ語 {経由: 英語}"
#
#    PE:
#      from: "pt"
#      to: "en"
#      reverse: "EP"
#      display: "ポルトガル語 - 英語"
#
#    PS:
#      from: "pt"
#      to: "es"
#      reverse: "SP"
#      display: "ポルトガル語 - スペイン語 {経由: 英語}"
#
#    PF:
#      from: "pt"
#      to: "fr"
#      reverse: "FP"
#      display: "ポルトガル語 - フランス語 {経由: 英語}"
#
#    PI:
#      from: "pt"
#      to: "it"
#      reverse: "IP"
#      display: "ポルトガル語 - イタリア語 {経由: 英語}"
#
#    PJ:
#      from: "pt"
#      to: "ja"
#      reverse: "JP"
#      display: "ポルトガル語 - 日本語 {経由: 英語}"
#
#    PK:
#      from: "pt"
#      to: "ko"
#      reverse: "KP"
#      display: "ポルトガル語 - 韓国語 {経由: 英語}"
#
#    PC:
#      from: "pt"
#      to: "zh-hans"
#      reverse: "CP"
#      display: "ポルトガル語 - 中国語 (簡体) {経由: 英語}"
#
#    PCT:
#      from: "pt"
#      to: "zh-hant"
#      reverse: "CPT"
#      display: "ポルトガル語 - 中国語 (繁体) {経由: 英語}"
#
#    CG:
#      from: "zh-hans"
#      to: "de"
#      reverse: "GC"
#      display: "中国語 (簡体) - ドイツ語 {経由: 英語}"
#
#    CE:
#      from: "zh-hans"
#      to: "en"
#      reverse: "EC"
#      display: "中国語 (簡体) - 英語 {経由: 日本語}"
#
#    CS:
#      from: "zh-hans"
#      to: "es"
#      reverse: "SC"
#      display: "中国語 (簡体) - スペイン語 {経由: 英語}"
#
#    CF:
#      from: "zh-hans"
#      to: "fr"
#      reverse: "FC"
#      display: "中国語 (簡体) - フランス語 {経由: 英語}"
#
#    CI:
#      from: "zh-hans"
#      to: "it"
#      reverse: "IC"
#      display: "中国語 (簡体) - イタリア語 {経由: 英語}"
#
#    CJ:
#      from: "zh-hans"
#      to: "ja"
#      reverse: "JC"
#      display: "中国語 (簡体) - 日本語"
#
#    CK:
#      from: "zh-hans"
#      to: "ko"
#      reverse: "KC"
#      display: "中国語 (簡体) - 韓国語 {経由: 日本語}"
#
#    CP:
#      from: "zh-hans"
#      to: "pt"
#      reverse: "PC"
#      display: "中国語 (簡体) - ポルトガル語 {経由: 英語}"
#
#    CGT:
#      from: "zh-hant"
#      to: "de"
#      reverse: "GCT"
#      display: "中国語 (繁体) - ドイツ語 {経由: 英語}"
#
#    CET:
#      from: "zh-hant"
#      to: "en"
#      reverse: "ECT"
#      display: "中国語 (繁体) - 英語 {経由: 日本語}"
#
#    CST:
#      from: "zh-hant"
#      to: "es"
#      reverse: "SCT"
#      display: "中国語 (繁体) - スペイン語 {経由: 英語}"
#
#    CFT:
#      from: "zh-hant"
#      to: "fr"
#      reverse: "FCT"
#      display: "中国語 (繁体) - フランス語 {経由: 英語}"
#
#    CIT:
#      from: "zh-hant"
#      to: "it"
#      reverse: "ICT"
#      display: "中国語 (繁体) - イタリア語 {経由: 英語}"
#
#    CJT:
#      from: "zh-hant"
#      to: "ja"
#      reverse: "JCT"
#      display: "中国語 (繁体) - 日本語"
#
#    CKT:
#      from: "zh-hant"
#      to: "ko"
#      reverse: "KCT"
#      display: "中国語 (繁体) - 韓国語 {経由: 日本語}"
#
#    CPT:
#      from: "zh-hant"
#      to: "pt"
#      reverse: "PCT"
#      display: "中国語 (繁体) - ポルトガル語 {経由: 英語}"
