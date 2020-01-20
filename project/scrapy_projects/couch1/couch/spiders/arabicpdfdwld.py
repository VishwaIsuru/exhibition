import scrapy
import csv
import re
import requests

class WorkSpider(scrapy.Spider):
    name = 'arabicpdfwld'

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


        i=0
        for u in self.urls:
            yield scrapy.Request(url=u.strip(), callback=self.parse,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'},meta={'Index':i})
            i+=1

    def parse(self, response):
        details = response.xpath('//div[@id="docs-download-link"]').xpath('.//a')
        # links = []


        for detail in details:
            link = detail.xpath('./@href').extract()
            for fid in link:
                tofileid = fid.split('/d/')[-1].split('/view')[0]

                # print (tofileid)

            from google_drive_downloader import GoogleDriveDownloader as gdd

            gdd.download_file_from_google_drive(file_id=tofileid,
                                                dest_path='./drivedwload/'+tofileid+'.pdf')

            # links.append(link)







