// function switchToggle(target_id, choice_id) {
	// var target = document.getElementById(target_id);
	// var choice = document.getElementById(choice_id);
	
	// if ((choice.value === target.id) && (target.checked === true)) {
		// target.checked = false
	// } else {
		// choice.value = target.id
	// }
// }

function set_toggle(target_id) {
	var target = document.getElementById(target_id);
	var state = document.getElementById("state");
	
	state.checked = !target.checked;
}

function toggle(target_id) {
	var target = document.getElementById(target_id);
	// var state = document.getElementById("state");
	
	//target.checked = state.checked;
	target.checked = !target.checked;
	
	if (target.checked) {
		target.parentNode.className += " checked";
	} else {
		target.parentNode.className = target.parentNode.className.replace( /(?:^|\s)checked(?!\S)/g , '' );
	}
}