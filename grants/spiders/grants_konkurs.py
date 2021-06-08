import scrapy
import re
import psycopg2
import dateparser
import datetime

from scrapy import selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.loader import ItemLoader
from scrapy.selector import Selector


from grants.items import GrantsItem



class Grants_konkursLoader(ItemLoader):
    default_output_processor = Identity()

class GrantsKonkursSpider(scrapy.Spider):
    name = 'grants_konkurs'
    # allowed_domains = ['na-konferencii.ru']
    start_urls = ['https://konferencii.ru/']
    
    def parse(self, response, **kwargs):
        konkurs_name = response.css('.index_cat_tit a::text').getall()
        href = response.css('.index_cat_tit a::attr(href)').getall()
        location = response.css('.left p b::text').getall()
        organization = response.css('.small_p::text').getall()
        #subject = response.css('.index_cat_cur::text').getall()

        datelist1 = {}
        datelist2 = {}
        datelist3 = {}
        
        dat = response.css('.left::text').getall()
        for d in dat:
            cc = re.findall("\d+ \w*", ''.join(d.split('г.')))
            for c in cc:
                c1 = cc[0] + cc[1]
                c2 = cc[2] + cc[3]
                c3 = cc[4] + cc[5]
            l1 = dateparser.parse(c1).strftime("%Y-%m-%d")
            l2 = dateparser.parse(c2).strftime("%Y-%m-%d")
            l3 = dateparser.parse(c3).strftime("%Y-%m-%d")

            datelist1 = ''.join(l1)
            datelist2 = ''.join(l2)
            datelist3 = ''.join(l3)

        row_data = zip(konkurs_name, href, location,
                    organization)

        for item in row_data:
            # создать словарь для хранения извлеченной информации
            scraped_info = {
                #'page': response.url,
                'konkurs_name': item[0],
                'href': "https://konferencii.ru/" + item[1],
                'location': item[2],
                '2021-05-29': datelist1,
                '2029-12-19' : datelist2,
                '2021-11-11' : datelist3,
                'organization': item[3]
                #'subject': item[4],
                
            }

            # генерируем очищенную информацию для скрапа
            yield scraped_info

            next_page = response.css('.nav_arr a.next-page::attr(href)').get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)