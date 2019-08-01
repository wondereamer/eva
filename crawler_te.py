import re
import os
import csv
import json
import jsonlines
from urllib.request import urlopen
import requests
# import md5
url_domain_tradingeconomics = "https://tradingeconomics.com"
base_dir = "/Users/wudongyang/Documents/Develop/projects_py/crawler/"
first = "https://tradingeconomics.com/ws/stream.ashx?start=60200&size=100"
url_sample = "https://tradingeconomics.com/ws/stream.ashx?start=540&size=20"

def crawler_TE():
	for start in range(0, 60300, 100):
		print(start)
		out_file = "./data_out_TE/out_json_{}.json".format(start)
		print(out_file)
		with open(out_file, "w") as fw:
			url_loop = "https://tradingeconomics.com/ws/stream.ashx?start=%d&size=100" % start
			print(url_loop)
			html = urlopen(url_loop)
			s = html.read().decode("utf-8")
			json_content_list = json.loads(s)
			json.dump(json_content_list, fw)
		if start > 200:
			break

def process_json():
	json_dir = "./data_out_TE"
	json_pro_dir = "./data_processed_TE"

	str_all = ""
	with open("te_str_all.json", "a", encoding='utf-8') as fr_all:
		for json_file in os.listdir(json_dir):
			lines_json = None
			if json_file.endswith(".json"):
				with open(os.path.join(json_dir,json_file), "r", encoding='utf-8') as fr:
					lines = fr.read()
					lines_json = lines.replace("[","").replace("]","").replace('},', '}')
									
				with jsonlines.open(os.path.join(json_pro_dir,json_file[:-5]+".json"), mode="w") as fw:
					jsonlines.Writer.write(fw, lines_json)

				with jsonlines.open(os.path.join(json_pro_dir,json_file[:-5]+".json"), mode="r") as fr2:
					for item in fr2:
						json.dump(item, fr_all) 

def combine_to_oneFile():
	json_dir = "./data_out_TE"
	json_pro_dir = "./data_processed_TE"

	json_files = os.listdir(json_dir)
	with open("te_content_all.json", "w", encoding="utf-8") as fw:
		for json_file in json_files:
			if not json_file.endswith(".json"):
				continue
			with open(os.path.join(json_dir, json_file), "r") as fr:
				content = fr.read()
				content = content.replace("[","").replace("]","")
				sps = content.split("}, {") 
				for s in sps:
					s = "{" + s + "}"
					fw.write(s)
					fw.write("\n")
			

if __name__ == "__main__":
	# crawler_TE()
	# process_json()
	combine_to_oneFile()
