# vnragent.pro
# 1/22/2013 jichi

CONFIG += noqtgui dll
include(../../../config.pri)
include($$LIBDIR/detoursutil/detoursutil.pri)
include($$LIBDIR/libqxt/libqxt.pri)
include($$LIBDIR/memdbg/memdbg.pri)
include($$LIBDIR/ntinspect/ntinspect.pri)
include($$LIBDIR/qtembedded/qtembedded.pri)
include($$LIBDIR/qtmetacall/qtmetacall.pri)
include($$LIBDIR/qtjson/qtjson.pri)
include($$LIBDIR/sakurakit/sakurakit.pri)
include($$LIBDIR/singleapp/singleapp.pri)
include($$LIBDIR/windbg/windbg.pri)
include($$LIBDIR/winquery/winquery.pri)
include($$LIBDIR/wintimer/wintimer.pri)

#include($$LIBDIR/disasm/disasm.pri)
#include($$LIBDIR/vnragent/vnragent.pri)

# Services
HEADERS += $$SERVICEDIR/reader/metacall.h

## Libraries

#CONFIG  += noqt
QT      += core network
QT      -= gui

#INCLUDEPATH += $$D3D_HOME/include
#LIBS    += -ld3d9 -L$$D3D_HOME/lib/x86

LIBS    += -luser32 -lpsapi
LIBS    += -lgdi32 # needed by game engines

## Sources

TEMPLATE = lib
TARGET  = vnragent

HEADERS += \
  driver/driver.h \
  driver/driver_p.h \
  driver/rpccli.h \
  driver/rpccli_p.h \
  engine/enginedriver.h \
  engine/enginehash.h \
  engine/enginehijack.h \
  engine/enginemanager.h \
  ui/uidriver.h \
  ui/uidriver_p.h \
  ui/uihash.h \
  ui/uihijack.h \
  ui/uihijack_p.h \
  ui/uimanager.h \
  config.h \
  growl.h \
  loader.h
SOURCES += \
  driver/driver.cc \
  driver/rpccli.cc \
  engine/enginedriver.cc \
  engine/enginehijack.cc \
  engine/enginemanager.cc \
  ui/uidriver.cc \
  ui/uidriver_p.cc \
  ui/uihijack.cc \
  ui/uihijack_p.cc \
  ui/uimanager.cc \
  growl.cc \
  loader.cc \
  main.cc

HEADERS += \
  model/engine/majiro.h \
  model/engine.h \
  model/manifest.h
SOURCES += \
  model/engine/majiro.cc \
  model/engine.cc

#!wince*: LIBS += -lshell32
#RC_FILE += vnragent.rc

OTHER_FILES += vnragent.rc

# EOF
