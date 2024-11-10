import base64
import datetime
import hashlib
import json
import random
import string
import time
import urllib
import requests
import re

from bs4 import BeautifulSoup
from . import exceptions
from . import constants

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_random_string_hex(length):
    return ''.join(random.choice(string.hexdigits) for _ in range(length))


def check_response(response, function_description, expected_status):
    if response.status_code != expected_status:
        raise exceptions.ResponseError(
            f"({function_description}: Expected status code {expected_status}, received: {response.status_code}: " +
            f"{response.text}"
        )


def get_querystring_parameter_from_header_entry_url(response, header_entry, querystring_parameter):
    header_entry_value = response.headers[header_entry]
    parsed_url = urllib.parse.urlparse(header_entry_value)
    params = urllib.parse.parse_qs(parsed_url.query)
    return params.get(querystring_parameter, [None])[0]


class Authentication():
    # token:
    # - access_token
    # - refresh_token
    # - id_token
    # - unix_timestamp_token_received
    # - expires_in_sec
    # - acc_client_id
    # - scope

    def __init__(self, username, password, token, raw=False):
        self._username = username
        self._password = password
        self._token = token
        self._raw = raw
        self._app_version = constants.X_APP_VERSION
        self._update_app_version()

    def _check_token_is_valid(self):
        if self._token is not None:
            now = datetime.datetime.now()
            now_unix = time.mktime(now.timetuple())

            # multiple parts in access_token which are separated by .
            part_of_token_b64 = str(self._token["access_token"].split(".")[1])
            # as seen here: https://stackoverflow.com/questions/3302946/how-to-decode-base64-url-in-python
            part_of_token = base64.urlsafe_b64decode(
                part_of_token_b64 + '=' * (4 - len(part_of_token_b64) % 4))
            token_info_json = json.loads(part_of_token)

            expiry_in_token = token_info_json["exp"]

            if (now_unix > expiry_in_token) or \
                    (now_unix > self._token["unix_timestamp_token_received"] + self._token["expires_in_sec"]):

                if self._raw:
                    print("--- Token is expired")
                return False

            if self._raw:
                print("--- Token is valid")
            return True
        else:
            if self._raw:
                print("--- Token is invalid")
            return False

    def _get_api_key(self, timestamp: datetime.datetime, token: string):
        try:
            date = datetime.datetime(
                timestamp.year, timestamp.month, timestamp.day,
                timestamp.hour, timestamp.minute, timestamp.second,
                0, datetime.timezone.utc
            )
            timestamp_ms = str(int(date.timestamp() * 1000))
            
            components = [
                'Comfort Cloud'.encode('utf-8'),
                '521325fb2dd486bf4831b47644317fca'.encode('utf-8'),
                timestamp_ms.encode('utf-8'),
                'Bearer '.encode('utf-8'),
                token.encode('utf-8')
            ]

            input_buffer = b''.join(components)
            hash_obj = hashlib.sha256()
            hash_obj.update(input_buffer)
            hash_str = hash_obj.hexdigest()

            result = hash_str[:9] + 'cfc' + hash_str[9:]
            return result
        except Exception as ex:
            raise exceptions.ResponseError(
                f"(CFC: Failed to generate API key: " +
                f"{ex}"
            )

    def _get_new_token(self):
        requests_session = requests.Session()

        # generate initial state and code_challenge
        state = generate_random_string(20)
        code_verifier = generate_random_string(43)

        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(
                code_verifier.encode('utf-8')
            ).digest()).split('='.encode('utf-8'))[0].decode('utf-8')

        # --------------------------------------------------------------------
        # AUTHORIZE
        # --------------------------------------------------------------------

        response = requests_session.get(
            f'{constants.BASE_PATH_AUTH}/authorize',
            headers={
                "user-agent": "okhttp/4.10.0",
            },
            params={
                "scope": "openid offline_access comfortcloud.control a2w.control",
                "audience": f"https://digital.panasonic.com/{constants.APP_CLIENT_ID}/api/v1/",
                "protocol": "oauth2",
                "response_type": "code",
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
                "auth0Client": constants.AUTH_0_CLIENT,
                "client_id": constants.APP_CLIENT_ID,
                "redirect_uri": constants.REDIRECT_URI,
                "state": state,
            },
            allow_redirects=False)
        check_response(response, 'authorize', 302)

        # -------------------------------------------------------------------
        # FOLLOW REDIRECT
        # -------------------------------------------------------------------

        location = response.headers['Location']
        state = get_querystring_parameter_from_header_entry_url(
            response, 'Location', 'state')

        if not location.startswith(constants.REDIRECT_URI):
            response = requests_session.get(
                f"{constants.BASE_PATH_AUTH}/{location}",
                allow_redirects=False)
            check_response(response, 'authorize_redirect', 200)

            # get the "_csrf" cookie
            csrf = response.cookies['_csrf']

            # -------------------------------------------------------------------
            # LOGIN
            # -------------------------------------------------------------------

            response = requests_session.post(
                f'{constants.BASE_PATH_AUTH}/usernamepassword/login',
                headers={
                    "Auth0-Client": constants.AUTH_0_CLIENT,
                    "user-agent": "okhttp/4.10.0",
                },
                json={
                    "client_id": constants.APP_CLIENT_ID,
                    "redirect_uri": constants.REDIRECT_URI,
                    "tenant": "pdpauthglb-a1",
                    "response_type": "code",
                    "scope": "openid offline_access comfortcloud.control a2w.control",
                    "audience": f"https://digital.panasonic.com/{constants.APP_CLIENT_ID}/api/v1/",
                    "_csrf": csrf,
                    "state": state,
                    "_intstate": "deprecated",
                    "username": self._username,
                    "password": self._password,
                    "lang": "en",
                    "connection": "PanasonicID-Authentication"
                },
                allow_redirects=False)
            check_response(response, 'login', 200)

            # -------------------------------------------------------------------
            # CALLBACK
            # -------------------------------------------------------------------

            # get wa, wresult, wctx from body
            soup = BeautifulSoup(response.content, "html.parser")
            input_lines = soup.find_all("input", {"type": "hidden"})
            parameters = dict()
            for input_line in input_lines:
                parameters[input_line.get("name")] = input_line.get("value")

            user_agent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
            user_agent += "(KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36"

            response = requests_session.post(
                url=f"{constants.BASE_PATH_AUTH}/login/callback",
                data=parameters,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": user_agent,
                },
                allow_redirects=False)
            check_response(response, 'login_callback', 302)

            # ------------------------------------------------------------------
            # FOLLOW REDIRECT
            # ------------------------------------------------------------------

            location = response.headers['Location']

            response = requests_session.get(
                f"{constants.BASE_PATH_AUTH}/{location}",
                allow_redirects=False)
            check_response(response, 'login_redirect', 302)

        # ------------------------------------------------------------------
        # GET TOKEN
        # ------------------------------------------------------------------

        code = get_querystring_parameter_from_header_entry_url(
            response, 'Location', 'code')

        # do before, so that timestamp is older rather than newer
        now = datetime.datetime.now()
        unix_time_token_received = time.mktime(now.timetuple())

        response = requests_session.post(
            f'{constants.BASE_PATH_AUTH}/oauth/token',
            headers={
                "Auth0-Client": constants.AUTH_0_CLIENT,
                "user-agent": "okhttp/4.10.0",
            },
            json={
                "scope": "openid",
                "client_id": constants.APP_CLIENT_ID,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": constants.REDIRECT_URI,
                "code_verifier": code_verifier
            },
            allow_redirects=False)
        check_response(response, 'get_token', 200)

        token_response = json.loads(response.text)

        # ------------------------------------------------------------------
        # RETRIEVE ACC_CLIENT_ID
        # ------------------------------------------------------------------
        now = datetime.datetime.now()
        response = requests.post(
            f'{constants.BASE_PATH_ACC}/auth/v2/login',
            headers={
                "Content-Type": "application/json;charset=utf-8",
                "User-Agent": "G-RAC",
                "x-app-name": "Comfort Cloud",
                "x-app-timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "x-app-type": "1",
                "x-app-version": self._app_version,
                "x-cfc-api-key": self._get_api_key(now, token_response["access_token"]),
                "x-user-authorization-v2": "Bearer " + token_response["access_token"]
            },
            json={
                "language": 0
            })
        check_response(response, 'get_acc_client_id', 200)

        json_body = json.loads(response.text)
        acc_client_id = json_body["clientId"]

        self._token = {
            "access_token": token_response["access_token"],
            "refresh_token": token_response["refresh_token"],
            "id_token": token_response["id_token"],
            "unix_timestamp_token_received": unix_time_token_received,
            "expires_in_sec": token_response["expires_in"],
            "acc_client_id": acc_client_id,
            "scope": token_response["scope"]
        }

    def get_token(self):
        return self._token

    def set_token(self, token):
        self._token = token

    def is_token_valid(self):
        return self._check_token_is_valid()

    def login(self):
        if self._token is not None:
            if not self._check_token_is_valid():
                self._refresh_token()
                return "Refreshing"
        else:
            self._get_new_token()
            return "Authenticating"

        return "Valid"

    def logout(self):
        response = requests.post(
            f"{constants.BASE_PATH_ACC}/auth/v2/logout",
            headers=self._get_header_for_api_calls()
        )
        check_response(response, "logout", 200)
        if json.loads(response.text)["result"] != 0:
            # issue during logout, but do we really care?
            pass

    def _refresh_token(self):
        # do before, so that timestamp is older rather than newer
        now = datetime.datetime.now()
        unix_time_token_received = time.mktime(now.timetuple())

        response = requests.post(
            f'{constants.BASE_PATH_AUTH}/oauth/token',
            headers={
                "Auth0-Client": constants.AUTH_0_CLIENT,
                "user-agent": "okhttp/4.10.0",
            },
            json={
                "scope": self._token["scope"],
                "client_id": constants.APP_CLIENT_ID,
                "refresh_token": self._token["refresh_token"],
                "grant_type": "refresh_token"
            },
            allow_redirects=False)

        if response.status_code != 200:
            self._get_new_token()
            return

        token_response = json.loads(response.text)

        self._token = {
            "access_token": token_response["access_token"],
            "refresh_token": token_response["refresh_token"],
            "id_token": token_response["id_token"],
            "unix_timestamp_token_received": unix_time_token_received,
            "expires_in_sec": token_response["expires_in"],
            "acc_client_id": self._token["acc_client_id"],
            "scope": token_response["scope"]
        }

    def _get_header_for_api_calls(self, no_client_id=False):
        now = datetime.datetime.now()
        return {
            "Content-Type": "application/json;charset=utf-8",
            "x-app-name": "Comfort Cloud",
            "user-agent": "G-RAC",
            "x-app-timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "x-app-type": "1",
            "x-app-version": self._app_version,
            "x-cfc-api-key": self._get_api_key(now, self._token["access_token"]),
            "x-client-id": self._token["acc_client_id"],
            "x-user-authorization-v2": "Bearer " + self._token["access_token"]
        }

    def _get_user_info(self):
        response = requests.get(
            f'{constants.BASE_PATH_AUTH}/userinfo',
            headers={
                "Auth0-Client": self.AUTH_0_CLIENT,
                "Authorization": "Bearer " + self._token["access_token"]
            })
        check_response(response, 'userinfo', 200)

    def execute_post(self,
                     url,
                     json_data,
                     function_description,
                     expected_status_code):
        self._ensure_valid_token()

        try:
            response = requests.post(
                url,
                json=json_data,
                headers=self._get_header_for_api_calls()
            )
        except requests.exceptions.RequestException as ex:
            raise exceptions.RequestError(ex)

        self._print_response_if_raw_is_set(response, function_description)
        check_response(response, function_description, expected_status_code)
        return json.loads(response.text)

    def execute_get(self, url, function_description, expected_status_code):
        self._ensure_valid_token()

        try:
            response = requests.get(
                url,
                headers=self._get_header_for_api_calls()
            )
        except requests.exceptions.RequestException as ex:
            raise exceptions.RequestError(ex)

        self._print_response_if_raw_is_set(response, function_description)
        check_response(response, function_description, expected_status_code)
        return json.loads(response.text)

    def _print_response_if_raw_is_set(self, response, function_description):
        if self._raw:
            print("=" * 79)
            print(f"Response: {function_description}")
            print("=" * 79)
            print(f"Status: {response.status_code}")
            print("-" * 79)
            print("Headers:")
            for header in response.headers:
                print(f'{header}: {response.headers[header]}')
            print("-" * 79)
            print("Response body:")
            print(response.text)
            print("-" * 79)

    def _ensure_valid_token(self):
        if self._check_token_is_valid():
            return
        self._refresh_token()

    def _update_app_version(self):
        if self._raw:
            print("--- auto detecting latest app version")
        try:
            response = requests.get("https://play.google.com/store/apps/details?id=com.panasonic.ACCsmart")
            responseText = response.content.decode("utf-8")
            version_match = re.search(r'\[\"(\d+\.\d+\.\d+)\"\]', responseText)
            if version_match:
                version = version_match.group(1)
                self._app_version = version
                if self._raw:
                    print("--- found version: {}".format(self._app_version))
                return
            else:
                self._app_version = constants.X_APP_VERSION
                if self._raw:
                    print("--- error finding version")
                return

        except Exception:
            self._app_version = constants.X_APP_VERSION
            if self._raw:
                print("--- failed to detect app version using version default")
            pass

