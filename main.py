import time
import subprocess
from ping3 import ping, verbose_ping
from playwright.sync_api import Playwright, sync_playwright

def loginCampusNet():
    
    pass

IP_LIST=[
    "220.181.38.150", 
    "111.30.185.60", # "http://qq.com/"

    
    # "http://www.baidu.com/",
    
    # "http://www.sina.com.cn/",
    # "http://www.csdn.net",
    # "http://alibaba.cn/",
    # "http://www.baidu.com/",
    # "http://qq.com/",
    # "http://www.sina.com.cn/",
    # "http://www.csdn.net",
    # "http://alibaba.cn/",
]

# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=True)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("http://m.njust.edu.cn")
#     time.sleep(1)
#     # page.screenshot(path="example2.png")
    
#     browser.close()

# with sync_playwright() as playwright:
#     run(playwright)

def request(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    for i in range(10):
        start = time.perf_counter()
        response = page.goto(URL_LIST[i])
        if response.status == 200:
            print("请求成功！")
        else:
            print("请求失败！")
        end = time.perf_counter()
        print(end-start)
    browser.close()

def ping_some_ip(host,src_addr=None):
    second = ping(host,src_addr=src_addr,timeout=0.1)
    return second

if __name__ == "__main__":
    # start = time.perf_counter()
    # with sync_playwright() as playwright:
    #     request(playwright)
    # end = time.perf_counter()
    # print(end-start)
    for i in range(10):
        result = ping_some_ip(IP_LIST[0])
        if result is None:
                print(result)
                print('ping 失败！')
        else:
            print('ping-{}成功，耗时{}s'.format(IP_LIST[0],result))