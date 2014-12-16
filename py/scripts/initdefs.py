# coding: utf8
# initdefs.py
# 2/9/2014 jichi

# Directories

SAKURA_RELPATH = '../..' # Sakura

FRAMEWORK_RELPATH = SAKURA_RELPATH + '/..' # Frameworks
PYTHON_RELPATH = FRAMEWORK_RELPATH + '/Python'

LIBRARY_RELPATH = FRAMEWORK_RELPATH + '/..' # Library
#DICTIONARY_RELPATH = LIBRARY_RELPATH + '/Dictionaries'

APP_RELPATH = LIBRARY_RELPATH + '/..' # VNR
CACHE_RELPATH = APP_RELPATH + '/Caches'
INST_RELPATH = CACHE_RELPATH + '/Installers'
TMP_RELPATH = CACHE_RELPATH + '/tmp'
LOCK_RELPATH = TMP_RELPATH

CACHE_DIC_RELPATH = CACHE_RELPATH + '/Dictionaries'

CACHE_CABOCHA_RELPATH = CACHE_DIC_RELPATH + '/CaboCha'
CACHE_EDICT_RELPATH = CACHE_DIC_RELPATH + '/EDICT'
CACHE_IPADIC_RELPATH = CACHE_DIC_RELPATH + '/IPAdic'
CACHE_LINGOES_RELPATH = CACHE_DIC_RELPATH + '/Lingoes'
CACHE_JMDICT_RELPATH = CACHE_DIC_RELPATH + '/JMDict'
CACHE_UNIDIC_RELPATH = CACHE_DIC_RELPATH + '/UniDic'
CACHE_UNIDICMLJ_RELPATH = CACHE_DIC_RELPATH + '/UniDicMLJ'
CACHE_WADOKU_RELPATH = CACHE_DIC_RELPATH + '/Wadoku'

# URLs

DOMAIN_COM = '153.121.54.194'
DOMAIN_ORG = '153.121.52.138'

DOWNLOAD_GOOGLE_URL = "http://goo.gl/t31MqY"
DOWNLOAD_MAINLAND_URL = "https://mega.co.nz/#F!g00SQJZS!pm3bAcS6qHotPzJQUT596Q"

# Parameters
HELP_FLAGS = '--help', '-h', '-?'

# EOF
