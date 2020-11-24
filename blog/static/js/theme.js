function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function changeTheme() {
	element = document.getElementById("body");
	button = document.getElementById("themebtn");
  menubtn = document.getElementById("openbtn");
	if (element.className == "light") {
		element.className = "dark";
		button.className =  "themebtn sun";
    menubtn.className =  "openbtn light";
		setCookie("theme", "dark", 30);
	} else {
		element.className = "light";
		button.className =  "themebtn moon";
    menubtn.className =  "openbtn dark";
		setCookie("theme", "light", 30);
	}
}

function changeMenuState(state) {
  if(state == false)
    document.getElementById("menu").style.left = "-100%";
  else
    document.getElementById("menu").style.left = "0";
}