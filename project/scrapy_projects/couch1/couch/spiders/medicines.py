import scrapy
import csv

class WorkSpider(scrapy.Spider):
    name = 'medicines'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Url","Drug name:","Company name:","Active Ingredient:","Legal Status:"


        ]
    };

    urls = [
        "https://www.medicines.org.uk/emc/browse-medicines/0-9",
        # "https://www.drugs.com/alpha/0-9.html"
    ]
    i = 65
    while i < 91:
        ur = "https://www.medicines.org.uk/emc/browse-medicines/"+chr(i)
        urls.append(ur)
        i += 1

    def start_requests(self):


        i=0
        for u in self.urls:
            yield scrapy.Request(url=u, callback=self.parse,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'},meta={'Index':i})
            i+=1
            # break
    def parse(self, response):
        details = response.xpath('//div[@class="col-sm-9"]/h2/a')
        links = details.xpath('.//@href').extract()

        # print(links)
        # print links
        for link in links:
            l = 'https://www.medicines.org.uk' + link
            yield scrapy.Request(url=l,callback=self.parseInside,headers={'User-Agent': 'Mozilla Firefox 12.0'})
        # print l ,dont_filter=True


    def parseInside(self,response):

        drugname=  response.xpath('//div[@class="col-md-12 title"]/h1/text()').extract()
        company= response.xpath('//div[@class="col-xs-12 col-md-9 col-lg-8 content-main summary"]/div[@class="row"]/div[@class="col-xs-12"]/h2/a/text()').extract()
        ingradient = response.xpath('//div[@class="col-xs-12 col-md-9 col-lg-8 content-main summary"]/div[@class="row detail"]/div[@class="col-xs-12 col-sm-6"]/ul/li/text()').extract()
        legalstate = response.xpath('//div[@class="col-xs-12 col-md-9 col-lg-8 content-main summary"]/div[@class="row detail"]/div[@class="col-xs-12 col-sm-6"][2]/p/text()').extract()

        yield {
            "Url" : response.url,
            "Drug name:" : drugname,
            "Company name:" : company,
            "Active Ingredient:": ingradient,
            "Legal Status:": legalstate

        }

