# -*- coding: utf-8 -*-
import json
import ssl
import urllib
from logging import Logger
from urllib import request

from hs.api.constant import ModelResult, StatusCode, ServerKey, SecurityParam
from hs.common import rsa_utils
from hs.common.common_utils import get_info_logger
from hs.common.pb.common.constant.RequestMsgType_pb2 import PushsubscribeRequestMsgType, PushunsubscribeRequestMsgType
from hs.common.pb.hq.dto.Security_pb2 import Security
from hs.common.pb.hq.request.PushsubscribeRequest_pb2 import PushsubscribeRequest
from hs.common.pb.hq.request.PushunsubscribeRequest_pb2 import PushunsubscribeRequest
from hs.common.request_msg_type_enum import RequestMsgTypeEnum
from hs.common.socket_client import SocketClient
from hs.common.token_client import TokenClient
import json

logging_name: str = __name__


class QuoteSocketClient(SocketClient):
    """行情接口Socket Client"""

    @property
    def subscribe_dict(self):
        return self._subscribe_dict

    def __init__(self, rsa_public_key: str,
                 rsa_private_key: str,
                 login_domain: str,
                 login_country_code: str,
                 login_mobile: str,
                 login_passwd: str,
                 trading_passwd: str,
                 use_lv2: bool,
                 token_client: TokenClient,
                 device_no: str,
                 logger: Logger):
        super().__init__(rsa_public_key,
                         rsa_private_key,
                         login_domain,
                         login_country_code,
                         login_mobile,
                         login_passwd,
                         trading_passwd,
                         logger,
                         token_client,
                         device_no,
                         ServerKey.HQ_SERVER_KEY)
        self._logging = logger
        self._check_keep_alive_seconds_timeout = 0  # it maybe equals to _check_keep_alive_seconds_interval*3。skip timeout check if 0
        self._check_keep_alive_seconds_interval = 0  # using self._heartbeat_interval_sec if 0
        # 行情订阅字典 key(str): HQSubscribeTopicId, 如 str(HQSubscribeTopicId.BASIC_QOT) value(list): security_list，
        # 如 [SecurityParam(DataType.HK_STOCK, "00700.HK")]
        self._subscribe_dict = dict()
        self._use_lv2 = use_lv2

    def start(self, p_token, p_ip, p_port):
        super().start(p_token, p_ip, p_port)
        if self.is_alive() and self._init_connection_done:
            self._logging.info(f"Quote socket client start success.")
        else:
            self._logging.info(f"Quote socket client start fail.")
        if self._use_lv2:
            self.use_lv2_hq(self._login_domain + "/hs/hqPermission/lv2/switch")
        for key, value in self._subscribe_dict.items():
            self._logging.info(f"socket client重启后重新订阅行情: key={key}, value={value}")
            self.hq_subscribe(topic_id=int(key), security_list=value)

    def trading_login(self):
        """行情接口不需要交易登录"""
        return "", None

    def stop(self):
        self._logging.info("Stopping the quote socket client...")
        super().stop()
        self._logging.info("Stopped the quote socket client already!")

    def hq_subscribe(self, topic_id: int, security_list: list) -> ModelResult:
        """
        Subscribe to market updates
        :param topic_id Subscribe/Unsubscribe Quotes Push TopicId see HQSubscribeTopicId
        :param security_list: stock info list see SubSecurityParam
        :return model_result model: Whether the subscription is successful true-yes false-no
        """
        pb_security_list = []
        for security_param in security_list:
            pb_security = {'dataType': security_param.data_type, 'securityCode': security_param.stock_code}
            pb_security_list.append(pb_security)
        # build pb payload
        payload = PushsubscribeRequest()
        payload.topicId = topic_id
        payload.relatedParam = json.dumps({"securityCodes": pb_security_list})

        request_id, msg_bytes, sent_bytes_len = \
            self.build_request_bytes_then_send(request_msg_type=PushsubscribeRequestMsgType,
                                               msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                               token=self._get_token_from_cache(),
                                               pb_payload=payload)
        pb_response = self.async_get_result_direct(request_id)
        model_result = ModelResult(False, "", "", False)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK:
            model_result.with_model(True)  # model type: bool
            self._subscribe_dict[str(topic_id)] = security_list
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def hq_unsubscribe(self, topic_id: int, security_list: list) -> ModelResult:
        """
        Cancel Subscribe to market updates
        :param topic_id: Subscribe/Unsubscribe Quotes Push TopicId see HQSubscribeTopicId
        :param security_list: stock info list see SubSecurityParam
        :return model_result model: Whether the subscription is successful true-yes false-no
        """
        pb_security_list = []
        for security_param in security_list:
            pb_security = {'dataType': security_param.data_type, 'securityCode': security_param.stock_code}
            pb_security_list.append(pb_security)
        # build pb payload
        payload = PushunsubscribeRequest()
        payload.topicId = topic_id
        payload.relatedParam = str({"securityCodes": pb_security_list})

        request_id, msg_bytes, sent_bytes_len = \
            self.build_request_bytes_then_send(request_msg_type=PushunsubscribeRequestMsgType,
                                               msg_header_type_enum=RequestMsgTypeEnum.REQUEST,
                                               token=self._get_token_from_cache(),
                                               pb_payload=payload)
        pb_response = self.async_get_result_direct(request_id)
        model_result = ModelResult(False, "", "", False)
        if pb_response and pb_response.responseCode == StatusCode.RET_OK:
            model_result.with_model(True)  # model type: bool
            if str(topic_id) in self._subscribe_dict:
                del self._subscribe_dict[str(topic_id)]
        elif pb_response:
            model_result.with_error(pb_response.responseCode, pb_response.responseMsg)
        return model_result

    def use_lv2_hq(self, url):
        for i in range(1):  # 错误重试1次
            try:
                data = {
                    "token": self._get_token_from_cache()
                }
                headers = {'Content-Disposition': 'form-data', 'Accept-Charset': 'utf-8',
                           'Content-Type': 'application/x-www-form-urlencoded'}
                data = urllib.parse.urlencode(data).encode("utf-8")
                req = request.Request(url=url, data=data, headers=headers, method='POST')
                with request.urlopen(req, context=ssl._create_unverified_context()) as resp:
                    response = resp.read()
                response = json.loads(rsa_utils.bytes_to_str(response))
                self._logging.info(f"Query hq permission, response：{response}")
                resp_code = response.get("respCode")
                if resp_code == '0000':
                    self._logging.info(f"Got lv2 hq Permission！")
            except Exception as e:
                self._logging.error(f"Got hq Permission error：{e}")
