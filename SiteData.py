# -*- coding: utf-8 -*-
#
# this is a helper
# record url and title for different sites
# if the bat executed unsccessfully, try to open the site manually and check the data
#
# created by suyuning@corp.netease.com
#

from enum import Enum

class SiteConfig(Enum):
    # 大麦网
    DAMAI = 1,

siteData = {
    SiteConfig.DAMAI: {
        # 网站主页
        'site_url' : 'https://www.damai.cn/',
        # 主页标题
        'site_title' : '大麦网-全球演出赛事官方购票平台',
        # 账号登陆页面
        'login_url' : 'https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F',
        # 登录成功cookie标志
        'login_succ_flag' : 'damai.cn_user',
        # 可以点击的购买按钮
        'can_buy_button' : ['立即预定', '立即购买', '选座购买'],
    },
}