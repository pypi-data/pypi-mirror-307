import {
  login,
  check_access_token,
  check_web_token,
  redirect_to_sphinx_page,
} from "./login_fn.js";

window.onload = async function () {
  const webToken = get_token_from_querystring();
  if (webToken !== null) {
    if (await check_web_token(webToken)) {
      redirect_to_sphinx_page();
    }
    return;
  }

  const access_token = sessionStorage.getItem("access_token");
  if (access_token !== null) {
    if (await check_access_token(access_token)) {
      redirect_to_sphinx_page();
    }
    return;
  }

  setup_login();
};


function setup_login() {
  const pwElement = document.getElementById("pwtg");
  pwElement.onclick = toggle_pw;

  const loginElement = document.getElementById("login_fn");
  loginElement.onclick = login;

  const passwordElement = document.getElementById("password");
  passwordElement.onkeyup = enter_key;
}

function enter_key() {
  if (window.event.keyCode == 13) {
    login()
  }
}

function toggle_pw() {
  const pwElement = document.getElementById("password");
  const tgimgElement = document.getElementById("tgimg");

  if (pwElement.type === "text") {
    pwElement.type = "password";
    tgimgElement.src = "_static/toggle.svg";
  } else {
    pwElement.type = "text";
    tgimgElement.src = "_static/toggle_false.svg";
  }
}

function get_token_from_querystring() {
  // get token from current URL
  const currentUrl = window.location.href;
  const urlSearchParams = new URLSearchParams(currentUrl.split("?")[1]);
  const token = urlSearchParams.get("token");

  // clear url
  const newUrl = currentUrl.replace(`token=${token}`, "");
  history.replaceState(null, null, newUrl);

  return token;
}
