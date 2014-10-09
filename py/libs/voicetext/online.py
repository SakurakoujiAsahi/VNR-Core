# coding: utf8
# online.py
# 10/9/2014 jichi
#
# API: http://dws.voicetext.jp/tomcat/data.xml
#
# See: http://voicetext.jp/
# Example:
#
# HIKARI (ja) Normal:
# Text: 憎しみは憎しみしか生まない。
# POST http://dws.voicetext.jp/tomcat/servlet/vt [HTTP/1.1 200 OK 587ms]
# - X-Requested-With: XMLHttpRequest
# - Referer: http://dws.voicetext.jp/tomcat/demonstration/top.html
# - Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# - Request: text=%E6%86%8E%E3%81%97%E3%81%BF%E3%81%AF%E6%86%8E%E3%81%97%E3%81%BF%E3%81%97%E3%81%8B%E7%94%9F%E3%81%BE%E3%81%AA%E3%81%84%E3%80%82&talkID=306&volume=100&speed=100&pitch=100&dict=3
# - Response: comp=2014101001_2254_0375.mp3
#
# GET http://dws.voicetext.jp/tomcat/servlet/put_count [HTTP/1.1 200 OK 167ms]
# GET http://dws.voicetext.jp/tomcat/servlet/get_count [HTTP/1.1 200 OK 361ms]
# GET http://dis.voicetext.jp/ASLCLCLVVS/JMEJSYGDCHMSMHSRKPJL/2014101001_2254_0375.mp3 [HTTP/1.1 206 Partial Content 565ms]
# GET http://dis.voicetext.jp/ASLCLCLVVS/JMEJSYGDCHMSMHSRKPJL/2014101001_2254_0375.mp3 [HTTP/1.1 206 Partial Content 841ms]
#
# put_count/get_count are used to track visit counts and not needed.
#
# HIKARI (ja) Micro
# Text: 憎しみは憎しみしか生まない。
# POST http://dws.voicetext.jp/tomcat/servlet/vt [HTTP/1.1 200 OK 542ms]
# - Request: text=%E6%86%8E%E3%81%97%E3%81%BF%E3%81%AF%E6%86%8E%E3%81%97%E3%81%BF%E3%81%97%E3%81%8B%E7%94%9F%E3%81%BE%E3%81%AA%E3%81%84%E3%80%82&talkID=356&volume=100&speed=100&pitch=100&dict=3
#
# GET http://dws.voicetext.jp/tomcat/servlet/put_count_micro [HTTP/1.1 200 OK 155ms]
# GET http://dws.voicetext.jp/tomcat/servlet/get_count_micro [HTTP/1.1 200 OK 309ms]
# GET http://dis.voicetext.jp/ASLCLCLVVS/JMEJSYGDCHMSMHSRKPJL/2014101001_2700_0915.mp3 [HTTP/1.1 206 Partial Content 470ms]
# GET http://dis.voicetext.jp/ASLCLCLVVS/JMEJSYGDCHMSMHSRKPJL/2014101001_2700_0915.mp3 [HTTP/1.1 206 Partial Content 1052ms]
#
# HYERYUN (ko) Normal:  text=%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94.+%EC%A0%80%EB%8A%94+VoiceText%EC%9D%98+%ED%98%9C%EB%A0%A8%EC%9E%85%EB%8B%88%EB%8B%A4.%0A%EB%B3%B8%EC%A0%90%EC%9D%98+%EC%98%81%EC%97%85+%EC%8B%9C%EA%B0%84%EC%97%90+%EB%8C%80%ED%95%B4%EC%84%9C+%EC%95%8C%EB%A0%A4+%EB%93%9C%EB%A6%BD%EB%8B%88%EB%8B%A4.&talkID=14&volume=100&speed=100&pitch=100&dict=0
# HYERYUN (ko) Micro:   text=%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94.+%EC%A0%80%EB%8A%94+VoiceText%EC%9D%98+%ED%98%9C%EB%A0%A8%EC%9E%85%EB%8B%88%EB%8B%A4.%0A%EB%B3%B8%EC%A0%90%EC%9D%98+%EC%98%81%EC%97%85+%EC%8B%9C%EA%B0%84%EC%97%90+%EB%8C%80%ED%95%B4%EC%84%9C+%EC%95%8C%EB%A0%A4+%EB%93%9C%EB%A6%BD%EB%8B%88%EB%8B%A4.&talkID=64&volume=100&speed=100&pitch=100&dict=0
#
# BRIDGET (en) Normal:  text=Hello+world&talkID=500&volume=100&speed=100&pitch=100&dict=3
# BRIDGET (en) Micro:   text=Hello+world&talkID=550&volume=100&speed=100&pitch=100&dict=3
#
# HONG (小紅, zht) Normal:  text=%E6%82%A8%E5%A5%BD%EF%BC%8C%E6%88%91%E6%98%AFVoiceText%E5%B0%8F%E7%B4%85%E3%80%82%0A%E5%85%B3%E4%BA%8E%E6%9C%AC%E5%BA%97%E7%9A%84%E8%90%A5%E4%B8%9A%E6%97%B6%E9%97%B4%E5%91%8A%E7%9F%A5&talkID=204&volume=100&speed=100&pitch=100&dict=0
# HONG (小紅, zht) Micro:   text=%E6%82%A8%E5%A5%BD%EF%BC%8C%E6%88%91%E6%98%AFVoiceText%E5%B0%8F%E7%B4%85%E3%80%82%0A%E5%85%B3%E4%BA%8E%E6%9C%AC%E5%BA%97%E7%9A%84%E8%90%A5%E4%B8%9A%E6%97%B6%E9%97%B4%E5%91%8A%E7%9F%A5&talkID=254&volume=100&speed=100&pitch=100&dict=0

# EOF
