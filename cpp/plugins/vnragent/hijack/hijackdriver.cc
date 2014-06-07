// hijackdriver.cc
// 5/1/2014 jichi
#include "hijack/hijackdriver.h"
#include "hijack/hijackhelper.h"
#include "hijack/hijackfuncs.h"
#include <QtCore/QTimer>

/** Private class */

class HijackDriverPrivate
{
  typedef HijackDriver Q;

  enum { RefreshInterval = 5000 }; // interval checking if new module/process is loaded
  QTimer *refreshTimer;
public:
  HijackHelper *helper;

  explicit HijackDriverPrivate(Q *q)
  {
    helper = new HijackHelper(q);

    refreshTimer = new QTimer(q);
    refreshTimer->setSingleShot(false);
    refreshTimer->setInterval(RefreshInterval);
    q->connect(refreshTimer, SIGNAL(timeout()), SLOT(refresh()));

    refreshTimer->start();
  }
};

/** Public class */

HijackDriver::HijackDriver(QObject *parent) : Base(parent), d_(new D(this)) {}
HijackDriver::~HijackDriver() { delete d_; }

// Properties

void HijackDriver::setEncoding(const QString &v)
{ d_->helper->setEncoding(v); }

// Actions

void HijackDriver::refresh()
{ Hijack::overrideModules(); }

void HijackDriver::unload()
{ Hijack::restoreModules(); }

// EOF