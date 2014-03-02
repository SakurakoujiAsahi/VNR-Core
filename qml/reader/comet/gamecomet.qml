/** gamecomet.qml
 *  2/28/2014 jichi
 */
import QtQuick 1.1
import '.' as Comet

Comet.Comet { id: root_

  property int gameId

  property int connectionCount
  signal postReceived(variant obj)
  signal postUpdated(variant obj)

  // - Private -

  path: 'game/' + gameId

  onMessage: {
    var obj = JSON.parse(data) // may throw
    // No idea why switch-case does not work here ...
    if (obj.type === 'count')
      root_.connectionCount = Number(obj.data) // may becomes NaN
    else if (obj.type === 'post') {
      if (obj.data.id)
        root_.postReceived(obj.data)
    } else if (obj.type === 'post/update') {
      if (obj.data.id)
        root_.postUpdated(obj.data)
    } else
      console.log("gamecomet.qml:onMessage: unknown data type:", obj.type)
  }
}
