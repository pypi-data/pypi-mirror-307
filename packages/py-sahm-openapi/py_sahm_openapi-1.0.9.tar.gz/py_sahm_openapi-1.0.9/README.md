# Sahm OpenAPI-Python
-------------------
###### current：V1.0.0

### Install
```
for linux/macos
$>./local_install_build.sh

for windwos
$>python setup.py sdist bdist_wheel
$>cd dist
$>pip install py-sahm-openapi-1.x.x.tar.gz
###### Note: This API supports Python3.7+ 

###### Usage frot stock trade####
start interactive python programme
$>python

import stock trade test module 
>>> from hs.examples import stock_trade_demo

start test
>>>stock_trade_demo.start_trade_test(login_mobile='13662311971', login_passwd='Aa123456@', trading_passwd='123456')

import quote trade test module
>>>from hs.examples import stock_quote_demo

start test
>>>stock_quote_demo.start_quote_test(login_mobile='13662311971', login_passwd='Aa123456@')

### Api Document
access document：https://quant-open.hstong.com/api-docs/


### Change History
V1.0.0（2023-09-08） Increase and improve OpenAPI for transaction and quotation interface.
v1.0.7(2024-02-01)   Fix some bugs and add new feature.
v1.0.8(2024-02-28)   Modify domain name, enable https, and fix bugs in API response.