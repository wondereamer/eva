import os
import json
import csv

base_dir = "/Users/wudongyang/Documents/Develop/projects_py/crawler"
origin_data_json = base_dir + "/TE_News_all20190712.json"
data_InterestRate = base_dir + "/TE_News_InterestRate.json"
data_InterestRate_UnitedStates = base_dir + "/TE_News_InterestRate_UnitedStates.json"
data_UnemploymentRate = base_dir + "/TE_News_UnemploymentRate.json"
data_UnemploymentRate_US = base_dir + "/TE_News_UnemploymentRate_US.json"

def process_te():
    category_set = set()
    country_set = set()
    interestRate_news_list = list()
    interestRate_news_US_list = list()
    unemploymentRate_news_list = list()
    unemploymentRate_news_US_list = list()
    with open(origin_data_json, "r") as fr:
        lines = fr.readlines()
        for line in lines:
            d = json.loads(line)  # str to dict
            category = d["category"]
            country = d["country"]
            if category == "Interest Rate":
                interestRate_news_list.append(line)
            if category == "Interest Rate" and country == "United States":
                interestRate_news_US_list.append(line)
            if category == "Unemployment Rate":
                unemploymentRate_news_list.append(line)
            if category == "Unemployment Rate" and country == "United States":
                unemploymentRate_news_US_list.append(line)
    # with open(data_InterestRate, "w") as fw:
    #     for ir_news in interestRate_news_list:
    #         fw.write(ir_news)
    # with open(data_InterestRate_UnitedStates, "w") as fw:
    #     for ir_news in interestRate_news_US_list:
    #         fw.write(ir_news)
    # with open(data_UnemploymentRate, "w") as fw:
    #     for ir_news in unemploymentRate_news_list:
    #         fw.write(ir_news)
    with open(data_UnemploymentRate_US, "w") as fw:
        for ir_news in unemploymentRate_news_US_list:
            fw.write(ir_news)

if __name__ == "__main__":
    process_te()
