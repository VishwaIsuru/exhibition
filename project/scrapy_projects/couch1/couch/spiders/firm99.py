import scrapy
import csv


class WorkSpider(scrapy.Spider):
    name = 'firm99'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Company Name","Domain","Hourly rate","Address","Main Url","Service Focus","Industry"


        ]
    };

    urls = [
        "https://99firms.com/advertising-companies/","https://99firms.com/branding-companies/",
        "https://99firms.com/digital-marketing-companies/","https://99firms.com/content-marketing-companies/",
        "https://99firms.com/social-media-marketing-companies/","https://99firms.com/ppc-agencies/",
        "https://99firms.com/seo-agencies/","https://99firms.com/email-marketing-companies/",
        "https://99firms.com/video-marketing-companies/","https://99firms.com/app-marketing-companies/","https://99firms.com/pr-companies/",
        "https://99firms.com/web-development-companies/","https://99firms.com/joomla-development-agencies/",
        "https://99firms.com/wordpress-companies/","https://99firms.com/ecommerce-development-companies/",
        "https://99firms.com/app-development/","https://99firms.com/shopify-developers/",
        "https://99firms.com/magento-development-agencies/","https://99firms.com/ruby-on-rails-companies/",
        "https://99firms.com/net-development-companies/","https://99firms.com/php-development-companies/",
        "https://99firms.com/drupal-development-agencies/",
        "https://99firms.com/internet-of-things-companies/","https://99firms.com/virtual-reality-companies/",
        "https://99firms.com/augmented-reality-companies/","https://99firms.com/ai-companies/",
        "https://99firms.com/big-data-companies/","https://99firms.com/data-recovery-companies/",
        "https://99firms.com/blockchain-companies/","https://99firms.com/cyber-security/",
        "https://99firms.com/cloud-consulting-companies/","https://99firms.com/spam-filtering-companies/",
        "https://99firms.com/web-design-companies/","https://99firms.com/ux-design-agencies/",
        "https://99firms.com/app-design-companies/","https://99firms.com/logo-design-agencies/"

    ]


    def start_requests(self):


        i=0
        for u in self.urls:
            yield scrapy.Request(url=u, callback=self.parse,meta={'Index':i})
            i+=1

    def parse(self, response):


        divdetails = response.xpath('//div[@class="w-100"]')
        for onediv in divdetails:
            company = onediv.xpath('.//div[@class="position-relative"]/div[@class="pr-2 font-weight-bold color-black m-0 post_title text-center text-md-left"]')
            companyNames= ''.join([x.strip() for x in company.xpath('.//text()').extract()])
            companyName=companyNames.split('. ')[-1]


            domains = onediv.xpath('.//div[@class="d-flex flex-wrap pl-lg-0 justify-content-center justify-content-sm-start justify-content-lg-center vi_col-12 vi_col-lg-4 mx-auto"]')
            domain = domains.xpath('.//a[2]/@href').extract()

            rate = onediv.xpath('.//div[@class="mt-lg-0 text-center price font-weight-bold"]')
            hourlyrate= ''.join([x.strip() for x in rate.xpath('.//text()').extract_first()])

            adresess = onediv.xpath('.//div[@class="gmw-sl-address gmw-sl-element"]/span[@class="address"]')
            adress = adresess.xpath('.//text()').extract_first()

            servise= onediv.xpath('.//ul[@class="px-1 pt-0 list-unstyled d-inline-block text-left pb-0 mb-0"]/ul')
            servisefocus=servise.xpath('.//li/text()').extract()

            # for industry in response.url:
            #     industry = industry
            industry = response.url.split('https://99firms.com/')[-1]
            industries = industry.split('/')[0]
            # s = business.css('a.email-business::attr(href)').extract()
            # item['email'] = [item.replace('mailto:', '') for item in s]

            yield {
                    "Main Url": response.url,
                    "Company Name":companyName,
                    "Domain":domain,
                    "Hourly rate": hourlyrate,
                    "Address":adress,
                    "Service Focus":servisefocus,
                    "Industry":industries


            }
