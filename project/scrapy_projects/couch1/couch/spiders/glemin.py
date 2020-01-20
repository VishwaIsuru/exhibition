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
    name = "gleim"
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["LINK","State Selected","City Selected","Name","Address","Phone","Fax","Cell","EMAIL","Website","Member of","Instructs In","Additional Info"]
    }

    def start_requests(self):
        urls=["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        for u in urls:
            url='https://www.gleim.com/aviation/directories/index.php?avTab=cfi&search=us&selectState='+str(u)
            yield scrapy.Request(url=url.strip(), callback=self.parse,
                                     headers={'User-Agent': '' + u
                                         , 'Host': 'www.gleim.com', 'Connection': 'keep-alive',
                                              'Upgrade-Insecure-Requests': 1}
                                     ,meta={'state':u}, dont_filter=True)

    def parse(self,response):
        stateSt=response.meta['state']
        state=response.css('.mainColWithSidebar').xpath('./text()').extract_first().split('\n')[-1]

        cities=response.xpath('//select[@name="selectCity"]/option')

        cityVals=[]
        citySearchStrs=[]
        for city in cities:
            cityVal=city.xpath('./@value').extract_first()
            citySearchStr=cityVal.strip().replace(' ','+')
            cityVals.append(cityVal)
            citySearchStrs.append(citySearchStr)

        for i in range(len(citySearchStrs)):
            cityVal=cityVals[i]
            citySearchStr=citySearchStrs[i]
            url='https://www.gleim.com/aviation/directories/index.php?avTab=cfi&search=us&selectCity='+citySearchStr+'&cityCount=1000&selectState='+stateSt
            yield scrapy.Request(url=url.strip(), callback=self.parseInside,
                                 headers={'User-Agent': '' + url
                                     , 'Host': 'www.gleim.com', 'Connection': 'keep-alive',
                                          'Upgrade-Insecure-Requests': 1}
                                 , meta={'state': state,'city':cityVal}, dont_filter=True)

    def parseInside(self,response):
        links=[]
        names=[]
        contents=response.css('.mainColWithSidebar').xpath('./p')[:-1]

        for c in contents:
            a='https://www.gleim.com'+c.css('a').xpath('./@href').extract_first()
            name=c.css('a').xpath('./text()').extract_first()
            links.append(a)
            names.append(name)

        i=0
        for a in links:
            yield scrapy.Request(url=a.strip(), callback=self.parseItem,
                                 headers={'User-Agent': '' + a
                                     , 'Host': 'www.gleim.com', 'Connection': 'keep-alive',
                                          'Upgrade-Insecure-Requests': 1}
                                 , meta={'state': response.meta['state'], 'city': response.meta['city'],'name':names[i]}, dont_filter=True)
            i+=1


    def parseItem(self,response):
        text=response.css('.largeText').xpath('.//text()').extract()
        ass=response.css('.largeText').xpath('.//a')

        address=''
        phone=''
        cell=''
        fax=''
        email=''
        website=''


        for t in text:
            if 'Profile last' in t:
                continue
            if ':' in  t:
                break
            address+=t+'\n'
        address=address.strip()

        for t in text:
            if 'Phone:' in t and 'Cell' not in t:
                phone=t.replace('Phone:','').strip()
            elif 'Fax:' in t:
                fax=t.replace('Fax:','').strip()
            elif 'Cell' in t and ':' in t:
                cell=t.split(':')[1].strip()

        for a in ass:
            href=a.xpath('./@href').extract_first()
            if 'mailto:' in href:
                email=href.split('mailto:')[1]
            else:
                con=''.join(a.xpath('.//text()').extract()).strip()
                if '://' in con:
                    website=con
        memberOf=''
        instructIn=''
        additionalInfo=''

        b=False
        for t in text:
            if 'Member of:'==t.strip():
                b=True
            elif ':' in t:
                b=False

            if b:
                memberOf+=t+'\n'

        b = False
        for t in text:
            if 'Instructs in:' == t.strip():
                b = True
            elif ':' in t:
                b = False

            if b:
                instructIn += t + '\n'

        b = False
        for t in text:
            if 'Additional information:' == t.strip():
                b = True
            elif ':' in t:
                b = False

            if b:
                additionalInfo += t + '\n'

        yield {
            "LINK":response.url, "State Selected":response.meta['state'], "City Selected":response.meta['city'], "Name":response.meta['name'], "Address":address, "Phone":phone, "Fax":fax, "Cell":cell, "EMAIL":email, "Website":website,
        "Member of":memberOf, "Instructs In":instructIn, "Additional Info":additionalInfo
        }



