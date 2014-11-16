# inject-site.coffee
# 11/14/2014 jichi
# Invoked by QWebFrame::evaluaeJavaScript
# Beans:
# - cdnBean: coffeebean.CdnBean
# - settingsBean: coffeebean.SettingsBean

unless @siteInjected
  @siteInjected = true

  linkcss = (url) -> # string -> el  return the inserted element
    el = document.createElement 'link'
    #el.type = 'text/css'
    el.rel = 'stylesheet'
    el.href = url #+ '.css'
    document.head.appendChild el
    el

  linkjs = (url) -> # string -> el  return the inserted element
    el = document.createElement 'script'
    el.src = url #+ '.js'
    document.body.appendChild el
    el

  linkcss cdnBean.url 'client-site.css'
  linkjs cdnBean.url 'client-site'

# EOF
