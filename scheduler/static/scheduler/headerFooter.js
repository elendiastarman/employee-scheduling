function activate_tab() {
	var url = window.location.href;
	var host = window.location.host;
	
	var first_slash = url.indexOf('/', 7+host.length);
	var second_slash = url.indexOf('/', first_slash+1);
	var root = url.substring(first_slash+1, second_slash);
	
	if (url.indexOf('policies') > 0) {
		root = 'policies';
	}
	
	var elem = document.getElementById( root );
	elem.className += " active_tab";
}

function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    }
  }
}

window.onload = activate_tab;