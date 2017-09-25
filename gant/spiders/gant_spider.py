
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.http import Request
from gant.items import GantItemLoader, GantColorLoader

import datetime

class GantSpider(CrawlSpider):
    name = 'gant'
    allowed_domains = ['gant.com', 'gant.se', 'gant.co.uk', 'gant.fr', 'gant.de']
    start_urls = ['http://www.gant.com']

    # define rules for vertical & horizontal crawling
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@class="tree-container" or @class="gant-navigation-banner__ctas"]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//*[@class="product"]'), callback='parse_item')
        )

    def parse_item(self, response):
        """This function parses a product page."""

        # initialize ItemLoader
        loader = GantItemLoader(response=response)
        # add elements to ItemLoader
        loader.add_value('product_id', response.url )
        loader.add_value('source', 'Gant')
        loader.add_xpath('country', '//@data-market')
        loader.add_value('url', response.url)
        loader.add_xpath('language', '//@lang')
        loader.add_value('category', response.url.split("/")[3].split("-",1)[1])
        loader.add_value('sub_category', '')
        loader.add_value('third_category', '')
        loader.add_value('meta', datetime.datetime.utcnow().isoformat())
        loader.add_value('sex', response.url.split("/")[3].split("-")[0])
        loader.add_xpath('ref', '//*[@class = "style-code gant-typog-h4"]/text()')
        loader.add_xpath('main_title', '//*[@itemprop="name"]//text()')
        loader.add_xpath('description', '//*[@itemprop="description"]//text()')
        loader.add_xpath('colors', '//*[@class="alternatives"]/div//@data-title')
        loader.add_xpath('material', '//*[@id="product-care-information"]/p[position()=last()]/text()')

        # define xpath of color-urls and add to itemloader
        xpath_color_urls = '//*[@class="alternatives"]/div//@href'
        loader.add_xpath('color_urls', xpath_color_urls)

        yield loader.load_item()

        # loop through color-urls and parse color-specific pages
        color_urls = response.xpath(xpath_color_urls).extract()
        for color_url in color_urls:
            request = Request(color_url, callback=self.parse_color, dont_filter=True)
            yield request


    def parse_color(self, response):
        """Parses page for color-specific data"""

        # initialize ColorLoader
        loader = GantColorLoader(response=response)
        # add elements to ItemLoader
        loader.add_xpath('ref', '//*[@class = "style-code gant-typog-h4"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('color', '//*[@class="swatch current"]//@data-title')
        loader.add_xpath('images', '//*[@class="thumb"]/@data-large-image-src')
        loader.add_xpath('price_hierarchy', '//*[@itemprop="price"]/@content')
        loader.add_xpath('sizes', '//*[@class="store-stock-checker-product__size"]//text()')
        loader.add_value('sizes_not_available', '')
        loader.add_xpath('color_snippets', '//*[@id="alternative-colors"]//@src')

        yield loader.load_item()
