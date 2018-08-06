function toggle_modal(modal_name){
	var modal = document.getElementById(modal_name + '_modal');
	modal.classList.toggle('is-active');
}

function async_request(url, callback){
	var xmlhttp;
	xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
				if (this.readyState == 4 && this.status == 200) {
						callback(this);
			 }
		};
	xmlhttp.open("GET", url, true);
	xmlhttp.send();
}

function edit_pet_callback(response){
	var response = JSON.parse(response.responseText);
	document.getElementById(response['rowid']).classList.remove('is-loading');
	document.getElementById("checkmark_" + response['rowid']).style = "";
}

function edit_pet(element){
	var rowid = element.id;
	element.classList.add('is-loading');
	var url = "/edit_pet/" + rowid + "?";
	possible_edits = ['name', 'species', 'breed', 'age', 'price'];
	for (var i = possible_edits.length - 1; i >= 0; i--) {
		input_id = possible_edits[i] + "_" + rowid;
		val = document.getElementById(input_id).value;
		if(val){
			get_param = possible_edits[i] + "=" + val + "&";
			url += get_param;
		}
	}
	url = url.slice(0, -1); // get rid of trailing &
	async_request(url, edit_pet_callback);
}

function toggle_pet_like(element){
	rowid = element.id.split('_')[2];
	var url = '/toggle_pet_like?rowid=' + rowid;
	async_request(url, toggle_pet_like_callback);
}

function toggle_pet_like_callback(response){
	var rowid = JSON.parse(response.responseText)['rowid'];
	document.getElementById('pet_like_' + rowid).classList.toggle('liked');
}