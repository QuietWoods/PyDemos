#!/usr/bin python  
# -*- coding:utf-8 -*-  
""" 
@author: quietwoods 
@file: crawl2.py 
@time: 2020/05/09
@contact: wanglei2xf@163.com
@site:  
@software: PyCharm 
"""
import pandas as pd
import time
import requests
import json
from bs4 import BeautifulSoup  # 解析网页数据

# 构造循环爬取的函数
def format_url(base_url, num):
    base_url = base_url + "&s=44"
    urls = []
    for i in range(44, num * 44, 44):
        urls.append(base_url[:-2] + str(i))
    return urls


# 解析和爬取单个网页
def parse_page(url, cookies, headers):
    result = pd.DataFrame()
    html = requests.get(url, headers=headers, cookies=cookies)
    bs = html.text
    # 获取头部索引地址
    start = bs.find('g_page_config = ') + len('g_page_config = ')
    # 获取尾部索引地址
    end = bs.find('"shopcardOff":true}') + len('"shopcardOff":true}')
    js = json.loads(bs[start:end + 1])
    status = js['mods']['itemlist']['status']
    if status == "hide":
        return result

    # 所有数据都在这个auctions中
    for i in js['mods']['itemlist']['data']['auctions']:
        # 产品标题
        product = i['raw_title']
        # 店铺名称
        market = i['nick']
        # 店铺地址
        place = i['item_loc']
        # 价格
        price = i['view_price']
        # 收货人数
        if 'view_sales' in i:
            sales = i['view_sales']
        else:
            sales = None
        url = 'https:' + i['detail_url']
        r = pd.DataFrame({'店铺': [market], '店铺地址': [place], '价格': [price],
                          '收货人数': [sales], '网址': [url], '产品标题': [product]})
        result = pd.concat([result, r])

        # parse_detail_page(url, cookies, headers)
    time.sleep(5.20)
    return result


# 解析和爬取单个网页
def parse_detail_page(url, cookies, headers):
    result = pd.DataFrame()
    html = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(html.text, 'html.parser')

    item = soup.find("div", class_="attributes")

    content = item.text.strip()

    # r = pd.DataFrame({'店铺': [market], '店铺地址': [place], '价格': [price],
    #                       '收货人数': [sales], '网址': [url], '产品标题': [product]})
    # result = pd.concat([result, r])
    time.sleep(5.20)
    return result


# 汇总
def main(filename):
    # 爬取的基准网页（s = 0）

    base_url = 'https://s.taobao.com/search?q=%E6%B4%97%E5%8F%91%E6%B0%B4&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=0'
    base_url = 'https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20200509&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E7%89%9B%E5%A5%B6&suggest=history_1&_input_charset=utf-8&wq=&suggest_query=&source=suggest&cps=yes&cat=51152013'
    base_url = "https://s.taobao.com/search?q=%E7%89%9B%E5%A5%B6&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200509&ie=utf8"
    # 定义好headers和cookies

    cookies = {'cookie': '输入自己的COOKIES'}

    cookies = {"cookie": "t=d2e37a3b7265d5c4c975d6b298894110; cna=Uyk8FxGYxAECAXzK8gb4tej9; tfstk=cIfFBmwo3xh_GSNOHBdyRfOsno_dZyQhrf8XKtPKNwZrqBphiRnJS_aH7UtYspf..; sgcookie=EoeSAdzd6sgRjZO7AEY0n; uc3=vt3=F8dBxGXJZUWsNNDgaIA%3D&nk2=31zW%2BjjIgyaFpYk%3D&lg2=UIHiLt3xD8xYTw%3D%3D&id2=UoH635Dl1q76xQ%3D%3D; lgc=%5Cu5BC2%5Cu9759%5Cu7684%5Cu6797%5Cu5B503; uc4=nk4=0%403ahT5cxhkHTNNWFIKco24bu%2FYmFubg%3D%3D&id4=0%40UOnlYBmhoPRlwLkT7Gu9GK3xbWHV; tracknick=%5Cu5BC2%5Cu9759%5Cu7684%5Cu6797%5Cu5B503; _cc_=URm48syIZQ%3D%3D; enc=0RYnkLgNA%2FSAvkfPGfZCY%2FO43hdaTqDtDSd2xWwjCcJQUYxr49gkhvsIU%2BEQuG2LfovCLxt0M2%2BrnQ4jUlkIXw%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; mt=ci=5_1; JSESSIONID=1722EBB2F854C37C821EFF813EB30562; isg=BHZ2nbKXNHddgMCQK6Kt7H9sx6V4l7rRaYPImeBfYtn0Ixa9SCcK4dzRP_dPkLLp; l=eBj6lCQgQGHusefCBOfaFurza77OSIRYYuPzaNbMiT5P_41B5sO5WZbyE786C3GNh6bkR3kTM5OHBeYBYQAonxv92j-la_kmn"}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    # 设置好存储结果的变量

    current_page = 1
    # 循环爬取5页
    for url in format_url(base_url, 100):
        print(current_page)
        print(url)
        current_page += 1
        # final_result = pd.concat([final_result, parse_page(url, cookies=cookies, headers=headers)])
        result_df = parse_page(url, cookies=cookies, headers=headers)
        result_df.to_csv(filename, mode='a+')

    return True


if __name__ == "__main__":
    keyword = "牛奶"
    filename = keyword + '_' + time.strftime(
        "%Y-%m-%d_%H-%M-%S",
        time.localtime(time.time())) + '.csv'
    final_result = main(filename)

    if final_result:
        print("end successfully..")
    else:
        print('end error..')
    # final_result.to_csv('tt.csv')
