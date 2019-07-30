# -*- coding: utf-8 -*-
import scrapy
import re
import time

from news_spider.items import NewsSpiderItem


class CnnSpider(scrapy.Spider):
    name = 'cnn'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['https://edition.cnn.com/world/']

    def parse(self, response):
        href = response.xpath('//article//h3//a/@href')
        for i in href:
            url = response.urljoin(i.extract())
            if self.is_url_needed(url):
                yield scrapy.Request(url, callback=self.parse_news)

    def parse_news(self, response):
        url = response.url
        title = response.xpath('//article//h1/text()').extract_first()
        post_time = response.xpath(
            '//article//p[@class="update-time"]/text()').extract_first()
        content = response.xpath(
            '//*[@id="body-text"]//*[contains(@class, "zn-body__paragraph")]//text()'
        )
        content = ' '.join(content.extract())
        item = NewsSpiderItem()
        item['url'] = url
        item['title'] = title
        item['report_time'] = post_time
        item['content'] = content
        item['crawl_time'] = time.time()
        yield item

    def is_url_needed(self, url):
        if url.endswith('.html') and re.search(
                r'(20\d{2})[/:-]([0-1]?\d)[/:-]([0-3]?\d)', url):
            return True
        else:
            return False
