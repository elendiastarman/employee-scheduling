function loadImageNow(target_id) {
	elem = document.getElementById(target_id);
	elem.setAttribute('src', elem.getAttribute('data-src'));
}