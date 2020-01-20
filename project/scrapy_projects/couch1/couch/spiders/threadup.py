# -*- coding: utf-8 -*-
import scrapy
import re
import json
import csv
import pymysql.cursors
from scrapy.http import FormRequest
import random
import string
import sys
# -*- coding: utf-8 -*-
reload(sys)
sys.setdefaultencoding('utf8')
# import pandas
from difflib import SequenceMatcher


class workspider(scrapy.Spider):
    name = "threadup"
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["LINK","Categoty","Price","Discounted Price","Signup Price"]
    }

    def start_requests(self):
        urls=[['https://www.thredup.com/products/women?department_tags=women&page=',521,'Clothing'],
              ['https://www.thredup.com/products/handbags?department_tags=handbags&page=',134,'Handbag'],
              ['https://www.thredup.com/products/shoes?department_tags=shoes&page=',214,'Shoe'],
              ['https://www.thredup.com/products/accessories?department_tags=accessories&page=',249,'Accessories'],
              ['https://www.thredup.com/products/jewelry?department_tags=jewelry&page=',44,'Jewelry']]
        for u in urls:
            for i in range(1,u[1]):
                url=u[0]+str(i)
                yield scrapy.Request(url=url.strip(), callback=self.parse,
                                     headers={'User-Agent': '' + url
                                         , 'Host': 'www.thredup.com', 'Connection': 'keep-alive',
                                              'Upgrade-Insecure-Requests': 1},meta={'cat':u[2]}
                                     , dont_filter=True)

    def parse(self,response):
        list=response.css('.results-grid')
        items=list.css('.results-grid-item')

        for item in items:
            link=item.css('.item-card-top').css('a').xpath('./@href').extract_first()
            currPrice=''
            try:
                currPrice=''.join(item.css('.formatted-price').xpath('.//text()').extract()).replace('$','').strip()
            except:
                pass
            prevPrice=''
            try:
               prevPrice= ''.join(item.css('.formatted-msrp').xpath('.//text()').extract()).replace('$','').strip()
            except:
                pass
            signUpBonus=''
            try:
                signUpBonus=''.join(item.css('._2goO2._1zjF5').css('.u-font-extra-bold').xpath('.//text()').extract())
            except:
                pass

            yield {
                "LINK":link, "Categoty":response.meta["cat"], "Price":prevPrice, "Discounted Price":currPrice, "Signup Price":signUpBonus
            }