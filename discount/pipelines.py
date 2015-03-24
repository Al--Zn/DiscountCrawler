# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import urllib2
from scrapy.exceptions import DropItem

class DiscountPipeline(object):
    def process_item(self, item, spider):
        return item



class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.item_saved = set()
        self.category_saved = set()
        self.json_data = ''
        self.first_line = True
        self.count = 0
    def open_spider(self, spider):
        if (spider.name == 'jd'):
            self.file = codecs.open('jd.json', 'wrb', encoding='utf-8')
            self.file.write('{\n"item":[\n')
            self.json_data += '{\n"item":[\n'
        elif (spider.name == 'smzdm'):
            self.file = codecs.open('smzdm.json', 'wrb', encoding='utf-8')
            self.file.write('{\n"item":[\n')
            self.json_data += '{\n"item":[\n'
    def process_item(self, item, spider):
        if (item['name'] in self.item_saved):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.category_saved.add(item['category'])
            self.item_saved.add(item['name'])
            if (not self.first_line):
                line =  ",\n" + json.dumps(dict(item), ensure_ascii=False)
            else:
                self.first_line = False
                line = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(line)
            self.json_data += line
            # url = 'http://162.105.174.98/django/discount/savedata/'
            # self.json_data = '{\n"item":[\n' + json.dumps(dict(item), ensure_ascii=False) + '\n]\n}'
            # req = urllib2.Request(url=url, data=self.json_data.encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'}, )
            # try:
            #     f = urllib2.urlopen(req)
            # except:
            #     print self.json_data
            return item

    def close_spider(self, spider):

        self.file.write('\n]\n}')
        self.json_data += '\n]\n}'
        self.file.close()

        url = 'http://162.105.174.98/django/discount/savedata/'
        req = urllib2.Request(url=url, data=self.json_data.encode('utf-8'), headers={'Content-Type': 'application/json; charset=utf-8'}, )
        f = urllib2.urlopen(req)
        print f.read()

