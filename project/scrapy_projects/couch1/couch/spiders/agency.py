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
    name = "agency123"
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["LINK","Name","Industry","Sub Industry","Location","Size","Website"]
    }

    urls=[]

    def start_requests(self):
        with open('agency.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                self.urls.append(row[0])

        while(len(self.urls)>0):
            url=self.urls.pop(0)
            yield scrapy.Request(url=url.strip(), callback=self.parse,
                                     headers={'User-Agent': ''+url
                                              ,'Host':'www.agencyspotter.com','Connection':'keep-alive','DNT':1,'Upgrade-Insecure-Requests':1}
                                 ,dont_filter=True)


    def parse(self,response):

        base=response.css('#agency_name_and_industry')
        companyName=' '.join(base.css('h1').xpath('.//text()').extract())

        industries=','.join([x.strip() for x in base.xpath('.//h2//text()').extract()])
        subIndustries=','.join([x.strip() for x in base.xpath('.//h3//text()').extract()])
        industries=industries.replace(',,',',')
        subIndustries=subIndustries.replace(',,',',')

        website='';
        try:
            website=response.css('#agency_contact_info .connect-website').xpath('./@href').extract_first()
        except:
            pass

        address=''
        try:
            address=','.join(response.css('#agency_location').xpath('.//text()').extract()[1::])
        except:
            pass
        size=''
        try:
            size=''.join(response.css('#agency_size').xpath('.//text()').extract()[1::])
        except:
            pass

        if website.strip()!='#':
            yield {
                "LINK":response.url, "Name":companyName, "Industry":industries, "Sub Industry":subIndustries, "Location":address, "Size":size, "Website":website
            }
        else:
            print("sssssssssssssssssssssssssssssssss")
            self.urls.append(response.url)




