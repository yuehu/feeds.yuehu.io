(function(d) {

  var colors = [
    // colors from http://developer.android.com/design/style/color.html
    '#33b5e5',
    '#aa66cc',
    '#99cc00',
    '#ffbb44',
    '#ff4444',

    '#0099cc',
    '#9933cc',
    '#669900',
    '#ff8800',
    '#cc0000',

    // colors from http://purecss.io/
    '#0e90d2',
    '#8058a5',
    '#5eb95e',
    '#dd514c',
    '#f37b1d',
    '#fad232'
  ];
  var index = 0;

  function createItem(title, type, name) {
    var el = d.createElement('a');
    el.className = 'item ' + type;
    var href = '/' + type + '/' + name + '.xml';
    el.href = href;
    el.innerHTML = '<h3>' + title + '</h3><p>' + href + '</p>';
    el.style.backgroundColor = colors[index];
    d.body.appendChild(el);
    index += 1;
    if (index >= colors.length) {
      index = 0;
    }
  }

  function request(type) {
    var url = '/' + type + '.json';
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
      if (req.readyState === 4) {
        var data = JSON.parse(req.response);
        for (var key in data) {
          createItem(data[key].title, type, key);
        }
      }
    };
    req.open('GET', url);
    req.send();
  }

  createItem('知乎日报', 'zhihu', 'daily');
  request('weixin');
  request('zhihu');
})(document);
