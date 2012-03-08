function put_message(level, text) {
  var $messages = $('#messages'),
    html = $messages.children('.template').html();

  html = html.replace('%level', level).replace('%message', text);
  $messages.append(html);
}