# -*- coding: utf-8 -*-
from hs.api.constant import ModelResult, StatusCode, SecurityParam, MktTmType, ExchangeType
from hs.common.common_utils import get_info_logger
from hs.common.network_utils import NetworkUtil
from hs.common.pb.common.constant.RequestMsgType_pb2 import QuoteSaudiBasicQotRequestMsgType, \
    QuoteUsBasicQotRequestMsgType, QuoteSaudiKLRequestMsgType, QuoteUsKLRequestMsgType, \
    QuoteSaudiOrderBookRequestMsgType, QuoteUsOrderBookRequestMsgType, \
    QuoteUsTickerRequestMsgType, QuoteSaudiTickerRequestMsgType, QuoteSaudiTimeShareRequestMsgType, \
    QuoteUsTimeShareRequestMsgType, QuoteUsOptionChainExpireDateRequestMsgType, QuoteUsOptionChainCodeRequestMsgType
from hs.common.pb.hq.dto.Security_pb2 import Security
from hs.common.pb.hq.request.BasicQotRequest_pb2 import BasicQotRequest
from hs.common.pb.hq.request.KLRequest_pb2 import KLRequest
from hs.common.pb.hq.request.OrderBookRequest_pb2 import OrderBookRequest
from hs.common.pb.hq.request.TickerRequest_pb2 import TickerRequest
from hs.common.pb.hq.request.TimeShareRequest_pb2 import TimeShareRequest
from hs.common.pb.hq.request.UsOptionChainCodeRequest_pb2 import UsOptionChainCodeRequest
from hs.common.pb.hq.request.UsOptionChainExpireDateRequest_pb2 import UsOptionChainExpireDateRequest
from hs.common.protobuf_utils import parse_payload, proto_to_dict
from hs.common.quote_socket_client import QuoteSocketClient
from hs.common.request_msg_type_enum import RequestMsgTypeEnum
from hs.common.token_client import TokenClient

logging_name: str = __name__


class QuoteAPI(object):
    """
    开箱即用的行情API
    行情独立程序，建议用此API
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
        # 订阅的最新基础行情数据对象
        self._basic_qot = None
        # token client
        self._token_client = TokenClient(logger)
        self._token_client.set_token_client_data(rsa_public_key=rsa_public_key,
                                                 rsa_private_key=rsa_private_key,
                                                 login_domain=login_domain,
                                                 login_country_code=login_country_code,
                                                 login_mobile=login_mobile,
                                                 login_passwd=login_passwd,
                                                 device_no=self._device_no,
                                                 quote_stand_alone=True)

        self._socket_client = QuoteSocketClient(rsa_public_key=rsa_public_key,
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
        """检查StockClient是否正常连接状态"""
        return self._socket_client.is_alive()

    def get_token(self):
        return self._token_client.get_token(self._login_country_code, self._login_mobile)

    def start(self, p_token):
        """Start the business API context and restart StockClient"""
        host, port = self._socket_client.get_server(p_token)
        if host is None or port is None:
            raise Exception('Got hq server info error, host/port is None.')
        self._socket_client.restart(p_token, host, port)

    def stop(self):
        """Exit the business API context and stop StockClient"""
        self._socket_client.stop()

    def get_login_code_mobile(self):
        return self._login_country_code + ":" + self._login_mobile

    def _get_token_from_cache(self):
        return self._token_client.get_token_from_cache(self._login_country_code, self._login_mobile)

    @staticmethod
    def pb_to_result(pb_response: object, payload_key: str = '') -> ModelResult:
        """
        Convert Protobuf Response To  ModelResult
        :param  pb_response protobuf format response
        :param  payload_key get payload data by key
        :return ModelResult result model
        """
        if not pb_response:
            return ModelResult.with_error(StatusCode.INVOKE_API_FAILED, StatusCode.INVOKE_API_FAILED_DESCRIPTION)

        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        payload = parse_payload(pb_response)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            payload_dict = proto_to_dict(payload)
            if payload_key and payload_key in payload_dict:
                model_result.with_model(payload_dict[payload_key])  # model type
            else:
                model_result.with_model(payload_dict)
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        else:
            model_result.with_error(StatusCode.INVOKE_TIME_OUT, StatusCode.INVOKE_TIME_OUT_DESCRIPTION)
        return model_result

    def query_hq_basic_qot(self, exchange_type: str, security_list: list) -> ModelResult:
        """
        Query basic stock quotes in batches
        :param exchange_type: exchange type ,possible value: 'S'-Saudi Stock, 'P'-US Stock see ExchangeType
        :param security_list list[SecurityParam] required stock information
        :return model_result model: basic quotes：[BasicQot]
        """
        pb_security_list = []
        for security_param in security_list:
            pb_security = Security()
            pb_security.dataType = security_param.data_type
            pb_security.stockCode = security_param.stock_code
            pb_security_list.append(pb_security)
        # build pb payload
        payload = BasicQotRequest()
        for pb_security in pb_security_list:
            payload.security.append(pb_security)

        # Determine request type
        if ExchangeType.S is exchange_type:
            request_type = QuoteSaudiBasicQotRequestMsgType
        elif ExchangeType.P is exchange_type:
            request_type = QuoteUsBasicQotRequestMsgType
        else:
            model_result = ModelResult(False, StatusCode.EXCHANGE_TYPE_NOT_SUPPORT,
                                       StatusCode.EXCHANGE_TYPE_NOT_SUPPORT_DESCRIPTION, "")
            return model_result

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=request_type,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        return QuoteAPI.pb_to_result(pb_response, 'basicQot')

    def query_saudi_hq_order_book(self, security_param: SecurityParam,
                                  order_book_type: str) -> ModelResult:
        """
        Query saudi stock order book
        :param security_param: stock info
        :param order_book_type Depth Arrangement see SaudiOrderBookType
        model_result: success, is_success=>true,  data=> order book info
        """
        # build pb payload
        payload = OrderBookRequest()
        payload.security.dataType = security_param.data_type
        payload.security.stockCode = security_param.stock_code

        if order_book_type:
            payload.saudiOrderBookType = order_book_type

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QuoteSaudiOrderBookRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        return QuoteAPI.pb_to_result(pb_response)

    def query_us_hq_order_book(self, security_param: SecurityParam, mkt_tm_type: int = MktTmType.MID_SESSION,
                               depth_book_type=None) -> ModelResult:
        """
        Query us stock order book
        :param security_param  stock info
        :param mkt_tm_type: trading period. US stocks: pre-market: -1, intra-market: 1, after-market: -2;
        :param depth_book_type Depth Arrangement see DepthBookType
        model_result: success, is_success=>true,  data=> order book info
        """
        # build pb payload
        payload = OrderBookRequest()
        payload.security.dataType = security_param.data_type
        payload.security.stockCode = security_param.stock_code
        payload.mktTmType = mkt_tm_type
        if depth_book_type is not None:
            payload.depthBookType = depth_book_type

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QuoteUsOrderBookRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        return QuoteAPI.pb_to_result(pb_response)

    def query_hq_ticker(self, exchange_type: str, security_param: SecurityParam, limit: int) -> ModelResult:
        """
        Query the recent ticker list
        :param exchange_type: exchange type ,possible value: 'S'-Saudi Stock, 'P'-US Stock
        :param security_param: stock info
        :param limit: The number of transactions returned, the actual number returned may not be so many, the maximum number returned is 1000
        :return model_result model: ticker info
        """
        if not exchange_type:
            model_result = ModelResult(False, StatusCode.EXCHANGE_TYPE_REQUIRED,
                                       StatusCode.EXCHANGE_TYPE_REQUIRED_DESCRIPTION, "")
            return model_result

        if ExchangeType.S is exchange_type:
            request_type = QuoteSaudiTickerRequestMsgType
        elif ExchangeType.P is exchange_type:
            request_type = QuoteUsTickerRequestMsgType
        else:
            model_result = ModelResult(False, StatusCode.EXCHANGE_TYPE_NOT_SUPPORT,
                                       StatusCode.EXCHANGE_TYPE_NOT_SUPPORT_DESCRIPTION, "")
            return model_result

        # build pb payload
        payload = TickerRequest()
        payload.security.dataType = security_param.data_type
        payload.security.stockCode = security_param.stock_code
        payload.limit = limit
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=request_type,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)

        return QuoteAPI.pb_to_result(pb_response)

    def query_hq_kline(self, exchange_type: str, security_param: SecurityParam,
                       start_date: str,
                       direction: int,
                       ex_right_flag: int,
                       cyc_type: int,
                       limit: int) -> ModelResult:
        """
        Query KL info
        :param exchange_type: exchange type ,possible value: 'S'-Saudi Stock, 'P'-US Stock
        :param security_param stock info
        :param start_date: start date format:yyyyMMdd
        :param direction: query direction see Direction
        :param ex_right_flag:restoration type see ExRightFlag
        :param cyc_type K line type see CycType
        :param limit Query the limit on the number of K lines
        :return model_result model: KL info
        """
        if not exchange_type:
            model_result = ModelResult(False, StatusCode.EXCHANGE_TYPE_REQUIRED,
                                       StatusCode.EXCHANGE_TYPE_REQUIRED_DESCRIPTION, "")
            return model_result

        if ExchangeType.S is exchange_type:
            request_type = QuoteSaudiKLRequestMsgType
        elif ExchangeType.P is exchange_type:
            request_type = QuoteUsKLRequestMsgType
        else:
            model_result = ModelResult(False, StatusCode.EXCHANGE_TYPE_NOT_SUPPORT,
                                       StatusCode.EXCHANGE_TYPE_NOT_SUPPORT_DESCRIPTION, "")
            return model_result

        # build pb payload
        payload = KLRequest()
        payload.security.dataType = security_param.data_type
        payload.security.stockCode = security_param.stock_code
        payload.startDate = int(start_date)
        payload.direction = direction
        payload.exRightFlag = ex_right_flag
        payload.cycType = cyc_type
        payload.limit = limit
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=request_type,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)

        return QuoteAPI.pb_to_result(pb_response)

    def query_hq_time_share(self, exchange_type: str, security_param: SecurityParam) -> ModelResult:
        """
        Query timeshare data
        :param exchange_type: exchange type ,possible value: 'S'-Saudi Stock, 'P'-US Stock
        :param security_param: stock info
        :return model_result model: timeshare info list
        """
        if not exchange_type:
            model_result = ModelResult(False, StatusCode.EXCHANGE_TYPE_REQUIRED,
                                       StatusCode.EXCHANGE_TYPE_REQUIRED_DESCRIPTION, "")
            return model_result

        if ExchangeType.S is exchange_type:
            request_type = QuoteSaudiTimeShareRequestMsgType
        elif ExchangeType.P is exchange_type:
            request_type = QuoteUsTimeShareRequestMsgType
        else:
            model_result = ModelResult(False, StatusCode.EXCHANGE_TYPE_NOT_SUPPORT,
                                       StatusCode.EXCHANGE_TYPE_NOT_SUPPORT_DESCRIPTION, "")
            return model_result

        # build pb payload
        payload = TimeShareRequest()
        payload.security.dataType = security_param.data_type
        payload.security.stockCode = security_param.stock_code
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=request_type,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)

        return QuoteAPI.pb_to_result(pb_response)

    def query_us_option_expire_date_list(self, stock_code: str) -> ModelResult:
        """
        Query us option chain expiration date list by stock code
        :param stock_code:stock code
        :return model_result model: option expire date list
        """
        # build pb payload
        payload = UsOptionChainExpireDateRequest()
        payload.securityCode = stock_code

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=QuoteUsOptionChainExpireDateRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    token=self._get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)

        return QuoteAPI.pb_to_result(pb_response, 'expireDate')

    def query_us_option_code_list(self, stock_code: str, expire_date: str, flag_in_out: int,
                                  option_type: str) -> ModelResult:
        """
        Query us option chain code list by option expiration date
        :param stock_code: stock code
        :param expire_date: expire date format->yyyy/MM/dd
        :param flag_in_out: price type see OptionPriceFlag
        :param option_type: option type see OptionType
        :return model_result model: option code list
        """
        # build pb payload
        payload = UsOptionChainCodeRequest()
        payload.securityCode = stock_code
        payload.expireDate = expire_date
        payload.flagInOut = flag_in_out
        payload.optionType = option_type
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QuoteUsOptionChainCodeRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)

        return QuoteAPI.pb_to_result(pb_response, 'optionCode')

    def hq_subscribe(self, topic_id: int, security_list: list) -> ModelResult:
        """
        订阅行情推送
        :param topic_id 订阅/取消订阅行情推送的TopicId 参考常量类：HQSubscribeTopicId
        :param security_list list[SecurityParam] 必填 股票信息，可批量
        :return model_result model: 是否订阅成功 true-是 false-否
        """
        with self._socket_client:
            return self._socket_client.hq_subscribe(topic_id=topic_id, security_list=security_list)

    def hq_unsubscribe(self, topic_id: int, security_list: list) -> ModelResult:
        """
        取消订阅行情推送
        :param topic_id 订阅/取消订阅行情推送的TopicId 参考常量类：HQSubscribeTopicId
        :param security_list list[SecurityParam] 必填 股票信息，可批量
        :return model_result model: 是否取消订阅成功 true-是 false-否
        """
        with self._socket_client:
            return self._socket_client.hq_unsubscribe(topic_id=topic_id, security_list=security_list)

    def add_notify_callback(self, callback):
        """
        增加消息推送回调函数
        """
        self._socket_client.handle_notify_for_ever(callback)
