# ========================================================================================
# 方案1. 校园网连接成功后,一般有24小时的连续在线时长,可以考虑在中途抽取时间点测试,在24小时附近重点测试
# 方案2. 每隔(10ms) ping一次网路, 成功则表示校园网正常,失败则表示断网,然后去执行联网函数
# 方案3. 直接无脑搁一段时间重新登出再登入校园网,刷新它的连续在线时长.
# 目前使用方案3,最简单.
# 注意:用ping判断断网与否比用request请求速度更快,甚至可以快一个数量级.
# ========================================================================================

import time
import random
import threading
import subprocess
from ping3 import ping
from playwright.sync_api import Playwright, sync_playwright

# global variables
dog_flag = True # dog为真,表示断网;dog为假,表示联网.
login_flag = False # login为真,表示联网;login为假,表示断网.
IP_LIST=[
    "180.97.36.72", # http://www.hao123.com/tejia
    "222.186.18.89", # https://auto.sina.com.cn/
    "112.25.53.216",
    "58.222.19.24", # https://www.zol.com.cn/
    "180.97.36.72", # http://tuijian.hao123.com/
    "153.35.100.139", # "https://www.made-in-china.com/"
    "223.109.128.92", # "https://www.qcc.com/"
    "222.186.18.88", # "https://www.qcc.com/"
    "112.25.53.216", # "https://www.sina.com.cn/"
    "222.186.184.150", # "https://www.jd.com/"
    "58.215.98.111", # "https://www.zhihu.com/hot"
    "112.25.53.216", # "http://www.sina.com.cn/"
    "180.101.50.188", # "http://www.baidu.com/"
    ########
    "49.79.225.41", # https://www.runoob.com/
    "36.150.14.114", # "https://www.4399.com/"
    "118.184.173.40", # "https://www.sogou.com/"
    "218.98.31.67", # "https://www.suning.com/"
    "218.78.243.233", # "http://www.gov.cn/"
]

def ping_watchdog():
    time_circles = [0.01,0.02,0.03,0.04,0.05,0.06]
    jdx = 0
    num_ips = len(IP_LIST)
    idx = random.randint(0, num_ips-1)
    while True:
        result = ping(IP_LIST[idx],src_addr=None,timeout=0.05) # 50ms内不响应视为失败.
        if result is None:
            dog_flag = True
        print(f"ping-{IP_LIST[idx]}成功，耗时{result}s")
        idx += 1
        idx %= num_ips
        time.sleep(time_circles[jdx])
        jdx += 1
        jdx %= len(time_circles)


def loginCampusNet(playwright: Playwright):
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://m.njust.edu.cn")
        page.fill("id=username", "XXXXXX")
        page.fill("id=password", "******")
        if not page.is_checked('#ck_rmbUser'):
            page.check('#ck_rmbUser')
        # page.screenshot(path="before_login.png")
        page.click("id=loginBtn")
        # page.screenshot(path="after_login.png")
        login_flag = True
        dog_flag = False
    except:
        print(u"登陆函数异常")
        login_flag = False
    finally:
        browser.close()

def logout(playwright: Playwright):
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://m.njust.edu.cn")
        page.fill("id=username", "XXXXXXX")
        page.fill("id=password", "*******")
        if not page.is_checked('#ck_rmbUser'):
            page.check('#ck_rmbUser')
        # page.screenshot(path="before_login.png")
        page.click("id=loginBtn")
        time.sleep(0.5)
        # page.screenshot(path="after_login.png")
        login_flag = True
        dog_flag = False
    except:
        print(u"退出函数异常")
        login_flag = False
    finally:
        browser.close()

def logout_login(playwright: Playwright):
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("http://m.njust.edu.cn")
        page.click("id=logoutBtn")
        time.sleep(0.3)
        # print("logout")
        page.screenshot(path="logout.png")
        page.fill("id=username", "XXXXXX")
        page.fill("id=password", "******")
        if not page.is_checked('#ck_rmbUser'):
            page.check('#ck_rmbUser')
        # page.screenshot(path="before_login.png")
        time.sleep(0.35)
        page.click("id=loginBtn")
        # print("login")
        page.screenshot(path="after_login.png")
        # login_flag = True
        # dog_flag = False
    except:
        print(u"函数异常")
        login_flag = False
    finally:
        browser.close()

if __name__ == "__main__":
    print (u"Hi,校园网自动登陆脚本正在运行")
    while True:
        with sync_playwright() as playwright:
            logout_login(playwright)
        print("登出登入成功")
        time.sleep(60*60*24-20)
        
    #     if dog_flag and not login_flag: # 表示断网
    #         with sync_playwright() as playwright:
    #             login_flag = loginCampusNet(playwright)
    #     if not dog_flag and login_flag: # 登录成功
    #         login_time = time.time()
    #         
    #         t.start()
    
