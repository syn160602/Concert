# -*- coding: utf-8 -*-
#
# This is main file.
# Concert class is a ticket buyer, before execute we have to set the config that
# which site we are going to buy ticket.
# 'target_url' is the exact concert page we want,
# we should visit it first and then paste the url in code.
#
# created by suyuning@corp.netease.com
#

import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By

class Concert():
    def __init__(self, siteData, target_url):
        self.status = 0
        self.login_methon = 1
        self.driver = webdriver.Chrome()

        self.site_url = siteData['site_url']
        self.site_title = siteData['site_title']
        self.login_url = siteData['login_url']
        self.login_succ_flag = siteData['login_succ_flag']
        # self.can_buy_list = siteData['can_buy_list']

        self.target_url = target_url

    def set_cookies(self):
        self.driver.get(self.site_url)
        while 1:
            print('######点击登录######')
            while self.driver.title.find(self.site_title) != -1:
                time.sleep(1)
            # 程序控制浏览器, 账号密码或者手机短信登录可能无法通过验证
            print('######扫码登录######')
            while self.driver.title.find(self.site_title) == -1:
                time.sleep(1)
            # 可以根据self.driver.get_cookies()函数返回的内容判断是否有扫码登录成功的行为
            if self._isScanningSuccess(self.driver.get_cookies()):
                print('######扫码完成######')
                pickle.dump(self.driver.get_cookies(), open('cookies.pkl', 'wb'))
                print('######保存cookies成功######')
                self.status = 1
                self.driver.get(self.target_url)
                break

    def get_cookies(self):
        cookies = pickle.load(open('cookies.pkl', 'rb'))
        for cookie in cookies:
            cookie_dict = {
                'domain': cookie.get('domain'),
                'name' : cookie.get('name'),
                'value' : cookie.get('value')
            }
            self.driver.add_cookie(cookie_dict)
        print('######载入cookies######')

    def clear_cookies(self):
        if os.path.exists('cookies.pkl'):
            os.remove('cookies.pkl')

    def login(self):
        if self.login_methon == 0:
            self.driver.get(self.login_url)
            print('######开始登录######')
        elif self.login_methon == 1:
            if not os.path.exists('cookies.pkl'):
                self.set_cookies()
            else:
                # 已有登录数据, 直接跳转抢票页面, 并自动登录
                self.driver.get(self.target_url)
                self.get_cookies()

    def enter_concert(self):
        print('######打开浏览器并进入网站主页######')
        self.login()
        # 刷新页面
        self.driver.refresh()
        # 登录成功
        self.status = 2
        print('######登录成功######')
        # 处理弹窗
        if self._isElementExist(By.XPATH, '/html/body/div[2]/div[2]/div/div/div[3]/div[2]'):
            self.driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div[3]/div[2]').click()

    def choose_ticket(self):
        # 抢票并下单
        if self.status == 2:
            print('=' * 30)
            print('######选择日期和票价######')
            while self.driver.title.find('确认订单') == -1:
                buyButton = None
                if self._isElementExist(By.CLASS_NAME, 'buybtn'):
                    buyButton = self.driver.find_element(By.CLASS_NAME, 'buybtn')
                elif self._isElementExist(By.CLASS_NAME, 'buy-link'):
                    buyButton = self.driver.find_element(By.CLASS_NAME, 'buy-link')
                else:
                    print('######没有找到购买按钮, 需要自行查看网页元素######')
                if buyButton.text == '提交缺货登记':
                    self.status = 2
                    # 刷新页面, 重新尝试抢票
                    # TODO: 能否尝试其他策略, 开放预选时间、价位区间, 当前没票可以选其他的
                    self.driver.get(self.target_url)
                    continue
                buyButton.click()
                self.status = 3

                title = self.driver.title
                if title == '选座购买':
                    # 选座特殊处理
                    self.choose_seats()
                elif title == '确认订单':
                    while 1:
                        print('加载中......')
                        if self._isElementExist('//*[@id="container]/div/div[9]/button'):
                            # 实名信息存在, 可以下单
                            self.check_order()
                            break

    def choose_seats(self):
        while self.driver.title == '选座购买':
            while self._isElementExist('//*[@id="app]/div[2]/div[2]/div[1]/div[2]/img'):
                print('快速选择座位！！！！！！！')
                # TODO: 考虑加入用户自定义变量, 支持脚本自动随机选座
            while self._isElementExist('//*[@id="app]/div[2]/div[2]/div[2]/div'):
                self.driver.find_element(By.XPATH, '//*[@id="app]/div[2]/div[2]/div[2]/button').click()

    def check_order(self):
        if self.status == 3:
            print('######正在进行订单确认######')
            time.sleep(0.5)
            try:
                # 选取第一个购票人信息
                self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[2]/div[2]/div[1]/div/label').click()
            except Exception as e:
                print('######购票人信息选中失败, 需要自行查看元素位置######')
                print(e)
            # 提交订单
            time.sleep(0.5)
            self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[9]/button').click()
            time.sleep(20)

    def finish(self):
        self.driver.quit()

    def _isScanningSuccess(self, cookies):
        for cookie in cookies:
            name = cookie.get('name')
            if name == self.login_succ_flag:
                return True
        return False

    def _isElementExist(self, by, element):
        browser = self.driver
        try:
            browser.find_element(by, element)
            return True
        except:
            return False
    