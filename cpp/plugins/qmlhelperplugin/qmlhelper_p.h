#ifndef QMLHELPER_P_H
#define QMLHELPER_P_H

// qmlhelper_p.h
// 12/9/2012 jichi

#include <QtCore/QObject>
QT_FORWARD_DECLARE_CLASS(QDeclarativeItem)

class QmlHelper : public QObject
{
  Q_OBJECT
  typedef QObject Base;
public:
  explicit QmlHelper(QObject *parent=nullptr);

  /**
   *  @param  q  QDeclarativeTextEditItem
   *  @return  QTextDocument
   */
  Q_INVOKABLE static QObject *textedit_document(QDeclarativeItem *q);
};

#ifdef _MSC_VER
# pragma warning (disable:4189)   // C4189: local variable is initialized bot not referenced
#endif // _MSC_VER

#endif // QMLTHELPER_P_H
