'''
@Description:
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
@LastEditors: Demoon
@LastEditTime: 2020-07-01 11:13:46
'''
#  基础模块
import sys
import time
import json
#   selenium相关
from selenium import webdriver
#   qt5
from PyQt5 import QtWidgets
from PyQt5.Qt import QThread
from PyQt5.QtCore import pyqtSignal, QObject, QDate, Qt
#   引入ui文件
from home import Ui_MainWindow as Ui
#   引入登录模块
import login as lgm
#   引入requests类
from UploadData import UploadData as UpData
from MpGather import MpGather
import utils as myTools


class MyApp(QtWidgets.QMainWindow, Ui):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.account_info = None
        self.browser = None
        self.threadPools = []
        Ui.__init__(self)
        self.setupUi(self)
        self._initdata()
        self.signinButton.clicked.connect(self.signin)

    #   数据初始化
    def _initdata(self):
        with open("./config-default.json", encoding='utf-8') as defcfg:
            cfg = json.load(defcfg)
        notelist = cfg['instructions'].split('；')
        for line in notelist:
            self.log(line, False)
        today = QDate.currentDate()
        self.DateEdit.setDate(today)
        self.DateEdit.setCalendarPopup(True)
        self.DateEdit_2.setCalendarPopup(True)
        self.DateEdit_2.setDate(today.addDays(-2))

    #   时间处理
    def _timeCheck(self):
        endDate = self.DateEdit.date()
        startDate = self.DateEdit_2.date()
        days = startDate.daysTo(endDate)
        if days < 0:
            QtWidgets.QMessageBox.information(self, '提示', '请选择正确日期！', QtWidgets.QMessageBox.Yes)
            return False
        elif days > 8:
            QtWidgets.QMessageBox.information(self, '提示', '最多采集8日数据！', QtWidgets.QMessageBox.Yes)
            return False
        return (self.DateEdit_2.date(), self.DateEdit.date())

    #   按钮触发
    def signin(self):
        dates = self._timeCheck()
        if dates:
            self.lgGether(dates)

    #   登录并采集
    def lgGether(self, dateary: tuple):
        self.browser = browserInit()
        jump_urls = lgm.mp_weixin_login(self.browser, URL['mp_weixin_login'])
        self.log('广告主总计'+str(len(jump_urls)) + '个，开始采集')
        for idx, url in enumerate(jump_urls):
            cookies, token = lgm.mp_weixin_jump(self.browser, url)
            comp_info = '广告主 ' + str(idx+1) + ' 完成'
            th = MpThread(cookies, token, comp_info, dateary)
            th.sig.completed.connect(self.log)
            self.threadPools.append(th)
            th.start()
        self.browser.quit()

    #    输出信息
    def log(self, text, line=True):
        if line:
            self.logView.appendPlainText('-' * 20)
        self.logView.appendPlainText(text)
        return True


#   自定义的信号  完成信号
class CompletionSignal(QObject):
    completed = pyqtSignal(str)


# oppo采集线程
class MpThread(QThread):
    def __init__(self, cookies: dict, token: str, loginfo: str, dateary: tuple):
        super().__init__()
        self.cookies = cookies
        self.token = token
        self.info = loginfo
        self.dateAry = dateary
        self.sig = CompletionSignal()

    def run(self):
        up = UpData()
        #   开发平台数据采集
        ger = MpGather(self.cookies, self.token, self.dateAry)
        res = ger.runCollect()
        up.up('addWeixinMp', res)
        self.sig.completed.emit(self.info)


# 浏览器开启
def browserInit():
    # 实例化一个chrome浏览器
    chrome_options = webdriver.ChromeOptions()
    # options.add_argument(".\ChromePortable\App\Chrome\chrome.exe");
    chrome_options.binary_location = ".\\ChromePortable\\App\\Chrome\\chrome.exe"
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # browser = webdriver.Chrome(options=chrome_options)
    browser = webdriver.Chrome(options=chrome_options)
    return browser


if __name__ == '__main__':
    # 定义为全局变量，方便其他模块使用
    global URL, RUN_EVN
    # 登录界面的url
    URL = {
        "mp_weixin_login": "https://a.weixin.qq.com/index.html",
    }
    try:
        RUN_EVN = sys.argv[1]
    except Exception:
        pass
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
