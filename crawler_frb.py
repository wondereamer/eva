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

url_domain_frb = "https://www.federalreserve.gov"
url_frb_2019 = "https://www.federalreserve.gov/newsevents/pressreleases/2019-press.htm"
url_frb_2018 = "https://www.federalreserve.gov/newsevents/pressreleases/2018-press.htm"
url_frb_2017 = "https://www.federalreserve.gov/newsevents/pressreleases/2017-press.htm"
url_frb_2016 = "https://www.federalreserve.gov/newsevents/pressreleases/2016-press.htm"

base_dir = "/Users/wudongyang/Documents/Develop/projects_py/crawler/"
test_file = "./testfile.txt"

def crawler_FRB():
	html = urlopen(url_frb_2016)
	bsObj = BeautifulSoup(html, "html.parser")	
	events_list_obj = bsObj.find("div", {"class":"row eventlist"}).find("div", {"class":"col-xs-12 col-sm-8 col-md-8"})
	event_rows_obj = events_list_obj.findAll("div", {"class":"row"})

	# news_list = list()

	with open(base_dir + "csv_frb.csv", "a") as fw:
		csvwriter = csv.writer(fw)
		csvwriter.writerow(["title", "href", "date", "type", "content"])
		for event_row_obj in event_rows_obj:
			try:
				news = News()
				date_obj = event_row_obj.find("div", {"class":"col-xs-3 col-md-2 eventlist__time"})
				news.date = date_obj.find("time").text
				event_obj = event_row_obj.find("div", {"class":"col-xs-9 col-md-10 eventlist__event"})
				news.href = url_domain_frb + event_obj.find("a").attrs['href']
				news.title = event_obj.find("p").find("a").find("em").text
				news.type = event_obj.find("p", {"class":"eventlist__press"}).find("em").find("strong").text
				news.content = get_content(news.href)
				r = [news.title,news.href,news.date,news.type,news.content]
				csvwriter.writerow(r)
				# news_list.append(news)
			except:
				print("except..")
			
	# return news_list

def get_content(url):
	content_list = list()
	contents = ""
	html = urlopen(url)
	bsObj = BeautifulSoup(html, "html.parser")
	artical_obj = bsObj.find("div", {"id":"content"}).find("div", {"id":"article"})
	content_obj = artical_obj.find("div", {"class":"col-xs-12 col-sm-8 col-md-8"})
	content_ps_objs = content_obj.findAll("p")
	for content_p in content_ps_objs:
		content_list.append(content_p.text)
		contents = contents + content_p.text + "\n"
	return contents

def store_to_csv(news_list, csv_file):
	tocsv(news_list, csv_file)

if __name__ == "__main__":
	# news_list = crawler_FRB()
	crawler_FRB()
	base_dir = "/Users/wudongyang/Documents/Develop/projects_py/crawler/"
	# csv_file = base_dir + "csv_frb.csv"
	# store_to_csv(news_list,csv_file)
