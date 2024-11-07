# -*- coding: utf-8 -*-
import struct

from google.protobuf.json_format import MessageToDict
from snappy import snappy

from hs.common import rsa_utils
from hs.common.aes_ecb import AESCipher
from hs.common.common_utils import get_logger
from hs.common.pb.common.init.InitConnectResp_pb2 import InitConnectResp
from hs.common.pb.common.msg.Notify_pb2 import PBNotify
from hs.common.pb.common.msg.Response_pb2 import PBResponse
from hs.common.pb.common.response.CommonBoolResponse_pb2 import CommonBoolResponse
from hs.common.pb.common.response.CommonIntResponse_pb2 import CommonIntResponse
from hs.common.pb.common.response.CommonStringResponse_pb2 import CommonStringResponse
from hs.common.pb.hq.notify.OrderBookFullV2Notify_pb2 import OrderBookFullV2Notify
from hs.common.pb.hq.notify.StatisticsNotify_pb2 import StatisticsNotify
from hs.common.pb.hq.notify.StatisticsV2Notify_pb2 import StatisticsV2Notify
from hs.common.pb.hq.notify.TradeTickerV2Notify_pb2 import TradeTickerV2Notify
from hs.common.pb.hq.response.BasicQotResponse_pb2 import BasicQotResponse
from hs.common.pb.hq.response.KLResponse_pb2 import KLResponse
from hs.common.pb.hq.response.OrderBookResponse_pb2 import OrderBookResponse
from hs.common.pb.hq.response.TickerResponse_pb2 import TickerResponse
from hs.common.pb.hq.response.TimeShareResponse_pb2 import TimeShareResponse
from hs.common.pb.hq.response.UsOptionChainCodeResponse_pb2 import UsOptionChainCodeResponse
from hs.common.pb.hq.response.UsOptionChainExpireDateResponse_pb2 import UsOptionChainExpireDateResponse
from hs.common.pb.trade.notify.TransactionCallBackNotify_pb2 import TransactionCallBackNotify
from hs.common.pb.trade.response.CancelOrderResponse_pb2 import CancelOrderResponse
from hs.common.pb.trade.response.ModifyOrderResponse_pb2 import ModifyOrderResponse
from hs.common.pb.trade.response.PlaceOrderResponse_pb2 import PlaceOrderResponse
from hs.common.pb.trade.response.QueryCashStatementListResponse_pb2 import QueryCashStatementListResponse
from hs.common.pb.trade.response.QueryFundInfoResponse_pb2 import QueryFundInfoResponse
from hs.common.pb.trade.response.QueryHistoryOrderListResponse_pb2 import QueryHistoryOrderListResponse
from hs.common.pb.trade.response.QueryMaxBuyingPowerResponse_pb2 import QueryMaxBuyingPowerResponse
from hs.common.pb.trade.response.QueryOrderDetailResponse_pb2 import QueryOrderDetailResponse
from hs.common.pb.trade.response.QueryPortfolioListResponse_pb2 import QueryPortfolioListResponse
from hs.common.pb.trade.response.QueryPositionListResponse_pb2 import QueryPositionListResponse
from hs.common.pb.trade.response.QueryTodayOrderListResponse_pb2 import QueryTodayOrderListResponse
from hs.common.pb.trade.response.TransactionPushSubscribeResponse_pb2 import TransactionPushSubscribeResponse
from hs.common.pb.trade.response.UnLockTradeResponse_pb2 import UnLockTradeResponse
from hs.common.request_msg_header import RequestMsgHeader
from hs.common.request_msg_type_enum import RequestMsgTypeEnum

logging = get_logger(__name__)

# 包头FORMAT
MESSAGE_HEADER_FMT = "<2s1h2B2I128sBQ"
"""
    #pragma pack(push, APIProtoHeader, 1)
    struct APIProtoHeader
    {
        u8_t szHeaderFlag[2];   //2s-[2字节] 包头起始标志，固定为：“HS”
        u8_t msgType[2];        //1h-[2字节] 消息类型0：心跳 1：请求 2：响应 3：推送
        u8_t protoFmtType;      //B-[1字节] 协议格式类型，0为Protobuf格式
        u8_t protoVer;          //B-[1字节] 协议版本，用于迭代兼容, 目前填0
        u32_t serialNo;         //I-[4字节] 包序列号，用于对应请求包和回包，要求递增
        u32_t bodyLen;          //I-[4字节] 包体长度
        u8_t bodySHA1[128];     //128s-[128字节] 包体原始数据(加密后)的SHA1哈希值
        u8_t compressAlgorithm; //B-[1字节] 压缩算法，0：不压缩
        u8_t reserved[8];       //Q-[8字节] 保留8字节扩展
    };
    #pragma pack(pop, APIProtoHeader)
"""
PB_NOTIFY_CLASS_LIST = [
    StatisticsNotify,  # 行情推送
    OrderBookFullV2Notify,  # 买卖档推送
    TradeTickerV2Notify,  # 逐笔推送
    TransactionCallBackNotify,  # 交易推送
    StatisticsV2Notify  # 行情推送V2
]
PB_RESPONSE_CLASS_LIST = [
    InitConnectResp,
    QueryPortfolioListResponse,
    PlaceOrderResponse,
    CancelOrderResponse,
    ModifyOrderResponse,
    QueryCashStatementListResponse,
    QueryFundInfoResponse,
    QueryHistoryOrderListResponse,
    QueryMaxBuyingPowerResponse,
    QueryPortfolioListResponse,
    QueryPositionListResponse,
    QueryTodayOrderListResponse,
    UnLockTradeResponse,
    TransactionPushSubscribeResponse,
    BasicQotResponse,
    KLResponse,
    OrderBookResponse,
    TickerResponse,
    TimeShareResponse,
    UsOptionChainCodeResponse,
    UsOptionChainExpireDateResponse,
    CommonBoolResponse,
    CommonIntResponse,
    CommonStringResponse,
    QueryOrderDetailResponse
]


def pack_request(request_msg_header: RequestMsgHeader, encrypt_payload: str) -> bytes:
    if type(encrypt_payload) is not bytes:
        encrypt_payload = bytes(encrypt_payload, 'utf-8')
    request_msg_header.body_len = len(encrypt_payload)
    logging.debug("pack_request, request_msg_header.body_len=" + str(request_msg_header.body_len))
    return struct.pack(MESSAGE_HEADER_FMT + "%ds" % request_msg_header.body_len,
                       bytes(request_msg_header.sz_header_flag, "utf-8"),
                       request_msg_header.msg_type,
                       request_msg_header.proto_fmt_type,
                       request_msg_header.proto_ver,
                       request_msg_header.serial_no,
                       request_msg_header.body_len,
                       request_msg_header.body_sha1,
                       request_msg_header.compress_algorithm,
                       request_msg_header.reserved,
                       encrypt_payload)


def unpack_response(response: bytes, rsa_public_key: str, rsa_private_key: str, encrypt_secret_key: str):
    pack_size = struct.calcsize(MESSAGE_HEADER_FMT)
    logging.debug(f"unpack_response->len(response)：{len(response)}, header pack_size：{pack_size}，response：{response}")
    unpack_msg = struct.unpack(MESSAGE_HEADER_FMT + "%ds" % (len(response) - pack_size), response)
    logging.debug(f"unpack_response->header unpack_msg：{unpack_msg}")
    request_msg_header = RequestMsgHeader(sz_header_flag=unpack_msg[0].decode("utf-8"),
                                          msg_type=unpack_msg[1],
                                          proto_fmt_type=unpack_msg[2],
                                          proto_ver=unpack_msg[3],
                                          serial_no=unpack_msg[4],
                                          body_len=unpack_msg[5],
                                          body_sha1=unpack_msg[6],
                                          compress_algorithm=unpack_msg[7],
                                          reserved=unpack_msg[8])
    # 私钥解密body
    decrypt_body_bytes = unpack_msg[9]
    if request_msg_header.serial_no == 0:
        encrypt_secret_key = rsa_private_key
        if request_msg_header.msg_type == RequestMsgTypeEnum.REQUEST.value \
                or request_msg_header.msg_type == RequestMsgTypeEnum.RESPONSE.value:
            # Socket登录初始化RSA
            decrypt_body_bytes = rsa_utils.decrypt_data(unpack_msg[9], encrypt_secret_key)
    else:
        # 业务请求AES
        if request_msg_header.msg_type == RequestMsgTypeEnum.REQUEST.value \
                or request_msg_header.msg_type == RequestMsgTypeEnum.RESPONSE.value \
                or request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value:
            decrypt_body_bytes = AESCipher(encrypt_secret_key).decrypt(unpack_msg[9])
    pb_response = PBNotify() if (request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value) else PBResponse()
    # 如果压缩 使用snappy解压缩
    if request_msg_header.compress_algorithm > 0:
        decrypt_body_bytes = snappy.uncompress(decrypt_body_bytes)
    # 公钥验签
    if request_msg_header.msg_type == RequestMsgTypeEnum.REQUEST.value \
            or request_msg_header.msg_type == RequestMsgTypeEnum.RESPONSE.value \
            or request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value:
        if rsa_utils.rsa_verify_sign(decrypt_body_bytes, request_msg_header.body_sha1, rsa_private_key):
            pb_response.ParseFromString(decrypt_body_bytes)
            if request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value:
                logging.debug(f"验签通过，notifyMsgType：{pb_response.notifyMsgType}，")
            else:
                logging.debug(f"验签通过，response消息：{pb_response.responseMsg}，")
        else:
            pb_response.ParseFromString(decrypt_body_bytes)
            if request_msg_header.msg_type == RequestMsgTypeEnum.NOTIFY.value:
                logging.debug(f"验签后的notifyMsgType：{pb_response.notifyMsgType}")
            else:
                logging.debug(f"验签后的response消息：{pb_response.responseMsg}")
    else:
        logging.debug("验签通过[免验]")
    logging.debug(f"unpack_response->response：{pb_response}")
    payload = parse_payload(pb_response)
    return request_msg_header, pb_response, payload


def parse_payload(pb_response):
    """解析any类型的payload"""
    if pb_response is None:
        return None
    payload = None
    payload_any = pb_response.payload
    if pb_response.DESCRIPTOR.name == PBNotify.DESCRIPTOR.name:
        for pb_class in PB_NOTIFY_CLASS_LIST:
            if payload_any.Is(pb_class.DESCRIPTOR):
                pb_class_response = pb_class()
                pb_response.payload.Unpack(pb_class_response)
                payload = pb_class_response
                logging.debug(f"parse_payload->{pb_class_response.DESCRIPTOR.name}：{payload}")
                break
    else:
        for pb_class in PB_RESPONSE_CLASS_LIST:
            if payload_any.Is(pb_class.DESCRIPTOR):
                pb_class_response = pb_class()
                pb_response.payload.Unpack(pb_class_response)
                payload = pb_class_response
                logging.debug(f"parse_payload->{pb_class_response.DESCRIPTOR.name}：{payload}")
                break
    return payload


def proto_to_dict(pb_obj):
    """
    proto obj to dict
    :param pb_obj:
    :return: dict
    """
    return MessageToDict(pb_obj, preserving_proto_field_name=True)
