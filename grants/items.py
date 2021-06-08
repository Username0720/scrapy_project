# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GrantsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    konkurs_name = scrapy.Field()
    href = scrapy.Field()
    organization = scrapy.Field()
    date_begin = scrapy.Field()
    date_end = scrapy.Field()
    date_ = scrapy.Field()
    location = scrapy.Field()
    
