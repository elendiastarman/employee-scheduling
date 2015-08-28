function addFormBlock(id) {
	// elems = document.getElementsByName(name);
	
	// for (var i=0; i<elems.length; i++) {
		// console.log(elems[i].getAttribute("value"));
	// }
	var elem = document.getElementById(id);
	// var toCopy = elem.lastChild;
	// elem.appendChild(toCopy);
	var divs = elem.getElementsByTagName("div");
	var toCopy = divs[divs.length-1];
	var toClear = toCopy.cloneNode(true)
	elem.appendChild(toClear);
	elem.appendChild( document.createElement("br") );
	var num = (parseInt(toCopy.getAttribute("value"))+1).toString();
	toClear.setAttribute("value",num);
	
	var inputs = toClear.getElementsByTagName("input");
	var errors = toClear.getElementsByClassName("error");
	
	for (var i=0; i<inputs.length; i++) {
		inputs[i].value = "";
		inputs[i].setAttribute("name", inputs[i].getAttribute("name").substring(0,2) + num.toString());
	}
	for (var i=0; i<errors.length; i++) {
		errors[i].innerHTML = "";
	}
}