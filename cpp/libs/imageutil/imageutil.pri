# imageutil.pri
# 4/5/2014 jichi
#include(../../../config.pri)
DEFINES += WITH_LIB_IMAGEUTIL

DEPENDPATH += $$PWD

HEADERS += \
  $$PWD/contour.h

SOURCES += \
  $$PWD/contour.cc

INCLUDEPATH     += $$QT_SRC
QT      += core gui

# EOF