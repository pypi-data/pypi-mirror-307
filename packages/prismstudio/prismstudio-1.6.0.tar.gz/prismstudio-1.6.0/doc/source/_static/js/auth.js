import { check_access_token } from "./login_fn.js";
import { redirect_prefix } from "./config.js";

window.onload = async function () {
  const access_token = sessionStorage.getItem("access_token");
  if (access_token === null || access_token === "") {
    window.location.href = `${redirect_prefix}/index.html`;
  }

  await check_access_token(access_token);
  return false;
};
