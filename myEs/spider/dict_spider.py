#-*- coding = utf-8 -*-
#@Time : 2020/9/27 11:09
#@Author : straightup
"""
爬虫文件,爬取柯林斯词典
https://www.collinsdictionary.com/browse/english/words-starting-with-a
"""
import time
import requests
from lxml import etree
from multiprocessing.dummy import Pool

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}
url = 'https://www.collinsdictionary.com/browse/english/words-starting-with-%s'
initial_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
urls = [(url%i) for i in initial_list]

deep_url_list = []  #装真正爬取词组的url

def get_urls(url):
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    url_list = tree.xpath('//*[@id="main_content"]/div[2]/div/div/ul[2]/li/a/@href')
    deep_url_list.extend(url_list)

def get_words(url):
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//*[@id="main_content"]/div[2]/div/div/ul[2]/li')
    with open("word.txt", "a", encoding="utf-8") as f:
        for li in li_list:
            word = li.xpath('./a/text()')[0]
            f.write(word + '\n')

start = time.time()
pool = Pool(26)
pool.map(get_urls, urls)
result = pool.map_async(get_words, deep_url_list)
result.wait()
print("执行完毕")
print("耗时：", time.time()-start)


