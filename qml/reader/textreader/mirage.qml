/** mirage.qml
 *  6/23/2013 jichi
 */
import QtQuick 1.1
import QtDesktop 0.1 as Desktop
import org.sakuradite.reader 1.0 as Plugin
import '../../../js/sakurakit.min.js' as Sk
import '../../../js/reader.min.js' as My
import '../../../js/util.min.js' as Util
import '../../imports/qmleffects' as Effects
import '../../ui' as Ui
import '../share' as Share

Item { id: root_
  signal yakuAt(string text, int x, int y) // popup honyaku of text at (x, y)

  property int contentHeight: shadow_.y + shadow_.height

  property bool dragging: headerMouseArea_.drag.active ||
      !!highlightMouseArea && highlightMouseArea.drag.active
  property bool empty: !listModel_.count

  //property alias borderVisible: borderAct_.checked
  //onBorderVisibleChanged:
  //  if (_borderButton && _borderButton.checked !== borderVisible)
  //    _borderButton.checked = borderVisible

  property bool ignoresFocus: false

  property bool clipboardEnabled

  property bool mouseEnabled
  onMouseEnabledChanged:
    if (mouseEnabled)
      textspy_.start()
    else
      textspy_.stop()

  property bool textVisible
  property bool translationVisible

  property bool speaksText
  property bool speaksTranslation

  property bool popupEnabled: true
  property bool readEnabled: true

  property bool copyEnabled: true

  property bool hoverEnabled: false

  property bool shadowEnabled: true

  //property bool revertsColor: false

  property string rubyType: settings_.rubyType
  property string rubyDic: settings_.meCabDictionary
  property bool rubyEnabled: !!settings_.meCabDictionary

  property bool convertsChinese: false // convert Simplified Chinese to Chinese

  //property bool msimeParserEnabled: false // whether use msime or mecab

  function scrollBeginning() {
    listView_.positionViewAtBeginning()
    //showScrollBar()
  }
  function scrollEnd() {
    cls()
    //showScrollBar()
  }

  function show() {
    visible = true
    cls()
    if (mouseEnabled)
      textspy_.start()
  }

  function hide() {
    listView_.positionViewAtEnd()
    visible = false
    textspy_.stop()
  }

  // - Private -

  opacity: 0
  states: State {
    when: root_.visible
    PropertyChanges { target: root_; opacity: 1.0 }
  }
  transitions: Transition {
    NumberAnimation { property: 'opacity'; duration: 400 }
  }

  Plugin.MainObjectProxy { id: main_ }
  Plugin.TextSpyProxy { id: textspy_ }
  Plugin.TextReaderProxy { id: textreader_ }

  Plugin.Settings { id: settings_ } // Already defined in kagami

  property real zoomFactor: settings_.grimoireZoomFactor

  //property alias shadowOpacity: shadow_.opacity
  property real shadowOpacity: settings_.grimoireShadowOpacity

  property color translationColor: 'green'

  //property alias shadowColor: shadow_.color
  property alias shadowColor: settings_.grimoireShadowColor

  property color fontColor: settings_.grimoireFontColor
  property color textColor: settings_.grimoireTextColor
  //property color commentColor: settings_.grimoireSubtitleColor

  property bool alignCenter: settings_.grimoireAlignCenter
  //property bool copiesText: false

  // Cached
  property color infoseekColor: settings_.infoseekColor
  property color exciteColor: settings_.exciteColor
  property color bingColor: settings_.bingColor
  property color googleColor: settings_.googleColor
  property color baiduColor: settings_.baiduColor
  property color lougoColor: settings_.lougoColor
  property color jbeijingColor: settings_.jbeijingColor
  property color dreyeColor: settings_.dreyeColor
  property color ezTransColor: settings_.ezTransColor
  property color atlasColor: settings_.atlasColor
  property color lecColor: settings_.lecColor
  property color lecOnlineColor: settings_.lecOnlineColor
  property color transruColor: settings_.transruColor

  property string japaneseFont: settings_.japaneseFont
  property string englishFont: settings_.englishFont
  property string chineseFont: settings_.chineseFont
  //property string simplifiedChineseFont
  property string koreanFont: settings_.koreanFont
  property string thaiFont: settings_.thaiFont
  property string vietnameseFont: settings_.vietnameseFont
  property string malaysianFont: settings_.malaysianFont
  property string indonesianFont: settings_.indonesianFont
  property string germanFont: settings_.germanFont
  property string frenchFont: settings_.frenchFont
  property string italianFont: settings_.italianFont
  property string spanishFont: settings_.spanishFont
  property string portugueseFont: settings_.portugueseFont
  property string russianFont: settings_.russianFont
  property string polishFont: settings_.polishFont
  property string dutchFont: settings_.dutchFont

  //property int _FADE_DURATION: 400

  property QtObject highlightMouseArea

  property int listFooterY: 0

  //Plugin.BBCodeParser { id: bbcode_ }
  //function renderComment(comment) {
  //  var t = comment.text
  //  if (root_.convertsChinese && comment.language === 'zhs')
  //    t = bean_.convertChinese(t)
  //  return bbcode_.parse(t)
  //}

  Plugin.MirageBean { id: bean_
    //width: root_.width; height: root_.heigh
    Component.onCompleted: {
      bean_.show.connect(root_.show)
      bean_.clear.connect(root_.clear)
      bean_.pageBreak.connect(root_.pageBreak)
      bean_.showText.connect(root_.showText)
      bean_.showTranslation.connect(root_.showTranslation)
    }
  }

  Plugin.Tts { id: tts_ }

  Plugin.ClipboardProxy { id: clipboard_
    onTextChanged:
      if (root_.clipboardEnabled) {
        var t = Util.trim(text)
        if (t)
          textreader_.addText(t)
      }
  }

  function fontFamily(lang) {
    //return 'DFGirl Std W7'
    //return 'STCaiyun'
    switch (lang) {
    case 'ja': return japaneseFont
    case 'en': return englishFont
    case 'zhs': case 'zht': return chineseFont
    //case 'zhs': return simplifiedChineseFont
    case 'ko': return koreanFont
    case 'th': return thaiFont
    case 'vi': return vietnameseFont
    case 'ms': return malaysianFont
    case 'id': return indonesianFont
    case 'de': return germanFont
    case 'es': return spanishFont
    case 'fr': return frenchFont
    case 'it': return italianFont
    case 'nl': return dutchFont
    case 'pl': return polishFont
    case 'pt': return portugueseFont
    case 'ru': return russianFont
    default: return "DFGirl"
    }
  }

  Rectangle { id: header_
    anchors {
      //left: listView_.left
      left: listView_.left; leftMargin: -9
      bottom: listView_.top; bottomMargin: 4
    }
    width: 50; height: 20
    radius: 9

    //visible: !root_.locked
    visible: !root_.empty

    property bool active: listMouseArea_.containsMouse ||
                          toolTip_.containsMouse ||
                          closeButton_.hover ||
                          //speakButton_.hover ||
                          !!highlightMouseArea && highlightMouseArea.hover

    //color: '#33000000' // black
    //color: active ? '#aa000000' : '#01000000'
    color: root_.shadowColor
    opacity: 0.01

    states: State { name: 'ACTIVE'
      when: header_.active
      PropertyChanges { target: header_; opacity: 0.8 }
      //PropertyChanges { target: horizontalScrollBar_; opacity: 1 }
    }

    transitions: Transition { from: 'ACTIVE'
      NumberAnimation { property: 'opacity'; duration: 400 }
    }

    //gradient: Gradient {  // color: aarrggbb
    //  //GradientStop { position: 0.0;  color: '#ec8f8c8c' }
    //  //GradientStop { position: 0.17; color: '#ca6a6d6a' }
    //  //GradientStop { position: 0.77; color: '#9f3f3f3f' }
    //  //GradientStop { position: 1.0;  color: '#ca6a6d6a' }
    //}

    MouseArea { id: headerMouseArea_
      anchors.fill: parent
      acceptedButtons: Qt.LeftButton
      //enabled: !root_.locked
      drag {
        target: root_
        axis: Drag.XandYAxis
        //minimumX: root_.minimumX; minimumY: root_.minimumY
        //maximumX: root_.maximumX; maximumY: root_.maximumY
      }

      Rectangle {
        anchors.fill: parent
        anchors.margins: -9
        color: '#01000000'

        Desktop.TooltipArea { id: toolTip_
          anchors.fill: parent
          text: qsTr("You can drag me to move the text box.")
        }
      }
    }

    Share.CloseButton { id: closeButton_
      anchors {
        verticalCenter: parent.verticalCenter
        left: parent.left
        //leftMargin: header_.radius
      }
      //visible: header_.active
      color: root_.fontColor
      onClicked: root_.hide()
      toolTip: qsTr("Hide text box")
    }

    Desktop.ContextMenu { id: headerMenu_

      //Desktop.MenuItem {
      //  text: qsTr("Scroll to the beginning")
      //  onTriggered: root_.scrollBeginning()
      //}

      //Desktop.MenuItem {
      //  text: qsTr("Scroll to the end")
      //  onTriggered: root_.scrollEnd()
      //}

      //Desktop.MenuItem {
      //  text: qsTr("Reset Position")
      //  onTriggered: root_.resetPosRequested()
      //}

      Desktop.MenuItem {
        text: Sk.tr("Close")
        onTriggered: root_.hide()
      }
    }

    MouseArea {
      anchors.fill: parent
      acceptedButtons: Qt.RightButton
      onPressed: if (!root_.ignoresFocus) {
        var gp = mapToItem(null, x + mouse.x, y + mouse.y)
        headerMenu_.showPopup(gp.x, gp.y)
      }
    }
  }

  Rectangle { id: shadow_
    anchors {
      left: listView_.left; right: listView_.right
      margins: -8
    }
    y: Math.max(-listView_.contentY, 0)
    height: Math.min(listView_.height,
            -listView_.contentY + root_.listFooterY - y)
            + 5
    visible: root_.shadowEnabled && listView_.count > 0
    //color: root_.revertsColor ? '#99ffffff' : '#44000000'
    color: root_.shadowColor //'#44000000'
    //opacity: 0.27 // #44
    opacity: root_.shadowOpacity
    z: -1
    radius: 18

    //Share.CloseButton {
    //  anchors { left: parent.left; top: parent.top; margins: 2 }
    //  //border.width: 2
    //  onClicked: root_.hide()
    //  toolTip: qsTr("Hide text box")
    //}
  }

  ListView { id: listView_
    anchors.fill: parent
    //width: root_.width; height: root_.height
    clip: true
    boundsBehavior: Flickable.DragOverBounds // no overshoot bounds
    snapMode: ListView.SnapToItem   // move to bounds

    MouseArea { id: listMouseArea_
      anchors {
        left: parent.left; right: parent.right
        top: parent.top
      }
      height: 9
      hoverEnabled: true
      acceptedButtons: Qt.NoButton
    }

    //contentWidth: width
    //contentHeight: 2000

    //effect: Effect.DropShadow {
    //  blurRadius: 8
    //  offset: "1,1"
    //  color: '#aa007f' // purple-like
    //}

    model: ListModel { id: listModel_ }

    highlightFollowsCurrentItem: true
    highlightMoveDuration: 0
    highlightResizeDuration: 0

    highlight: Rectangle {
      width: listView_.width
      radius: 5
      color: root_.shadowEnabled ? '#33000000' : 'transparent'

      MouseArea { id: highlightMouseArea_ // drag area
        Component.onCompleted: root_.highlightMouseArea = highlightMouseArea_

        anchors.fill: parent
        acceptedButtons: Qt.LeftButton
        enabled: root_.shadowEnabled //&& !root_.locked
        drag {
          target: root_
          axis: Drag.XandYAxis
          //minimumX: root_.minimumX; minimumY: root_.minimumY
          //maximumX: root_.maximumX; maximumY: root_.maximumY
        }

        property alias hover: toolTip_.containsMouse

        Desktop.TooltipArea { id: toolTip_
          anchors.fill: parent
          text: qsTr("You can drag this black bar to move the text box.")
        }
      }

      //Share.CloseButton { id: closeButton_
      //  anchors {
      //    verticalCenter: parent.verticalCenter
      //    left: parent.left
      //    leftMargin: 10
      //  }
      //  onClicked: root_.hide()
      //  toolTip: qsTr("Hide the text box")
      //}

      //Share.TextButton { id: saveButton_
      //  anchors {
      //    verticalCenter: parent.verticalCenter
      //    left: parent.left
      //    margins: 20
      //  }
      //  width: 20; height: 15
      //  text: "[" + Sk.tr("save")
      //  font.pixelSize: 14
      //  font.bold: false
      //  styleColor: 'deepskyblue'
      //  backgroundColor: hover ? '#336a6d6a' : 'transparent' // black
      //  //effect: Share.TextEffect {}
      //  style: Text.Raised
      //  onClicked: root_.savePosRequested()
      //  toolTip: qsTr("Save text box position")
      //}

      //Share.TextButton { id: loadButton_
      //  anchors {
      //    verticalCenter: parent.verticalCenter
      //    left: saveButton_.right
      //    margins: 15
      //  }
      //  width: 20; height: 15
      //  text: Sk.tr("load") + "]"
      //  font.pixelSize: 14
      //  font.bold: false
      //  styleColor: 'deepskyblue'
      //  backgroundColor: hover ? '#336a6d6a' : 'transparent' // black
      //  //effect: Share.TextEffect {}
      //  style: Text.Raised
      //  onClicked: root_.loadPosRequested()
      //  toolTip: qsTr("Move text box to the saved position")
      //}

      Text { //id: placeHolder_
        anchors.centerIn: parent
        visible: root_.shadowEnabled
        font.pixelSize: 10
        //font.bold: true
        //font.italic: true
        text: qsTr("you can drag me!") + " >_<"

        color: 'snow'
        //style: Text.Raised
        //styleColor: 'deepskyblue'
        //styleColor: 'black'
      }
    }

    // See: http://doc.qt.digia.com/4.7-snapshot/qml-textedit.html#selectWord-method
    //function ensureVisible(r) {
    //  if (contentX >= r.x)
    //    contentX = r.x
    //  else if (contentX+width <= r.x+r.width)
    //    contentX = r.x+r.width-width
    //  if (contentY >= r.y)
    //    contentY = r.y
    //  else if (contentY+height <= r.y+r.height)
    //    contentY = r.y+r.height-height
    //}

    // Behavior on x { SpringAnimation { spring: 3; damping: 0.3; mass: 1.0 } }
    // Behavior on y { SpringAnimation { spring: 3; damping: 0.3; mass: 1.0 } }

    //MouseArea {
    //  acceptedButtons: Qt.LeftButton
    //  anchors.fill: parent
    //  drag.target: parent; drag.axis: Drag.XandYAxis
    //  onPressed: { /*parent.color = 'red';*/ /*parent.styleColor = 'orange';*/ }
    //  onReleased: { /*parent.color = 'snow';*/ /*parent.styleColor = 'red';*/ }
    //}

    states: State {
      when: listView_.movingVertically || listView_.movingHorizontally
      PropertyChanges { target: verticalScrollBar_; opacity: 1 }
      //PropertyChanges { target: horizontalScrollBar_; opacity: 1 }
    }

    transitions: Transition {
      NumberAnimation { property: 'opacity'; duration: 400 }
    }

    delegate: textComponent_
    //delegate: Loader {
    //  sourceComponent: model.component
    //  property QtObject model: model
    //}

    footer: Item {
      width: listView_.width //height: model.height
      height: Math.max(0, listView_.height - 10) // margin: 10

      onYChanged: root_.listFooterY = y

      //Rectangle {
      //  anchors {
      //    left: parent.left; right: parent.right
      //    bottom: parent.top
      //  }
      //  height: listView_.childrenRect.height
      //  visible: root_.shadowEnabled
      //  color: root_.revertsColor ? '#99ffffff' : '#44000000'
      //  z: -1
      //  radius: 20
      //}
    }
  }

  Ui.ScrollBar { id: verticalScrollBar_
    width: 12
    height: Math.max(0, listView_.height - 12)
    anchors {
      verticalCenter: listView_.verticalCenter
      left: listView_.right
      leftMargin: 2
    }
    opacity: 0
    orientation: Qt.Vertical
    position: listView_.visibleArea.yPosition
    pageSize: listView_.visibleArea.heightRatio
  }

  //Ui.ScrollBar { id: horizontalScrollBar_
  //  width: Math.max(0, listView_.width - 12)
  //  height: 12
  //  anchors.bottom: listView_.bottom
  //  anchors.horizontalCenter: listView_.horizontalCenter
  //  opacity: 0
  //  orientation: Qt.Horizontal
  //  position: listView_.visibleArea.xPosition
  //  pageSize: listView_.visibleArea.widthRatio
  //}

  function showScrollBar() {
    verticalScrollBar_.opacity = 1
  }

  // - List components -

  //property string _JAPANESE_FONT: "MS Gothic"
  ////property string _JAPANESE_FONT: "Meiryo"
  //property string _CHINESE_FONT: "YouYuan"
  //property string _ENGLISH_FONT: "Helvetica"

  //Effect.DropShadow {
  //  blurRadius: 8
  //  offset: "1,1"
  //  color: model.color
  //}

  Component { id: textComponent_
    Item { id: textItem_
      width: visible ? textEdit_.width: 0
      height: visible ? textEdit_.height + 5: 0 // with margins

      visible: {
        //if (model.comment && (model.comment.disabled || model.comment.deleted))
        //  return false
        switch (model.type) {
          case 'text': return root_.textVisible
          //case 'name': return root_.nameVisible && root_.textVisible
          case 'tr': return root_.translationVisible
          //case 'name.tr': return root_.nameVisible && root_.translationVisible
          //case 'comment': return root_.commentVisible
          default: return true
        }
      }

      //NumberAnimation on opacity { // fade in animation
      //  from: 0; to: 1; duration: _FADE_DURATION
      //}

      TextEdit { id: textEdit_
        //Component.onCompleted:
        //  listModel_.setProperty(model.index, 'textEdit', textEdit_)

        //Rectangle {   // Shadow
        //  color: '#44000000'
        //  anchors.fill: parent
        //  z: -1
        //  radius: 15
        //}
        onLinkActivated: Qt.openUrlExternally(link)

        MouseArea { id: textCursor_
          anchors.fill: parent
          //acceptedButtons: enabled ? Qt.LeftButton : Qt.NoButton
          acceptedButtons: Qt.LeftButton
          enabled: !!model.text
          hoverEnabled: enabled

          //property bool enabled:
          //  model.type === 'text' || model.type === 'tr'

          //hoverEnabled: root_.hoverEnabled && model.language === 'ja'

          property string lastSelectedText
          onPositionChanged: {
            if (!root_.hoverEnabled || model.language !== 'ja')
              return

            textEdit_.cursorPosition = textEdit_.positionAt(mouse.x, mouse.y)
            textEdit_.selectWord()
            var t = textEdit_.selectedText
            if (t && t !== lastSelectedText) {
              lastSelectedText = t
              //var gp = Util.itemGlobalPos(parent)
              var gp = mapToItem(null, x + mouse.x, y + mouse.y)
              root_.yakuAt(t, gp.x, gp.y)
            }
          }

          onClicked: {
            if (model.language) {
              textEdit_.cursorPosition = textEdit_.positionAt(mouse.x, mouse.y)
              textEdit_.selectWord()
              var t = textEdit_.selectedText
              if (t) {
                lastSelectedText = t
                if (root_.popupEnabled && model.language === 'ja') {
                  //var gp = Util.itemGlobalPos(parent)
                  var gp = mapToItem(null, x + mouse.x, y + mouse.y)
                  root_.yakuAt(t, gp.x, gp.y)
                }
                if (root_.copyEnabled)
                  textEdit_.copy()
                if (root_.readEnabled && model.language === 'ja')
                  tts_.speak(t, model.language)
              }
            }
          }

          onDoubleClicked:
            if (model.language) {
              var t = model.text
              if (t) {
                textEdit_.deselect()
                if (root_.copyEnabled)
                  clipboard_.text = t
                if (root_.readEnabled)
                  tts_.speak(t, model.language)
              }
            }
        }

        Desktop.TooltipArea { id: toolTip_
          anchors.fill: parent

          visible: !!model.text && model.type !== 'text' && model.type !== 'name'

          text: //model.comment ? commentSummary(model.comment) :
                model.provider ? translationSummary() :
                //model.type === 'name' ? My.tr("Character name") :
                My.tr("Game text")

          //function typeSummary() {
          //  switch (model.type) {
          //  case 'tr': return "Machine translation"
          //  case 'subtitle': return "Community subtitle"
          //  case 'comment': return "User comment"
          //  default: return ""
          //  }
          //}

          function translationSummary() {
            var tr = My.tr(Util.translatorName(model.provider))
            var lang = Sk.tr(model.language)
            return tr + " (" + lang + ")"
          }

          //function commentSummary(c) {
          //  var us = '@' + c.userName
          //  var lang = c.language
          //  lang = "(" + lang + ")"
          //  var sec = c.updateTimestamp > 0 ? c.updateTimestamp : c.timestamp
          //  var ts = Util.timestampToString(sec)
          //  return us + lang + ' ' + ts
          //}
        }

        // height is the same as painted height
        width: listView_.width

        effect: Effects.TextShadow {
          blurRadius: 8; offset: '1,1'
          enabled: !!textEdit_.text
          color: {
            if (toolTip_.containsMouse || textCursor_.containsMouse)
              return 'red'
            switch (model.type) {
            case 'text': return root_.textColor
            //case 'name':
            //case 'comment': return model.comment.color || root_.commentColor
            case 'tr':
            //case 'name.tr':
              switch(model.provider) {
              case 'jbeijing': return root_.jbeijingColor
              case 'dreye': return root_.dreyeColor
              case 'eztrans': return root_.ezTransColor
              case 'atlas': return root_.atlasColor
              case 'lec': return root_.lecColor
              case 'lecol': return root_.lecOnlineColor
              case 'transru': return root_.transruColor
              case 'infoseek': return root_.infoseekColor
              case 'excite': return root_.exciteColor
              case 'bing': return root_.bingColor
              case 'google': return root_.googleColor
              case 'baidu': return root_.baiduColor
              case 'lou': return root_.lougoColor
              default: return root_.translationColor
              }
            default: return  'transparent'
            }
          }
        }

        anchors.centerIn: parent
        textFormat: TextEdit.RichText
        text: renderText(
          //model.comment ? root_.renderComment(model.comment) :
          root_.rubyEnabled && model.type === 'text' && model.language === 'ja' ?
            bean_.renderJapanese(
              model.text,
              //root_.msimeParserEnabled,
              root_.rubyType,
              root_.rubyDic,
              Math.round(root_.width / (23 * zoomFactor)), // char per line
              Math.round(10 * zoomFactor) + 'px', // ruby size of furigana
              toolTip_.containsMouse || textCursor_.containsMouse, // colorize
              root_.alignCenter
            ) :
          model.text
        )
        readOnly: true
        focus: false
        //smooth: false // readonly, no translation

        //wrapMode: model.needsWrap ? TextEdit.Wrap : TextEdit.NoWrap
        wrapMode: model.language === 'ja' && model.type === 'text' ?
            TextEdit.NoWrap : TextEdit.Wrap

        verticalAlignment: TextEdit.AlignVCenter
        //horizontalAlignment: TextEdit.AlignHCenter
        horizontalAlignment: root_.alignCenter ? TextEdit.AlignHCenter : TextEdit.AlignLeft
        //selectByMouse: true

        //onCursorRectangleChanged: listView_.ensureVisible(cursorRectangle)

        font.family: root_.fontFamily(model.language)
        //font.bold: Util.isAsianLanguage(model.language)
        //font.italic: Util.isLatinLanguage(model.language)

        //color: root_.revertsColor ? '#050500' : 'snow'
        color: root_.fontColor
        font.pixelSize: 18 * zoomFactor

        function renderText(t) {
          return t || ""
          //return !t ? "" : root_.shadowEnabled ? t :
          //  '<span style="background-color:rgba(0,0,0,10)">' + t + '</span>'
        }
      }
    }
  }


  // Index of the first item on the last page
  // Assume page index is always less then list view count
  property int _pageIndex: 0
  property int _timestamp: 0 // current text timestamp

  function loadSettings() {
    clipboardEnabled = settings_.mirageClipboardEnabled
    mouseEnabled = settings_.mirageMouseEnabled
    textVisible = settings_.mirageTextVisible
    translationVisible = settings_.mirageTranslationVisible
    speaksText = settings_.mirageSpeaksText
    speaksTranslation = settings_.mirageSpeaksTranslation
  }
  function saveSettings() {
    settings_.mirageClipboardEnabled = clipboardEnabled
    settings_.mirageMouseEnabled = mouseEnabled
    settings_.mirageTextVisible = textVisible
    settings_.mirageTranslationVisible = translationVisible
    settings_.mirageSpeaksText = speaksText
    settings_.mirageSpeaksTranslation = speaksTranslation
  }

  Component.onDestruction: {
    saveSettings()
  }
  Component.onCompleted: {
    loadSettings()
    qApp.aboutToQuit.connect(saveSettings)
    console.log("mirage.qml: pass")

    pageBreak()
    var msg = Sk.tr("Empty") + "! &gt;&lt;"
    showTranslation(msg, '', '', 0)
  }

  function createTextItem(text, lang, type, provider) {
    return {
      language: lang
      , text: text
      , type: type // text, tr, comment, name, or name.tr
      , provider: provider
      //, textEdit: undefined // callbacks
    }
  }

  function addText(text, lang, type, provider) {
    var item = createTextItem.apply(this, arguments)
    listModel_.append(item)
    listView_.currentIndex = _pageIndex
  }

  function showText(text, lang, timestamp) {
    _timestamp = timestamp
    addText(text, lang, 'text')
    if (speaksText)
      tts_.speak(text, lang)
  }

  function showTranslation(text, lang, provider, timestamp) {
    //text = text.replace(/\n/g, "<br/>")
    var item = createTextItem(text, lang, 'tr', provider)
    if (_timestamp === Number(timestamp))
      listModel_.append(item)
    else if (_pageIndex <= listModel_.count)
      listModel_.insert(_pageIndex++, item)
    else // this should never happen
      listModel_.append(item)
    listView_.currentIndex = _pageIndex
    if (speaksTranslation)
      tts_.speak(text, lang)
  }

  //function showComment(c) {
  //  addText(c.text, c.language, 'comment', undefined, c)
  //}


  // Insert a page break
  function pageBreak() {
    slimList()
    _pageIndex = listModel_.count
    addText()
    cls()
  }

  // Limit total number of items in the list by removing extra items in the beginning
  function slimList() {
    if (listModel_.count > 100) {   // if the list size is greater than 100
      //console.log("grimoire.qml:slimList: enter: count =", listModel_.count)
      while (listModel_.count > 70) // remove the first 30 items
        listModel_.remove(0)
      if (listView_.currentIndex >= 30) // 30 = 100 - 70
        listView_.currentIndex -= 30
      //console.log("grimoire.qml:slimList: leave: count =", listModel_.count)
      console.log("grimoire.qml:slimList: pass")
    }
  }

  // Clean the screen by scrolling
  function cls() {
    if (_pageIndex + 1 < listView_.count)
      listView_.positionViewAtIndex(_pageIndex + 1, ListView.Beginning)
    else
      listView_.positionViewAtEnd()
  }

  function clear() {
    _pageIndex = 0
    listModel_.clear()
    console.log("grimoire.qml:clear: pass")
  }

  // - Context Menu -

  // Popup globalPos

  property int popupX
  property int popupY

  function popupIndex() {
    var pos = listView_.mapFromItem(null, popupX, popupY)
    return listView_.indexAt(listView_.contentX + pos.x, listView_.contentY + pos.y)
  }

  function textEditAt(index) {
    if (index >= 0 && index < listModel_.count) {
      var item = listModel_.get(index)
      if (item)
        return item.textEdit
    }
    return undefined
  }

  function textEditHoveredText(textEdit) {
    if (!textEdit.selectedText) {
      var pos = textEdit.mapFromItem(null, popupX, popupY)
      textEdit.cursorPosition = textEdit.positionAt(pos.x, pos.y)
      textEdit.selectWord()
    }
    return textEdit.selectedText
  }

  Desktop.ContextMenu { id: contextMenu_
    function popup(x, y) {
      popupX = x; popupY = y

      //var item = listModel_.get(popupIndex())
      //var hasComment = !!(item && item.comment)
      //editAct_.enabled = hasComment
      //userAct_.enabled = hasComment

      showPopup(x, y)
    }

    Desktop.MenuItem {
      text: Sk.tr("Copy")
      //shortcut: "Ctrl+A"
      onTriggered: {
        var item = listModel_.get(popupIndex())
        if (item && item.text)
          clipboard_.text = item.text
      }
    }

    Desktop.MenuItem {
      text: My.tr("Read Sentence") + " (" + Sk.tr("Double-click") + ")"
      //shortcut: "Ctrl+A"
      onTriggered: {
        var item = listModel_.get(popupIndex())
        if (item && item.text && item.language) {
          tts_.speak(item.text, item.language)
          console.log("grimoire.qml:readAll: pass")
        }
      }
    }

    //Desktop.MenuItem {
    //  text: qsTr("Scroll to the Beginning")
    //  onTriggered: root_.scrollBeginning()
    //}

    //Desktop.MenuItem {
    //  text: qsTr("Scroll to the End")
    //  onTriggered: root_.scrollEnd()
    //}

    Desktop.Separator {}

    Desktop.MenuItem {
      text: My.tr("Monitor mouse")
      checked: root_.mouseEnabled
      checkable: true
      onTriggered: mouseEnabled = !mouseEnabled
    }

    Desktop.MenuItem {
      text: My.tr("Monitor clipboard")
      checked: root_.clipboardEnabled
      checkable: true
      onTriggered: clipboardEnabled = !clipboardEnabled
    }

    Desktop.Separator {}

    Desktop.MenuItem {
      text: Sk.tr("Show {0}").replace('{0}', Sk.tr("text"))
      checked: root_.textVisible
      checkable: true
      onTriggered: textVisible = !textVisible
    }

    Desktop.MenuItem {
      text: Sk.tr("Show {0}").replace('{0}', Sk.tr("translation"))
      checked: root_.translationVisible
      checkable: true
      onTriggered: translationVisible = !translationVisible
    }

    Desktop.MenuItem {
      text: My.tr("Speak {0}").replace('{0}', Sk.tr("text"))
      checked: root_.speaksText
      checkable: true
      onTriggered: {
        speaksText = !speaksText
        if (speaksText && speaksTranslation)
          speaksTranslation = false
      }
    }

    // TODO
    //Desktop.MenuItem {
    //  text: My.tr("Speak {0}").replace('{0}', Sk.tr("translation"))
    //  checked: root_.speaksTranslation
    //  checkable: true
    //  onTriggered: {
    //    speaksTranslation = !speaksTranslation
    //    if (speaksText && speaksTranslation)
    //      speaksText = false
    //  }
    //}

    Desktop.Separator {}

    Desktop.MenuItem {
      text: Sk.tr("Help")
      onTriggered: main_.showTextReaderHelp()
    }

    //Desktop.MenuItem {
    //  text: Sk.tr("Clear")
    //  onTriggered: root_.clear()
    //}

    Desktop.MenuItem {
      text: Sk.tr("Close")
      onTriggered: root_.hide()
    }
  }

  MouseArea {
    anchors.fill: parent
    acceptedButtons: Qt.RightButton
    onPressed: if (!root_.ignoresFocus) {
      var gp = mapToItem(null, x + mouse.x, y + mouse.y)
      contextMenu_.popup(gp.x, gp.y)
    }
  }
}

// EOF
