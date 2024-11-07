# -*- coding: utf-8 -*-
import threading

from hs.api.constant import ClientType, ModelResult, StatusCode, EntrustType, SessionType, TradeSubscribeTopicId, \
    TradeSubscribeFlag
from hs.common.common_utils import get_info_logger
from hs.common.network_utils import NetworkUtil
from hs.common.pb.common.constant.RequestMsgType_pb2 import (QueryPortfolioListRequestMsgType,
                                                             QueryFundInfoRequestMsgType,
                                                             QueryPositionListRequestMsgType,
                                                             QueryMaxBuyingPowerRequestMsgType,
                                                             PlaceOrderRequestMsgType, ModifyOrderRequestMsgType,
                                                             CancelOrderRequestMsgType,
                                                             TransactionPushSubscribeRequestMsgType,
                                                             QueryTodayOrderListRequestMsgType,
                                                             QueryHistoryOrderListRequestMsgType,
                                                             QueryCashStatementListRequestMsgType,
                                                             QueryOrderDetailRequestMsgType)
from hs.common.pb.trade.request.CancelOrderRequest_pb2 import CancelOrderRequest
from hs.common.pb.trade.request.ModifyOrderRequest_pb2 import ModifyOrderRequest
from hs.common.pb.trade.request.PlaceOrderRequest_pb2 import PlaceOrderRequest
from hs.common.pb.trade.request.QueryCashStatementListRequest_pb2 import QueryCashStatementListRequest
from hs.common.pb.trade.request.QueryFundInfoRequest_pb2 import QueryFundInfoRequest
from hs.common.pb.trade.request.QueryHistoryOrderListRequest_pb2 import QueryHistoryOrderListRequest
from hs.common.pb.trade.request.QueryMaxBuyingPowerRequest_pb2 import QueryMaxBuyingPowerRequest
from hs.common.pb.trade.request.QueryOrderDetailRequest_pb2 import QueryOrderDetailRequest
from hs.common.pb.trade.request.QueryPortfolioListRequest_pb2 import QueryPortfolioListRequest
from hs.common.pb.trade.request.QueryPositionListRequest_pb2 import QueryPositionListRequest
from hs.common.pb.trade.request.QueryTodayOrderListRequest_pb2 import QueryTodayOrderListRequest
from hs.common.pb.trade.request.TransactionPushSubscribeRequest_pb2 import TransactionPushSubscribeRequest
from hs.common.protobuf_utils import parse_payload, proto_to_dict
from hs.common.request_msg_type_enum import RequestMsgTypeEnum
from hs.common.token_client import TokenClient
from hs.common.trading_socket_client import TradingSocketClient

logging_name: str = __name__


class TradingAPI(object):
    """
    开箱即用的交易API
    交易独立程序，建议用此API
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
        # token client
        self._token_client = TokenClient(logger)
        self._token_client.set_token_client_data(rsa_public_key=rsa_public_key,
                                                 rsa_private_key=rsa_private_key,
                                                 login_domain=login_domain,
                                                 login_country_code=login_country_code,
                                                 login_mobile=login_mobile,
                                                 login_passwd=login_passwd,
                                                 device_no=self._device_no,
                                                 quote_stand_alone=False)

        self._socket_client = TradingSocketClient(rsa_public_key=rsa_public_key,
                                                  rsa_private_key=rsa_private_key,
                                                  login_domain=login_domain,
                                                  login_country_code=login_country_code,
                                                  login_mobile=login_mobile,
                                                  login_passwd=login_passwd,
                                                  trading_passwd=trading_passwd,
                                                  token_client=self._token_client,
                                                  device_no=self._device_no,
                                                  logger=logger)

    def is_alive(self):
        """检查StockClient是否正常连接状态"""
        return self._socket_client.is_alive()

    def get_token(self):
        return self._token_client.get_token(self._login_country_code, self._login_mobile)

    def start(self, p_token):
        """启动业务API上下文环境，重启StockClient"""
        host, port = self._socket_client.get_server(p_token)
        if host is None or port is None:
            raise Exception('Got trade server info error, host/port is None.')
        self._socket_client.restart(p_token, host, port)
        # 执行异步订阅
        self.async_trade_subscribe()

    def add_notify_callback(self, callback):
        """
        增加消息推送回调函数
        """
        self._socket_client.handle_notify_for_ever(callback)

    def stop(self):
        """退出业务API上下文环境，停止StockClient"""
        self._socket_client.stop()

    def get_login_code_mobile(self):
        return self._login_country_code + ":" + self._login_mobile

    def _get_token_from_cache(self):
        return self._token_client.get_token_from_cache(self._login_country_code, self._login_mobile)

    def query_rate_list(self, rate_type):
        return self._socket_client.get_rate_list(token=self._get_token_from_cache(), rate_type=rate_type)

    @staticmethod
    def pb_to_result(pb_response: object, payload_key: str = '') -> ModelResult:
        """
        Convert Protobuf Response To  ModelResult
        :param  pb_response protobuf format response
        :param  payload_key get payload data by key
        :return ModelResult result model
        """
        if not pb_response:
            return ModelResult(False, StatusCode.INVOKE_API_FAILED, StatusCode.INVOKE_API_FAILED_DESCRIPTION, "")

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

    def query_portfolio_list(self, exchange_type_list: list) -> ModelResult:
        """
        Query portfolio list
        :param exchange_type_list: exchange type list, possible "P", "S"
        :return model_result: success, is_success=>true,  data=>portfolio list or empty
        """
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        if not exchange_type_list:
            return model_result.with_error(StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION)
        # build payload
        payload = QueryPortfolioListRequest()
        payload.marketTypeList.extend(exchange_type_list)
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QueryPortfolioListRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        return TradingAPI.pb_to_result(pb_response, 'portfolioList')

    def query_fund_info(self, exchange_type: str, portfolio: str) -> ModelResult:
        """
        Query fund info
        :param exchange_type: exchange type possible ['K', 'P']
        :param portfolio: portfolio account
        :return model_result:  success, is_success=>true,  data=>fund info
        """
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        if not exchange_type or not portfolio:
            return model_result.with_error(StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION)
        # build payload
        payload = QueryFundInfoRequest()
        # exchange type
        payload.marketType = exchange_type
        payload.portfolio = portfolio
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QueryFundInfoRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        return TradingAPI.pb_to_result(pb_response, '')

    def query_position_list(self, exchange_type: str, portfolio: str) -> ModelResult:
        """
        Query Position List
        :param exchange_type: exchange type, possible value: 'S', 'P'
        :param portfolio: portfolio account
        :return: model_result:  success, is_success=>true,  data=>position list
        """
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        if not exchange_type or not portfolio:
            return model_result.with_error(StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION)
        # build payload
        payload = QueryPositionListRequest()
        payload.marketType = exchange_type
        payload.portfolio = portfolio
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QueryPositionListRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        return TradingAPI.pb_to_result(pb_response, 'positionList')

    def query_max_buying_power(self, exchange_type: str,
                               portfolio: str,
                               order_type: str,
                               stock_code: str,
                               order_price: str = '',
                               order_id: str = '',
                               ) -> ModelResult:
        """
        Query max buying power
        :param exchange_type: exchange type, possible value: 'S', 'P'
        :param portfolio: portfolio account
        :param order_type: order type
        :param order_price: order price
        :param order_id : [option] order id
        :param stock_code: [option] stock code
        :return: model_result:  success, is_success=>true
        """
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        if not exchange_type or not portfolio or not order_type or not order_price:
            return model_result.with_error(StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION)

        # build payload
        payload = QueryMaxBuyingPowerRequest()
        payload.marketType = exchange_type
        payload.portfolio = portfolio
        payload.orderType = order_type
        payload.orderPrice = order_price
        payload.stockCode = stock_code
        payload.orderId = order_id
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QueryMaxBuyingPowerRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        return TradingAPI.pb_to_result(pb_response, '')

    def place_order(self, exchange_type: str,
                    portfolio: str,
                    order_type: str,
                    stock_code: str,
                    order_qty: str,
                    order_side: str,
                    validity: str = '',
                    expiry_date: str = '',
                    session_type: str = '',
                    display_size: str = '',
                    order_price: str = '',
                    ) -> ModelResult:
        """
        Place Order
        :param exchange_type: exchange type, possible value: 'S'-Saudi Stock, 'P'-US Stock
        :param portfolio:  portfolio account
        :param order_type:  order type, possible value:  3-Limit、5-Market、31-Iceberg
        :param validity:   order validity period, US stocks are empty
        :param expiry_date:  validity period (yyyyMMdd), this field needs to be passed only when validity is 4 (GTD)
        :param order_qty:  order quantity
        :param order_side: buying and selling direction
        :param stock_code: stock code
        :param order_price: order price
        :param session_type:  whether to trade before or after the market (0: No, 1: Yes), US stocks need to be filled in,
                              if not filled in, the default is 0, the selection of market order is invalid, and only intraday
                              trading is available
        :param display_size: disclose the quantity, the iceberg form must be filled in, and the quantity shall not be less
                             than 5% of the entrusted quantity
        :param order_price: commission price
        :return: model_result:  success, is_success=>true,  data=>order id
        """
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        payload = PlaceOrderRequest()
        payload.marketType = exchange_type
        payload.portfolio = portfolio
        payload.stockCode = stock_code
        payload.orderPrice = order_price
        payload.orderQty = order_qty
        payload.orderSide = order_side
        payload.orderType = order_type
        payload.validity = validity
        payload.expiryDate = expiry_date
        payload.sessionType = session_type
        payload.displaySize = display_size

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=PlaceOrderRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        return TradingAPI.pb_to_result(pb_response, '')

    def modify_order(self, order_id: str,
                     portfolio: str,
                     exchange_type: str,
                     stock_code: str,
                     order_qty: str,
                     order_price: str = '',
                     validity: str = '',
                     expiry_date: str = '',
                     display_size: str = '',
                     ) -> ModelResult:
        """
        Modify Order
        :param order_id: order id
        :param portfolio: portfolio account
        :param exchange_type: exchange type ,possible value: 'S'-Saudi Stock, 'P'-US Stock
        :param stock_code: stock code
        :param order_qty: order quantity
        :param order_price: order price
        :param validity: order validity type, Saudi Stock needs to fill in
        :param expiry_date:  validity period (yyyyMMdd), this field needs to be passed only when validity is 4 (GTD)
        :param display_size: disclose the quantity, the iceberg form must be filled in, and the quantity shall not be less
                             than 5% of the entrusted quantity
        :return: model_result:  success, is_success=>true,  data=>order id
        """
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        payload = ModifyOrderRequest()
        payload.marketType = exchange_type
        payload.portfolio = portfolio
        payload.stockCode = stock_code
        payload.orderPrice = order_price
        payload.orderQty = order_qty
        payload.validity = validity
        payload.expiryDate = expiry_date
        payload.displaySize = display_size
        payload.orderId = order_id

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=ModifyOrderRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        return TradingAPI.pb_to_result(pb_response, 'orderId')

    def cancel_order(self, exchange_type: str,
                     portfolio: str,
                     order_id: str,
                     ) -> ModelResult:
        """
        Cancel Order
        :param exchange_type: exchange type ,possible value: 'S'-Saudi Stock, 'P'-US Stock
        :param portfolio: portfolio account
        :param order_id: order id
        :return: model_result:  success, is_success=>true,  data=>order id
        """
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        if not exchange_type or not portfolio or not order_id:
            return model_result.with_error(StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION)

        payload = CancelOrderRequest()
        payload.marketType = exchange_type
        payload.portfolio = portfolio
        payload.orderId = order_id
        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=CancelOrderRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)

        payload = parse_payload(pb_response)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK:
            if payload and payload.success:
                # cancel order success, do nothing
                pass
            elif not payload or not payload.success:
                model_result.with_error(StatusCode.INVOKE_API_FAILED, StatusCode.INVOKE_API_FAILED_DESCRIPTION)
        else:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def query_today_order_list(self, exchange_type: str,
                               portfolio: str = '',
                               offset: str = '',
                               limit: str = '',
                               order_status_list: list = ''
                               ) -> ModelResult:
        """
        Query Today Order List
        :param exchange_type: exchange type ,possible value: 'S'-Saudi Stock, 'P'-US Stock
        :param portfolio: option, portfolio account
        :param offset: used for pagination
        :param limit: maximum records per page to be returned in the response.
        :param order_status_list: status list
        :return: model_result:  success, is_success=>true,  data -> (today order list, offset, completed)
        """
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        if not exchange_type:
            return model_result.with_error(StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION)

        payload = QueryTodayOrderListRequest()
        payload.marketType = exchange_type
        payload.portfolio = portfolio
        payload.pageQueryKey = offset
        payload.limit = limit
        payload.orderStatusList.extend(order_status_list)

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QueryTodayOrderListRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model((payload.orderList, payload.pageQueryKey, payload.hasNext))  # model type
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        else:
            model_result.with_error(StatusCode.INVOKE_TIME_OUT, StatusCode.INVOKE_TIME_OUT_DESCRIPTION)
        return model_result

    def query_history_order_list(self, exchange_type: str,
                                 portfolio: str = '',
                                 start_date: str = '',
                                 end_date: str = '',
                                 stock_code: str = '',
                                 offset: str = '',
                                 limit: str = '',
                                 order_status_list=None
                                 ) -> ModelResult:
        """
        Query Today Order List
        :param exchange_type: exchange type ,possible value: 'S'-Saudi Stock, 'P'-US Stock
        :param portfolio: option, portfolio account
        :param start_date: option, start date (yyyymmdd, default is endDate-90 days)
        :param end_date option,end date (default is yesterday)
        :param stock_code: option, stock code
        :param offset: option, used for pagination
        :param limit: option, maximum records per page to be returned in the response
        :param order_status_list: option, status list
        :return: model_result:  success, is_success=>true,  data -> (today order list, offset, completed)
        """
        if order_status_list is None:
            order_status_list = []
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        if not exchange_type:
            model_result.with_error(StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION)

        payload = QueryHistoryOrderListRequest()
        payload.marketType = exchange_type
        payload.portfolio = portfolio
        payload.startDate = start_date
        payload.endDate = end_date
        payload.pageQueryKey = offset
        payload.limit = limit
        payload.stockCode = stock_code
        payload.orderStatusList.extend(order_status_list)

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QueryHistoryOrderListRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model((payload.orderList, payload.pageQueryKey, payload.hasNext))  # model type
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        else:
            model_result.with_error(StatusCode.INVOKE_TIME_OUT, StatusCode.INVOKE_TIME_OUT_DESCRIPTION)
        return model_result

    def query_order_detail(self, exchange_type: str, order_id: str):
        """
        :param exchange_type:  exchange type ,possible value: 'S'-Saudi Stock, 'P'-US Stock
        :param order_id:  order id, If you have multiple values that you want to pass in a single argument, separated by commas
        :return:  model_result:  success, is_success=>true,  data ->()
        """
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        if not exchange_type or not order_id:
            return model_result.with_error(StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION)
        payload = QueryOrderDetailRequest()
        payload.marketType = exchange_type
        payload.orderId = order_id

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QueryOrderDetailRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)

        payload = parse_payload(pb_response)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload)  # model type
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        else:
            model_result.with_error(StatusCode.INVOKE_TIME_OUT, StatusCode.INVOKE_TIME_OUT_DESCRIPTION)

        return model_result

    def query_cash_statement_list(self, exchange_type: str,
                                  portfolio: str,
                                  start_date: str = '',
                                  end_date: str = '',
                                  flow_direction: str = '',
                                  flow_type_category_list: list = [],
                                  offset: str = '',
                                  limit: str = ''
                                  ) -> ModelResult:
        """
        Query Cash Statement List
        :param exchange_type: exchange type ,possible value: 'S'-Saudi Stock, 'P'-US Stock
        :param portfolio: option
        :param start_date: option, start date (yyyymmdd, default is endDate-90 days)
        :param end_date: option, end date (default is yesterday, the interval between startDate and endDate cannot exceed 90 days)
        :param flow_direction: fund flow direction (0: all, 1: inflow, 2: outflow), default is 0
        :param flow_type_category_list: option, business classification (flowTypeCategory 1: Stock trading, 2: Fund deposits and withdrawals,
               3: Corporate actions, 4: New stock IPO, 5: Margin financing and securities lending, 6: Internal transfer, 7: Stock transfer business,
               8: Others)
        :param offset: option, used for pagination
        :param limit: option, maximum records per page to be returned in the response
        :return: model_result:  success, is_success=>true,  data -> (cash statement list, offset, completed)
        """
        model_result = ModelResult(True, StatusCode.RET_OK, "", "")
        if not exchange_type or not portfolio:
            return model_result.with_error(StatusCode.INVOKE_PARAM_INVALID, StatusCode.INVOKE_PARAM_INVALID_DESCRIPTION)

        payload = QueryCashStatementListRequest()
        payload.marketType = exchange_type
        payload.portfolio = portfolio
        payload.startDate = start_date
        payload.endDate = end_date
        payload.pageQueryKey = offset
        payload.flowDirection = flow_direction
        payload.limit = limit
        payload.flowTypeCategoryList.extend(flow_type_category_list)

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(request_msg_type=QueryCashStatementListRequestMsgType,
                                                                  msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                                                  token=self._get_token_from_cache(),
                                                                  pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model((payload.cashStatementList, payload.pageQueryKey, payload.hasNext))  # model type
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        else:
            model_result.with_error(StatusCode.INVOKE_TIME_OUT, StatusCode.INVOKE_TIME_OUT_DESCRIPTION)
        return model_result

    def trade_subscribe(self) -> ModelResult:
        """
        Subscribe to transaction push messages. Currently, only order transaction push messages are available.
        The initialized transaction link will subscribe to the order transaction push by default.
        :return model_result model: Whether the subscription is successful true-yes false-no
        """

        payload = TransactionPushSubscribeRequest()
        payload.topicId = TradeSubscribeTopicId.TRADE_PUSH
        payload.subscribe = TradeSubscribeFlag.SUBSCRIBE

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TransactionPushSubscribeRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    token=self._get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", False)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.success)  # model type: bool
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        else:
            model_result.with_error(StatusCode.INVOKE_TIME_OUT, StatusCode.INVOKE_TIME_OUT_DESCRIPTION)
        return model_result

    def trade_cancel_subscribe(self) -> ModelResult:
        """
        Subscribe cancel
        :return model_result model: Whether the subscription cancel is successful true-yes false-no
        """

        payload = TransactionPushSubscribeRequest()
        payload.topicId = TradeSubscribeTopicId.TRADE_PUSH
        payload.subscribe = TradeSubscribeFlag.CANCEL_SUBSCRIBE

        with self._socket_client:
            request_id, msg_bytes, sent_bytes_len = \
                self._socket_client.build_request_bytes_then_send(
                    request_msg_type=TransactionPushSubscribeRequestMsgType,
                    msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                    token=self._get_token_from_cache(),
                    pb_payload=payload)
            pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", False)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.success)  # model type: bool
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        else:
            model_result.with_error(StatusCode.INVOKE_TIME_OUT, StatusCode.INVOKE_TIME_OUT_DESCRIPTION)
        return model_result

    def trade_subscribe_ignore_resp(self):
        """"Trade subscribe without result """
        self.trade_subscribe()

    def async_trade_subscribe(self):
        """Async start trade subscribe"""
        self._logging.info("Async start trade subscribe...")
        sync_thread = threading.Thread(target=self.trade_subscribe_ignore_resp())
        sync_thread.setDaemon(True)
        sync_thread.start()

    def trading_login_with_result(self, trade_passwd: str):
        """trading login"""
        request_id, sent_bytes_len = self._socket_client.trading_login(trade_passwd)
        pb_response = self._socket_client.async_get_result_direct(request_id)
        payload = parse_payload(pb_response)
        model_result = ModelResult(False, "", "", False)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK and payload:
            model_result.with_model(payload.success)  # model type: bool
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        else:
            model_result.with_error(StatusCode.INVOKE_TIME_OUT, StatusCode.INVOKE_TIME_OUT_DESCRIPTION)
        return model_result
