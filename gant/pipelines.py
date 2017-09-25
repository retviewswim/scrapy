# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from gant.items import GantItem, GantColor

class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.item_file = open('items.jl', 'w')
        self.color_file = open('colors.jl', 'w')

    def close_spider(self, spider):
        self.item_file.close()
        self.color_file.close()

    def process_item(self, item, spider):
        if isinstance(item, GantItem):
            line = json.dumps(dict(item)) + "\n"
            self.item_file.write(line)
        if isinstance(item, GantColor):
            line = json.dumps(dict(item)) + "\n"
            self.color_file.write(line)
        return item
