import scrapy
import csv


class WorkSpider(scrapy.Spider):
    name = 'exhibitor'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["URL",
                               "Exhibitor Name",
                               "Booth",
                               "Address",
                               "Phone Number",
                               "Web",
                               "About",
                               "Contacts",
                               "Categery1","Categery2","Categery3","Categery4","Categery5","Categery6"

        ]
    };

    def start_requests(self):
        f = open("/home/vishwa/Desktop/exhibitor/exhibit.csv", "r")
        contents = f.read().replace("[", "").replace("]", "").split(",")
        print(contents)
        for content in contents:
            content = content.split("'")[1].replace('7_0', '8_0').strip()
            print(content)
            yield scrapy.Request(url=content.strip(), callback=self.parse)

        #url='file:///home/vishwa/Desktop/exhibitor/Exhibitor%20Directory%20-%20CES%202020.html'
        #yield scrapy.Request(url=url, headers={'User-Agent': 'Mozilla Firefox 12.0'},callback=self.parse)

    def parse(self, response):
        #urls1 = response.xpath('.//section/@class').extract()
        urls1 = ''.join([x.strip() for x in response.xpath('//h1[@class="flex-auto  ma0  mb3  mb0-xl  "]/text()').extract_first()])
        booth = response.xpath('//li[@class="o-List_Columns_Item  lh-title"]').xpath('//a[@id="newfloorplanlink"]/text()').extract_first()
        compnyDetail = ''.join([x.strip() for x in response.xpath('.//div[@class="dtc  pa0  pl2"]/text()').extract()])
        phone = response.xpath('//span[2][@class="break-word  lh-list"]/text()').extract()

        web = ''.join([x.strip() for x in response.xpath('//div[@class="flex-l  o-DynamicColumns"]').xpath('//*[@class="media  mb3"][3]/p[@class="lh-copy  ma0"]/a/text()').extract()])
        #f = 0
        #for a in web:
         #   f += int(a)
        #about = response.xpath('.//div[@class="lh-copy"]').extract()
        aboutDtl=''
        #for aboutDtl in about:
         #   try:
          #      aboutDtl = ''.join([x.strip() for x in about.xpath('./text()').extract_first()])
           # except:
            #    pass

        about = ''
        try:
            about = ''.join(response.xpath('.//div[@class="lh-copy"]/text()').extract()).strip()
        except:
            pass
        contact = ''.join([x.strip() for x in response.xpath('//ul[@class ="mys-bullets"]/li/text()').extract()])
        categery1 = ''.join([x.strip() for x in response.xpath('//ul[@class="o-List_Bullets  o-List_Columns"]/li[@class="o-List_Columns_Item  lh-title"][1]/text()').extract()])
        categery2 = ''.join([x.strip() for x in response.xpath('//ul[@class="o-List_Bullets  o-List_Columns"]/li[@class="o-List_Columns_Item  lh-title"][2]/text()').extract()])
        categery3 = ''.join([x.strip() for x in response.xpath('//ul[@class="o-List_Bullets  o-List_Columns"]/li[@class="o-List_Columns_Item  lh-title"][3]/text()').extract()])
        categery4 = ''.join([x.strip() for x in response.xpath('//ul[@class="o-List_Bullets  o-List_Columns"]/li[@class="o-List_Columns_Item  lh-title"][4]/text()').extract()])
        categery5 = ''.join([x.strip() for x in response.xpath('//ul[@class="o-List_Bullets  o-List_Columns"]/li[@class="o-List_Columns_Item  lh-title"][5]/text()').extract()])
        categery6 = ''.join([x.strip() for x in response.xpath('//ul[@class="o-List_Bullets  o-List_Columns"]/li[@class="o-List_Columns_Item  lh-title"][6]/text()').extract()])

        yield {
            "URL": response.url,
            "Exhibitor Name" : urls1,
            "Booth" : booth,
            "Address": compnyDetail,
            "Phone Number": phone,
            "Web" : web,
            "About" : about,
            "Contacts" : contact,
            "Categery1" : categery1,"Categery2" : categery2,"Categery3" : categery3,"Categery4" : categery4,"Categery5" : categery5,"Categery6" : categery6
        }



        #response.xpath('//div[@class=" showcase-wrapper_basic "]').extract()
        #for urls2 in url:

            #yield scrapy.Request(urls2, headers={'User-Agent': 'Mozilla Firefox 12.0'}, callback=self.parseInside,meta={'A':'sd'})

    #def parseInside(self,response):
        #up = response.xpath('//h1[/@class="flex-auto  ma0  mb3  mb0-xl  "]/text()').extract_first()
        #booth = response.xpath('//div[@class="dtc pa0 pl2"]').extract()


        #about = response.xpath('//div[@class="result-heading mb2 pb2"]/text()').extract()
        #aboutDtl = response.xpath('//div[@class= "lh-copy"]/text()').extract_first()
        #product = response.xpath('//li[@class = "o-List_Columns_Item  lh-title"]/text()').extract_first()

        #yield {

            #"Main type": up,
            #"Booth Title": booth,
            #"Company Name": compnyDetail,
            #"About": about,
            #"About Detail": aboutDtl,
            #"Product Categery": product,

        #}










