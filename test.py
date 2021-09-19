#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
需要安装selenium, pandas, xlrd, openpyxl, chromedriver/geckodriver取决于使用谷歌还是火狐

如不需要邮箱，删除邮箱并修改excel运行即可
邮箱信息非必须, 如不需要请删除

uaid获取方式: 微信打开推送的打卡信息, 右上角复制链接, 链接后即为uaid
"""

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import pandas as pd
import time
import sys
import string
final = ''


def signIn(row_lists):
    # 放在服务器时请选择不显示浏览器窗口模式
    # 这部分用来设置运行时不显示浏览器窗口 此处为使用火狐
    option = Options()
    option.add_argument('--headless')
    browser = webdriver.Firefox(options=option)

    # 模拟浏览器进行访问 此处为使用谷歌
    # 下面地址选择chromedriver的绝对路径
    # chrome_driver = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver_win32/chromedriver.exe"
    # browser = webdriver.Chrome(executable_path=chrome_driver)

    # uaid链接
    browser.get(row_lists[0])

    # 手机号
    browser.find_element_by_xpath("//*[@name='mobile']").clear()
    browser.find_element_by_xpath("//*[@name='mobile']").send_keys(row_lists[1])
    # 紧急联系人姓名
    browser.find_element_by_xpath("//*[@name='linkman']").clear()
    browser.find_element_by_xpath("//*[@name='linkman']").send_keys(row_lists[2])
    # 紧急联系人电话
    browser.find_element_by_xpath("//*[@name='linkmanmobile']").clear()
    browser.find_element_by_xpath("//*[@name='linkmanmobile']").send_keys(row_lists[3])
    # 家乡所在地
    select = Select(browser.find_element_by_css_selector(".ui-input-select .required[name='provinceHome']"))
    select.select_by_value(row_lists[4])
    select = Select(browser.find_element_by_css_selector(".ui-input-select .required[name='cityHome']"))
    select.select_by_value(row_lists[5])
    browser.find_element_by_xpath("//input[@name='addressHome']").clear()
    browser.find_element_by_xpath("//input[@name='addressHome']").send_keys(row_lists[6])
    # 常住地址
    browser.find_element_by_xpath("//*[@name='address2']").clear()
    browser.find_element_by_xpath("//*[@name='address2']").send_keys(row_lists[9])
    # 当前所在地
    select = Select(browser.find_element_by_css_selector(".ui-input-select .required[name='province']"))
    select.select_by_value(row_lists[7])
    select = Select(browser.find_element_by_css_selector(".ui-input-select .required[name='city']"))
    select.select_by_value(row_lists[8])
    browser.find_element_by_xpath("//*[@name='address']").clear()
    browser.find_element_by_xpath("//*[@name='address']").send_keys(row_lists[9])
    # 今日行程
    # 一直在中山
    if row_lists[10] == 0:
        browser.find_element_by_css_selector(".ui-radio .label[for='q16_1']").click()
    # 不在中山
    else:
        browser.find_element_by_css_selector(".ui-radio .label[for='q16_2']").click()
        browser.find_element_by_xpath("//input[@name='todaytraveaddress']").clear()
        browser.find_element_by_xpath("//input[@name='todaytraveaddress']").send_keys(row_lists[11])
        browser.find_element_by_css_selector(".ui-radio[refvalue="+row_lists[12]+"]").click()
    # 昨日行程
    # 一直在中山市
    if row_lists[13] == 0:
        browser.find_element_by_css_selector(".ui-radio .label[for='q86_1']").click()
    # 不在中山
    else:
        browser.find_element_by_css_selector(".ui-radio .label[for='q86_2']").click()
        browser.find_element_by_xpath("//input[@name='zuoritraveaddress']").clear()
        browser.find_element_by_xpath("//input[@name='zuoritraveaddress']").send_keys(row_lists[14])
        browser.find_element_by_css_selector(".ui-radio[refvalue=" + row_lists[15] + "]").click()
    # 近14天内是否有中高风险地区、封闭封控警戒区旅居史
    browser.find_element_by_css_selector(".ui-radio .label[for='q11_2']").click()
    # 本人目前健康状态
    try:
        browser.find_element_by_css_selector(".jqchecked[id='jq_q21_0']")
    except Exception:
        browser.find_element_by_css_selector(".ui-checkbox .label[for='jq_q21_0']").click()
    # 家庭成员目前健康状态
    try:
        browser.find_element_by_css_selector(".jqchecked[id='jq_q25_0']")
    except Exception:
        browser.find_element_by_css_selector(".ui-checkbox .label[for='jq_q25_0']").click()
    # 个人粤康码持码情况
    browser.find_element_by_css_selector(".ui-radio .label[for='q57_1']").click()
    # 接种新冠肺炎疫苗情况
    browser.find_element_by_css_selector(".ui-radio .label[for='qyimiao_3']").click()
    # 是否处于中高风险地区或国(境)外
    browser.find_element_by_css_selector(".ui-radio .label[for='q100_2']").click()
    # # 点击签到
    browser.find_element_by_xpath("//*[@id='ctlNext']").click()
    time.sleep(30)
    global final
    try:
        final = browser.find_element_by_xpath("//p[@class='su']").get_attribute('textContent')
    except Exception:
        final = "打卡失败"
    browser.quit()
    email(row_lists)


def email(row_lists):
    # 邮箱部分
    # 使用第三方 SMTP 服务发送
    # QQ 邮箱通过生成授权码来设置密码
    my_sender = ''                      # 发送邮件, 可设置为你的QQ邮箱或者其他邮箱
    my_pass = ''                         # 使用QQ邮箱生成的授权码
    my_user = row_lists[17]                              # 接收邮件, 可设置为你的QQ邮箱或者其他邮箱, 发送邮件和接收邮件可为同一邮箱
    msg = MIMEText(final, 'plain', 'utf-8')              # 设置邮件内容，用的是之前签到返回的提示信息, 无需修改
    msg['From'] = formataddr(['', my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号、 使用QQ号即可
    msg['To'] = formataddr([str(row_lists[16]), my_user])     # 括号里的对应收件人邮箱昵称、收件人邮箱账号、 使用QQ号即可
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


def excel():
    dataFrame = pd.DataFrame(pd.read_excel('HealthReport.xlsx', engine='openpyxl', keep_default_na=False))
    for index, row in dataFrame.iterrows():
        row_lists = list(row)
        if row_lists[0] == '':
            sys.exit()
        signIn(row_lists)


if __name__ == "__main__":
    excel()

