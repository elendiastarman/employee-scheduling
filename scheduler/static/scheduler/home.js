function switchToggle(target_id, choice_id) {
	var target = document.getElementById(target_id);
	var choice = document.getElementById(choice_id);
	
	if ((choice.value === target.id) && (target.checked === true)) {
		target.checked = false
	} else {
		choice.value = target.id
	}
}

function showAnnouncements(target_id) {
	document.getElementById(target_id).style.display = "block";
	var target2_id = "show "+target_id;
	document.getElementById(target2_id).style.display = "none";
}