server_url = "http://10.156.25.239:5000"

start_update_clock = ->
  setInterval update, 3000

update_url = ->
  server_url = $("#ip_form input").val()
  return false

update = ->
  $.ajax
    url: server_url
    success: update_view

question_time = (question) ->
  $("#question_dialog").show()
  $("#question_question").text(question)


win = ->
  $("#win").slideDown()

update_view = (data) ->
  data = $.parseJSON data

  if data.moved is "false"
    log_messages([["System", "It's not your turn! :]"]]) 
  else
    if data.win
      win()

    if data.question
      question_time(data.question)
    else
      end_question_time()

    if data.messages
      log_messages(data.messages)

    render_board data
    $("#last_update").text(new Date())

    update_buddy_list(data)


log_messages = (messages) ->
  for message in messages
    $("#log_window").append( "<div class='sender'>" + message[0] + "</div>")
    $("#log_window").append( "<div class='message'>" + message[1] + "</div>")
    lw = $("#log_window").get(0)
    lw.scrollTop = lw.scrollHeight;

end_question_time = ->
  $("#question_dialog").hide()
  $("#question_dialog input[type=text]").val("")

move = (x,y) =>
  return =>
    $.ajax
      url: server_url
      data:
        x: x
        y: y
      success: update_view
flag = (x,y) =>
  return (event) =>
    event.preventDefault()
    $.ajax
      url: server_url
      data:
        flag: true
        x: x
        y: y
      success: update_view
    return false

render_board = (data) =>
  board = $("#board_wrapper")
  board.html("")

  table = $ "<table>"
  board.append table

  ypos = 0

  for row in data.state
    table_row = $ "<tr>"
    
    table.append table_row

    xpos = 0

    for item in row
      

      item = if item is null then " " else item

      new_button = $ "<button class='mine_button'>#{item}</button>"
      if 0 <= (parseInt item) <= 8
        new_button.addClass("mine_" + item)
      if (parseInt item) is -1
        new_button.html "<i class='icon-asterisk'></i>"
      if (parseInt item) is -2
        new_button.html "<i class='icon-flag'></i>"
      new_button.click move ypos, xpos
      new_button.contextmenu flag ypos, xpos
      table_cell = $ "<td></td>"
      table_cell.append new_button
      table_row.append table_cell

      xpos += 1

    board.append("</tr>")

    ypos += 1

  board.append "</table>"

init_chat = ->
  $("#chat_form").submit (event) ->
    event.preventDefault()
    if $("#chat_form input").val()
      $.ajax
        url: server_url
        data:
          message: $("#chat_form input").val()
        success: update_view
      $("#chat_form input").val("") 
    return false

update_buddy_list = (data) ->
  buddies = data.connected

  $("#buddy_list").html("")
  for buddy in buddies
    entry = $ "<div class='buddy_list_item'>"
    entry.append $ "<div class='bear_small bear_#{buddy[1]}'>"
    if data.player[1] == buddy[1]
      entry.append $ "<p>#{buddy[0]} (you)</p>"
    else
      entry.append $ "<p>#{buddy[0]}</p>"
      
    entry.append $ "<p>#{buddy[2]}</p>"

    $("#buddy_list").append entry

init_ip_form = ->
  $("#ip_form input").val(server_url)
  $("#ip_form").submit update_url

$ ->
  $("#question_switch_button").click (event) ->
    event.preventDefault()
    $.ajax
      url: server_url
      data:
        switch: true
      success: update_view
    return false

  $("#question_dialog form").submit (event) ->
    event.preventDefault()
    $.ajax
      url: server_url
      data:
        answer: $("#question_dialog input[type=text]").val()
      success: update
    return false
  check_for_too_many_players_and_start = (response) ->
    console.log response
    if ($.parseJSON response).extra
      alert "Too many users logged in.  5 is the maximum."
    else
      init_ip_form()
      init_chat()
      end_question_time()
      update()
      start_update_clock()
  $.ajax
    url: server_url
    success: check_for_too_many_players_and_start



