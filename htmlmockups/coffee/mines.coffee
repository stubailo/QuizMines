server_url = "http://localhost:5000"

update = ->
  $.ajax
    url: server_url
    data:
      x: 1
      y: 1
    success: render_board

move = (x,y) =>
  return =>
    $.ajax
      url: server_url
      data:
        x: x
        y: y
      success: render_board

render_board = (data) =>
  board = $("#board_wrapper")
  board.html("")

  data = $.parseJSON data

  board.append "<table>"

  ypos = 0

  for row in data.state
    board.append "<tr>"

    xpos = 0

    for item in row

      item = if item is null then " " else item

      new_button = $ "<button class='mine_button'>#{item}</button>"
      new_button.click move ypos, xpos
      table_cell = $ "<td></td>"
      table_cell.append new_button
      board.append table_cell

      xpos += 1

    board.append("</tr>")

    ypos += 1

  board.append "</table>"

$ ->
  update()
