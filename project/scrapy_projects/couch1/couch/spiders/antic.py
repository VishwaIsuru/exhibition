import scrapy
import csv
import requests


class WorkSpider(scrapy.Spider):
    name = 'antic'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
                               "Main URL",
                               "Product Link",
                               "Article Number",
                               "Article Name",
                               "Diameter",
                               "Length",
                               "Width",
                               "Height",
                               "Weight",
                                "Image Name"
                               ]
    };
    urls = [
        "https://www.terrecottemital.it/catalog/vasen_de.html",
        "https://www.terrecottemital.it/catalog/kassette_de.html",
        "https://www.terrecottemital.it/catalog/vasen-und-verzierungen-von-pier_de.html",
        "https://www.terrecottemital.it/catalog/glas_de.html",
        "https://www.terrecottemital.it/catalog/vasen-und-ornamente-wand_de.html",
        "https://www.terrecottemital.it/catalog/garten-ornamente_de.html",
        "https://www.terrecottemital.it/catalog/statuen-und-busten_de.html"
    ]
    def start_requests(self):


        i=0
        for u in self.urls:
            yield scrapy.Request(url=u.strip(), callback=self.parse,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'},meta={'Index':i})
            i+=1

    def parse(self,response):
        items=response.css('.gradientBoxesWithOuterShadows')
        links=[]

        for item in items:
            link=item.css('a')[0].xpath('./@href').extract_first()
            links.append(link)

        for link in links:
            yield scrapy.Request(url=link, callback=self.parseInside,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'},meta={'Index': response.meta['Index']})

    def parseInside(self,response):
        productName=response.css('.brcrTitleBox > h1:nth-child(1)').xpath('./text()').extract_first()
        productCode=response.css('.small').xpath('.//text()').extract()[-1].strip()

        options=response.css('#opz').css('option')

        for op in options:
            texts=op.xpath('.//text()').extract()

            artNo=texts[1]
            valTxt=texts[2].split()
            artName=''

            for v in valTxt:
                if '.' in v:
                    break
                artName+=' '+v
            artName=artName.strip()

            diameter=''
            height=''
            weight=''
            width=''
            length=''

            for i in range(len(valTxt)):
                if valTxt[i]==u'\xd8':
                    diameter=valTxt[i+1]
                elif valTxt[i]=='h.':
                    height=valTxt[i+1]
                elif valTxt[i].lower()=='kg.':
                    weight=valTxt[i+1]
                elif 'x' in valTxt[i]:
                    width=valTxt[i].split('x')[0]
                    length=valTxt[i].split('x')[1]
            index=response.meta["Index"]
            imgUrl = response.css('.center-block').xpath('./@src').extract_first()
            response1 = requests.get(imgUrl)
            imgName = productName + "_" + productCode + ".jpeg"
            imgName = "./antic/" + str(index) + "/" + imgName.replace('/', '')
            if response1.status_code == 200:
                with open(imgName, 'wb') as f:
                    f.write(response1.content)
            yield {
                "Main URL":self.urls[index],
                "Product Link":response.url,
                "Article Number":artNo,
                "Article Name":artName,
                "Diameter":diameter,
                "Length":length,
                "Width":width,
                "Height":height,
                "Weight":weight,
                "Image Name":imgName
            }











