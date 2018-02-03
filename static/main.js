console.log('loading main.js')

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
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

function save(saveValue) {
  console.log(saveValue);
  setCookie("saved",saveValue,400);
}

function load() {
  return getCookie("saved");
}

function gebi(str){
  return document.getElementById(str);
}

function hide_load(){
  loadingoverlay = gebi('overlay');
  loadinganim = gebi('loader');

  loadingoverlay.style.opacity = 1;
  loadinganim.style.visibility = 'hidden';

  gebi('win').style.visibility = 'visible';
}

console.log('main.js loaded');
