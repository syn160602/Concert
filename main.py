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

import siteData
from concert import Concert
        
if __name__ == '__main__':
    # 选择抢票网站, 会使用对应网站的相关配置
    siteConfig = siteData.SiteConfig.DAMAI
    # 具体门票页面
    target_url = 'https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.556e4d15oCe5uA&id=739750721138&clicktitle=2023%E4%B8%8A%E6%B5%B7%E7%AE%80%E5%8D%95%E7%94%9F%E6%B4%BB%E8%8A%82'
    concert = Concert(siteData.siteDataDict.get(siteConfig), target_url)
    while 1:
        try:
            concert.enter_concert()
            concert.choose_ticket()
        except Exception as e:
            if type(e).__name__ == 'NoSuchWindowException':
                print('######用户手动关闭浏览器, 程序退出######')
                break
            elif type(e).__name__ == 'InvalidCookieDomainException':
                print('######登录信息失效, 需要重新手动登录######')
                concert.clear_cookies()
            elif type(e).__name__ == 'AttributeError':
                print('######网页元素未找到, 需要自行查看元素位置, 程序退出######')
                break