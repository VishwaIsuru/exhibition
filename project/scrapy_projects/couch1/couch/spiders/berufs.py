import scrapy
import csv


class WorkSpider(scrapy.Spider):
    name = 'berufs'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["URL",
                               "Job Title",
                               "Name",
                               "Telephone",
                               "Email",
                               "Website",
                               "Category"
                               ]
    };

    row=1;

    def start_requests(self):
        url='https://www.berufsfotografen.com/fotograf-hamburg?fbclid=IwAR1aAVAV0eaFGE4UXfT9gjgQnTZCBI3mghQnPcBz1vKEwAsL0K7vb1dI6N4'
        yield scrapy.Request(url=url, headers={'User-Agent': 'Mozilla Firefox 12.0'},callback=self.parse)

    def parse(self,response):
        urls1=response.css('.lass-block').xpath('./@href').extract()
        urls2=response.css('.photo-block').xpath('./@href').extract()
        urls3=response.css('.coloum1.detail-target').xpath('./@href').extract()

        urls=urls1+urls2+urls3

        for url in urls:
            l='https://www.berufsfotografen.com'+url
            yield scrapy.Request(url=l, headers={'User-Agent': 'Mozilla Firefox 12.0'}, callback=self.parseInside,meta={'A':'sd'})

    def parseInside(self,response):
        d=response.meta['A']
        jobTitle=response.xpath('//span[@itemprop="jobtitle"]/text()').extract_first()
        name=response.xpath('//span[@itemprop="name"]/text()').extract_first()
        telephone=response.xpath('//span[@itemprop="telephone"]/text()').extract_first()
        email=response.xpath('//a[@itemprop="email"]/text()').extract_first()
        url=response.xpath('//a[@itemprop="url"]/@href').extract_first()
        category=response.xpath('//p[@itemprop="description"]/text()').extract_first()

        yield {
            "URL":response.url,
            "Job Title":jobTitle,
            "Name":name,
            "Telephone":telephone,
            "Email":email,
            "Website":url,
            "Category":category
        }




