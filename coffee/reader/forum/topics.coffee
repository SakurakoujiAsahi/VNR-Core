# forum/topics.coffee
# 12/31/2014 jichi
# Required by chat.haml
#
# Require
# - jquery
# - haml
# - underscore
#
# Beans:
# - mainBean: coffeebean.MainBean
# - topicEditBean: topicedit.TopicEditorManagerBean

dprint = ->
  Array::unshift.call arguments, 'topics:'
  console.log.apply console, arguments

# Global variables

INIT_TOPIC_COUNT = 10
MORE_TOPIC_COUNT = 20

HIGHLIGHT_INTERVAL = 1500

HAML_TOPIC = null
createTemplates = ->

  # HAML for topic
  # - id
  # - type
  # - userName
  # - userStyle
  # - lang
  # - userAvatarUrl  url or null
  # - content: string  html
  # - createTime
  # - updateTime
  # - image  url or null
  # - likeCount  int
  # - dislikeCount  int

  HAML_TOPIC = Haml """\
.topic.topic-new(data-id="${id}" data-type="${type}")
  :if userAvatarUrl
    %a(href="${userAvatarUrl}" title="#{tr 'Avatar'}")
      %img.img-circle.avatar(src="${userAvatarUrl}" alt="#{tr 'Avatar'}")
  .right
    .header.line
      .item.type.text-warning = tr(type)
      %span.pull-right
        %a.item(href="javascript:" style="${userStyle}") @${userName}
        .item.text-minor = lang
        .item.text-minor = createTime
        .item.text-success = updateTime
    %a.item.title(title="#{tr 'Browse'}") ${title}
    :if scores
      .score
        .pp-table.dock
          :if scores.overall != undefined
            .pp-row(data-type='overall')
              .pp-name #{tr 'Overall'}:
              .pp-value ${scores.overall}/10
          :if scores.ecchi != undefined
            .pp-row(data-type='ecchi')
              .pp-name #{tr 'Ecchi'}:
              .pp-value ${scores.ecchi}/10
    .footer
      .btn-group.like-group
        %a.like.btn.btn-link.btn-sm(role="button" title="#{tr 'Like'}" data-value="${likeCount}")
          %span.fa.fa-thumbs-up
          %span.value = likeCount
        %a.dislike.btn.btn-link.btn-sm(role="button" title="#{tr 'Dislike'}" data-value="${dislikeCount}")
          %span.fa.fa-thumbs-down
          %span.value = dislikeCount
      .btn-group
        %a.btn-reply.btn.btn-link.btn-sm(role="button" title="#{tr 'Reply'}")
          #{tr 'Reply'}
          :if postCount
            = ' (' + postCount + ')'
        :if userName == USER_NAME
          %a.btn-edit.btn.btn-link.btn-sm(role="button" title="#{tr 'Edit'}") #{tr 'Edit'}
    :if image
      .image
        %a(href="${image.url}" title="${image.title}")
          %img(src="${image.url}" alt="${image.title}")
""".replace /\$/g, '#'

# Functions and classes

renderTopic = (data) -> # object topic -> string
  su = data.subupload
  if su
    su.ignoreCount = (su.totalCount or 0) - (su.createCount or 0) - (su.updateCount or 0) - (su.errorCount or 0)
    su.createTimeString = util.formatDate su.createTime
    su.updateTimeString = util.formatDate su.updateTime
  HAML_TOPIC
    id: data.id
    type: data.type
    lang: util.getLangName data.lang
    #userStyle: if data.userColor then "color:#{data.userColor}" else ''
    #userStyle: ''
    userAvatarUrl: util.getAvatarUrl data.userAvatar
    userStyle: if data.userColor then "color:#{data.userColor}" else ''
    title: data.title
    content: util.renderContent data.content
    createTime: util.formatDate data.createTime
    updateTime: if data.updateTime > data.createTime then util.formatDate data.updateTime else ''
    userName: data.userName
    image: if data.image then {title:data.image.title, url:util.getImageUrl data.image} else null
    postCount: data.postCount
    likeCount: data.likeCount or 0
    dislikeCount: data.dislikeCount or 0
    scores: data.scores # {overall:int score, ecchi:int score}
    su: su

editTopic = (topic) -> topicEditBean.editTopic JSON.stringify topic # long ->

# Classes
#
class TopicList
  subjectType: 'game'

  constructor: (container: @$sel, more:@$more, subjectId:@subjectId) ->
    @topics = [] # [object topic]

    @bind()
    @show()

  # Helper functions

  $getTopic: (topicId) =>  @$sel.find ".topic[data-id=#{topicId}]" # long -> $el
  getTopic: (topicId) => _.findWhere @topics, id:topicId # long -> object

  _bindNewTopics: =>
    self = @
    @$sel.find('.topic.topic-new').each ->
      $topic = $ @
        .removeClass 'topic-new'

      topicId = $topic.data 'id'
      topic = self.getTopic topicId

      $header = $topic.find '> .right > .header'
      $footer = $topic.find '> .right > .footer'

      $header.find('a.user').click ->
        mainBean.showUser topic.userName if topic?.userName
        false

      $footer.find('.btn-edit').click ->
        editTopic topic if topic
        false

      $footer.find('.btn-reply').click ->
        # TODO
        #replyPost self.topicId, postId if self.topicId and postId
        false

      $footer.find('.like-group').removeClass 'fade-in' if topic?.likeCount or topic?.dislikeCount

      $footer.find('.btn.like').click ->
        if topic and USER_NAME and USER_NAME isnt topic.userName
          $that = $footer.find '.btn.dislike.selected'
          if $that.length
            $that.removeClass 'selected'
            $value = $that.find '.value'
            $value.text -1 + Number $value.text()
          $this = $ @
          $this.parent('.like-group').removeClass 'fade-in'
          selected = $this.hasClass 'selected'
          value = if selected then 0 else 1
          ticket.update
            data:
              login: USER_NAME
              password: USER_PASSWORD
              targetType: 'topic'
              targetId: topicId
              type: 'like'
              value: value
            success: =>
              $this.toggleClass 'selected'
              $value = $this.find '.value'
              $value.text (if selected then -1 else 1) + Number $value.text()
        false

      $footer.find('.btn.dislike').click ->
        if topic and USER_NAME and USER_NAME isnt topic.userName
          $that = $footer.find '.btn.like.selected'
          if $that.length
            $that.removeClass 'selected'
            $value = $that.find '.value'
            $value.text -1 + Number $value.text()
          $this = $ @
          $this.parent('.like-group').removeClass 'fade-in'
          selected = $this.hasClass 'selected'
          value = if selected then 0 else -1
          ticket.update
            data:
              login: USER_NAME
              password: USER_PASSWORD
              targetType: 'topic'
              targetId: topicId
              type: 'like'
              value: value
            success: =>
              $this.toggleClass 'selected'
              $value = $this.find '.value'
              $value.text (if selected then -1 else 1) + Number $value.text()
        false

  addTopics: (topics) => # [object topic] ->
    @topics.push.apply @topics, topics
    #document.title = "#{PAGE_TITLE} (#{@topics.length})"
    # TODO: review
    h = (renderTopic it for it in topics when it.type isnt 'review').join ''
    @$sel.append h
    @_bindNewTopics()

  _highlightNewTopics: =>
    @$sel.find '.topic.topic-new'
      .effect 'highlight', HIGHLIGHT_INTERVAL

  addTopic: (topic) => # object topic ->
    @topics.push topic
    #document.title = "#{PAGE_TITLE} (#{@topics.length})"
    if topic.type isnt 'review'
      h = renderTopic topic
      @$sel.prepend h
      @_highlightNewTopics()
      @_bindNewTopics()
    else
      dprint 'addTopic: error: unknown topic type'

  updateTopic: (topic) => # object topic ->
    oldtopic = @getTopic topic.id
    if oldtopic
      util.fillObject oldtopic, topic
      $topic = @$getTopic topic.id
      if $topic.length
        h = renderTopic topic
        $topic.replaceWith h

        @_highlightNewTopics()
        @_bindNewTopics()
        return

    dprint 'updateTopic: error: topic lost'

  # AJAX actions

  bind: =>
    self = @
    @$more.hide().click ->
      $this = $ @
      unless $this.data 'locked'
        $this.data 'lock', true
        self.more()
        $this.data 'lock', false
      false

  show: =>
    self = @
    spin true
    rest.forum.list 'topic',
      data:
        subjectId: @subjectId
        subjectType: @subjectType
        sort: 'updateTime'
        asc: false
        complete: true
        limit: INIT_TOPIC_COUNT
      error: ->
        spin false
        growl.warn tr 'Internet error'
      success: (data) ->
        spin false
        if data.length
          self.addTopics data
          self.$more.show()
        else
          growl.warn tr 'Internet error'

  more: =>
    self = @
    spin true
    rest.forum.list 'topic',
      data:
        subjectId: @subjectId
        subjectId: @subjectType
        sort: 'updateTime'
        asc: false
        complete: true
        first: @topics.length
        limit: MORE_TOPIC_COUNT
      error: ->
        spin false
        growl.warn tr 'Internet error'
      success: (data) ->
        spin false
        if data.length
          self.addTopics data
        else
          growl tr "No more"

## Export ##

init = ->
  createTemplates()

@topicsjs =
  init: init
  TopicList: TopicList

# EOF
