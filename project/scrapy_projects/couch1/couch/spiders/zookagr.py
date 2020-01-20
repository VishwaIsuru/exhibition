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
    name = "zookagr"

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["Link","Category","Name","Address","Tel","Website"]
    }

    def start_requests(self):
        url='https://www.zorgkaartnederland.nl/overzicht/organisatietypes'
        yield scrapy.Request(url=url.strip(), callback=self.parse,
                             headers={'User-Agent': '' + url
                                 , 'Host': 'www.zorgkaartnederland.nl', 'Connection': 'keep-alive',
                                      'Upgrade-Insecure-Requests': 1}
                             , dont_filter=True)

    def parse(self,response):
        lis=response.css('#body-content').xpath('.//ul/li')

        counts=[]
        ass=[]
        catNames=[]
        for li in lis:
            count=''.join(li.xpath('.//text()').extract()).split('(')[1].replace(')','')
            count=int(count)
            a='https://www.zorgkaartnederland.nl'+li.xpath('./a/@href').extract_first()
            catName=li.xpath('./a/text()').extract_first()

            counts.append(count)
            ass.append(a)
            catNames.append(catName)

        for i in range(len(counts)):
            it=count/20+1
            for j in range(it):
                url=ass[i]+'/pagina'+str(j+1)
                yield scrapy.Request(url=url.strip(), callback=self.parseList,
                                     headers={'User-Agent': '' + url
                                         , 'Host': 'www.zorgkaartnederland.nl', 'Connection': 'keep-alive',
                                              'Upgrade-Insecure-Requests': 1}
                                     , meta={'name':catNames[i]})

    def parseList(self,response):
        catName=response.meta['name']

        items=response.css('.media')
        links=[]

        for item in items:
            link = 'https://www.zorgkaartnederland.nl'+item.css('.media-heading').xpath('./a/@href').extract_first()

            description=''.join(item.css('.description').xpath('.//text()').extract())
            if 'Organisatie' not in description:
                links.append(link)

        for link in links:
            yield scrapy.Request(url=link.strip(), callback=self.parseInside,
                                 headers={'User-Agent': '' + link
                                     , 'Host': 'www.zorgkaartnederland.nl', 'Connection': 'keep-alive',
                                          'Upgrade-Insecure-Requests': 1}
                                 , meta={'name': catName})

    def parseInside(self,response):
        cat=response.meta['name']
        name=response.xpath('//span[@itemprop="name"]/text()').extract_first()

        addressRow=response.css('.address_row')

        address=''
        tel=''
        website=''

        for ad in range(len(addressRow)):
            try:
                bold=addressRow[ad].xpath('./b/text()').extract_first().strip()
                if bold=='Adres':
                    address+=' '.join(addressRow[ad].xpath('.//span//text()').extract()).strip()
                    k=ad+1
                    while True:
                        bold = addressRow[k].xpath('./b/text()').extract_first()
                        if bold!=None and bold.strip()!='':
                            break
                        else:
                            address += ','.join(addressRow[k].xpath('.//span//text()').extract()).strip()
                        k+=1
                elif bold=='Telefoon':
                    tel=' '.join(addressRow[ad].xpath('./span//text()').extract()).strip()
                elif bold=='Website':
                    website=' '.join(addressRow[ad].xpath('./span//text()').extract()).strip()
                address=address.replace('\n','')
                address=' '.join(address.split())

            except:
                pass
        yield {
            "Link": response.url, "Category": cat, "Name": name, "Address": address, "Tel": tel, "Website": website
        }


