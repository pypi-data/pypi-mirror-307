# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
----------------------------------------
@所属项目 : hoime_sdk
----------------------------------------
@作者     : French<1109527533@hoime.cn>
@软件     : PyCharm
@文件名   : test.py
@创建时间 : 2024/10/16 - 19:16
@修改时间 : 2024/10/16 - 19:16
@文件说明 :
"""
import time
from hoime_sdk.api.user import UserApi

start_time = time.time()
user_api = UserApi(code="HhlvIi1UWF5sdqX17", key="Hoime-Fqomng7lL5RLm+02blfMKQ==-EKge2m+u/3u9QIEwuJs7qmseSD3K4fUJzJf2LVWSHEI=-1pVLuTwbFMPb+/cY2h2Btg==")
response = user_api.login(email="1109527533@qq.com", password="123321")
print(response)
print(time.time() - start_time)