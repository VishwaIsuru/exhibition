import scrapy
import csv

class WorkSpider(scrapy.Spider):
    name = 'almanak'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Main Name",
            # "Sub Set Of Name",
            "Bezoekadres",
            "Postadres",
            "Telefoon",
            "Fax",
            "Internet",
            "E-mail",

        ]
    };

    urls = [
        "https://almanak.overheid.nl/Provincies/",
        "https://almanak.overheid.nl/Ministeries/",
        "https://almanak.overheid.nl/Staten-Generaal/",
        "https://almanak.overheid.nl/Hoge_Colleges_van_Staat/",
        "https://almanak.overheid.nl/Adviescolleges/",
        "https://almanak.overheid.nl/Openbare_lichamen_voor_beroep_en_bedrijf/",
        "https://almanak.overheid.nl/Koepelorganisaties/",
        "https://almanak.overheid.nl/Kabinet_van_de_Koning/",
        "https://almanak.overheid.nl/Rechtspraak/",
        "https://almanak.overheid.nl/Politie_en_brandweer/",
        "https://almanak.overheid.nl/Caribisch_Nederland/"

    ]


    def start_requests(self):


        i=0
        for u in self.urls:
            yield scrapy.Request(url=u.strip(), callback=self.parse,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'},meta={'Index':i})
            i+=1

    def parse(self, response):
        details = response.xpath('//*[@data-roo-element="organisationtype-content"]').xpath('.//a')
        links = []


        for detail in details:
            link = detail.xpath('./@href').extract_first()
            links.append(link)

        #print("I am here")
        for link in links:
            l = 'https://almanak.overheid.nl'+link
            yield scrapy.Request(url=l.strip(), callback=self.parseInside,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'}, meta={'Index': response.meta['Index']})


            #print(l)

    def parseInside(self,response):
        #others =response.xpath('./a/@href').extract_first()
        #postadreslist= []
        beadress=''.join([x.strip() for x in response.xpath('//td[@data-before="Bezoekadres"]/text()').extract()])
        postadres = ''.join([x.strip() for x in response.xpath('//td[@data-before="Postadres"]/text()').extract()])


        #parts=(postadres.strip("urnt") for parts in postadres)
        #d =''.join(strip() for x in postadres)

        telepone = ''.join([x.strip() for x in response.xpath('//td[@data-before="Telefoon"]/text()').extract_first()])
        fax = response.xpath('//td[@data-before="Fax"]/text()').extract_first()
        intrnt = response.xpath('//td[@data-before="Internet"]//a/@href').extract()
        email = response.xpath('//td[@data-before="E-mail"]//a/text()').extract()
        #print others strip()
        #s=[3,5,6]

        #d=''.join([x*2 for x in s])

        yield {
            "Main Name": response.url,
            # "Sub Set Of Name":
            "Bezoekadres" : beadress,
            "Postadres" : postadres,
            "Telefoon" : telepone,
            "Fax" : fax,
            "Internet" :intrnt,
            "E-mail" : email

        }

