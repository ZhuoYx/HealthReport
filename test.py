#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
需要安装selenium, chromedriver/geckodriver取决于使用谷歌还是火狐

需要修改如下信息：uaid 手机号 籍贯 家乡所在地 当前所在地 邮箱信息
邮箱信息非必须, 如不需要请删除
其他信息默认正常无需修改

uaid获取方式: 打开打卡信息, 右上角复制链接, 链接后即为uaid
"""

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import time
import sys
import string

# 放在服务器时请选择不显示浏览器窗口模式
# 这部分用来设置运行时不显示浏览器窗口 此处为使用火狐
option = Options()
option.add_argument('headless')
browser = webdriver.Firefox(options=option)

# 模拟浏览器进行访问 此处为使用谷歌
# 使用谷歌时候需引用chrome, 如下
# from selenium.webdriver.chrome.options import Options
# 下面地址选择chromedriver的绝对路径
# chrome_driver = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver_win32/chromedriver.exe"
# browser = webdriver.Chrome(executable_path=chrome_driver)

# uaid链接
browser.get("http://srv.zsc.edu.cn/f/jiankang?uaid=xxxx")  # 将uaid修改为自己的

# 手机号
browser.find_element_by_xpath("//*[@id='q6']").clear()
browser.find_element_by_xpath("//*[@id='q6']").send_keys("电话号码")  # 此处修改电话号码
# 籍贯
select = Select(browser.find_element_by_xpath("//*[@id='cmbProvince2']"))
select.select_by_value('广东')    # 此处修改籍贯省份
select = Select(browser.find_element_by_xpath("//*[@id='cmbCity2']"))
select.select_by_value('韶关市')  # 此处修改籍贯市
# 家乡所在地
select = Select(browser.find_element_by_css_selector(".ui-input-select .required[name='provinceHome']"))
select.select_by_value('广东')    # 此处修改家乡所在地省份
select = Select(browser.find_element_by_css_selector(".ui-input-select .required[name='cityHome']"))
select.select_by_value('韶关市')  # 此处修改家乡所在地市
# 当前所在地
select = Select(browser.find_element_by_xpath("//*[@id='cmbProvince']"))
select.select_by_value('广东')    # 此处修改当前所在地省份
select = Select(browser.find_element_by_xpath("//*[@id='cmbCity']"))
select.select_by_value('韶关市')  # 此处修改当前所在地市
browser.find_element_by_xpath("//*[@id='q5']").clear()
browser.find_element_by_xpath("//*[@id='q5']").send_keys("xxx")  # 此处修改当前所在地的详细信息

# 近14天内有没有去过高风险地区
browser.find_element_by_css_selector(".ui-radio .label[for='q11_2']").click()
# 是否近两周接触过疑似病例或确诊病例
browser.find_element_by_css_selector(".ui-radio .label[for='q16_2']").click()
# 是否近两周接触过有病例报告得社区街道的发热、咳嗽等呼吸道症状的患者
browser.find_element_by_css_selector(".ui-radio .label[for='q36_2']").click()
# 是否近两周接触过境外或高风险国家人员
browser.find_element_by_css_selector(".ui-radio .label[for='q46_2']").click()
# 返校前7天是否已做学校安排的核酸检测
browser.find_element_by_css_selector(".ui-radio .label[for='q7_2']").click()
# 本人目前健康状态
browser.find_element_by_css_selector(".ui-checkbox .label[for='jq_q21_0']").click()
# 家庭成员目前健康状态
browser.find_element_by_css_selector(".ui-checkbox .label[for='jq_q25_0']").click()
# 个人粤康码持码情况
browser.find_element_by_css_selector(".ui-radio .label[for='q57_1']").click()
# 接种新冠肺炎疫苗情况
browser.find_element_by_css_selector(".ui-radio .label[for='qyimiao_3']").click()
# 是否处于中高风险地区或国(境)外
browser.find_element_by_css_selector(".ui-radio .label[for='q100_2']").click()
# 点击签到
browser.find_element_by_xpath("//*[@id='ctlNext']").click()
time.sleep(30)
try:
    final = browser.find_element_by_xpath("//p[@class='su']").get_attribute('textContent')
except Exception:
    final = "打卡失败"
browser.quit()

# 邮箱部分
# 使用第三方 SMTP 服务发送
# QQ 邮箱通过生成授权码来设置密码
my_sender = ''                      # 发送邮件, 可设置为你的QQ邮箱或者其他邮箱
my_pass = ''                                         # 使用QQ邮箱生成的授权码
my_user = ''                        # 接收邮件, 可设置为你的QQ邮箱或者其他邮箱, 发送邮件和接收邮件可为同一邮箱
msg = MIMEText(final, 'plain', 'utf-8')              # 设置邮件内容，用的是之前签到返回的提示信息, 无需修改
msg['From'] = formataddr(["", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号、 使用QQ号即可
msg['To'] = formataddr(["", my_user])      # 括号里的对应收件人邮箱昵称、收件人邮箱账号、 使用QQ号即可
msg['Subject'] = "健康打卡提醒"                       # 邮件的主题，也可以说是标题
# 发送邮件
try:
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)             # 发件人邮箱中的SMTP服务器，端口是25
    server.login(my_sender, my_pass)                          # 括号中对应的是发件人邮箱账号、邮箱密码
    server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
    server.quit()                                             # 关闭连接
    print("邮件发送成功")
except Exception:
    print("邮件发送失败")
