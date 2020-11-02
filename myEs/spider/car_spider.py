#-*- coding = utf-8 -*-
#@Time : 2020/9/27 11:09
#@Author : straightup
"""
爬虫文件,爬取汽车之家新闻
目标:文章标题 标题链接(+文章分类) 图片链接 首页简介
https://www.autohome.com.cn/all/
"""
import time
import requests
from lxml import etree
from multiprocessing.dummy import Pool

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}
url = 'https://www.autohome.com.cn/all/%d/#liststart'

urls = [(url % i) for i in range(3005, 6006)]

def get_data(url):
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//*[@id="auto-channel-lazyload-article"]/ul/li')
    with open("car2.txt", "a", encoding="utf-8") as f:
        for li in li_list:
            try:
                title = li.xpath('./a/h3/text()')[0]
                title_url = 'https:'+li.xpath('./a/@href')[0]
                tag = title_url.split('/')[3]
                img_url = 'https:'+li.xpath('./a/div[1]/img/@src')[0]
                desc = li.xpath('./a/p/text()')[0]
                # 写入文件
                data = title + '|' + title_url + '|' + desc + '|' + tag + '|' + img_url
                f.write(data + '\n')
            except:
                continue

start = time.time()
pool = Pool(50)
pool.map(get_data, urls)
print("执行完毕")
print("耗时：", time.time()-start)

