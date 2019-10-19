# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector


class InfoSpider(scrapy.Spider):
    name = 'info'
    allowed_domains = ['github.com']
    start_urls = [
        'https://github.com/Germey?tab=repositories']

    # 首先要对当前页进行解析，如果当前页有下一页的话就继续对下一页进行解析，
    # 首先我需要得到所有页数的url

    def parse(self, response):
        sel = Selector(response)
        # container = []
        next_url = sel.xpath('//div[@class="BtnGroup"]/a/@href').extract()[-1]
        for data in sel.xpath('//div[@id="user-repositories-list"]/ul/li'):
            article_title = data.xpath('div[1]/div[1]/h3/a/text()').extract_first()
            article_url = 'https://github.com' + data.xpath('div[1]/div[1]/h3/a/@href').extract_first()
            yield scrapy.Request(article_url, callback=self.parse_url, meta={'title': article_title})
            # print(article_title, article_url)
            # container.append(article_title)
        # print(len(container))
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_url(self, response):
        sel = Selector(response)
        title = response.request.meta['title']
        for file in sel.xpath(
                '//table[@class="files js-navigation-container js-active-navigation-container"]'
                '/tbody//tr[@class="js-navigation-item"]'
        ):
            file_title = file.xpath('td[2]/span/a/text()').extract_first()
            file_url = 'https://github.com' + file.xpath('td[2]/span/a/@href').extract_first()
            print(file_title, file_url)

