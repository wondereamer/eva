# -*- coding: utf-8 -*-
import scrapy


class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['www.bbc.com/news']
    start_urls = ['http://www.bbc.com/news/world/']

    def parse(self, response):
        print(response.text)
