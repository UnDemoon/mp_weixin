'''
@Description: 登录模块
@Version: 1.0
@Autor: Demoon
@Date: 1970-01-01 08:00:00
@LastEditors: Demoon
@LastEditTime: 2020-06-09 12:04:41
'''
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import urllib
import time


# 登录
def mp_weixin_login(browser: object, url: str):
    browser.set_page_load_timeout(8)
    try:
        browser.get(url)
    except BaseException:
        # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
        browser.execute_script("window.stop()")
    #   长等待获取是否获取用户名
    long_wait = WebDriverWait(browser, 120)
    a_tag_list = False
    try:
        els = long_wait.until(lambda x: x.find_elements_by_xpath("//*[@class='Table_new__table-3fEjG']//a[@class='ui-mr-medium ui-d-ib']"))
        # long_wait.until(
        #     EC.presence_of_element_located(
        #         (By.CSS_SELECTOR, '[class~="CoreLayout__accountInfo-3aUYF"]')))
        # els = browser.find_elements_by_xpath("//*[@class='Table_new__table-3fEjG']//a[@class='ui-mr-medium ui-d-ib']")
        a_tag_list = list(map(lambda x: x.get_attribute("href"), els))
    except BaseException:
        pass
    return a_tag_list


def mp_weixin_jump(browser: object, url: str):
    browser.set_page_load_timeout(5)
    try:
        browser.get(url)
    except BaseException:
        # 当页面加载时间超过设定时间，通过js来stop，即可执行后续动作
        browser.execute_script("window.stop()")
    wait = WebDriverWait(browser, 8)
    cookies = False
    token = False
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[class~="nickname"]')))
        cookies = browser.get_cookies()
        result = urllib.parse.urlparse(browser.current_url)
        result = urllib.parse.parse_qs(result.query)
        token = result.get('token')[0]
    except BaseException:
        pass
    return (cookies, token)
