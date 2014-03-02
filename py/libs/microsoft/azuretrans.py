# coding: utf8
# bingtrans.py
# 11/2/2011 jichi
#
# URLs
# - Sign up accound get Primary Account Key
#   https://datamarket.azure.com/account
# - Subscribe free translation service:
#   https://datamarket.azure.com/checkout/21075018-a3b5-4254-8ff2-1ec48002a4ec
if __name__ == '__main__':
  import sys
  sys.path.append('..')

# My azure market accout
# URL: https://datamarket.azure.com/account/datasets

# Name: jichifly at live, annotcound at gmail
AZURE_MARKET_ID = 'tuSmXew4CSnnGaX0vZyYdNLCrlInvAUepCX6p5l5THc='

# Name: jichifly at gmail, jichifly at hotmail
#AZURE_MARKET_ID = 'BSdMfJwHLNPsyTIPC/7eQHOYC8oATzqiudJBTcVk130'

BT_API = "https://api.datamarket.azure.com/Data.ashx/Bing/MicrosoftTranslator/Translate"

BT_QUERY_TEXT =  'Text'
BT_QUERY_FROM =  'From'
BT_QUERY_TO   =  'To'

BT_AUTH_USERNAME = 'name'
BT_AUTH_PASSWORD = AZURE_MARKET_ID

import re, requests
from sakurakit import skstr
from sakurakit.skdebug import dwarn, error
from sakurakit.sknetio import GZIP_HEADERS

# http://www.developer.nokia.com/Community/Discussion/showthread.php?211356-QNetworkRequest-Authentication
# http://docs.python-requests.org/en/latest/user/advanced/#custom-authentication
# "Authorization", "Basic " + QByteArray(QString("%1:%2").arg("USERNAME").arg("PASSWORD").toAscii()).toBase64());
AUTH = requests.auth.HTTPBasicAuth(BT_AUTH_USERNAME, BT_AUTH_PASSWORD)

# See: http://msdn.microsoft.com/en-us/library/hh456380.aspx
MS_LCODE = {
  'en' : 'en',
  'ja' : 'ja',
  'zht': 'zh-CHT',
  'zhs': 'zh-CHS',
  'ko' : 'ko',
  'de' : 'de',
  'es' : 'es',
  'fr' : 'fr',
  'it' : 'it',
  'pl' : 'pl',
  'pt' : 'pt',
  'ru' : 'ru',
  'vi' : 'vi',
  'th' : 'th',
  'id' : 'id',
}

__re_search = re.compile(r"%s%s%s" % (
  re.escape('<d:Text m:type="Edm.String">'),
  r'(.*?)',
  re.escape('</d:Text>')
), re.DOTALL) #|re.IGNORECASE)

def bad_translation(text):
  """Return whether the translated text is an error message from microsoft
  @param  unicode  text
  @return  bool
  """
  return text == "Insufficient balance for the subscribed offer in user's account\r\n"

def translate(text, to='en', fr='ja'):
  """Return translated text, which is NOT in unicode format
  @param  text  unicode not None
  @param  fr  unicode not None, must be valid language code
  @param  to  unicode not None, must be valid language code
  @return  unicode or None
  """
  try:
    r = requests.get(BT_API,
      headers=GZIP_HEADERS,
      auth=AUTH,
      params={
        BT_QUERY_FROM: "'%s'" % MS_LCODE[fr],
        BT_QUERY_TO: "'%s'" % MS_LCODE[to],
        BT_QUERY_TEXT: "'%s'" % text.replace("'", ""), # quoted
      }
    )

    #print r.headers['Content-Type']
    ret = r.content

    # return error message if not r.ok
    # example response: {"t":[{"text":"hello"}]}
    if r.ok and len(ret) > 100 and ret.startswith("<feed "):
      # Extract text within '<d:Text m:type="Edm.String">' and '</d:Text>'
      m = __re_search.search(ret)
      if m:
        ret = m.group(1)
        ret = skstr.unescapehtml(ret)
        ret = skstr.unescapehtml(ret) # has to escape twice...
      else:
        dwarn("content not matched: %s" % ret)
    return ret

  #except socket.error, e:
  #  dwarn("socket error", e.args)
  except requests.ConnectionError, e:
    dwarn("connection error", e.args)
  except requests.HTTPError, e:
    dwarn("http error", e.args)
  except KeyError, e:
    dwarn("invalid language", e.)
  except Exception, e:
    derror(e)

  dwarn("failed")

  try: dwarn(r.url)
  except: pass

  return ""

if __name__ == '__main__':
  print translate(u"あのね & すもももももももものうち")
  print bad_translation(translate("hello"))
  print translate(u"你好", 'en', 'zhs')

# EOF

# Sample request: http://api.microsofttranslator.com/v2/Http.svc/Translate?appId=FCB48AFBE3CB7B0E7AA146C950762FC87EA13FBB&text=hello&from=en&to=ja
# Sample reply:
# <feed xmlns:base="https://api.datamarket.azure.com/Data.ashx/Bing/MicrosoftTranslator/Translate" xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" xmlns="http://www.w3.org/2005/Atom">
#   <title type="text" />
#   <subtitle type="text">Microsoft Translator</subtitle>
#   <id>https://api.datamarket.azure.com/Data.ashx/Bing/MicrosoftTranslator/Translate?Text='hello'&amp;To='ja'&amp;$top=100</id>
#   <rights type="text" />
#   <updated>2012-07-02T03:54:54Z</updated>
#   <link rel="self" href="https://api.datamarket.azure.com/Data.ashx/Bing/MicrosoftTranslator/Translate?Text='hello'&amp;To='ja'&amp;$top=100" />
#   <entry>
#     <id>https://api.datamarket.azure.com/Data.ashx/Bing/MicrosoftTranslator/Translate?Text='hello'&amp;To='ja'&amp;$skip=0&amp;$top=1</id>
#     <title type="text">Translation</title>
#     <updated>2012-07-02T03:54:54Z</updated>
#     <link rel="self" href="https://api.datamarket.azure.com/Data.ashx/Bing/MicrosoftTranslator/Translate?Text='hello'&amp;To='ja'&amp;$skip=0&amp;$top=1" />
#     <content type="application/xml">
#       <m:properties>
#         <d:Text m:type="Edm.String">こんにちは</d:Text>
#       </m:properties>
#     </content>
#   </entry>
# </feed>
