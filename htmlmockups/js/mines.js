// Generated by CoffeeScript 1.3.3
(function() {
  var render_board, server_url, update;

  server_url = "http://localhost:5000";

  update = function() {
    return $.ajax({
      url: server_url,
      data: {
        x: 1,
        y: 1
      },
      success: render_board
    });
  };

  render_board = function(data) {
    var board, item, row, _i, _len, _ref, _results;
    alert("heyo");
    board = $("#board_wrapper");
    board.html("");
    console.log(data);
    _ref = data.state;
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      row = _ref[_i];
      _results.push((function() {
        var _j, _len1, _results1;
        _results1 = [];
        for (_j = 0, _len1 = row.length; _j < _len1; _j++) {
          item = row[_j];
          _results1.push(board.append("x"));
        }
        return _results1;
      })());
    }
    return _results;
  };

  $(function() {
    return update();
  });

}).call(this);