#pragma once

// rpccli.h
// 2/1/2013 jichi

#include "sakurakit/skglobal.h"
#include <QtCore/QObject>

class RpcClientPrivate;
class RpcClient : public QObject
{
  Q_OBJECT
  Q_DISABLE_COPY(RpcClient)
  SK_EXTEND_CLASS(RpcClient, QObject)
  SK_DECLARE_PRIVATE(RpcClientPrivate)

public:
  explicit RpcClient(QObject *parent = nullptr);
  ~RpcClient();
  bool isActive() const;

  // - API -
signals:
  // UI
  void clearUiRequested();
  void enableUiRequested(bool t);
  void uiTranslationReceived(QString json); // json: {hash:text}

public slots:
  void requestUiTranslation(const QString &json); // json: {hash:text}

  void showMessage(const QString &message);
  void showWarning(const QString &message);
  void showError(const QString &message);
};

// EOF
