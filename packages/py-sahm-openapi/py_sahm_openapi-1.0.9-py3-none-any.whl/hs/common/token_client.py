# -*- coding:utf-8 -*-
import base64
import datetime
import json
import ssl
import urllib
import urllib.request as request
from logging import Logger

from hs.api.constant import ServerKey
from hs.common import rsa_utils

TOKEN_CACHE_TIME: int = 900  # token缓存时间15分钟
TOKEN_CACHE_DATA = dict()

# cache key 
CACHE_KEY_RSA_PUBLIC_KEY = 'rsa_public_key'
CACHE_KEY_RSA_PRIVATE_KEY = 'rsa_private_key'
CACHE_KEY_LOGIN_DOMAIN = 'login_domain'
CACHE_KEY_LOGIN_COUNTRY_CODE = 'login_country_code'
CACHE_KEY_LOGIN_MOBILE = 'login_mobile'
CACHE_KEY_LOGIN_PASSWD = 'login_passwd'
CACHE_KEY_DEVICE_NO = 'device_no'
CACHE_KEY_QUOTE_STAND_ALONE = 'quote_stand_alone'
CACHE_KEY_TOKEN = 'token'
CACHE_KEY_TIME = 'time'


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@singleton
class TokenClient(object):
    """
    Token管理类
    """

    def __init__(self, logger: Logger):
        self._logging = logger
    
    def _get_cache_data(self, login_country_code, login_mobile):
        cache_data_key = login_country_code + "_" + login_mobile
        if cache_data_key not in TOKEN_CACHE_DATA:
            return None

        cache_data = TOKEN_CACHE_DATA[cache_data_key]
        return cache_data
    
    def set_token_client_data(self, rsa_public_key: str,
                              rsa_private_key: str,
                              login_domain: str,
                              login_country_code: str,
                              login_mobile: str,
                              login_passwd: str,
                              device_no: str,
                              quote_stand_alone: bool):
        cache_data_key = login_country_code + "_" + login_mobile
        if cache_data_key in TOKEN_CACHE_DATA:
            return
        
        _rsa_private_key = rsa_private_key
        if not rsa_private_key.startswith('-----'):
            _rsa_private_key = "-----BEGIN RSA PRIVATE KEY-----\n" + rsa_private_key + "\n-----END RSA PRIVATE KEY-----"

        cache_data = dict()
        cache_data[CACHE_KEY_RSA_PUBLIC_KEY] = rsa_public_key
        cache_data[CACHE_KEY_RSA_PRIVATE_KEY] = _rsa_private_key
        cache_data[CACHE_KEY_LOGIN_DOMAIN] = login_domain
        cache_data[CACHE_KEY_LOGIN_COUNTRY_CODE] = login_country_code
        cache_data[CACHE_KEY_LOGIN_MOBILE] = login_mobile
        cache_data[CACHE_KEY_LOGIN_PASSWD] = login_passwd
        cache_data[CACHE_KEY_DEVICE_NO] = device_no
        cache_data[CACHE_KEY_QUOTE_STAND_ALONE] = quote_stand_alone  # 行情作为独立程序
        cache_data[CACHE_KEY_TOKEN] = None
        cache_data[CACHE_KEY_TIME] = datetime.datetime.now()
        TOKEN_CACHE_DATA[cache_data_key] = cache_data

    def get_token(self, login_country_code, login_mobile):
        """
        start firstly and get platform token
        
        Returns
        -------
        """
        cache_data = self._get_cache_data(login_country_code, login_mobile)
        if cache_data is None:
            return 
        
        # get http login token
        token, _ = self._get_token(
            url=cache_data[CACHE_KEY_LOGIN_DOMAIN] + "/hs/login",
            country_code=login_country_code,
            mobile=login_mobile,
            passwd=cache_data[CACHE_KEY_LOGIN_PASSWD])

        if token is None:
            raise Exception('Got login token error, token is None.')

        cache_data[CACHE_KEY_TOKEN] = token
        cache_data[CACHE_KEY_TIME] = datetime.datetime.now()  # 缓存时间
        self._logging.info(f"Token client http login and set token cache and return.")
        return token

    def reconnect_get_token(self, server_key, login_country_code, login_mobile):
        """
        重连获取平台登录Token
        Parameters
        ----------
        server_key
        login_country_code
        login_mobile
        Returns
        -------
        """
        cache_data = self._get_cache_data(login_country_code, login_mobile)
        if cache_data is None:
            return 

        cache_token = cache_data[CACHE_KEY_TOKEN]
        if server_key == ServerKey.HQ_SERVER_KEY \
                and not cache_data[CACHE_KEY_QUOTE_STAND_ALONE] \
                and cache_token is not None:
            self._logging.info(f"Quote client get token cache and return.")
            return cache_token

        if cache_token is not None:  # 校验时间
            start = cache_data[CACHE_KEY_TIME] 
            now = datetime.datetime.now()
            seconds = (now - start).seconds
            if seconds < TOKEN_CACHE_TIME:  # 未过期
                self._logging.info(f"Token client get token from cache and return, interval: {seconds}s")
                return cache_token

        try:
            token = self.get_token(login_country_code, login_mobile)

            if token is not None:
                cache_data[CACHE_KEY_TOKEN] = token
                cache_data[CACHE_KEY_TIME] = datetime.datetime.now()
                self._logging.info(f"Token client reconnect update token cache, date time: {datetime.datetime.now()}")
            return token
        except Exception as e:
            self._logging.error(f"Token client get token exception, please try again later. {e}")

    def get_token_from_cache(self, login_country_code, login_mobile):
        cache_data = self._get_cache_data(login_country_code, login_mobile)
        if cache_data is None:
            return 
        return cache_data[CACHE_KEY_TOKEN]

    def _get_token(self, url: str, country_code: str, mobile: str, passwd: str):
        cache_data = self._get_cache_data(country_code, mobile)
        if cache_data is None:
            return None, None
        rsa_public_key = cache_data[CACHE_KEY_RSA_PUBLIC_KEY]
        device_no = cache_data[CACHE_KEY_DEVICE_NO]
        rsa_private_key = cache_data[CACHE_KEY_RSA_PRIVATE_KEY]
        for i in range(1):  # 错误重试3次
            try:
                passwd = rsa_utils.encrypt_data(passwd, rsa_public_key)
                passwd = base64.b64encode(passwd).decode("utf-8")
                data = {
                    "countryCode": country_code,
                    "mobile": mobile,
                    "deviceNo": device_no,
                    "password": passwd,
                }
                headers = {'Content-Disposition': 'form-data', 'Accept-Charset': 'utf-8',
                           'Content-Type': 'application/x-www-form-urlencoded'}
                data = urllib.parse.urlencode(data).encode("utf-8")
                req = request.Request(url=url, data=data, headers=headers, method='POST')
                with request.urlopen(req, context=ssl._create_unverified_context()) as resp:
                    response = resp.read()
                response = json.loads(rsa_utils.bytes_to_str(response))
                if response.get("respCode") != 0:
                    self._logging.error(f"HTTP Login fail response：{response}")
                    return None, None
                token = response.get("data").get("token")
                decrypt_token = rsa_utils.decrypt_data(token, rsa_private_key)
                decrypt_token_str = rsa_utils.bytes_to_str(decrypt_token)
                self._logging.info(f"Got Token：{decrypt_token_str}")
                return decrypt_token_str, response
            except Exception as e:
                self._logging.error(f"Got token error：{e}")
        return None, None
