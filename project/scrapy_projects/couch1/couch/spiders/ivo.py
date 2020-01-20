import scrapy
import csv
import re
import requests

class WorkSpider(scrapy.Spider):
    name = 'ivo'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Main Url",
            "Item Url"
            # "Item Name",

        ]
    };
    urls = [
        # "file:///home/vishwa/Desktop/ivvo/Sinks%20&%20Faucets%20|%20IVO%20Cabinets%20&%20Surfaces%20|%20CNY.html",
        "file:///home/vishwa/Desktop/ivvo/granite|%20IVO%20cabine%20granite/Granite%20|%20IVOCabinets.html",
        #"file:///home/vishwa/Desktop/ivvo/granite|%20IVO%20cabine%20granite/Backsplash%20|%20IVO%20Cabinets%20&%20Surfaces%20|%20CNY.html"
        #"file:///home/vishwa/Desktop/ivvo/granite|%20IVO%20cabine%20granite/Flooring%20|%20IVO%20Cabinets%20&%20Surfaces%20|%20CNY.html"
        #"file:///home/vishwa/Desktop/ivvo/granite|%20IVO%20cabine%20granite/Onyx%20|%20IVOCabinets.html"
        # "file:///home/vishwa/Desktop/ivvo/granite|%20IVO%20cabine%20granite/Quartz%20|%20IVOCabinets.html"
    ]

    def start_requests(self):

        i = 0
        for u in self.urls:
            yield scrapy.Request(url=u.strip(), callback=self.parse,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'}, meta={'Index': i})
            i += 1

    def parse(self, response):
        details = response.css('#pro-gallery-container')

        links = []
        #names=[]
        # d= []

        for detail in details:
            link = detail.xpath('.//canvas/@data-src').extract()
            #names=detail.xpath('.//div[@class="gallery-item-title"]/span/text()').extract()

            for l in link:
                links.append(l)
            #for n in names:
                #names.append(n)

        # for d in links re.findall(".*.png",d)
        # d = re.findall(".*.jpg", links)
        i=0
        for link in links:
            yield {
                "Main Url": response.url,
                "Item Url": link

            }

            linkCorrect=link.split('/v1')[0]
            response1 = requests.get(linkCorrect)
            imgName =str(i) + linkCorrect[-4:]
            imgName = "./granite/" +imgName.replace('/', '')
            if response1.status_code == 200:
                with open(imgName, 'wb') as f:
                    f.write(response1.content)
            i+=1