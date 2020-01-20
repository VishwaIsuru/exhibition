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
    name = "world"

    def start_requests(self):
        yield scrapy.Request('http://worldpopulationreview.com/countries/countries-in-americas/', callback=self.parse,
                             meta={'continent': 'Americas'})
        yield scrapy.Request('http://worldpopulationreview.com/countries/countries-in-africa/', callback=self.parse,
                             meta={'continent': 'Americas'})
        yield scrapy.Request('http://worldpopulationreview.com/countries/countries-in-asia/', callback=self.parse,
                             meta={'continent': 'Asia'})
        yield scrapy.Request('http://worldpopulationreview.com/countries/countries-in-europe/', callback=self.parse,
                             meta={'continent': 'Europe'})
        yield scrapy.Request('http://worldpopulationreview.com/countries/countries-in-oceania/', callback=self.parse,
                             meta={'continent': 'Australia'})


    def parse(self,response):
        rows=response.css('.table').xpath('./tbody/tr/td[1]/a')

        links=[]
        countries=[]

        for row in rows:
            c=row.xpath('./text()').extract_first()
            link=row.xpath('./@href').extract_first()

            links.append(link)
            countries.append(c)

        i=0
        for link in links:
            l='http://worldpopulationreview.com'+link+'cities/'
            yield scrapy.Request(l,
                                 callback=self.parseInside,
                                 meta={'continent': response.meta['continent'],'country':countries[i]})
            i+=1

    def parseInside(self,response):
        table=response.css('.table-striped')


        trs=trs=table.xpath('./tbody/tr')

        for tr in trs:
            name=tr.xpath('./td[1]/text()').extract_first().strip()
            population=''
            try:
                population=int(tr.xpath('./td[2]/text()').extract_first().replace(',','').strip())
            except:
                pass
            mapLink=tr.xpath('./td[3]/a/@href').extract_first()

            yield {
                "Continent":response.meta['continent'],'Country':response.meta['country'],'City':name,'Populaion':population,'MapLink':mapLink
            }

