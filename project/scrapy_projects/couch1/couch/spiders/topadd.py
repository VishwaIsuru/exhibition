import scrapy
import csv

class WorkSpider(scrapy.Spider):
    name = 'topadd'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Main Url","Company Name","Description","Services Focus","Web site","Rating"


        ]
    };

    urls = [
        "https://clutch.co/agencies"

    ]
    i = 2
    while i < 7:
        ur = "https://clutch.co/agencies?page=" + str(i)
        urls.append(ur)
        i += 1

    def start_requests(self):


        i=0
        for u in self.urls:
            yield scrapy.Request(url=u, callback=self.parse,meta={'Index':i})
            i+=1

    def parse(self, response):

        advertiesments = response.xpath('//li[@class="provider-row"]')
        for advertis in advertiesments:
            company = advertis.xpath('.//h3[@class="company-name"]/a')
            # for companyName in company:
            companyName= company.xpath('./text()').extract()
            # yield {"Company Name": companyName}
            rating = advertis.xpath('.//span[@class="rating"]')
            ratingPoint = rating.xpath('./text()').extract()
            discription= advertis.xpath('.//blockquote/p')
            discriptionof=discription.xpath('./text()').extract()
            services=advertis.xpath('.//div[@class="chartAreaContainer spm-bar-chart"]/div')

            serviceFocus= services.xpath('./@data-content').extract()



            yield {
                    "Main Url": response.url,
                    "Company Name": companyName,
                    "Rating": ratingPoint,
                    "Description":discriptionof,
                     "Services Focus":serviceFocus
            }
