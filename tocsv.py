import csv

def tocsv(news_list, csv_file):
    with open(csv_file, "a") as fw:
        csvwriter = csv.writer(fw)
        csvwriter.writerow(["title", "href", "date", "type", "content"])
        for news in news_list:
            r = [news.title,news.href,news.date,news.type,news.content]
            csvwriter.writerow(r)
