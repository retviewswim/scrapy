
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst, Identity
from w3lib.html import remove_tags

def compact(s):
    """ returns None if string is empty, otherwise string itself """
    return s if s else None

class GantItem(Item):
    """Gant Item fields"""
    ref = Field()
    product_id = Field()
    source = Field()
    country = Field()
    url = Field()
    language = Field()
    category = Field()
    sub_category = Field()
    third_category = Field()
    timestamp = Field()
    sex = Field()
    main_title = Field()
    description = Field()
    colors = Field()
    material = Field()
    color_urls = Field()
    details = Field()

class GantColor(Item):
    """Gant color-specific fields"""
    ref = Field()
    url = Field()
    color = Field()
    images = Field()
    price_hierarchy = Field()
    sizes = Field()
    sizes_not_available = Field()
    color_snippets = Field()
    stocks = Field()

class GantItemLoader(ItemLoader):
    """ItemLoader"""
    default_item_class = GantItem
    # remove tags & take only first value by default
    default_input_processor = MapCompose(remove_tags)
    default_output_processor = TakeFirst()

    # convert list with empty value to string with 1 ref
    ref_in = MapCompose(remove_tags, str.strip, compact)
    # convert list to 1 string
    main_title_in = MapCompose(remove_tags, str.strip, compact) 
    main_title_out = Join()
    description_in = MapCompose(remove_tags, str.strip, compact)
    description_out = Join()
    # keep full list
    details_out = Identity()
    sizes_out = Identity()
    sizes_not_available = Identity()
    colors_in = MapCompose(remove_tags, str.strip)
    colors_out = Identity()


class GantColorLoader(ItemLoader):
    default_item_class = GantColor

    default_input_processor = MapCompose(remove_tags)
    default_output_processor = TakeFirst()

    ref_in = MapCompose(remove_tags, str.strip, compact)
    images_out = Identity()
    color_urls_out = Identity()
