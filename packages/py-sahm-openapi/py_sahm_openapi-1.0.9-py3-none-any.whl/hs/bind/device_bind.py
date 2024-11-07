#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback

from hs.bind import network_request, network_utils
from hs.bind.common_utils import get_logger
from hs.bind.mobile_validator import is_mobile

logging = get_logger(__name__)


def bind():
    env = "1"
    country_code = ""
    mobile = ""
    key = ""

    for i in range(4):
        env = input("Please select an environment to link(1：Development 2：Production)：")
        if len(env) == 0:
            print("Please select a link environment!!")
            continue
        elif env != "1" and env != "2":
            print("Please select a link environment!!")
            continue
        else:
            break

    for i in range(4):
        country_code_mobile = input(
            "\r\nPlease enter the mobile phone number used for developer login. (format CHN-18668017138) [Note: It must be a real mobile phone number to receive the verification code, and for the area code, please refer to the area code dictionary]:")
        if len(country_code_mobile) == 0:
            print("Please enter the phone number!!")
            continue
        else:
            str_arr = country_code_mobile.split('-')
            if len(str_arr) < 2:
                print("Mobile phone number format is incorrect!!")
                continue
            country_code = str_arr[0]
            mobile = str_arr[1]
            if not is_mobile(mobile, country_code):
                print("Mobile phone number format is incorrect!!")
                continue
            break

    for i in range(4):
        key = input("\r\nPlease enter the developer private key：")
        if len(key) == 0:
            print("The developer private key is incorrect!!")
            continue
        else:
            try:
                if not key.startswith('-----'):
                    key = "-----BEGIN RSA PRIVATE KEY-----\n" + key + "\n-----END RSA PRIVATE KEY-----"
                resp_code, resp_msg = network_request.send_auth_code(env, country_code, mobile, key)
                if resp_code != 0:
                    print(f"Failed to send verification code!! error code：{resp_code}，error message：{resp_msg}")
                else:
                    print("Verification code was sent successfully!")
                    break
            except Exception as e:
                print("Verification code failed to be sent, please try again!!")
                logging.error(traceback.print_exc())

    for i in range(4):
        code = input("\r\nPlease enter the verification code：")
        if len(code) == 0:
            print("The mobile phone verification code is incorrect!!")
            continue
        else:
            try:
                device_no = network_utils.get_mac_address()
                resp_code, resp_msg = network_request.send_bind_request(env, country_code, mobile, key, code, device_no)
                if resp_code != 0:
                    if i == 3:
                        print(f"Device binding failed, error code：{resp_code}，error message：{resp_msg}")
                    else:
                        print(f"There are too many errors, please contact customer service! error code：{resp_code}, error message：{resp_msg}")
                else:
                    print(f"Mobile: {mobile}, device no.: {device_no}  Linked successfully!!")
                    break
            except Exception as e:
                print("Device binding failed, please try again!!")
                logging.error(traceback.print_exc())
    exit(0)