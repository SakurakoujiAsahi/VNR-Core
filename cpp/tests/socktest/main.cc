// main.cc
// 4/29/2014 jichi

//#include "qtsocketsvc/socketclient.h"
#include "qtsocketsvc/bufferedlocalsocketclient.h"
#include "qtsocketsvc/socketpack.h"
#include <QtCore>


int main(int argc, char *argv[])
{
  QByteArray data;

  int x = 100;
  data = SocketService::packUInt32(x);
  x = SocketService::unpackUInt32(data);
  qDebug() << x;

  QStringList l = QStringList() << "hello" << "world";
  data = SocketService::packStringList(l);
  l = SocketService::unpackStringList(data);
  qDebug() << l;

  QCoreApplication a(argc, argv);
  BufferedLocalSocketClient cli;
  cli.setServerName("/tmp/pipetest");
  cli.start();
  cli.waitForConnected();
  qDebug() << cli.isConnected();
  cli.dumpSocketInfo();
  const char *text = "hello";
  cli.sendDataLater(text);

  //cli.waitForBytesWritten();
  cli.sendDataLater(text);

  //cli.dumpSocketInfo();

  QObject::connect(&cli, SIGNAL(disconnected()), qApp, SLOT(quit()));
  return a.exec();
}

// EOF
