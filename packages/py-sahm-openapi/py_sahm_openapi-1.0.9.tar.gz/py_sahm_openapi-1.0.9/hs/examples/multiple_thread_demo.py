# -*- coding: utf-8 -*-
import threading
import time

from hs.examples.stock_quote_demo import StockQuoteDemo
from hs.examples.stock_trade_demo import StockTradeDemo


def get_time(f):
    def inner(*arg, **kwarg):
        s_time = time.time()
        res = f(*arg, **kwarg)
        e_time = time.time()
        print('耗时：{}秒'.format(e_time - s_time))
        return res

    return inner


# 定义异步执行的逻辑
@get_time
def async_call_trading(trade_demo: StockTradeDemo = None):
    # 2、初始化交易API对象、增加消息推送回调函数、启动交易API上下文
    if not trade_demo:
        print(f"async_call_trading trade_demo is empty, exit.")
        exit(1)
    # 3、Call当前OpenAPI所有支持的业务方法
    # 检查连接状态（非必需）
    trade_demo.check_alive()

    # 委托下单
    order_params = """{"exchange_type":"S", "portfolio":"130000196", "order_type":"3", "stock_code":"2222.SA", "order_price":"10", "order_qty":"10", "order_side":"1", "validity":"1"} """
    order_model_result = trade_demo.place_order(order_params)
    if order_model_result.is_success:
        print(f"position list：{order_model_result.get_model()}")
    else:
        print(f"fail to query, code: {order_model_result.code}, msg: {order_model_result.msg}")

    # 查询持仓
    position_params = """{"exchange_type":"S", "portfolio":"130000196"}"""
    position_model_result = trade_demo.query_position_list(position_params)
    if position_model_result.is_success:
        print(f"position list：{position_model_result.get_model()}")
    else:
        print(f"fail to query, code: {position_model_result.code}, msg: {position_model_result.msg}")

@get_time
def async_call_quote(quote_demo: StockQuoteDemo = None,
                     call_hq: bool = True,
                     subscribe_hq: bool = True):
    # 初始化行情API对象、增加消息推送回调函数、启动行情API上下文
    if not quote_demo:
        print(f"async_call_quote quote_demo is empty, exit.")
        exit(1)
    # 3、Call当前OpenAPI所有支持的业务方法
    # 检查连接状态（非必需）
    quote_demo.check_alive()
    if call_hq:
        # 查询最近多少条的逐笔列表
        quote_demo.query_hq_ticker("""{"exchange_type": "P", "limit": 10, "security_param": {"data_type": 20000, "stock_sode": "BABA"}}""")
        # 查询K线数据
        quote_demo.query_hq_kline("""{"exchange_type": "S", "limit": 10, "start_date": "20230925", "direction": 0, "ex_right_flag": 0, "cyc_type": 2, "security_param": {"data_type": 60000, "stock_sode": "2222.SA"}}""")
        # 查询分时数据
        quote_demo.query_hq_time_share("""{"exchange_type": "P", "security_param": {"data_type": 20000, "stock_sode": "BABA"}}""")
    if subscribe_hq:
        pass
    # 最后，如有需要可以退出业务API上下文，以释放业务对象
    # quote_demo.stop()


def multiple_async_call_quote(num_times: int = 1):
    quote_demo = StockQuoteDemo(**params).add_notify_callback()
    token = quote_demo.get_token()
    quote_demo.start(token)

    async_call_quote(quote_demo, call_hq=False, subscribe_hq=True)
    # 重复调用接口次数：num_times
    for i in range(num_times):
        print(f"call quote num_times: {i}")
        async_call_quote(quote_demo, call_hq=True, subscribe_hq=False)
    # 断开连接 释放资源
    quote_demo.stop()


def multiple_async_call_trading(num_times: int = 1):
    trade_demo = StockTradeDemo(**params).add_notify_callback()
    token = trade_demo.get_token()
    trade_demo.start(token)
    # 重复调用接口次数：num_times
    for i in range(num_times):
        print(f"call trading num_times: {i}")
        async_call_trading(trade_demo)
    # 断开连接 释放资源
    trade_demo.stop()


def async_call_trading_and_quote():
    async_call_trading()
    async_call_quote()


if __name__ == '__main__':
    # 1、配置启动参数
    # 平台公钥，请求的时候使用（如果请求生产环境，需要替换为生产环境公钥，参考在线文档）
    ENCRYPT_RSA_PUBLICKEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCbRuA8hsbbzBKePEZZWaVtYpOjq2XaLZgAeVDlYqgy4lt4" \
                            "D+H2h+47AxVhYmS24O5lGuYD34ENlMoJphLrZkPbVBWJVHJZcRkpC0y36LFdFw7BSEA5+5+kdPFe8gR+wwXQ7" \
                            "sj9usESulRQcqrl38LoIz/vYUbYKsSe3dADfEgMKQIDAQAB"
    # 开发者RSA私钥。和直接私钥对应的公钥，需要填写到平台，给平台加密使用
    ENCRYPT_RSA_PRIVATEKEY = """MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAKr24lt+FMSEzGzP
                                 CMmc+LCaaRoymseEwNdQGYc4FFSpkBKdEKhcEXndInkkqcjpNMTByTRqzLIR/qYA
                                 TuNWl6uCs8Ck5w8aHyDwmb6+72SyAa0LSfWoYRGKA/eps3efrK4uyzrsOvIafwPf
                                 pXG8Q5Z+2yBDrRwVI8YM9lOzAlFZAgMBAAECgYAlzAlFQv2iaN2tHKSLtkmA+dJM
                                 uW1guOfNcmcCbxKHmSlCBDl/j0NJ1urdL47d3TkOWu15yjbRE4th9eV6+1TyeKTl
                                 1JQ9TdA4/NG70aqU25P/ZTSkbuG0MRBBZIsKEQTJrKcei2cIKoIb+QwvBwzwUkXl
                                 aRbUgMvhSNLL7l8IRQJBANE8hcGrOi0XXWQJmYfLcGRbWajwp09uf5OaB/T1mFyq
                                 z6ehAw0TtUx/zaoX0bgaOdWTCDg4eDp3HEQJWDYyLAMCQQDRLJ/6kpqr8pm1ipqU
                                 pzR0gWYb+WhLF8vraoLoD688zuacxvhqJEtjriPLtzcvOHHA+KleedwHeacRs34/
                                 7YRzAkBrHqEb1Z2jGCMn5AJGE1EnD92HMC137QpDdsg8EMBAMPK+zx/QwhY/Y+7W
                                 9frYVhTl0rCSl9Z1mCVQb7hJhsYhAkBet4JJiJEZQ2Vu2zBcF8qc5utBx5H+Tuw7
                                 0aMtSczkEBxE6aQbDAxHOtdiq7gFXd3Er9ShvzRu/hs03L5SXE8ZAkAEdRkRzQnc
                                 ruq7ueQAvGsczg2wuNNh4EXIfq2krXLS3riN0SSeXejF9+FL8wEExwPpdLVBR+JT
                                 eDr7onfVE+FX
                                 """
    params = {
        "rsa_public_key": ENCRYPT_RSA_PUBLICKEY,
        "rsa_private_key": ENCRYPT_RSA_PRIVATEKEY,
        "login_domain": "https://quantapi-feature.sahmcapital.com", # 生产环境domain为：https://quantapi.sahmcapital.com
        "login_country_code": "SAU",
        # If it is a mobile phone number in Hong Kong or the United States, it needs to be modified to the
        # corresponding area code. Area code query：https://quant-open.hstong.com/api-docs/#%E6%95%B0%E6%8D%AE%E5%AD
        # %97%E5%85%B8
        "login_mobile": '611000229',  # 登录账号无需加区号
        "login_passwd": 'Hst11111',
        "trading_passwd": '111111',
        "logging_filename": None  # 日志文件路径（值为None则打印日志到console） e.g. "/tmp/hs.log"
    }
    # # 异步执行多次交易接口
    threading.Thread(target=multiple_async_call_trading, args=(1,)).start()
    print("async send trading command already!")

    # 异步执行多次行情接口
    threading.Thread(target=multiple_async_call_quote, args=(1,)).start()  # 1000次
    print("async send quote command already!")

    print("finished call thread...")
