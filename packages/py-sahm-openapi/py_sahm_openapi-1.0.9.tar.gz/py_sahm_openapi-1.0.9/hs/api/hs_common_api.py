# -*- coding: utf-8 -*-
from hs.common.common_utils import get_info_logger
from hs.common.network_utils import NetworkUtil
from hs.common.quote_socket_client import QuoteSocketClient
from hs.common.token_client import TokenClient
from hs.common.trading_socket_client import TradingSocketClient

logging_name: str = __name__


class CommonAPI(object):
    """
    开箱即用的统一API（包含交易、行情、期货接口调用）
    交易、行情等操作接口在同一个程序时，建议用此API
    接入文档参考：https://quant-open.hstong.com/api-docs/
    """

    def __init__(self, rsa_public_key: str,
                 rsa_private_key: str,
                 login_domain: str,
                 login_country_code: str,
                 login_mobile: str,
                 login_passwd: str,
                 trading_passwd: str,
                 logging_filename: str = None):
        # 统一日志对象
        logger = get_info_logger(logging_name, filename=logging_filename)
        self._logging = logger
        # 登录区域和手机号
        self._login_country_code = login_country_code
        self._login_mobile = login_mobile
        # network util
        self._network_util = NetworkUtil(logger)
        self._device_no = self._network_util.get_mac_address()
        # Token client
        self._token_client = TokenClient(logger)
        self._token_client.set_token_client_data(rsa_public_key=rsa_public_key,
                                                 rsa_private_key=rsa_private_key,
                                                 login_domain=login_domain,
                                                 login_country_code=login_country_code,
                                                 login_mobile=login_mobile,
                                                 login_passwd=login_passwd,
                                                 device_no=self._device_no,
                                                 quote_stand_alone=False)
        # trading_client
        self._trading_socket_client = TradingSocketClient(rsa_public_key=rsa_public_key,
                                                          rsa_private_key=rsa_private_key,
                                                          login_domain=login_domain,
                                                          login_country_code=login_country_code,
                                                          login_mobile=login_mobile,
                                                          login_passwd=login_passwd,
                                                          trading_passwd=trading_passwd,
                                                          token_client=self._token_client,
                                                          device_no=self._device_no,
                                                          logger=logger)
        # quote_client
        self._quote_socket_client = QuoteSocketClient(rsa_public_key=rsa_public_key,
                                                      rsa_private_key=rsa_private_key,
                                                      login_domain=login_domain,
                                                      login_country_code=login_country_code,
                                                      login_mobile=login_mobile,
                                                      login_passwd=login_passwd,
                                                      trading_passwd=trading_passwd,
                                                      use_lv2=True,
                                                      token_client=self._token_client,
                                                      device_no=self._device_no,
                                                      logger=logger)

    def is_alive(self):
        """
        检查StockClient是否正常连接状态
        交易与行情的长连接都处于正常连接状态
        """
        return self._trading_socket_client.is_alive() and self._quote_socket_client.is_alive()

    def get_token(self):
        return self._token_client.get_token(self._login_country_code, self._login_mobile)

    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        # 启动交易Client
        t_host, t_port = self._trading_socket_client.get_server(p_token)
        if t_host is None or t_port is None:
            raise Exception('Got trade server info error, host/port is None.')
        self._trading_socket_client.restart(p_token, t_host, t_port)

        # 启动行情Client
        h_host, h_port = self._quote_socket_client.get_server(p_token)
        if h_host is None or h_port is None:
            raise Exception('Got hq server info error, host/port is None.')
        self._quote_socket_client.restart(p_token, h_host, h_port)

    def add_notify_callback(self, callback):
        """增加消息推送回调函数"""
        self._trading_socket_client.handle_notify_for_ever(callback)
        self._quote_socket_client.handle_notify_for_ever(callback)

    def stop(self):
        """退出业务API上下文环境，停止StockClient"""
        self._trading_socket_client.stop()
        self._quote_socket_client.stop()

    def get_login_code_mobile(self):
        return self._login_country_code + ":" + self._login_mobile

    def _get_token_from_cache(self):
        return self._token_client.get_token_from_cache(self._login_country_code, self._login_mobile)
