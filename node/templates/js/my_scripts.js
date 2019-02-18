function createCORSRequest(method, url) {
	var xhr = new XMLHttpRequest();
	if ("withCredentials" in xhr) {
		xhr.open(method, url, true);
	} else if (typeof XDomainRequest != "undefined") {
		xhr = new XDomainRequest();
		xhr.open(method, url);
	} else {
		xhr = null;
	}
	return xhr;
}

function getChainLen(xhr){
	xhr.onload = function() {
		var text = xhr.responseText;
		console.log(text);
		var obj = JSON.parse(text);
		document.getElementById('place_for_chain_length').innerHTML = '<strong>' + obj.chain_length + '</strong>'
	};
	navigator.onLine
	try{
		xhr.send();
	}catch(err) {
	  document.getElementById("demo").innerHTML = err.message;
	}
}

function getBalanceWallet(xhr){
	if (event.keyCode !== 13)
		return;
	xhr.onload = function() {
		var text = xhr.responseText;
		console.log(text);
		var obj = JSON.parse(text);
		document.getElementById('place_for_balance').innerHTML = '<strong>' + obj + '</strong>'
	};
	try{
		xhr.send();
	}catch(err) {
	  document.getElementById("demo").innerHTML = err.message;
	}
}

function getBlockByHeight(xhr){
	if (event.keyCode !== 13)
		return;
	xhr.onload = function() {
		var text = xhr.responseText;
		var obj = JSON.parse(text);
		let tr = "";
		var tbody = document.getElementById('place_for_block_height');
		for (var key in obj) {
			if (key != "transactions") {
				tr += "<tr>" + "<td>" + key + "</td>" + "<td>" + obj[key] + "</td>" + "</tr>"
			} else {
				for (var j = 0; j < obj[key].length; j++)
					tr += "<tr>" + "<td>" + key + "</td>" + "<td>" + obj[key][j] + "</td>" + "</tr>"
			}
		}
		tbody.innerHTML += tr + "<br>";
	};
	try{
		xhr.send();
	}catch(err) {
	  document.getElementById("demo").innerHTML = err.message;
	}
}

function getBlockByHash(xhr){
	if (event.keyCode !== 13)
		return;
	xhr.onload = function() {
		var text = xhr.responseText;
		var obj = JSON.parse(text);
		let tr = "";
		var tbody = document.getElementById('place_for_block_by_hash');
		for (var key in obj) {
			if (key != "transactions") {
				tr += "<tr>" + "<td>" + key + "</td>" + "<td>" + obj[key] + "</td>" + "</tr>"
			} else {
				for (var j = 0; j < obj[key].length; j++)
					tr += "<tr>" + "<td>" + key + "</td>" + "<td>" + obj[key][j] + "</td>" + "</tr>"
			}
		}
		tbody.innerHTML += tr + "<br>";
	};
	try{
		xhr.send();
	}catch(err) {
	  document.getElementById("demo").innerHTML = err.message;
	}
}


function getChain(xhr){
	xhr.onload = function() {
		var text = xhr.responseText;
		var obj = JSON.parse(text);
		var tbody = document.getElementById('place_for_chain');
		for (var i = 0; i < Object.keys(obj).length; i++) {
			let tr = "";
			for (var key in obj[i]) {
				if (key != "transactions") {
					tr += "<tr>" + "<td>" + key + "</td>" + "<td>" + obj[i][key] + "</td>" + "</tr>"
				} else {
					for (var j = 0; j < obj[i][key].length; j++)
						tr += "<tr>" + "<td>" + key + "</td>" + "<td>" + obj[i][key][j] + "</td>" + "</tr>"
				}
			}
			tbody.innerHTML += tr + "<br>";
		}
	};
	try{
		xhr.send();
	}catch(err) {
	  document.getElementById("demo").innerHTML = err.message;
	}
}

