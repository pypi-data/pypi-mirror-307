import { redirect_prefix } from "./config.js";

function logout() {
  sessionStorage.removeItem("access_token");
  sessionStorage.removeItem("username");
  document.cookie = `doc_refresh_token=; max-age=0; path=/;`;
  document.cookie = `refresh_token=; max-age=0; path=/;`;
  window.location.href = `${redirect_prefix}/index.html`;
}

const logoutBtn = document.querySelector(".logout-btn");
logoutBtn.addEventListener("click", logout);
