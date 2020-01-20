import scrapy
import csv
import json

csv.register_dialect('myDialect', delimiter='/', quoting=csv.QUOTE_NONE)


class workspider(scrapy.Spider):
    name = "kfz"

    def start_requests(self):

        with open('kfz1.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["Num"])

        start = 'https://www.kfzteile24.de/'
        yield scrapy.Request(url=start, callback=self.parseMain)

    def parseMain(self, response):
        band_val = []
        try:
            i = 1
            while True:
                a = response.css('#typeSelectionField_1').xpath('.//*[name()="option"]').extract()[i].split('"')[1]
                band_val.append(a)
                i = i + 1
        except:
            pass

        for i in range(1,len(band_val)):
            url = 'https://www.kfzteile24.de/index.cgi?rm=headerChooseType&hernr=' + band_val[i]
            yield scrapy.Request(url=url, callback=self.parseInside)

    def parseInside(self, response):

        p = json.loads(response.body.decode('utf-8'))
        model_val = []
        try:
            i = 0
            while True:
                a = p['models'][i]['value']
                model_val.append(a)
                i = i + 1
        except:
            pass

        for i in range(0,len(model_val)):
            url = response.url + "&kmodnr=" + model_val[i]
            yield scrapy.Request(url=url, callback=self.parseOut)

    def parseOut(self, response):

        q = json.loads(response.body.decode('utf-8'))
        try:
            i = 0
            while True:
                a = q['types'][i]['value']
                with open('kfz1.csv', 'a+') as csvFile:
                    writer = csv.writer(csvFile,
                                        csv.register_dialect('myDialect', delimiter='/', quoting=csv.QUOTE_NONE))
                    writer.writerow([a])
                i = i + 1
        except:
            pass
