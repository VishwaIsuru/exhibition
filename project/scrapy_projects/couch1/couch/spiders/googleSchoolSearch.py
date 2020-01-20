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
    name = "googleSer"

    def start_requests(self):
        s='/home/couch1/Georgia Schools.csv';
        list=[]
        with open(s) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count==0:
                    line_count+=1
                    continue
                list.append(row[4])
        # header = {
        #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        #     "accept-encoding": "gzip, deflate, br",
        #     "accept-language": "en-US,en;q=0.9",
        #     "upgrade-insecure-requests": "1",
        #     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        # }
        i=0
        for li in list:
            p=li
            li=li.strip().replace(" ","+")+"+website"
            u="https://www.google.com/search?q="+li
            i+=1
            if i<=45:
                continue
            yield scrapy.Request(u, callback=self.parse,meta={'school':p,'index':i,'dont_redirect': True,"handle_httpstatus_list": [302]})
            break

    def parse(self,response):
        print(response.url)
        print(response.body)
        list=response.css('.jfp3ef')
        b=False
        for li in list:
            t=li.xpath('./a/div[2]//text()').extract()
            t=''.join(t).strip().replace('\\','').replace('203a','/').replace(' ','')

            if 'ga.us' in t and "?" not in t:
                yield {"index":response.meta["index"],"school":response.meta['school'],'url':t}
                b=True
                break

        if not b:
            t = list[0].xpath('./a/div[2]//text()').extract()
            t = ''.join(t).strip().replace('\\','').replace('203a','/').replace(' ','')
            yield {"index":response.meta["index"],"school": response.meta['school'], 'url': t}

