import scrapy
import re
import json
import csv
import pymysql.cursors
from scrapy.http import FormRequest
import random
import string
# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import csv

csv.register_dialect('myDialect', delimiter='/', quoting=csv.QUOTE_NONE)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='scrape', use_unicode=True, charset="utf8")


class workspider(scrapy.Spider):
    name = "amazonProduct1"
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["ID", "ASIN", "Link", "Product Title", "Sold by",
                               "Best Seller Ranking in Automotive",
                               "Sub Category Ranking","Sub Category Name", "Acutal price", "Cross off Price",
                               "FB 1st Item Link", "FB 1st Item Description", "FB 1st Item Price",
                               "FB 2nd Item Link",
                               "FB 2nd Item Description", "FB 2nd Item Price", "FB 3rd Item Link",
                               "FB 3rd Item Description", "3rd Item Price",
                               "CWB 1st Item Link", "CWB 1st Item Description", "CWB 1st Item Price",
                               "CWB 2nd Item Link", "CWB 2nd Item Description", "CWB 2nd Item Price",
                               "CWB 3rd Item Link", "CWB 3rd Item Description", "CWB 3rd Item Price",
                               "CWB 4th Item Link", "CWB 4th Item Description", "CWB 4th Item Price",
                               "CWB 5th Item Link", "CWB 5th Item Description", "CWB 5th Item Price",
                               "WTB 1st Item Link", "WTB 1st Item Description", "WTB 1st Item Price",
                               "WTB 2nd Item Link", "WTB 2nd Item Description", "WTB 2nd Item Price",
                               "WTB 3rd Item Link", "WTB 3rd Item Description", "WTB 3rd Item Price",
                               "WTB 4th Item Link", "WTB 4th Item Description", "WTB 4th Item Price",
                               "WTB 5th Item Link", "WTB 5th Item Description", "WTB 5th Item Price",
                               "Brand Name", "Item Weight", "Product Dimension", "Item Number",
                               "Manufacturer Number", "Reviews", "Shipping Weight", "Date First Available",
                               "Landing Image URL", "Availability"
                               ]
    };

    def start_requests(self):
        while True:
            notDoneItems = []
            chars = "df"
            # self.write()

            with connection.cursor() as cursor:
                sql = "SELECT ID,Link,ASIN FROM T_AMAZON2 where status = %s"
                cursor.execute(sql, ("PEND"))
                notDoneItems = cursor.fetchall()
                connection.commit()

            for d in notDoneItems:
                header = {
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
                        d[0]) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
                }
                # script = """
                #                                         function main(splash)
                #                                             local url = splash.args.url
                #                                             assert(splash:go(url))
                #                                             assert(splash:wait(6))
                #
                #                                             return {
                #                                                 html = splash:html(),
                #                                             }
                #                                         end
                #                                         """
                # yield scrapy.Request(d[1],
                #                      self.parse, meta={
                #         'splash': {
                #             'args': {'lua_source': script},
                #             'endpoint': 'execute',
                #         }, 'ID': d[0], 'LINK': d[1], 'ASIN': d[2]
                #     }, dont_filter=True)
                yield scrapy.Request(d[1], callback=self.parse, headers=header,
                                     meta={'ID': d[0], 'LINK': d[1], 'ASIN': d[2]},dont_filter=True)

    def parse(self, response):
        # print(response.body)
        try:
            title = response.css('#productTitle').xpath('./text()').extract_first().strip()
        except:
            print(response.body)
        title = response.css('#productTitle').xpath('./text()').extract_first().strip()
        soldBy = ''.join(response.css('#shipsFromSoldByInsideBuyBox_feature_div').xpath('.//text()').extract()).strip()
        if 'P.when("seller-register-popover")' in soldBy:
            soldBy=soldBy.split('P.when("seller-register-popover")')[0].strip()
        try:
            if len(soldBy) > 100:
                print(soldBy)
                return
        except:
            pass

        additionalInfo = response.css('#productDetails_db_sections')

        trs = additionalInfo.xpath('.//table//tr')

        bestSellerRankInAutomative = ''
        subCategory = ''
        # later added
        brandName = ''
        itemWeight = ''
        productDimensions = ''
        itemNumber = ''
        manufectureNumber = ''
        reviews = ''
        shippingWeight = ''
        dateAvailable = ''
        landingImageUrl = ''
        availability = ''
        subCategoryName=''
        for tr in trs:
            thStr = ''.join(tr.css('th').xpath('.//text()').extract())
            tdStr = ''.join(tr.css('td').xpath('.//text()').extract())

            if 'Best Sellers Rank' in thStr:
                try:
                    subCategoryName=tdStr.split(" in ")[-1].strip()
                except:
                    pass
                bestSellerRankInAutomative = tdStr.split("in Automotive")[0].replace(',', '').strip().split("in")[
                    0].strip()
                try:
                    subCategory = '#' + tdStr.split(')')[1].split('#')[1].split('in')[0].strip()
                except:
                    pass
            elif 'review' in thStr.lower():
                rs = tr.css('td').xpath('./text()').extract()
                for r in rs:
                    if 'of' in r:
                        reviews=r.strip();
                        break
            elif 'shipping weight' in thStr.lower():
                shippingWeight = tdStr.strip()
            elif 'date' in thStr.lower() and 'available' in thStr.lower():
                dateAvailable = tdStr.strip()

        landingImageUrl =  response.xpath('//span[@data-action="main-image-click"]//img/@data-old-hires').extract_first()
        availability = response.css('#availabilityInsideBuyBox_feature_div').xpath('.//text()').extract()
        availability=[a.strip() for a in availability]
        availability=' '.join(availability)

        try:
            availability=availability.strip()
        except:
            pass
        techInfo = response.css('#productDetails_techSpec_section_1')
        trs = techInfo.xpath('.//tr')

        for tr in trs:
            thStr = ''.join(tr.css('th').xpath('.//text()').extract()).lower()
            tdStr = ''.join(tr.css('td').xpath('.//text()').extract())

            if 'brand' in thStr:
                brandName = tdStr.strip()
            elif 'item weight' in thStr:
                itemWeight = tdStr.strip()
            elif 'product dimension' in thStr:
                productDimensions = tdStr.strip()
            elif 'item' in thStr and 'number' in thStr:
                itemNumber = tdStr.strip()
            elif 'manufacturer' in thStr and 'number' in thStr:
                manufectureNumber = tdStr.strip()

        # Sometimes left has all
        techInfo = response.css('#productDetails_detailBullets_sections1')
        trs = techInfo.xpath('.//tr')

        for tr in trs:
            thStr = ''.join(tr.css('th').xpath('.//text()').extract()).lower()
            tdStr = ''.join(tr.css('td').xpath('.//text()').extract())

            if 'brand' in thStr:
                brandName = tdStr.strip()
            elif 'item weight' in thStr:
                itemWeight = tdStr.strip()
            elif 'product dimension' in thStr:
                productDimensions = tdStr.strip()
            elif 'item' in thStr and 'number' in thStr:
                itemNumber = tdStr.strip()
            elif 'manufacturer' in thStr and 'number' in thStr:
                manufectureNumber = tdStr.strip()
            elif 'best sellers rank' in thStr:
                try:
                    subCategoryName=tdStr.split(" in ")[-1].strip()
                except:
                    pass
                bestSellerRankInAutomative = tdStr.split("in Automotive")[0].replace(',', '').strip().split("in")[
                    0].strip()
                try:
                    subCategory = '#' + tdStr.split(')')[1].split('#')[1].split('in')[0].strip()
                except:
                    pass
            elif 'review' in thStr.lower():
                rs = tr.css('td').xpath('./text()').extract()
                for r in rs:
                    if 'of' in r:
                        reviews=r.strip();
                        break
            elif 'shipping weight' in thStr.lower():
                shippingWeight = tdStr.strip()
            elif 'date' in thStr.lower() and 'available' in thStr.lower():
                dateAvailable = tdStr.strip()

        priceStr = response.css('#price').xpath('.//text()').extract()

        priceBefore = ''
        priceNow = ''
        priceStr = [p.strip() for p in priceStr]

        priceAct = []
        # print(priceStr)
        # print(priceAct)
        try:
            for p in priceStr:
                if 'was:' == p or 'Was:' == p or '$' in p or 'Price:' == p or 'price:' == p or 'List Price:' == p:
                    priceAct.append(p)

            if 'was' in priceAct[0] or 'Was' in priceAct[0] or 'List Price' in priceAct[0]:
                priceBefore = priceAct[1].split()[0]
            if 'price' in priceAct[0] or 'Price' in priceAct[0]:
                priceNow = priceAct[1].split()[0]
            elif 'price' in priceAct[2] or 'Price' in priceAct[2]:
                priceNow = priceAct[3].split()[0]
        except:
            pass

        similarItems = response.css('.similarities-widget.bucket .forScreenreaders ul li')

        fItemDesctriptions = []
        fItemPrices = []
        fItemLinks = []

        for li in range(0, len(similarItems)):
            text = similarItems[li].xpath('.//text()').extract()
            text=[t.strip() for t in text]
            fItemDesctriptions.append(' '.join(text).strip())
            b = False
            for t in text:
                if '$' in t:
                    fItemPrices.append(t.strip())
                    b = True
                    break
            if not b:
                fItemPrices.append('')
            a=''
            try:
                a = 'https://www.amazon.com' + similarItems[li].xpath('.//a/@href').extract_first()
            except:
                pass
            fItemLinks.append(a)

        count = 3 - len(fItemDesctriptions)
        if count > 0:
            for i in range(count):
                fItemDesctriptions.append('')
                fItemPrices.append('')
                fItemLinks.append('')
        fItemLinks[0]=''

        vps = response.css('#view_to_purchase-sims-feature ul li')

        vpsItemDescription = []
        vpsItemPrices = []
        vpsItemLinks = []

        for v in vps:
            desc = v.xpath('.//text()').extract()
            desc=[d.strip() for d in desc]
            vpsItemDescription.append(' '.join(desc).strip())
            b = False
            for vp in desc:
                if '$' in vp:
                    vpsItemPrices.append(vp)
                    b = True
                    break
            if not b:
                vpsItemPrices.append('')
            a = 'https://www.amazon.com' + v.xpath('.//a/@href').extract_first()
            vpsItemLinks.append(a)

        count = 5 - len(vpsItemDescription)
        if count > 0:
            for i in range(count):
                vpsItemDescription.append('')
                vpsItemPrices.append('')
                vpsItemLinks.append('')

        viewItems = response.css('#desktop-dp-sims_session-similarities-sims-feature ol li')

        viewItemDescriptions = []
        viewItemPrices = []
        viewItemLinks = []

        for v in viewItems:
            texts = v.xpath('.//text()').extract()
            texts=[t.strip() for t in texts]
            viewItemDescriptions.append(' '.join(texts).strip())

            b = False
            for text in texts:
                text = text.strip()
                if '$' in text:
                    viewItemPrices.append(text)
                    b = True
                    break
            if not b:
                viewItemPrices.append('')
            a = 'https://www.amazon.com' + v.xpath('.//a/@href').extract_first()
            viewItemLinks.append(a)

        count = 5 - len(viewItemDescriptions)
        if count > 0:
            for i in range(count):
                viewItemDescriptions.append('')
                viewItemPrices.append('')
                viewItemLinks.append('')

        yield {
            "ID": response.meta["ID"], "ASIN": response.meta['ASIN'], "Link": response.meta['LINK'],
            "Product Title": title, "Sold by": soldBy, "Best Seller Ranking in Automotive": bestSellerRankInAutomative,
            "Sub Category Ranking": subCategory,'Sub Category Name':subCategoryName, "Acutal price": priceNow, "Cross off Price": priceBefore ,
            "FB 1st Item Link": fItemLinks[0], "FB 1st Item Description": fItemDesctriptions[0],
            "FB 1st Item Price": fItemPrices[0], "FB 2nd Item Link": fItemLinks[1],
            "FB 2nd Item Description": fItemDesctriptions[1], "FB 2nd Item Price": fItemPrices[1],
            "FB 3rd Item Link": fItemLinks[2],
            "FB 3rd Item Description": fItemDesctriptions[2], "3rd Item Price": fItemPrices[2],
            "CWB 1st Item Link": vpsItemLinks[0], "CWB 1st Item Description": vpsItemDescription[0],
            "CWB 1st Item Price": vpsItemPrices[0],
            "CWB 2nd Item Link": vpsItemLinks[1], "CWB 2nd Item Description": vpsItemDescription[1],
            "CWB 2nd Item Price": vpsItemPrices[1],
            "CWB 3rd Item Link": vpsItemLinks[2], "CWB 3rd Item Description": vpsItemDescription[2],
            "CWB 3rd Item Price": vpsItemPrices[2],
            "CWB 4th Item Link": vpsItemLinks[3], "CWB 4th Item Description": vpsItemDescription[3],
            "CWB 4th Item Price": vpsItemPrices[3],
            "CWB 5th Item Link": vpsItemLinks[4], "CWB 5th Item Description": vpsItemDescription[4],
            "CWB 5th Item Price": vpsItemPrices[4],
            "WTB 1st Item Link": viewItemLinks[0], "WTB 1st Item Description": viewItemDescriptions[0],
            "WTB 1st Item Price": viewItemPrices[0],
            "WTB 2nd Item Link": viewItemLinks[1], "WTB 2nd Item Description": viewItemDescriptions[1],
            "WTB 2nd Item Price": viewItemPrices[1],
            "WTB 3rd Item Link": viewItemLinks[2], "WTB 3rd Item Description": viewItemDescriptions[2],
            "WTB 3rd Item Price": viewItemPrices[2],
            "WTB 4th Item Link": viewItemLinks[3], "WTB 4th Item Description": viewItemDescriptions[3],
            "WTB 4th Item Price": viewItemPrices[3],
            "WTB 5th Item Link": viewItemLinks[4], "WTB 5th Item Description": viewItemDescriptions[4],
            "WTB 5th Item Price": viewItemPrices[4],
            "Brand Name": brandName, "Item Weight": itemWeight, "Product Dimension": productDimensions,
            "Item Number": itemNumber,
            "Manufacturer Number": manufectureNumber, "Reviews": reviews, "Shipping Weight": shippingWeight,
            "Date First Available": dateAvailable,
            "Landing Image URL": landingImageUrl, "Availability": availability
        }

        with connection.cursor() as cursor:
            # print("DONE")
            sql = "UPDATE T_AMAZON2 SET status='GOT' WHERE" \
                  " ID=%s"
            cursor.execute(sql, response.meta["ID"])
            connection.commit()
