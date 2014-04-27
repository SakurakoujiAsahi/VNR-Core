// metacallthread.cc
// 4/27/2014 jichi
#include "qtmetacall/metacallthread.h"
#include "qtmetacall/metacallthread_p.h"
#include "qtmetacall/metacallpropagator.h"

#define DEBUG "metacallthread"
#include "sakurakit/skdebug.h"

/** Private class */

MetaCallThreadPrivate::MetaCallThreadPrivate(Q *q)
  : Base(q), q_(q), propagator(nullptr), role(ClientRole), port(0)
{}

MetaCallThreadPrivate::connectPropagator()
{
  if (propagator)
    connect(this, SIGNAL(asyncStopRequested()), propagator, SLOT(stop()), Qt::QueuedConnection);
}

MetaCallThreadPrivate::disconnectPropagator()
{
  if (propagator)
    disconnect(propagator);
}

/** Public class */

// - Construction -

MetaCallThread::MetaCallThread(QObject *parent)
  : Base(parent), d_(new D(this)) {}

MetaCallThread::~MetaCallThread() { delete d_; }

MetaCallPropagator *MetaCallThread::propagator() const
{ return d_->propagator; }

void MetaCallThread::setPropagator(MetaCallPropagator *value)
{
  if (d_->propagator != value) {
    if (d_->propagator)
      d_->disconnectPropagator();
    d_->propagator = value;
    if (value)
      d_->connectPropagator();
  }
}

// - Run -

void MetaCallThread::startClient(const QString &address, int port)
{
  d_->role = D::ClientRole;
  d_->address = address;
  d_->port = port;
  start();
}

void MetaCallThread::startServer(const QString &address, int port)
{
  d_->role = D::ServerRole;
  d_->address = address;
  d_->port = port;
  start();
}

void MetaCallThread::run()
{
  if (d_->propagator)
    switch (d_->role) {
    case D::ClientRole: d_->propagator->startClient(d_->address, d_->port); break;
    case D::ServerRole: d_->propagator->startServer(d_->address, d_->port); break;
    }
  exec();
}

void MetaCallThread::waitForReady() const
{
}

void MetaCallThread::stop()
{
  d_->emit stopRequested();
}

// - Actions -

// EOF
