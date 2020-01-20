import scrapy
import csv

class WorkSpider(scrapy.Spider):
    name = 'rafeeg'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Company Name","Main Url","Telephone","E mail","Company Type","Web site","City","License NUmber","Company Type","Expire Date",
            "Address",


        ]
    };

    urls = [
        "https://companies.rafeeg.ae/companies/page/5"

    ]
    i = 2
    while i < 7493:
        ur = "https://companies.rafeeg.ae/companies/page/" + str(i)
        urls.append(ur)
        i += 1

    def start_requests(self):


        i=0
        for u in self.urls:
            yield scrapy.Request(url=u, callback=self.parse,meta={'Index':i})
            i+=1

    def parse(self, response):
        details = response.xpath('.//header/h1[@class="title gradient-effect"]/a')

        link = details.xpath('.//@href').extract()

        for l in link:

            yield scrapy.Request(url=l, callback=self.parseInside,
                             headers={'User-Agent': 'Mozilla Firefox 12.0'}, meta={'Index': response.meta['Index']})
            # break

    def parseInside(self,response):

        companyName=response.xpath('//div[@class="meta"]/h1/text()').extract()
        telephone=response.xpath('//div[@class="grid-container company-info"]/div[@class="grid-50 tablet-grid-100"]/ul[@class="basic-list"]/li[4]/span[2]/a/text()').extract_first()
        city = response.xpath('//div[@class="grid-container company-info"]/div[@class="grid-50 tablet-grid-100"]/ul[@class="basic-list"]/li[1]/span[2]/text()').extract_first()
        email = response.xpath('//div[@class="grid-container company-info"]/div[@class="grid-50 tablet-grid-100"][2]/ul[@class="basic-list"]/li[4]/span[@class="basic-value"]/a/text()').extract()
        website = response.xpath('//div[@class="grid-container company-info"]/div[@class="grid-50 tablet-grid-100"][2]/ul[@class="basic-list"]/li[4]/span[@class="basic-value"]/a/text()').extract()
        license =response.xpath('//div[@class="grid-50 tablet-grid-100"]/ul[@class="basic-list"]/li[3]/span[@class="basic-value"]/text()').extract_first()
        companyType = response.xpath('//div[@class="grid-50 tablet-grid-100"]/ul[@class="basic-list"]/li[5]/span[@class="basic-value"]/text()').extract_first()
        expire = response.xpath('//div[@class="grid-50 tablet-grid-100"]/ul[@class="basic-list"]/li[6]/span[@class="basic-value"]/text()').extract_first()

        buils=['']
        streets=['']
        building = response.xpath('//div[@class="grid-container company-info"]/div[@class="grid-50 tablet-grid-100"][1]/ul[@class="basic-list"]/li[5]/span[@class="basic-value"]//text()').extract()


        street=response.xpath('//div[@class="grid-container company-info"]/div[@class="grid-50 tablet-grid-100"][1]/ul[@class="basic-list"]/li[2]/span[@class="basic-value"]//text()').extract()

        pobx= response.xpath('//div[@class="grid-container company-info"]/div[@class="grid-50 tablet-grid-100"][1]/ul[@class="basic-list"]/li[3]/span[@class="basic-value"]//text()').extract()

        adress = ''.join(building) + ''.join(street)+ ', '.join(pobx)
        # print building
        # print street


        yield {
            "Main Url":response.url,
            "Company Name":companyName,
            "Telephone":telephone,
            "City":city,
            "Web site":website,
            "E mail":email,
            "License NUmber":license,
            "Company Type":companyType,
            "Expire Date":expire,
            "Address":adress

        }
