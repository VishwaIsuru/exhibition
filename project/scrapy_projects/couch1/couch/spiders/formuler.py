import scrapy
import csv

class WorkSpider(scrapy.Spider):
    name = 'formuler'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Company Name","Franchise sinds","Aantal vestigingen","Waarvan franchise ","Totale investering ","Eigen vermogen ",
            "Main Url"


        ]
    };

    urls = [
        "https://franchiseplus.nl/formules"

    ]
    i = 0
    while i < 24:
        ur = "https://franchiseplus.nl/formules?n_title=&page=" + str(i)
        urls.append(ur)
        i += 1

    def start_requests(self):


        i=0
        for u in self.urls:
            yield scrapy.Request(url=u, callback=self.parse,meta={'Index':i})
            i+=1

    def parse(self, response):


        details = response.xpath('//a[@class="field-group-link group-right notranslate"]')
        # cnames= response.xpath('//div[@class="node-title"]/span/h2')
        # conames=[]
        # for compyname in cnames:
        #     company = compyname.xpath('./text()').extract_first()
        #     conames.append(company)
        #     yield {"Company Name":company}

        links = []

        for detail in details:
            link = detail.xpath('./@href').extract_first()
            links.append(link)

        # print("I am here")
        for link in links:
            l = 'https://franchiseplus.nl' + link
            yield scrapy.Request(url=l.strip(), callback=self.parseInside,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'}, meta={'Index': response.meta['Index']})

    def parseInside(self, response):

        franchise = ''.join([x.strip() for x in response.xpath('//div[@class="inner"]/div[@class="node-franchising-since"]/text()[2]').extract()])
        aantal = ''.join([x.strip() for x in response.xpath('//div[@class="inner"]/div[@class="node-offices-this-year"]/text()[2]').extract()])
        waaravanfran = ''.join([x.strip() for x in response.xpath('//div[@class="inner"]/div[@class="node-franchises-this-year"]/text()[2]').extract()])
        totalinvesting = ''.join([x.strip() for x in response.xpath('//div[@class="inner"]/div[@class="node-total-investment"]/text()[2]').extract()])
        eigeonvermo = ''.join([x.strip() for x in response.xpath('//div[@class="inner"]/div[@class="node-required-capital"]/text()[2]').extract()])
        comany = ''.join([x.strip() for x in response.xpath('//div[@class="node-title"]//h1/text()').extract()])

        yield {
                "Main Url": response.url,

                "Franchise sinds": franchise,
                "Aantal vestigingen": aantal,
                "Waarvan franchise ":waaravanfran,
                "Totale investering ":totalinvesting,
                "Eigen vermogen ":eigeonvermo,
                "Company Name":comany


        }
