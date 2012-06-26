server_url = "http://localhost:5000"

update = ->
  $.ajax
    url: server_url
    data:
      x: 1
      y: 1
    success: render_board

render_board = (data) ->
  alert "heyo"
  board = $("#board_wrapper")
  board.html("")

  console.log data

  for row in data.state
    for item in row
      board.append "x"

$ ->
  update()
