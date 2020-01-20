import scrapy
import csv
import json
import zlib
import gzip
import requests
import os
import shutil

csv.register_dialect('myDialect', delimiter='/', quoting=csv.QUOTE_NONE)


class workspider(scrapy.Spider):
    name = "appliance"
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["Chanel",
                               "Brand",
                               "Type",
                               "Model",
                               "Name",
                               "OEM Part Number",
                               "Source/Dealer part number",
                               "Manufacturer",
                               "Price",
                               "Images",
                               "Link"
                               ]
    };

    def start_requests(self):
        yield scrapy.Request(url='https://www.partselect.com/Appliance-Parts.htm', callback=self.getBrand,
                             headers={"User-Agent": "Mozilla Firefox 12.0"})

    def getBrand(self, response):
        brands = response.css('#Central_Content_Links')

        lis = brands.xpath('./ul/li')

        brands = []
        brandNames = []

        for li in lis:
            aHref = 'https://www.partselect.com' + li.xpath('./a/@href').extract_first()
            aName = li.xpath('./a/text()').extract_first()

            brands.append(aHref)
            brandNames.append(aName)

        i = 0
        for br in brands:
            yield scrapy.Request(url=br, callback=self.getPopularModels,
                                 headers={"User-Agent": "Mozilla Firefox 12.0"}, meta={'brand': brandNames[i]})
            i += 1

    def getPopularModels(self, response):
        moreLink = 'https://www.partselect.com' + response.css('.mm-section-footer > a:nth-child(1)').xpath(
            './@href').extract_first()
        # print("Dfg")
        # print(moreLink)
        yield scrapy.Request(url=moreLink, callback=self.getModels,
                             headers={"User-Agent": "Mozilla Firefox 12.0"}, meta={'brand': response.meta['brand']})

    def getModels(self, response):
        print('I am here')
        pages = int(
            response.css('#Central_Content_PagerTop > div:nth-child(3)').xpath('./text()').extract_first().split()[
                -1].replace(',', '')) / 100 + 1
        pages = int(pages)

        links = response.css('.list-links').xpath('./li/a')

        modelLinks = []
        modelNames = []

        for link in links:
            modelLinks.append('https://www.partselect.com' + link.xpath('./@href').extract_first())
            modelNames.append(link.xpath('./text()').extract_first())

        i = 0
        for l in modelLinks:
            l = l + '/Parts'
            yield scrapy.Request(url=l, callback=self.getAllParts,
                                 headers={"User-Agent": "Mozilla Firefox 12.0"},
                                 meta={'brand': response.meta['brand'], 'model': modelNames[i]})
            i += 1

        for j in range(2, pages + 1):
            p = '?start=' + str(j) + '#Central_Content_PagerTop'
            url = response.url + p
            yield scrapy.Request(url=url, callback=self.parseList,
                                 headers={"User-Agent": "Mozilla Firefox 12.0"},
                                 meta={'brand': response.meta['brand']})

    def parseList(self, response):
        links = response.css('.list-links').xpath('./li/a')

        modelLinks = []
        modelNames = []

        for link in links:
            modelLinks.append('https://www.partselect.com' + link.xpath('./@href').extract_first())
            modelNames.append(link.xpath('./text()').extract_first())

        i = 0
        for l in modelLinks:
            l = l + '/Parts'
            yield scrapy.Request(url=l, callback=self.getAllParts,
                                 headers={"User-Agent": "Mozilla Firefox 12.0"},
                                 meta={'brand': response.meta['brand'], 'model': modelNames[i]})
            i += 1

    def getAllParts(self, response):
        partCount = \
        response.css('#Central_Content_PagerTop > div:nth-child(3)').xpath('./text()').extract_first().split()[
            -1].replace(',', '')
        partCount = int(int(partCount) / 14 + 1)

        for k in range(1, partCount):
            url = response.url + '?start=' + str(k) + '#Central_Content_PagerTop'
            yield scrapy.Request(url=url, callback=self.getItems,
                                 headers={"User-Agent": "Mozilla Firefox 12.0"},
                                 meta={'brand': response.meta['brand'], 'model': response.meta['model']},
                                 dont_filter=True)

    def getItems(self, response):
        parts = response.css('.mm-part')

        partLinks = []
        partNames = []

        for part in parts:
            a = part.css('.rating-part-name').xpath('./a')
            partLinks.append('https://www.partselect.com' + a.xpath('./@href').extract_first())
            partNames.append(a.xpath('./text()').extract_first())

        i = 0
        for p in partLinks:
            yield scrapy.Request(url=p, callback=self.parseInside,
                                 headers={"User-Agent": "Mozilla Firefox 12.0"},
                                 meta={'brand': response.meta['brand'], 'model': response.meta['model'],
                                       'part': partNames[i]})

            i += 1

    def parseInside(self, response):
        print(response.meta['brand'])
        print(response.meta['model'])
        print(response.meta['part'])

        chanel = 'Appliance'
        brand = response.meta['model'].split()[1]
        type = ' '.join(response.meta['model'].split()[2:])
        model = response.meta['model'].split()[0]
        name = response.css('h1.title-standard').xpath('./text()').extract_first()
        partNumber = response.xpath('//span[@itemprop="productID"]')[0].xpath('.//text()').extract_first()
        dealerpart = response.xpath('//span[@itemprop="mpn"]')[0].xpath('.//text()').extract_first()
        manufactoredBy = response.xpath('//span[@itemprop="brand"]')[0].xpath('.//text()').extract_first()
        price = ''.join(response.css('.price').xpath('.//text()').extract())
        images=response.css('.piv-thumb-temp')
        imgSrc=''
        for img in images:
            try:
                imgSrc+=","+img.xpath('.//img/@src').extract_first().replace('-S-','-L-')

            except:
                pass
        if len(imgSrc)>0:
            imgSrc=imgSrc[1:]

        yield {
            "Chanel": chanel,
            "Brand": brand,
            "Type": type,
            "Model": model,
            "Name": name,
            "OEM Part Number": partNumber,
            "Source/Dealer part number": dealerpart,
            "Manufacturer": manufactoredBy,
            "Price": price,
            "Images":imgSrc,
            "Link":response.url
        }
