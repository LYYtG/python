#!/usr/bin/env python

# -*- coding: utf-8 -*-


## 本程序使用bs4+lxml方式对网页元素进行解析和查找，并输出到文本文件中
# 3190103519 李杨野
# 2021-9-22 

import requests
import lxml
from bs4 import BeautifulSoup
import re
#打开文件ZJUnews.txt 将输出结果保存到文本文件中
f = open('ZJUnews.txt', "w",encoding='utf-8')
#采用伪装成浏览器的策略应对反爬
Header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
#主网址
url1 = 'http://www.zju.edu.cn'
#利用requests获取网页源代码，利用BS4进行解析
zju = requests.get(url1,headers=Header)
zjuobj = BeautifulSoup(zju.content,'lxml')
#获取主页面的分类列表文本
for j in range(1,11):
    jmenu = (zjuobj.find(id = 'jMenu')).find(class_ = 'subcon i'+str(j))
    f.write(jmenu.a.string+'\n')
    k = 1
    submenu = jmenu.find(class_ = 'i'+str(j)+'-'+str(k))
    while(submenu!=None):
        f.write('\t'+submenu.a.string+'\n')
        k = k+1
        submenu = jmenu.find(class_ = 'i'+str(j)+'-'+str(k))
#获取新闻板块所在模块信息
title = zjuobj.find(class_ = 'news-bottom')
t = title.div
#利用正则表达式匹配对应的模块
lists = title.find_all('div', attrs = {"frag":re.compile('面板2*')})
i = 1
#通过获取href中的超链接，进入各个分类的新闻页面，对子页面分别解析
for a in lists:
    t2 = t.find('h2',attrs = {'id':'news_tab'+str(i)})
    i = i+1
    f.write(t2.string+'\n')
    b = a.find('li',attrs = {'style':'text-align:right'})
    #该网站第四个页面的链接类型与其他页面类型不同，单独提出
    if(i == 5):
        link = '/wtxw/list.htm'
    else:
        link = b.a['href']
    for page in range(1,6):
        #构建子页面链接
        if(page == 1):
            url = url1+link[0:-4]+'.htm'
        else:
            url = url1+link[0:-4]+str(page)+'.htm'
        subpage = requests.get(url,headers=Header)
        #防止子页面报错，采用try-except策略
        try:
            subpageobj = BeautifulSoup(subpage.content,'lxml').find(class_ = 'news')
            newslist = subpageobj.find_all('li')
            f.write('   第'+str(page)+'页'+'\n')
            for news in newslist:
                f.write('\t'+news.a['title']+'\n')
            del subpage,subpageobj
        except:
            continue
#关闭文本文件
f.close()