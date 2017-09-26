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
        elif isinstance(item, GantColor):
            line = json.dumps(dict(item)) + "\n"
            self.color_file.write(line)
        return item


class MergeJsonWriterPipeline(object):
    def __init__(self):
        self.refs_seen = set()
        self.items = {} # dict of items with key = ref, items = records
        self.colors = []

    def open_spider(self, spider):
        self.items_colors_file = open('items_colors.jl', 'w')

    def close_spider(self, spider):
        self.items_colors_file.close()

    def process_item(self, item, spider):
        if isinstance(item, GantItem):
            ref = item['ref']
            # put items in dictionary
            if ref in self.refs_seen:
                # ignore record if ref already exists
                pass
            else:
                # add ref to set of seen refs
                self.refs_seen.add(ref)
                # add item to dictionary of items
                self.items[ref] = item
        elif isinstance(item, GantColor):
            color_record = dict(item)
            color = color_record['color']
            ref = color_record['ref']
            if ref in self.refs_seen:
                # add to record if item already exists
                try:
                    self.items[ref]['details'][color] = color_record
                except:
                    # if key 'details' doesn't exist, create new
                    self.items[ref]['details'] = {}
                    self.items[ref]['details'][color] = color_record
                # check if item is now complete
                number_of_colors = len(self.items[ref]['colors'])       # number of colors according to item
                number_of_color_records = len(self.items[ref]['details'])    # number of color records
                # if complete, remove record from dict and write to file
                if number_of_colors == number_of_color_records:
                    # take full item
                    color_item = self.items[ref]
                    # write to json file
                    #print("color_item type: ", type(color_item))
                    #print("color_item dict type: ", type(dict(color_item)))
                    color_item = dict(color_item)
                    line = json.dumps(color_item) + "\n"
                    self.items_colors_file.write(line)
                    # remove from dict & refs_seen
                    del(self.items[ref])
                    self.refs_seen.remove(ref)
            else:
                # store in temp list if item doesn't exist yet
                self.colors.append(color_record)

        return item
