var socket;

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
	    
	    $("#display tr").eq(2*i+1).find("td").eq(j).text(title);
	    $("#display tr").eq(2*i+2).find("td").eq(j).text(value).css("color", color);
	}
    }
}

function buttonClick() {
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
    $("a").click(buttonClick);
    socketReconnect();
});

$(document).keydown(function(dat) {
    var key;

    if (dat.keyCode >= 65 && dat.keyCode <= 90) {
	key = String.fromCharCode(dat.keyCode);
    }
    else if (dat.keyCode >= 97 && dat.keyCode <= 122) {
	key = String.fromCharCode(dat.keyCode-32);	
    }
    else if (dat.keyCode >= 47 && dat.keyCode <= 57) {
	key = String.fromCharCode(dat.keyCode);
    }
    else if (dat.keyCode == 8) {
	key = "DEL";
    }
    else if (dat.keyCode == 46) {
	key = "CLR";
    }
    else {
	return true;
    }

    socketSend(key);
    return false;
});
