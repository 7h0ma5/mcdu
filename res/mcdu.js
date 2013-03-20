var socket;

function clickSound() {
    $("#click-sound")[0].play();
}

function socketReconnect() {
    $("#status").css("background-color", "orange");

    var loc = window.location;
    socket = new WebSocket("ws://" + loc.host + "/socket");
    socket.onopen = socketOpen;
    socket.onclose = socketClose;
    socket.onmessage = socketMsg;
}

function socketOpen() {
    $("#status").css("background-color", "green");
}

function socketClose() {
    $("#status").css("background-color", "red");
    setTimeout(socketReconnect, 500);
}

function socketSend(msg) {
    socket.send(msg);
}

function socketMsg(evt) {
    var data = JSON.parse(evt.data);

    if (!(typeof data.title === "undefined")) {
	$("#title").text(data.title);
    }

    if (!(typeof data.scratch === "undefined")) {
	$("#scratch").text(data.scratch);
    }
    
    if (!data.fields) return;

    for (var i = 0; i < data.fields.length; i++) {
	var fields = data.fields[i];
	
	for (var j = 0; j < 2; j++) {
	    var title = "";
	    var value = "";
	    var color = "#ffffff";

	    if (fields[j]) {
		title = fields[j]["title"];
		value = fields[j]["value"];
		color = fields[j]["color"];
	    }
	    
	    $("#display tr").eq(2*i+1).find("span").eq(j).text(title);
	    $("#display tr").eq(2*i+2).find("span").eq(j).text(value).css("color", color);
	}
    }
}

function buttonClick(evt) {
    clickSound();

    evt.stopPropagation();
    evt.preventDefault();

    var id = $(this).attr("id");
    
    if (id.substring(0, 3) == "NUM") {
	id = id.substring(3, 4);
    }
    else if (id == "DOT") {
	id = ".";
    }
    else if (id == "SP") {
	id = " ";
    }
    else if (id == "SLASH") {
	id = "/";
    }
    else if (id == "PLUSMINUS") {
	id = "-";
    }
    
    socketSend(id);
}

$(document).ready(function() {
    $("a").on("click", buttonClick);
    socketReconnect();
});

$(document).keydown(function(evt) {
    var key;

    if (evt.keyCode >= 65 && evt.keyCode <= 90) {
	key = String.fromCharCode(evt.keyCode);
    }
    else if (evt.keyCode >= 97 && evt.keyCode <= 122) {
	key = String.fromCharCode(evt.keyCode-32);	
    }
    else if (evt.keyCode >= 47 && evt.keyCode <= 57) {
	key = String.fromCharCode(evt.keyCode);
    }
    else if (evt.keyCode == 8) {
	key = "DEL";
    }
    else if (evt.keyCode == 46) {
	key = "CLR";
    }
    else {
	return true;
    }

    evt.preventDefault();
    socketSend(key);
    return false;
});
