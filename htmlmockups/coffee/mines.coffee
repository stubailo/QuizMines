server_url = "http://10.156.25.207:5000"

update = ->
  $.ajax
    url: server_url
    data:
      x: 1
      y: 1
    success: -> render_board

render_board = (data) ->
  board = $("#board_wrapper")
  board.html("")
 
  board.html(data)

$ ->
  update()
