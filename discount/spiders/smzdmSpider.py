# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from discount.items import DiscountItem
from scrapy.http import Request, Response
import re


def first_element(element_list):
    return element_list[0].strip() if isinstance(element_list, list) and len(element_list) > 0 else None


def last_element(element_list):
    return element_list[-1].strip() if isinstance(element_list, list) and len(element_list) > 0 else None


class SmzdmSpider(CrawlSpider):
    name = 'smzdm'
    allowed_domains = ['smzdm.com']
    start_urls = ['http://www.smzdm.com/youhui/']
    # start_urls = ['http://item.jd.com/1203874.html']
    base_url = 'http://www.smzdm.com'
    page_pat = re.compile(r'/p(.*)$')
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('http://www.smzdm.com/youhui/fenlei/.*', '/youhui/fenlei/.*'), ),
             callback='parse_item'),

    )


    def parse_item(self, response):
        sel = Selector(response)
        item_entries = sel.xpath('/html/body/section/div[1]/div[@class="list list_preferential "]')
        category = first_element(sel.xpath('/html/body/section/div[1]/div[1]/div[2]/ul/li/a/span/text()').extract())
        for entry in item_entries:
            item = DiscountItem()
            item['name'] = first_element(entry.xpath('div[1]/h2/a/text()').extract())
            item['discount'] = first_element(entry.xpath('div[1]/h2/a/span/text()').extract())
            item['imgsrc'] = first_element(entry.xpath('a/img/@src').extract())
            item['description'] = first_element(entry.xpath('div[2]/div[2]/p/text()').extract())
            item['url'] = first_element(entry.xpath('div[2]/div[3]/div[1]/div/a/@href').extract())
            item['source'] = first_element(entry.xpath('div[2]/div[3]/div[1]/a/text()').extract())
            item['category'] = category
            pos_vote = first_element(entry.xpath('div[2]/div[3]/a[1]/span[1]/text()').extract())
            neg_vote = first_element(entry.xpath('div[2]/div[3]/a[2]/span[1]/text()').extract())
            item['rate'] = float(pos_vote) / (float(pos_vote) + float(neg_vote))
            item['price'] = None
            item['time'] = first_element(entry.xpath('div[2]/div[1]/span[1]/text()').extract())
            yield item
        next_page = first_element(sel.xpath('//li[@class="pagedown"]/a/@href').extract())
        match = self.page_pat.search(response.url)
        if (match):
            page_id = int(match.group(1))
            if (page_id < 5 and next_page):
                yield Request(next_page)
        else:
            if (next_page):
                yield Request(next_page)
