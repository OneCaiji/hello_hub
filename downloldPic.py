# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 15:16:56 2019

@author: 谁又动我电脑
"""

import requests
from lxml import etree
import datetime
import os
import progressbar
import re


headers1 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"
        }
headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Referer":"https://i.meizitu.net"
        }

url = 'https://www.mzitu.com/search/'
#
def get_ElementList(url,xpath):
    try:
        url_HTML = requests.get(url,timeout = 10,headers = headers1)
    except:
        print('网络连接失败')
    url_Content = etree.HTML(url_HTML.text)
    url_Element_List = url_Content.xpath(xpath)
    return url_Element_List
#download
def download_Pic(path,url):
    try:
        pic_HTML = requests.get(url,timeout = 10,headers = headers2)
    except:
        print('连接失败！')
    try:
        with open(path,'wb') as f:
            f.write(pic_HTML.content)
            f.close()
    except:
        pass
#
def get_Urllist(keyword):
    Name_Url = dict()
    pic_urlList = []
    node_li_list = []
    
    search_url = url + '/' + keyword 
    #number of page
    page_num = int(get_ElementList(search_url,'/html/body/div[2]/div[1]/div[2]/nav/div/a[last()-1]')[0].text)
    for i in range(1,page_num+1):
        node_li_list += get_ElementList(search_url+'/page/'+str(i),'//*[@id="pins"]//li')
    print('正在获取图片地址:')
    p = progressbar.ProgressBar()
    for item in p(node_li_list):
        fold_Name = item.find('.//span/a').text
        fold_Name = re.sub(r'\?|:|<|>|\|',' ',fold_Name)
        Url = item.find('.//span/a').attrib['href']
        #number of pic
        pic_num = int(get_ElementList(Url,'/html/body/div[2]/div[1]/div[4]/a[last()-1]/span')[0].text)
        eg_url = get_ElementList(Url,'/html/body/div[2]/div[1]/div[3]/p/a/img')[0].attrib['src']
        for i in range(1,pic_num+1):
            if i < 10:
                pic_urlList.append(eg_url[:-5]+str(i)+'.jpg')
            else:
                pic_urlList.append(eg_url[:-6]+str(i)+'.jpg')        
        Name_Url.update({fold_Name:pic_urlList})
        pic_urlList = []
    return Name_Url

# 
def download(keyword):
    #
    try:
        os.makedirs('E://'+keyword)
    except:
        print('"' + keyword + '"' + '文件夹已创建或创建失败!')
    Name_Url = get_Urllist(keyword)
    for name,urllist in Name_Url.items():
        try:
            os.makedirs('E://'+keyword+'/'+name)
            print('正在下载图集:'+name+'……')
        except:
            print(name + '文件夹已创建或创建失败')
            continue
        p = progressbar.ProgressBar()
        for url in p(urllist):
            download_Pic('E://'+keyword+'/'+name+'/'+url[-6:-4]+'.jpg',url)
        
if __name__ == "__main__":
    starttime = datetime.datetime.now()
    download('黄楽然')
    
    endtime = datetime.datetime.now()
    print('用时为：' + str((endtime-starttime).seconds) + 's')
