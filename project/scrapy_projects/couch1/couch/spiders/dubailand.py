import csv
import pandas as pd
import scrapy
import re
import json
import csv


csv.register_dialect('myDialect', delimiter='/', quoting=csv.QUOTE_NONE)


class workspider(scrapy.Spider):
    name = "dubland"
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["Office Name",
                               "BRN",
                               "Broker Name",
                               "Phone",
                               "Mobile",
                               "Email"
                               ]
    };

    def start_requests(self):
        df = pd.read_csv('run_results1.csv', header=0, delimiter=',')
        for index, row in df.iterrows():
            url=row["URL"]
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_inside,
                                 headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                          'Accept-Encoding': 'gzip, deflate, br',
                                          'Accept-Language': 'en-US,en;q=0.5',
                                          'Connection': 'keep-alive', 'TE': 'Trailers', 'Upgrade-Insecure-Requests': 1,
                                          'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'})

    def parse_inside(self,response):
        officeName=response.css('#ctl00_ctl40_g_f94d535f_def1_4273_8824_f4c0e5b4a01a_lblOfficeNameValue').xpath('./text()').extract_first().strip()

        brokers=response.css("#tbBrokers")
        b=True
        try:
            trs=brokers.css('tbody').css('tr')
            for tr in trs:
                tds=tr.css('td')

                brn=tds[0].xpath('./text()').extract_first().strip()
                brokerName=tds[1].xpath('./text()').extract_first().strip()
                phone=tds[2].xpath('./text()').extract_first().strip()
                mobile=tds[3].xpath('./text()').extract_first().strip()
                email=tds[4].xpath('./text()').extract_first().strip()

                b=False
                yield {
                    'Office Name': officeName,
                    'BRN':brn,
                    'Broker Name':brokerName,
                    'Phone':phone,
                    'Mobile':mobile,
                    'Email':email
                }
        except:
            pass

        if b:
            yield {
                'Office Name': officeName,
                'BRN': '',
                'Broker Name': '',
                'Phone': '',
                'Mobile': '',
                'Email': ''
            }