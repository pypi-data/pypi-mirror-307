# -*- coding: utf-8 -*-
from dataclasses import dataclass


class StatusCode(object):
    """系统/业务状态码"""
    RET_OK = 0  # 处理成功
    INVOKE_TIME_OUT = 1015  # timeout
    INVOKE_TIME_OUT_DESCRIPTION = "The api calls timeout"
    INVOKE_PARAM_INVALID = 1016  # param illegal
    INVOKE_PARAM_INVALID_DESCRIPTION = "The api call parameter is illegal"
    INVOKE_API_FAILED = 1017  # api invoke failed
    INVOKE_API_FAILED_DESCRIPTION = "The api call failed"
    EXCHANGE_TYPE_NOT_SUPPORT = 9000  # exchange type not support
    EXCHANGE_TYPE_NOT_SUPPORT_DESCRIPTION = "Exchange type don't support"
    EXCHANGE_TYPE_REQUIRED = 9001  # exchange type required
    EXCHANGE_TYPE_REQUIRED_DESCRIPTION = "Exchange type required"


class ServerKey(object):
    """Get the Key of the long-term connection IP port"""
    HQ_SERVER_KEY = "hqServer"
    TRADING_SERVER_KEY = "tradeServer"


@dataclass
class ModelResult:
    """API统一返回的模型对象"""
    is_success: bool = False
    code: int = None
    msg: str = ""
    data: object = None

    def with_model(self, model):
        self.is_success = True
        self.data = model
        return self

    def get_model(self):
        return self.data

    def with_error(self, error_code, error_msg):
        self.is_success = False
        self.code = error_code
        self.msg = error_msg
        return self

    def to_str(self) -> str:
        return "{" + f"is_success: {self.is_success}, code: \"{self.code}\", msg: \"{self.msg}\", data: {self.data}" + "}"


@dataclass
class SecurityParam(object):
    """The entity class of stock information, used to construct the parameters of the market query interface"""
    data_type: int  # Stock Type, Reference Constant Class：DataType
    stock_code: str  # Stock Code


class ClientType(object):
    """客户端类型"""
    INTERNET = 0  # internet


class QueryType(object):
    """查询类型"""
    DEFAULT = 0  # 默认
    MARGIN = 1  # Margin


class EntrustBS(object):
    """买卖方向"""
    BUY = "1"  # 多头开仓
    SELL = "2"  # 多头平仓
    SHORT_SELL = "3"  # 空头平仓
    SHORT_BUY = "4"  # 空头开仓


class ExchangeType(object):
    """Market Type"""
    S = "S"  # Saudi Stock
    P = "P"  # US stock


class EntrustType(object):
    """
    委托类型
    港股：'0'-竞价限价、'1'-竞价、'2'-增强限价盘、'3'-限价盘、'4'-特别限价盘、'6'-暗盘
    美股：'3'-限价盘、'5'-市价盘、'8'-冰山市价、'9'-冰山限价、'10'-隐藏市价、'11'-隐藏限价
    A股：'3'-限价盘
    条件单：'31'-止盈限价单、'32'-止盈市价单(美股)、'33'-止损限价单、'34'-止损市价单(美股)、'35'-追踪止损限价单、'36'-追踪止损市价单(美股)
    """
    AUCTION_LIMIT = "0"  # 竞价限价
    AUCTION = "1"  # 竞价
    ENHANCED_LIMIT = "2"  # 增强限价盘
    LIMIT = "3"  # 限价盘
    SPECIAL_LIMIT = "4"  # 特别限价盘
    MARKET = "5"  # 市价盘
    DARK = "6"  # 暗盘
    ICEBERG_MARKET = "8"  # 冰山市价
    ICEBERG_LIMIT = "9"  # 冰山限价
    HIDE_MARKET = "10"  # 隐藏市价
    HIDE_LIMIT = "11"  # 隐藏限价

    COND_STOP_PROFIT_POINT = "31"  # 止盈限价单
    COND_STOP_PROFIT_MARKET = "32"  # 止盈市价单
    COND_STOP_LOSS_POINT = "33"  # 止损限价单
    COND_STOP_LOSS_MARKET = "34"  # 止损市价单
    COND_TRACK_STOP_LOSS_POINT = "35"  # 追踪止损限价单
    COND_TRACK_STOP_LOSS_MARKET = "36"  # 追踪止损市价单


class SessionType(object):
    """"
    盘前盘后交易
    0:否 1:是 3:只支持盘中 5:港股支持盘中及暗盘 7:美股支持盘中及盘前盘后
    """
    GENERAL_ORDER_NO = "0"  # 否
    GENERAL_ORDER_YES = "1"  # 是

    COND_ORDER_DEFAULT = "3"  # 只支持盘中
    COND_ORDER_HK_DEFAULT_HIDDEN = "5"  # 港股支持盘中及暗盘
    COND_ORDER_US_DEFAULT_BEFOREAFTER = "7"  # 美股支持盘中及盘前盘后


class CondTrackType(object):
    """
    条件跟踪类型 1百分比、2价差、3价格
    """
    PERCENTAGE = "1"  # 百分比
    PRICE = "2"  # 价差
    FIX_PRICE = "3"  # 价格


class CondStatus(object):
    """
    条件单状态  1:待触发 2:已触发 3:暂停 4:已过期 5:已删除 6:错误 8:止盈止损单失效 9:除权除息失效
    """
    PENDING = 1  # 待触发
    FINISH = 2  # 已触发
    PAUSE = 3  # 暂停
    EXPIRE = 4  # 已过期
    DELETE = 5  # 已删除
    ERROR = 6  # 错误
    INVALID_PROFITLOSS = 8  # 止盈止损失效
    INVALID_DIVIDEND = 9  # 除权除息失效
    RECALL = 10  # 撤回


class EntrustEX(object):
    """交易所"""
    SMART = "SMART"
    AMEX = "AMEX"
    ARCA = "ARCA"
    BATS = "BATS"
    BEX = "BEX"
    BYX = "BYX"
    CBOE = "CBOE"
    CHX = "CHX"
    DRCTEDGE = "DRCTEDGE"
    EDGEA = "EDGEA"
    EDGX = "EDGX"
    IBKRTS = "IBKRTS"
    IEX = "IEX"
    ISE = "ISE"
    ISLAND = "ISLAND"
    LTSE = "LTSE"
    MEMX = "MEMX"
    NYSE = "NYSE"
    NYSENAT = "NYSENAT"
    PEARL = "PEARL"
    PHLX = "PHLX"
    PSX = "PSX"


class DataType(object):
    """Security type"""
    US_STOCK = 20000  # US stocks
    US_INDEX = 20001  # US stock index
    US_ETF = 20002  # US Stock ETF
    US_OPTION = 20003  # US stock options
    US_OCT = 20009  # US stock OTC
    SAU_STOCK = 60000  # Saudi stocks
    SAU_INDEX = 60001  # Saudi stock index
    SAU_ETF = 60002  # Saudi stock ETFs
    SAU_REIT = 60003  # Saudi stock REITs
    SAU_CEF = 60004  # Saudi Stock CEFs
    SAU_WARRANT = 60005  # Saudi stock warrant
    SAU_BOND = 60006  # Saudi stock bond


"""
US stock security types
"""
US_STOCK_DATA_TYPE_LIST = [
    DataType.US_STOCK,
    DataType.US_INDEX,
    DataType.US_ETF,
    DataType.US_OPTION,
    DataType.US_OCT
]

"""
Saudi stock security types
"""
SAU_STOCK_DATA_TYPE_LIST = [
    DataType.SAU_STOCK,
    DataType.SAU_INDEX,
    DataType.SAU_ETF,
    DataType.SAU_REIT,
    DataType.SAU_CEF,
    DataType.SAU_WARRANT,
    DataType.SAU_BOND
]


class CycType(object):
    """K line type"""
    DAY = 2  # 日线
    WEEK = 3  # 周线
    MONTH = 4  # 月线
    MINUTE1 = 5  # 1分钟
    MINUTE5 = 6  # 5分钟
    MINUTE15 = 7  # 15分钟
    MINUTE30 = 8  # 30分钟
    MINUTE60 = 9  # 60分钟
    MINUTE120 = 10  # 120分钟
    QUARTER = 11  # 季度线
    YEAR = 12  # 年度线


class ExRightFlag(object):
    """复权类型"""
    BFQ = 0  # 不复权
    QFQ = 1  # 前复权
    HFQ = 2  # 后复权


class Direction(object):
    """查询方向"""
    QUERY_LEFT = 0  # 往左查询
    QUERY_RIGHT = 1  # 往右查询


class HQSubscribeTopicId(object):
    """subscribing/unsubscribing market push TopicId"""
    BASIC_QOT = '1036'  # basic quotes push
    TICKER = '1037'  # 逐笔推送
    ORDER_BOOK = '1017'  # 买卖档推送
    TOTALVIEW_BOOK = '1027'  # TOTALVIEW
    ARCA_BOOK = '1029'  # ARCABOOK
    MBO_BOOK = '1031'  # MBO


class TradeSubscribeTopicId(object):
    """"""
    TRADE_PUSH = "21"  # trade push


class TradeSubscribeFlag(object):
    SUBSCRIBE = "1"
    CANCEL_SUBSCRIBE = "0"


class MktTmType(object):
    """
    Trading period
    US stocks: Pre-market: -1 Intraday: 1 After-hours: -2
    """
    PRE_MARKET = -1  # Pre-market
    MID_SESSION = 1  # Intraday
    AFTER_HOURS = -2  # After-hours


class DepthBookType(object):
    """
    2 3 totalview arcabook
    """
    TOTAL_VIEW = 2  # totalview
    ARCA_BOOK = 3  # arcabook


class OptionPriceFlag(object):
    """
    Option In-the-money=1 Out-of-the-money=2
    """
    PRICE_IN = 1
    PRICE_OUT = 2


class OptionType(object):
    """
    Option Type Call=C Pu=P
    """
    CALL = "C"
    PUT = "P"


class FuturesEntrustType(object):
    """
    期货委托类型
    0 限价单、1 竞价单、2 市价单、3 条件单
    """
    LIMIT = "0"  # 限价单
    AUCTION = "1"  # 竞价单
    MARKET = "2"  # 市价单
    OPTION = "3"  # 条件单


class FuturesValidTimeType(object):
    """
    期货委托生效类型
    0 即日有效、1 成交并取消、2 全额或取消、3 到期日有效、4 指定日期有效
    """
    VALID_TODAY = "0"  # 即日有效
    DEAL_AND_CANCEL = "1"  # 成交并取消
    FULL_OR_CANCEL = "2"  # 全额或取消
    VALID_ON_EXPIRY_DATE = "3"  # 到期日有效
    VALID_ON_SPECIFIED_DATE = "4"  # 指定日期有效


class AlgoStrategyType(object):
    VWAP = "1"  # VWAP
    TWAP = "1001"  # TWAP
    ICE_BERG = "1002"  # ICE_BERG
    TPOV = "1003"  # TPOV
    INLINE = "1005"  # INLINE


class AlgoEntrustType(object):
    LIMIT = "1"  # 限价单
    MARKET = "2"  # 市价单


class AlgoActionType(object):
    START = "1"  # START
    STOP = "2"  # STOP
    SUSPEND = "3"  # SUSPEND
    RESUME = "4"  # RESUME


class AlgoStrategySensitivityType(object):
    NEUTRAL = "1"  # 中性
    AGGRESSIVE = "2"  # 主动
    PASSIVE = "3"  # 被动


class RateType(object):
    EXCHANGE = 0  # 换汇汇率
    IMMEDIATE = 1  # 即期汇率


class SaudiOrderBookType(object):
    """Saudi stock book type"""
    MBO = "MBO"  # Market by order
    MBP = "MBP"  # Market by price
