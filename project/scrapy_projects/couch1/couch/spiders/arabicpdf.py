import scrapy
import csv
import re
import requests

class WorkSpider(scrapy.Spider):
    name = 'arabicpdf'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Main Url","Item Url"


        ]
    };
    urls = [

        "https://uae-school.com/archives/70322",

    ]

    def start_requests(self):

        i = 0
        for u in self.urls:
            yield scrapy.Request(url=u.strip(), callback=self.parse,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'}, meta={'Index': i})
            i += 1

    def parse(self, response):
        details = response.xpath('//div[@id="docs-download-link"]')


        for detail in details:
            link = detail.xpath('.//@href').extract()


        i=0
        for link in link:
            yield {
                "Main Url": response.url,
                "Item Url": link

            }
            # response1 = ['']
            response1 =requests.get(link)
            imgName = str(i)
            imgName = "./arabicpdf1/" +imgName.replace('/', '')
            # response1.append(response1s)
            # if response1.status_code == 200:
            #     with open(imgName, 'wb') as f:
            #         f.write(response1.content)
            # header = response1.headers['Content-Disposition']
            # file_name = re.search(r'filename="(.*)"', header).group(1)
            # with open(file_name, 'wb') as f:
            #     f.write(response1.content)

            CHUNK_SIZE = 32768

            with open(imgName, "wb") as f:
                for chunk in response1.iter_content(CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

        i += 1

