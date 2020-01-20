import scrapy
import csv


class WorkSpider(scrapy.Spider):
    name = 'goodFirm'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["Number",
                               "Company name",
                               "URL",
                               "Company Domain",
                               "Industry",
                               "Employees",
                               "Place",
                               "Hourly Rate",
                               "Founded In",
                               "URL on GoodFirm"
                               ]
    };

    row=1;

    def start_requests(self):
        list = [
            [148, 'https://www.goodfirms.co/directory/languages/top-software-development-companies'],
            [266, 'https://www.goodfirms.co/directory/cms/top-website-development-companies'],
            [136, 'https://www.goodfirms.co/ecommerce-development-companies'],
            [30, 'https://www.goodfirms.co/directory/services/list-blockchain-technology-companies'],
            [226, 'https://www.goodfirms.co/directory/marketing-services/top-digital-marketing-companies'],
            [186, 'https://www.goodfirms.co/seo-agencies'],
            [240, 'https://www.goodfirms.co/directory/platforms/top-web-design-companies'],
            [58, 'https://www.goodfirms.co/big-data-analytics'],
            [26, 'https://www.goodfirms.co/artificial-intelligence'],
            [35, 'https://www.goodfirms.co/internet-of-things'],
            [14, 'https://www.goodfirms.co/augmented-virtual-reality'],
            [64, 'https://www.goodfirms.co/software-testing-companies'],
            [67, 'https://www.goodfirms.co/cloud-computing-companies']
        ]

        for li in list:
            for i in range(1, li[0] + 1):
                url = li[1] + '?page=' + str(i)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        content = response.css('.directory-content')
        list = content.xpath('./div')

        name = ''
        url = ''
        domain = ''
        industry = ''
        minProjectVal = ''
        employees = ''
        place = ''
        hourlyRate = ''
        urlOfGoodFirm = ''
        foundedIn=''
        for li in list:
            try:
                name = ''.join(li.css('.company-info-title').xpath('.//text()').extract()).split('.')[1]
                name = name.strip()
            except:
                return
            urlOfGoodFirm='https://www.goodfirms.co'+li.css('.star-block-a').xpath('./@href').extract_first()
            url = li.css('.firms-r').xpath('.//a[contains(@class, "visit-website")]/@href').extract_first()
            try:
                domain = url.split('//')[1].split('/')[0].split('?')[0].replace('www.', '')
            except:
                pass
            industry = li.css('.utagline').xpath('./text()').extract_first()
            hourlyRate = li.css('.firm-pricing').xpath('./text()').extract_first()
            employees = li.css('.firm-employees').xpath('./text()').extract_first()
            foundedIn=li.css('.firm-founded').xpath('./text()').extract_first()
            place=','.join(li.css('.firm-location').xpath('.//text()').extract())

            yield {
                "Number":self.row,
                "Company name":name,
                "URL":url,
                "Company Domain":domain,
                "Industry":industry,
                "Employees":employees,
                "Place":place,
                "Hourly Rate":hourlyRate,
                "Founded In":foundedIn,
                "URL on GoodFirm":urlOfGoodFirm
            }

            self.row+=1