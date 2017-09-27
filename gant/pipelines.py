# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from gant.items import GantItem, GantColor

class JsonWriterPipeline(object):
    def open_spider(self, spider):
        """open the item- & color-file"""
        self.item_file = open('items.jl', 'w')
        self.color_file = open('colors.jl', 'w')

    def close_spider(self, spider):
        self.item_file.close()
        self.color_file.close()

    def process_item(self, item, spider):
        """write item to corresponding file"""
        if isinstance(item, GantItem):
            line = json.dumps(dict(item)) + "\n"
            self.item_file.write(line)
        elif isinstance(item, GantColor):
            line = json.dumps(dict(item)) + "\n"
            self.color_file.write(line)
        return item


class MergeJsonWriterPipeline(object):
    """Pipeline that writes the scraped items into 1 file
       The color-records are added to the items as dictionaries
    """
    def __init__(self):
        self.refs_seen = set()  # set that keeps track of the refs seen
        self.items = {}         # dict of items with key = ref, items = records
        self.temp_colors = []   # list to temporarily store color records if loaded before item records

    def open_spider(self, spider):
        self.items_colors_file = open('items_colors.jl', 'w')

    def close_spider(self, spider):
        self.items_colors_file.close()

    def process_item(self, item, spider):
        # process Items
        if isinstance(item, GantItem):
            ref = item['ref']
            # check if refs were already seen
            if ref not in self.refs_seen:
                # add ref to set of seen refs
                self.refs_seen.add(ref)
                # add item to dictionary of items
                self.items[ref] = item
                # check if ref can be found in temporary color list
                for color in self.temp_colors:
                    if ref == color['ref']:
                        # if found, re-process GantColor item
                        self.process_item(color)
            else:
                pass

        # process Colors
        elif isinstance(item, GantColor):
            color_record = dict(item)
            color = color_record['color']
            ref = color_record['ref']
            if ref in self.refs_seen:
                # add to record if item already exists
                try:
                    self.items[ref]['details'][color] = color_record
                except IndexError:
                    # if key 'details' doesn't exist, create new
                    self.items[ref]['details'] = {}
                    self.items[ref]['details'][color] = color_record

                # check if item is now complete
                number_of_colors = len(self.items[ref]['colors'])           # number of colors according to item
                number_of_color_records = len(self.items[ref]['details'])   # number of color records

                # TO ADD: check if colors are the same
                colors_items = self.items[ref]['colors']
                colors_records = self.items[ref]['details']

                # if complete, remove record from dict and write to file
                if number_of_colors == number_of_color_records:
                    # take full item
                    color_item = self.items[ref]
                    # write to json file
                    line = json.dumps(dict(color_item)) + "\n"
                    self.items_colors_file.write(line)
                    # remove from dict & refs_seen
                    del(self.items[ref])
                    self.refs_seen.remove(ref)
            else:
                # store in temp list if item doesn't exist yet
                self.temp_colors.append(color_record)

        return item
