# wintimer.pri
# 7/20/2011 jichi
win32 {

DEFINES += WITH_LIB_WINTIMER

DEPENDPATH      += $$PWD

HEADERS += $$PWD/winmaker.h
SOURCES += $$PWD/winmaker.cc

#LIBS    += -lkernel32 -luser32
}

# EOF
