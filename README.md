# 中山学院健康上报打卡

需要安装selenium, 使用chromedriver/geckodriver取决于使用谷歌还是火狐

* 需要修改如下信息：uaid, 手机号, 籍贯, 家乡所在地, 当前所在地, 邮箱信息
* 邮箱信息非必须, 如不需要请删除
* 其他信息默认正常无需修改

#### uaid获取方式: 学校公众号打开打卡信息, 右上角复制链接, 链接后即为uaid

由于selenium3.141版本不支持92版本chrome使用静默模式(不打开浏览器窗口模式), 于是在服务器上我选择的是firefox, geckodriver

### 邮箱定时发送提醒邮件
邮箱部分可参考: https://www.runoob.com/python/python-email.html
QQ邮箱教程拉至最下即可看到

### 服务器测试能否运行
安装完python后输入 python3 test.py

### 服务器定时执行
使用crontab, 可参考: https://www.runoob.com/w3cnote/linux-crontab-tasks.html

如 0 7 * * * . /etc/profile;python3 /project/test.py 为每日7点执行程序
