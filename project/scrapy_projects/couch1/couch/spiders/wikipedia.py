import scrapy
import re
import json
import csv
import pymysql.cursors
from scrapy.http import FormRequest
import random
import string
# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf8')

class workspider(scrapy.Spider):
    name = "wikipedia"

    def start_requests(self):
        yield scrapy.Request('https://simple.wikipedia.org/wiki/List_of_countries_by_continents#Africa', callback=self.parse,
                             meta={'continent': 'Africa'})

    def parse(self,response):
        africaCountries=response.xpath('/html/body/div[3]/div[3]/div[4]/div/ul[1]/li/a[1]/text()').extract()
        asiaCountries=response.xpath('/html/body/div[3]/div[3]/div[4]/div/ul[2]/li/a[1]/text()').extract()
        europeCountries=response.xpath('/html/body/div[3]/div[3]/div[4]/div/ul[3]/li/a[1]/text()').extract()
        northAmerica=response.xpath('/html/body/div[3]/div[3]/div[4]/div/ul[4]/li/a[1]/text()').extract()
        southAmerica=response.xpath('/html/body/div[3]/div[3]/div[4]/div/ul[5]/li/a[1]/text()').extract()
        australia=response.xpath('/html/body/div[3]/div[3]/div[4]/div/ul[6]/li/a[1]/text()').extract()

        for a in africaCountries:
            yield {"Continent":"Africa","Country":a}

        for a in asiaCountries:
            yield {"Continent": "Asia", "Country": a}

        for a in europeCountries:
            yield {"Continent": "Europe", "Country": a}
        for a in northAmerica:
            yield {"Continent": "North America", "Country": a}
        for a in southAmerica:
            yield {"Continent": "South America", "Country": a}
        for a in australia:
            yield {"Continent": "Australia", "Country": a}