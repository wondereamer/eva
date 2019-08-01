import re
import os
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import time
from news import News
from database import *
from tocsv import tocsv
import pandas as pd

url_domain_pboc = "http://www.pbc.gov.cn/"
base_dir = "/Users/wudongyang/Documents/Develop/projects_py/crawler/"
news_list_indexes_file = base_dir + "pboc_news_indexes.csv"
out_file = base_dir + "csv_pboc.csv"

def crawler_PBOC():

    with open(news_list_indexes_file, "r") as fr:
        with open(out_file, "w") as fw:
            csvwriter = csv.writer(fw)
            csvwriter.writerow(["title", "href", "date", "content"])
            for index_url in fr.readlines():
                # print(index_url)
                html = urlopen(index_url)
                # print(html)
                bsObj = BeautifulSoup(html, "lxml")
                print(bsObj)

                news_objs = bsObj.find("div", {"class":"mainw950"})\
                    .find("div", {"opentype":"page"}).find("td", {"colspan":"2"})\
                    .find("div", {"id":"r_con"}).find("div", {"class":"portlet"})\
                    .find("div", {"style":"height:480px"}).find("table").find("td").findAll("table")
                # print(news_objs)
                # return
                for news_obj in news_objs:
                    try:
                        news = News()
                        news.date = news_obj.find("span", {"class":"hui12"})
                        news.href = url_domain_pboc + news_obj.find("a").attrs['href']
                        news.title = news_obj.find("a").text
                        news.content = getget_content(news.href)
                        r = [news.title,news.href,news.date,news.content]
                        csvwriter.writerow(r)
                    except:
                        print("except..")

def get_content(url):
	content_list = list()
	contents = ""
	html = urlopen(url)
	bsObj = BeautifulSoup(html, "html.parser")
	content_obj = bsObj.find("div", {"id":"zoom"})
	content_ps_objs = content_obj.findAll("p")
	for content_p in content_ps_objs:
		content_list.append(content_p.text)
		contents = contents + content_p.text + "\n"
	return contents

def store_to_csv(news_list, csv_file):
	tocsv(news_list, csv_file)

if __name__ == "__main__":
	crawler_PBOC()
	base_dir = "/Users/wudongyang/Documents/Develop/projects_py/crawler/"