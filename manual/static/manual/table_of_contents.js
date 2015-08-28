function toggle(target_id) {
	var target = document.getElementById(target_id);
	
	var c = '';
	
	if (target.className == "collapsed") {
		c = "expanded";
	} else {
		c = "collapsed";
	}
	
	target.className = c;
	
	var targ2_id = 'li_'+(parseInt(target_id.replace('ul_',''))-1).toString();
	// alert(targ2_id);
	var targ2 = document.getElementById(targ2_id);
	var iH = targ2.children[0].innerHTML;
	var loc1 = iH.indexOf('+');
	var loc2 = iH.indexOf('-');
	
	if (loc1 > -1) {
		iH = iH.replace('+','-');
	} else if (loc2 > -1) {
		iH = iH.replace('-','+');
	}
	
	targ2.children[0].innerHTML = iH;
	
	// for (var i=0; i<target.children.length; i++;) {
		// target.children[i].className = c;
	// }
}

function set_plusminus() {
	var uls = document.getElementsByTagName('ul');
	
	for (var i=1; i<uls.length; i++) {
		var ul_id = uls[i].id;
		var li_id = 'li_'+(parseInt(ul_id.replace('ul_',''))-1).toString();
		
		var elem = document.getElementById(li_id);
		
		if (uls[i].className == "expanded") {
			var c = '-';
		} else if (uls[i].className == "collapsed") {
			var c = '+';
		}
		
		if (elem) {elem.children[0].innerHTML = c + elem.children[0].innerHTML;}
	}
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

addLoadEvent(set_plusminus);