import scrapy
import csv

class WorkSpider(scrapy.Spider):
    name = 'drugs'

    # custom_settings = {
    #     # specifies exported fields and order
    #     'FEED_EXPORT_FIELDS': [
    #         "Url","Generic Name:","Brand Name:","What is","Dosage Forms","Index Terms"
    #
    #
    #     ]
    # };

    urls = [
        "https://www.drugs.com/alpha/ab.html",
        # "https://www.drugs.com/alpha/0-9.html"
    ]
    # i = 98
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/a"+chr(i)+".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/b" + chr(i) +".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/c" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/d" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/e" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/f" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/g" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/j" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/i" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/j" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/k" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/l" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/m" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/n" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/o" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/p" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/q" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/r" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/s" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/t" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/u" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/v" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/w" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/x" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/y" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/z" + chr(i) + ".html"
    #     urls.append(ur)
    #     i += 1
    # i = 97
    # while i < 122:
    #     ur = "https://www.drugs.com/alpha/" + chr(i) + "0-9.html"
    #     urls.append(ur)
    #     i += 1

    def start_requests(self):


        i=0
        for u in self.urls:
            yield scrapy.Request(url=u, callback=self.parse,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'},meta={'Index':i})
            i+=1
            # break
    def parse(self, response):
        details = response.xpath('//ul[@class="ddc-list-column-2"]/li/a')
        links = details.xpath('.//@href').extract()

        # print(links)
        # print links
        for link in links:
            l = 'https://www.drugs.com' + link
            yield scrapy.Request(url=l,callback=self.gotto_overview,headers={'User-Agent': 'Mozilla Firefox 12.0'},dont_filter=True)
        # print l

    def gotto_overview(self,response):
        lis=response.css('.nav-tabs').css('li')

        for li in lis:
            text=""
            try:
                text=li.xpath('./a//text()').extract_first().strip()
            except:
                text = li.xpath('.//text()').extract_first().strip()
                if text=='Overview':
                    yield scrapy.Request(url=response.url, callback=self.parseInside,
                                         headers={'User-Agent': 'Mozilla Firefox 12.0'},dont_filter=True)
                    return
            if text=='Overview':
                href='https://www.drugs.com'+li.xpath('./a/@href').extract_first()
                yield scrapy.Request(url=href, callback=self.parseInside, headers={'User-Agent': 'Mozilla Firefox 12.0'},dont_filter=True)
                return

    def parseInside(self,response):
        genaricNames = ""
        try:
            genaricNames = ''.join(response.xpath('//p[@class="drug-subtitle"]').xpath('.//text()').extract()).replace('Generic Name:','')

        except:
            genaricNames=""

        brandNames = ""
        try:
            brandNames = ''.join(response.xpath('//p[@class="drug-subtitle"]/i').xpath(".//text()").extract()).replace('Brand Names:','')

        except:
            brandNames=""

        content=response.css('.drug-subtitle')
        h2s = content.css('b')
        indexTerm = ""
        afterIndexTerm = ""
        for h2 in h2s:
            if indexTerm != "":
                afterIndexTerm = h2.xpath('./text()').extract_first()
                break
            text = h2.xpath('./text()').extract_first()

            if 'Generic Name:' in text:
                indexTerm = h2.xpath('./text()').extract_first()
        all_text = ''.join(content.xpath('.//text()').extract())
        genaricNames = ""
        if indexTerm != "" and afterIndexTerm!="":
            genaricNames = all_text.split(indexTerm)[1].split(afterIndexTerm)[0].strip()
        elif indexTerm!="":
            genaricNames = all_text.split(indexTerm)[1].strip()

        dosage_form_before = ""
        dosage_form_after = ""
        for h2 in h2s:
            if dosage_form_before != "":
                dosage_form_after = h2.xpath('./text()').extract_first()
                break
            text = h2.xpath('./text()').extract_first()

            if 'Brand Name' in text:
                dosage_form_before = h2.xpath('./text()').extract_first()
        all_text = '\n'.join(content.xpath('.//text()').extract())
        brandNames = ""
        if dosage_form_before != "" and dosage_form_after != "":
            brandNames = all_text.split(dosage_form_before)[1].split(dosage_form_after)[0].strip()
        elif dosage_form_before!="":
            brandNames = all_text.split(dosage_form_before)[1].strip()

        if '...' in brandNames:
            brandNames=brandNames.split('...')[0]+brandNames.split("brand names.")[1]

        content=response.css(".contentBox")

        h2s=content.css('h2')
        what_is_text=""
        after_what_is=""
        for h2 in h2s:
            if what_is_text!="":
                after_what_is=h2.xpath('./text()').extract_first()
                break
            text=h2.xpath('./text()').extract_first()

            if 'What is' in text:
                what_is_text=h2.xpath('./text()').extract_first()
        all_text='\n'.join(content.xpath('.//text()').extract())
        what_is=""
        if what_is_text!="" and after_what_is!="":
            what_is=all_text.split(what_is_text)[1].split(after_what_is)[0].strip()


        # profetabs= response.xpath('//ul[@class="nav-tabs nav-tabs-collapse vmig"]/li[4]/a')
        # prolinks = []
        #
        # for protab in profetabs:
        #     prolink = protab.xpath('./@href').extract_first()
        #     prolinks.append(prolink)



        lis = response.css('.nav-tabs').css('li')

        for li in lis:
            text=""
            try:
                text=li.xpath('./a//text()').extract_first().strip()
            except:
                text = li.xpath('.//text()').extract_first().strip()
                if text=='Professional':
                    yield scrapy.Request(url=response.url, callback=self.ppadata,
                                         headers={'User-Agent': 'Mozilla Firefox 12.0'},meta={'genaricname': genaricNames,'brandname': brandNames, 'whatis':what_is},dont_filter=True)
                    return
            if text=='Professional':
                href='https://www.drugs.com'+li.xpath('./a/@href').extract_first()
                yield scrapy.Request(url=href, callback=self.ppadata, headers={'User-Agent': 'Mozilla Firefox 12.0'},meta={'genaricname': genaricNames,'brandname': brandNames, 'whatis':what_is},dont_filter=True)        # try:
        #     i = 0
        #     for p in prolinks:
        #         l = 'https://www.drugs.com' + p
        #         yield scrapy.Request(url=l, callback=self.ppadata,
        #                              headers={"User-Agent": "Mozilla Firefox 12.0"},
        #                              meta={'genaricname': genaricNames[i],'brandname': brandNames[i], 'whatis':whIs[i],'whatis1':whIs1[i],'whatis2':whIs2[i]})
        #
        #         i += 1
        # except:
        #     pass

    def ppadata(self,response):

        # index=response.xpath('//div[@class="content"]')
        #
        # for x in index.xpath('//h2/text()').extract():
        #     a=x.split('Pronunciation')[0]
        #     b=a.split('Dosage Forms')[-1]

        content = response.css(".contentBox")

        h2s = content.css('h2')
        indexTerm = ""
        afterIndexTerm = ""
        for h2 in h2s:
            if indexTerm != "":
                afterIndexTerm = h2.xpath('./text()').extract_first()
                break
            text = h2.xpath('./text()').extract_first()

            if 'Index Terms' in text:
                indexTerm = h2.xpath('./text()').extract_first()
        all_text = '\n'.join(content.xpath('.//text()').extract())
        index = ""
        if indexTerm != "" and afterIndexTerm != "":
            index = all_text.split(indexTerm)[1].split(afterIndexTerm)[0].strip()

        dosage_form_before = ""
        dosage_form_after = ""
        for h2 in h2s:
            if dosage_form_before != "":
                dosage_form_after = h2.xpath('./text()').extract_first()
                break
            text = h2.xpath('./text()').extract_first()

            if 'Dosage Forms' in text:
                dosage_form_before = h2.xpath('./text()').extract_first()
        all_text = '\n'.join(content.xpath('.//text()').extract())
        dosage_form = ""
        if dosage_form_before != "" and dosage_form_after != "":
            dosage_form = all_text.split(dosage_form_before)[1].split(dosage_form_after)[0].strip()

        # dsg1= response.xpath('//p[3]/text()').extract()
        # dsg2= response.xpath('//p[4]/text()').extract()
        # dsg3= response.xpath('//p[5]/text()').extract()
        # dosage= ''.join(dsg1)+''.join(dsg2)+''.join(dsg3)


        yield {
            "Url": response.url,
            # "Dosage Forms": dosage,


            "Generic Name":response.meta['genaricname'],
            "Brand Name:": response.meta['brandname'],
            "What is": response.meta['whatis'],
            "Index Term":index,
            "Dosage Form":dosage_form

        }

