import { url, redirect_prefix } from "./config.js";

async function check_access_token(access_token) {
  if (!access_token) {
    return false;
  }

  const headers = new Headers();
  headers.append("Authorization", `Bearer ${access_token}`);

  try {
    const response = await fetch(`${url}/auth/doc_access`, {
      method: "GET",
      headers: headers,
    });

    // try refreshing token
    if (response.status !== 200) {
      await validate_refresh_token();
    }

    const data = await response.json();
    return data.rescontent?.status === "success";
  } catch (err) {
    clear_session_storage();
    return false;
  }
}

async function check_web_token(webToken) {
  if (!webToken) {
    return false;
  }

  const queryParams = new URLSearchParams();
  queryParams.append("token", webToken);

  try {
    const response = await fetch(
      `${url}/auth/doc_web?${queryParams.toString()}`,
      {
        method: "GET",
        credentials: "include",
      }
    );

    if (response.status != 200) {
      clear_session_storage();
      return false;
    }

    const { access_token, username } = await response.json();
    set_session_storage(access_token, username);

    return true;
  } catch (err) {
    clear_session_storage();
    return false;
  }
}

async function validate_refresh_token() {
  try {
    const response = await fetch(`${url}/doc_refresh_token`, {
      method: "POST",
      credentials: "include",
    });

    if (response.status != 200) {
      clear_session_storage();
      clear_cookie("doc_refresh_token");
      clear_cookie("refresh_token");
      redirect_to_login_page();
      return false;
    }

    const { access_token, username } = await response.json();
    set_session_storage(access_token, username);

    return true;
  } catch (err) {
    clear_session_storage();
    return false;
  }
}

function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const passwordHash = CryptoJS.SHA512(password).toString(CryptoJS.enc.Hex);

  const formdata = new FormData();
  formdata.append("username", username);
  formdata.append("password", passwordHash);

  fetch(`${url}/auth/doc_login`, {
    method: "POST",
    credentials: "include",
    body: formdata,
  })
    .then((res) => {
      if (res.status != 200) {
        const errbox = document.getElementById("error-box");
        errbox.style.display = "inline";
      } else {
        res.json().then(({ access_token, username }) => {
          set_session_storage(access_token, username);
          window.location.href = `${redirect_prefix}/root_page.html`;
        });
      }
    })
    .catch(() => {
      const errbox = document.getElementById("error-box");
      errbox.style.display = "inline";
    });
}

function set_session_storage(access_token, username) {
  sessionStorage.setItem("access_token", access_token);
  sessionStorage.setItem("username", username);
}

function clear_session_storage() {
  sessionStorage.removeItem("access_token");
  sessionStorage.removeItem("username");
}

function clear_cookie(name) {
  // set the cookie's max-age to 0
  document.cookie = `${name}=; max-age=0; path=/;`;
}

function redirect_to_login_page() {
  window.location.replace(`${redirect_prefix}/index.html`);
}

function redirect_to_sphinx_page() {
  window.location.href = `${redirect_prefix}/root_page.html`;
}

export {
  login,
  check_access_token,
  validate_refresh_token,
  check_web_token,
  redirect_to_login_page,
  redirect_to_sphinx_page,
};
