# -*- coding: utf-8 -*-

import time

from hs.examples.hs_common_api_demo import HsCommonApiDemo

if __name__ == '__main__':
    account_connect_info = dict() # 多账号连接信息
    
    ###################### 账号1：配置启动参数和初始化连接 ######################
    account_1st_login_country_code = "CHN" # 如果为香港或美国地区手机号，需要修改为对应区域编码，区域编码查询：https://quant-open.hstong.com/api-docs/#%E6%95%B0%E6%8D%AE%E5%AD%97%E5%85%B8
    account_1st_login_mobile = "<<your account 1st login mobile>>" # 登录账号无需加区号
    
    # 平台公钥，请求的时候使用（如果请求生产环境，需要替换为生产环境公钥，参考在线文档）
    ACCOUNT_1ST_ENCRYPT_RSA_PUBLICKEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCbRuA8hsbbzBKePEZZWaVtYpOjq2XaLZgAeVDlYqgy4lt4" \
                            "D+H2h+47AxVhYmS24O5lGuYD34ENlMoJphLrZkPbVBWJVHJZcRkpC0y36LFdFw7BSEA5+5+kdPFe8gR+wwXQ7" \
                            "sj9usESulRQcqrl38LoIz/vYUbYKsSe3dADfEgMKQIDAQAB"
    # 开发者RSA私钥。和直接私钥对应的公钥，需要填写到平台，给平台加密使用
    ACCOUNT_1ST_ENCRYPT_RSA_PRIVATEKEY = "<<your account 1st encrypt rsa private key>>"
    
    params = {
        "rsa_public_key": ACCOUNT_1ST_ENCRYPT_RSA_PUBLICKEY,
        "rsa_private_key": ACCOUNT_1ST_ENCRYPT_RSA_PRIVATEKEY,
        "login_domain": "https://quantapi-feature.sahmcapital.com",  # 生产环境domain为：https://quantapi.sahmcapital.com
        "login_country_code": account_1st_login_country_code, 
        "login_mobile": account_1st_login_mobile, 
        "login_passwd": "<<your account 1st login password>>",
        "trading_passwd": "<<your account 1st trading password>>",
        "logging_filename": None  # 日志文件路径（值为None则打印日志到console） e.g. "/tmp/hs.log"
    }
    # 初始化Common API对象、增加消息推送回调函数
    account_1st_common_api_demo = HsCommonApiDemo(**params).add_notify_callback()
    # 执行HTTP登录、获取token及连接ip port
    account_1st_token = account_1st_common_api_demo.get_token()
    # 启动Common API上下文，并会初始化连接、交易登录
    account_1st_common_api_demo.start(account_1st_token)
    # 检查连接状态
    account_1st_is_alive = account_1st_common_api_demo.check_alive()
    # 缓存账号1连接信息
    account_connect_info[account_1st_login_mobile] = account_1st_common_api_demo

    ###################### 账号2：配置启动参数和初始化连接 ######################
    account_2nd_login_country_code = "CHN" # 如果为香港或美国地区手机号，需要修改为对应区域编码，区域编码查询：https://quant-open.hstong.com/api-docs/#%E6%95%B0%E6%8D%AE%E5%AD%97%E5%85%B8
    account_2nd_login_mobile = "<<your account 2nd login mobile>>" # 登录账号无需加区号

    # 平台公钥，请求的时候使用（如果请求生产环境，需要替换为生产环境公钥，参考在线文档）
    ACCOUNT_2ND_ENCRYPT_RSA_PUBLICKEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCbRuA8hsbbzBKePEZZWaVtYpOjq2XaLZgAeVDlYqgy4lt4" \
                                        "D+H2h+47AxVhYmS24O5lGuYD34ENlMoJphLrZkPbVBWJVHJZcRkpC0y36LFdFw7BSEA5+5+kdPFe8gR+wwXQ7" \
                                        "sj9usESulRQcqrl38LoIz/vYUbYKsSe3dADfEgMKQIDAQAB"
    # 开发者RSA私钥。和直接私钥对应的公钥，需要填写到平台，给平台加密使用
    ACCOUNT_2ND_ENCRYPT_RSA_PRIVATEKEY = "<<your account 2nd encrypt rsa private key>>"

    params = {
        "rsa_public_key": ACCOUNT_2ND_ENCRYPT_RSA_PUBLICKEY,
        "rsa_private_key": ACCOUNT_2ND_ENCRYPT_RSA_PRIVATEKEY,
        "login_domain": "https://quantapi-feature.sahmcapital.com",  # 生产环境domain为：https://quantapi.sahmcapital.com
        "login_country_code": account_2nd_login_country_code,
        "login_mobile": account_2nd_login_mobile,
        "login_passwd": "<<your account 2nd login password>>",
        "trading_passwd": "<<your account 2nd trading password>>",
        "logging_filename": None  # 日志文件路径（值为None则打印日志到console） e.g. "/tmp/hs.log"
    }
    # 初始化Common API对象、增加消息推送回调函数
    account_2nd_common_api_demo = HsCommonApiDemo(**params).add_notify_callback()
    # 执行HTTP登录、获取token及连接ip port
    account_2nd_token = account_2nd_common_api_demo.get_token()
    # 启动Common API上下文，并会初始化连接、交易登录
    account_2nd_common_api_demo.start(account_2nd_token)
    # 检查连接状态
    account_2nd_is_alive = account_2nd_common_api_demo.check_alive()
    # 缓存账号2连接信息
    account_connect_info[account_2nd_login_mobile] = account_2nd_common_api_demo

    if account_1st_is_alive and account_2nd_is_alive:
        # 增加线程接口轮询，维持登录态
        account_1st_common_api_demo.timer_callback(interval=30)
        account_2nd_common_api_demo.timer_callback(interval=30)
        
        entrustResult = None
        # 命令形式展示 
        while True:
            print("###### 接口名: {mobile}:query_margin_fund_info，            接口描述: 交易接口-查询客户资金信息									 ######")
            print("###### 接口名: {mobile}:query_holds_list，                  接口描述: 交易接口-查询持仓股票列表									 ######")
            print("###### 接口名: {mobile}:query_buy_amount，                  接口描述: 交易接口-获取最大可买数量									 ######")
            print("###### 接口名: {mobile}:query_sell_amount，                 接口描述: 交易接口-获取最大可卖数量									 ######")
            print("###### 接口名: {mobile}:query_real_fund_jour_list，         接口描述: 交易接口-查询客户当日资金流水列表							 ######")
            print("###### 接口名: {mobile}:query_history_fund_jour_list，      接口描述: 交易接口-查询客户历史资金流水列表							 ######")
            print("###### 接口名: {mobile}:entrust，                           接口描述: 订单接口-委托/改单/撤单									 ######")
            print("###### 接口名: {mobile}:entrust_cond，                      接口描述: 订单接口-条件单委托/改单/撤单								 ######")
            print("###### 接口名: {mobile}:query_real_entrust_list，           接口描述: 订单接口-查询客户当日委托信息								 ######")
            print("###### 接口名: {mobile}:query_history_entrust_list，        接口描述: 订单接口-查询客户历史委托信息								 ######")
            print("###### 接口名: {mobile}:query_real_deliver_list，           接口描述: 订单接口-查询客户当日成交信息								 ######")
            print("###### 接口名: {mobile}:query_history_deliver_list，        接口描述: 订单接口-查询客户历史成交信息								 ######")
            print("###### 接口名: {mobile}:query_before_and_after_support，    接口描述: 订单接口-查询是否支持盘前盘后交易						     ######")
            print("###### 接口名: {mobile}:query_max_available_asset，         接口描述: 订单接口-查询最大可用资产						             ######")
            print("###### 接口名: {mobile}:query_stock_short_info，            接口描述: 订单接口-查询股票沽空信息       						     ######")
            print("###### 接口名: {mobile}:query_real_cond_order_list，        接口描述: 订单接口-查询当日条件单列表      						     ######")
            print("###### 接口名: {mobile}:query_history_cond_order_list，     接口描述: 订单接口-查询历史条件单列表       						     ######")
            print("###### 接口名: {mobile}:trade_subscribe，                   接口描述: 订单接口-订阅交易推送消息									 ######")
            print("###### 接口名: {mobile}:trade_unsubscribe，                 接口描述: 订单接口-取消订阅交易推送消息								 ######")
            print("###### 接口名: {mobile}:query_hq_basic_qot，                接口描述: 行情接口-基础报价                                           ######")
            print("###### 接口名: {mobile}:query_hq_broker，                   接口描述: 行情接口-买卖经纪摆盘                                       ######")
            print("###### 接口名: {mobile}:query_order_book，                  接口描述: 行情接口-查询买卖档                                         ######")
            print("###### 接口名: {mobile}:query_hq_ticker，                   接口描述: 行情接口-查询最近多少条的逐笔列表                           ######")
            print("###### 接口名: {mobile}:query_hq_kline，                    接口描述: 行情接口-K线数据                                            ######")
            print("###### 接口名: {mobile}:query_hq_time_share，               接口描述: 行情接口-查询分时数据                                       ######")
            print("###### 接口名: {mobile}:query_depth_order_book，            接口描述: 行情接口-查询深度摆盘数据                                   ######")
            print("###### 接口名: {mobile}:hq_subscribe_basic_qot，            接口描述: 行情接口-订阅基础行情推送消息（需要时才使用）               ######")
            print("###### 接口名: {mobile}:hq_subscribe_ticker，               接口描述: 行情接口-订阅逐笔推送消息（需要时才使用）                   ######")
            print("###### 接口名: {mobile}:hq_subscribe_broker，               接口描述: 行情接口-订阅买卖经纪推送消息（需要时才使用）               ######")
            print("###### 接口名: {mobile}:hq_subscribe_order_book，           接口描述: 行情接口-订阅买卖档推送消息（需要时才使用）                 ######")
            print("###### 接口名: {mobile}:hq_subscribe_total_view_book，      接口描述: 行情接口-订阅深度摆盘TOTALVIEW推送消息（需要时才使用）      ######")
            print("###### 接口名: {mobile}:hq_subscribe_arca_book，            接口描述: 行情接口-订阅深度摆盘ARCABOOK推送消息（需要时才使用）       ######")
            print("###### 接口名: {mobile}:hq_unsubscribe_basic_qot，          接口描述: 行情接口-取消订阅基础行情推送消息（需要时才使用）           ######")
            print("###### 接口名: {mobile}:hq_unsubscribe_ticker，             接口描述: 行情接口-取消订阅逐笔推送消息（需要时才使用）               ######")
            print("###### 接口名: {mobile}:hq_unsubscribe_broker，             接口描述: 行情接口-取消订阅买卖经纪推送消息（需要时才使用）           ######")
            print("###### 接口名: {mobile}:hq_unsubscribe_order_book，         接口描述: 行情接口-取消订阅买卖档推送消息（需要时才使用）             ######")
            print("###### 接口名: {mobile}:hq_unsubscribe_total_view_book，    接口描述: 行情接口-取消订阅深度摆盘TOTALVIEW推送消息（需要时才使用）  ######")
            print("###### 接口名: {mobile}:hq_unsubscribe_arca_book，          接口描述: 行情接口-取消订阅深度摆盘ARCABOOK推送消息（需要时才使用）   ######")
            print("###### 接口名: {mobile}:futures_entrust，                   接口描述: 期货接口-期货委托/改单/撤单                                 ######")
            print("###### 接口名: {mobile}:futures_query_holds_list，          接口描述: 期货接口-期货查询持仓                                       ######")
            print("###### 接口名: {mobile}:futures_query_fund_info，           接口描述: 期货接口-期货查询资金信息                                   ######")
            print("###### 接口名: {mobile}:futures_query_max_buy_sell_amount， 接口描述: 期货接口-查询期货最大可买/卖                                ######")
            print("###### 接口名: {mobile}:futures_query_real_entrust_list，   接口描述: 期货接口-期货查询今日委托                                   ######")
            print("###### 接口名: {mobile}:futures_query_history_entrust_list，接口描述: 期货接口-期货查询历史委托                                   ######")
            print("###### 接口名: {mobile}:futures_query_real_deliver_list，   接口描述: 期货接口-期货查询今日成交                                   ######")
            print("###### 接口名: {mobile}:futures_query_history_deliver_list，接口描述: 期货接口-期货查询历史成交                                   ######")
            print("###### 接口名: {mobile}:futures_query_product_info，        接口描述: 期货接口-期货查询产品信息                                   ######")
            print("###### 接口名: {mobile}:futures_trade_subscribe，           接口描述: 期货订阅接口-期货订阅交易推送消息                           ######")
            print("###### 接口名: {mobile}:futures_trade_unsubscribe，         接口描述: 期货订阅接口-取消订阅期货交易推送消息                       ######")
            print("###### 接口名: stop，                              		   接口描述: ！！！程序退出，该函数将退出交易登录，并断开TCP链接！！！	 ######")
            account_method_name = input("请输入需要查看的账号及接口名（账号和接口用':'分隔）: ")

            if account_method_name == "stop":
                # 【！！！注意：调用该函数将退出登录，并断开TCP链接。请在停止程序时调用！！！】
                for _, _common_api_demo in account_connect_info.items():
                    _common_api_demo.stop()
                exit(1)
    
            if ':' not in account_method_name:
                print("账号和接口名输入有误，请参考提示重新输入！")
                continue
    
            account, method_name = account_method_name.split(":")
            if len(account) == 0 or len(method_name) == 0 or account not in account_connect_info:
                print("账号和接口名输入有误，请参考提示重新输入！")
                continue

            common_api_demo = account_connect_info[account]
            if method_name == "query_margin_fund_info":
                # 交易接口-查询客户资金信息
                common_api_demo.query_margin_fund_info()
            elif method_name == "query_holds_list":
                # 查询持仓股票列表
                common_api_demo.query_holds_list()
            elif method_name == "query_buy_amount":
                # 获取最大可买数量
                common_api_demo.query_buy_amount()
            elif method_name == "query_sell_amount":
                # 获取最大可卖数量
                common_api_demo.query_sell_amount()
            elif method_name == "query_real_fund_jour_list":
                # 查询客户当日资金流水列表
                common_api_demo.query_real_fund_jour_list()
            elif method_name == "query_history_fund_jour_list":
                # 查询客户历史资金流水列表
                common_api_demo.query_history_fund_jour_list()
            elif method_name == "entrust":
                # 委托下单
                entrustResult = common_api_demo.entrust()
                time.sleep(1)
                # 改单（需要时才改单）
                # result = common_api_demo.change_entrust(entrustResult.get_model())
                time.sleep(1)
                # 撤单（需要时才撤单）
                # common_api_demo.cancel_entrust(entrustResult.get_model())
            elif method_name == "entrust_cond":
                # 条件单委托下单
                entrustResult = common_api_demo.entrust_cond()
                time.sleep(1)
                # 条件单改单（需要时才改单）
                # result = common_api_demo.change_entrust_cond(entrustResult.get_model())
                time.sleep(1)
                # 条件单撤单（需要时才撤单）
                # common_api_demo.cancel_entrust_cond(entrustResult.get_model())
            elif method_name == "query_real_entrust_list":
                # 查询客户当日委托信息
                if entrustResult is not None:
                    entrustIds = list()
                    entrustIds.append(entrustResult.get_model())
                    common_api_demo.query_real_entrust_list(entrustIds)
                else:
                    common_api_demo.query_real_entrust_list(list())
            elif method_name == "query_history_entrust_list":
                # 查询客户历史委托信息
                common_api_demo.query_history_entrust_list()
            elif method_name == "query_real_deliver_list":
                # 查询客户当日成交信息
                common_api_demo.query_real_deliver_list()
            elif method_name == "query_history_deliver_list":
                # 查询客户历史成交信息
                common_api_demo.query_history_deliver_list()
            elif method_name == "query_before_and_after_support":
                # 查询是否支持盘前盘后交易
                common_api_demo.query_before_and_after_support()
            elif method_name == "query_max_available_asset":
                # 查询最大可用资产
                common_api_demo.query_max_available_asset()
            elif method_name == "query_stock_short_info":
                # 查询股票沽空信息
                common_api_demo.query_stock_short_info()
            elif method_name == "query_real_cond_order_list":
                # 查询当日条件单列表
                common_api_demo.query_real_cond_order_list()
            elif method_name == "query_history_cond_order_list":
                # 查询历史条件单列表
                common_api_demo.query_history_cond_order_list()
            elif method_name == "trade_subscribe":
                # 订阅交易推送消息（需要时才使用）
                common_api_demo.trade_subscribe()
            elif method_name == "trade_unsubscribe":
                # 取消订阅交易推送消息（需要时才使用）
                common_api_demo.trade_unsubscribe()
            if method_name == "query_hq_basic_qot":
                # 批量查询股票基础报价
                common_api_demo.query_hq_basic_qot()
            elif method_name == "query_hq_broker":
                # 查询买卖经纪摆盘
                common_api_demo.query_hq_broker()
            elif method_name == "query_order_book":
                # 查询买卖档
                common_api_demo.query_order_book()
            elif method_name == "query_hq_ticker":
                # 查询最近多少条的逐笔列表
                common_api_demo.query_hq_ticker()
            elif method_name == "query_hq_kline":
                # 查询K线数据
                common_api_demo.query_hq_kline()
            elif method_name == "query_hq_time_share":
                # 查询分时数据
                common_api_demo.query_hq_time_share()
            elif method_name == "query_depth_order_book":
                # 查询深度摆盘数据
                common_api_demo.query_depth_order_book()
            elif method_name == "hq_subscribe_basic_qot":
                # 订阅基础行情推送消息（需要时才使用）
                common_api_demo.hq_subscribe_basic_qot()
            elif method_name == "hq_subscribe_ticker":
                # 订阅逐笔推送消息（需要时才使用）
                common_api_demo.hq_subscribe_ticker()
            elif method_name == "hq_subscribe_broker":
                # 订阅买卖经纪推送消息（需要时才使用）
                common_api_demo.hq_subscribe_broker()
            elif method_name == "hq_subscribe_order_book":
                # 订阅买卖档推送消息（需要时才使用）
                common_api_demo.hq_subscribe_order_book()
            elif method_name == "hq_subscribe_total_view_book":
                # 订阅深度摆盘TOTALVIEW推送消息（需要时才使用）
                common_api_demo.hq_subscribe_total_view_book()
            elif method_name == "hq_subscribe_arca_book":
                # 订阅深度摆盘ARCABOOK推送消息（需要时才使用）
                common_api_demo.hq_subscribe_arca_book()
            elif method_name == "hq_unsubscribe_basic_qot":
                # 取消订阅基础行情推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_basic_qot()
            elif method_name == "hq_unsubscribe_ticker":
                # 取消订阅逐笔推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_ticker()
            elif method_name == "hq_unsubscribe_broker":
                # 取消订阅买卖经纪推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_broker()
            elif method_name == "hq_unsubscribe_order_book":
                # 取消订阅买卖档推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_order_book()
            elif method_name == "hq_unsubscribe_total_view_book":
                # 取消订阅深度摆盘TOTALVIEW推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_total_view_book()
            elif method_name == "hq_unsubscribe_arca_Book":
                # 取消订阅深度摆盘ARCABOOK推送消息（需要时才使用）
                common_api_demo.hq_unsubscribe_arca_Book()
            if method_name == "futures_entrust":
                # 委托下单
                entrustResult = common_api_demo.futures_entrust()
                time.sleep(1)
                # 改单（需要时才改单）
                # result = common_api_demo.futures_change_entrust(entrustResult.get_model())
                time.sleep(1)
                # 撤单（需要时才撤单）
                # common_api_demo.futures_cancel_entrust(entrustResult.get_model())
            elif method_name == "futures_query_holds_list":
                # 查询接口-期货查询持仓
                common_api_demo.futures_query_holds_list()
            elif method_name == "futures_query_fund_info":
                # 查询接口-期货查询资金信息
                common_api_demo.futures_query_fund_info()
            elif method_name == "futures_query_max_buy_sell_amount":
                # 查询接口-查询期货最大可买/卖
                common_api_demo.futures_query_max_buy_sell_amount()
            elif method_name == "futures_query_real_entrust_list":
                # 查询接口-期货查询今日委托
                common_api_demo.futures_query_real_entrust_list()
            elif method_name == "futures_query_history_entrust_list":
                # 查询接口-期货查询历史委托
                common_api_demo.futures_query_history_entrust_list()
            elif method_name == "futures_query_real_deliver_list":
                # 查询接口-期货查询今日成交
                common_api_demo.futures_query_real_deliver_list()
            elif method_name == "futures_query_history_deliver_list":
                # 查询接口-期货查询历史成交
                common_api_demo.futures_query_history_deliver_list()
            elif method_name == "futures_query_product_info":
                # 查询接口-期货查询产品信息
                common_api_demo.futures_query_product_info()
            elif method_name == "futures_trade_subscribe":
                # 订阅接口-期货订阅交易推送消息
                common_api_demo.futures_trade_subscribe()
            elif method_name == "futures_trade_unsubscribe":
                # 订阅接口-取消订阅期货交易推送消息
                common_api_demo.futures_trade_unsubscribe()
            else:
                print("接口名输入有误，请参考提示重新输入！")
    else:
        # 【！！！注意：调用该函数将退出登录，并断开TCP链接。请在停止程序时调用！！！】
        for _, _common_api_demo in account_connect_info.items():
            _common_api_demo.stop()
        exit(1)