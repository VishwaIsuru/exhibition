import scrapy
import csv

class WorkSpider(scrapy.Spider):
    name = 'exam'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Company Name","Rating","Web site","Introduction","Employee","Revenue",
            "Main Url"


        ]
    };

    urls = [
        "https://www.appfutura.com/software-development-companies"

    ]
    i = 2
    while i < 72:
        ur = "https://www.appfutura.com/software-development-companies?p=" + str(i)
        urls.append(ur)
        i += 1

    def start_requests(self):


        i=0
        for u in self.urls:
            yield scrapy.Request(url=u, callback=self.parse,meta={'Index':i})
            i+=1

    def parse(self, response):

        softwareDevelopers = response.xpath('//li[@class="widget"]')
        for swtdevelop in softwareDevelopers:
            company = swtdevelop.xpath('.//div[@class="col-lg-11 col-md-11  no-pad-top no-pad-bot no-pad-right vcenter"]/h3/a')
            companyName= company.xpath('./text()').extract()
            #
            ratings = swtdevelop.xpath('.//div[@class="rating"]')
            rating = ratings.xpath('./text()').extract()

            websites = swtdevelop.xpath('.//div[@class="row first-info"]')
            #
            if websites.xpath('.//div[@class="col-lg-2 col-md-3 vcenter no-pad-lef"]'):
                 website= websites.xpath('.//a/@href').extract_first()
            else:
                website= websites.xpath('.//span/@data-url').extract_first()



            introductions = swtdevelop.xpath('.//div[@class="developer"]/div[@class="row lh-22"]')
            introduction = ''.join([x.strip() for x in introductions.xpath('.//p/text()').extract()])

            employesss= swtdevelop.xpath('.//div[@class="col-lg-2 col-md-3 no-pad-top no-pad-lef no-pad-rig"]/ul[@class="list-unstyled no-mar"]')
            employes= employesss.xpath('./li[1]/text()').extract()

            revenues = swtdevelop.xpath('.//div[@class="col-lg-2 col-md-3 no-pad-top no-pad-lef no-pad-rig"]/ul[@class="list-unstyled no-mar"]')
            revenue = revenues.xpath('./li[2]/text()').extract()


            yield {
                    "Main Url": response.url,
                    "Company Name": companyName,
                    "Rating": rating,
                    "Web site": website,
                    "Introduction":introduction,
                    "Employee":employes,
                    "Revenue": revenue

            }
