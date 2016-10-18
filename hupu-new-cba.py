 #-*- coding: cp936 -*- 
 import re,time,os,uuid 
 from urlfetch import get 
 import urllib 
 import requests,sys 
 import pymongo 
 import traceback 
 import bs4 as bs 
from lxml import etree 
 #图片存放路径 
 imgstore = "/sports/image/news" 
 #获取网页 
 def get_page(link): 
     try: 
         page = requests.get(link) 
         return page.content 
     except: 
         return "" 
 #获取图片 
 def get_image_page(link): 
     try: 
         r = urllib.request.urlopen(link) 
         content = r.read() 
         return content 
     except: 
         return "" 
 
 def get_page_etree(link): 
     try: 
         page = str(get_page(link)) 
         tree = etree.HTML(page) 
         return tree 
     except: 
         return "" 
 
 
 def get_page_soup(link): 
     try: 
         page = get_page(link) 
         soup = bs.BeautifulSoup(page) 
         return  soup 
     except: 
         return "" 
 
 
 class article: 
     def __init__(self,db,link): 
         self.db = db 
         self.link = link 
   
     def get_img(self,link): 
         pic = get_image_page(link) 
         if os.path.exists(imgstore)==False: 
             os.makedirs(imgstore) 
         if link[link.rfind("/"):].find(".") == -1: 
             suffix = ".jpg" 
         else: 
             suffix = link[link.rfind("."):] 
         imagename = str(uuid.uuid1()).replace("-","")+suffix 
         files = imgstore + "/"+imagename 
         f = open(files,"w") 
         f.write(pic) 
         f.close() 
         if os.path.exists(files)==True: 
             return imagename 
         else: 
             return "" 
 
 
     def get_article(self,link): 
         tag = "NBA" 
         tree = get_page_etree(link) 
         news_list = tree.xpath('//div[@class="voice-main"]/div[@class="news-list"]/ul/li[1]') 
         #print news_list 
         for news in news_list: 
             title = "" 
             desc = "" 
             image = "" 
             source = "" 
             author = "" 
             date = "" 
             content = "" 
             keyword = "" 
             try: 
                 title = news.xpath(".//h4/a/text()")[0] 
             except: 
                 continue 
             if db.hupu.find({"title":title})!=None: 
                 continue 
             href = news.xpath(".//h4/a/@href")[0] 
             try: 
                 desc = news.xpath(".//span[@class='J_share_title']/text()")[0] 
             except: 
                 print "no desc" 
             try: 
                 source = news.xpath(".//span[@class='comeFrom']/a/text()")[0] 
             except: 
                 print "no source" 
             try: 
                 date = news.xpath(".//a[@class='time']/@title")[0] 
                 date = date[0:10] 
             except: 
                 print "no date" 
             d_tree = get_page_etree(href) 
             d_soup = get_page_soup(href) 
             imglink = d_tree.xpath('//div[@class="artical-content"]/div/div/img/@src')[0] 
             image = self.get_img(imglink) 
             try: 
                 contentss = d_soup.find("div","artical-content").find("div","artical-main-content") 
                 contents = contentss.findAll("p") 
                 for p in contents: 
                     content = content + str(p) 
                     if p.find("img")>=0: 
                         img_links = p.findAll("img") 
                         for img_link in img_links: 
                             src = img_link["src"] 
                             name = self.get_img(src) 
                             content = content.replace(src,"name") 
             except: 
                 print "no content" 
             try: 
                 keyword = d_tree.xpath(".//div[@class='relatedTag']/div/a/text()")[0] 
             except: 
                 print "no keyword" 
             mess = {"title":title, 
                     "image":image, 
                     "source":source, 
                     "author":author, 
                     "keyword":keyword, 
                     "datetime":date, 
                     "tag":tag, 
                     "flow":0, 
                     "descip":desc, 
                     "content":content, 
                     "comment":{}} 
             db.hupu.insert_one(mess) 
 

     def run(self): 
         self.get_article(self.link) 
         self.db.remove
 
 client = pymongo.MongoClient("localhost", 27017) 
 db = client.news 
 

 #共100页 
 for i in range(1,2): 
     try: 
         url = "http://voice.hupu.com/cba/"+str(i) 
         print url 
         article(db,url).run() 
         time.sleep(3) 
     except: 
         print traceback.print_exc() 
         time.sleep(3) 
