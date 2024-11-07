import requests

from ..._common.config import URL_ADMIN
from ..._utils import _validate_args, post, _authentication, _process_response


@_validate_args
def register_user(
    username: str,
    password: str
):
    body = {
        'username': username,
        'password': password
    }
    return post(URL_ADMIN + '/user', None, body)


@_validate_args
def delete_user(username: str):
    headers = _authentication()
    # Confirm the username with the user
    confirm_username = input(f"To confirm deletion, please type the username '{username}': ").strip()
    if confirm_username != username:
        print("Username confirmation failed. Aborting deletion.")
        return
    res = requests.patch(url=URL_ADMIN + f'/{username}', headers=headers)
    return _process_response(res)
