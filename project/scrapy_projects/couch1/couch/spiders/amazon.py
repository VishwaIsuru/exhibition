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
    name = "amazon"

    def write(self):
        # while(True):
        with connection.cursor() as cursor:
            sql = "SELECT distinct 0,ASIN,URL,TITLE,BY_V,VENDOR,VENDOR_ID,ALL_REVIEW,VERIFIED_REVIEW,NON_VERIFIED_REVIEW FROM T_ASIN_DATA WHERE NON_VERIFIED_REVIEW>0"
            cursor.execute(sql)
            data = cursor.fetchall()

            # asd=[]
            # for d in data:
            #     k = str(d[0]).strip()
            #     if 'X' not in k:
            #         # k=k+"y"
            #         k = k.lstrip("0")
            #     asd.append(k)
            # format_strings = ','.join(['%s'] * len(asd))
            # with connection.cursor() as cursor:
            #     sql = "UPDATE T_ASIN SET done='GOT' where ASIN IN (%s)"% format_strings
            # print(d[0].strip())
            # k=str(d[0]).strip()

            # cursor.execute(sql, (tuple(asd)))
            connection.commit()
            print("here")
            i = 0
            with open('asinData12.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(["ID","ASIN","URL","Title","By_V","Vendor","Vendor ID","All Review","Verfied Review","Non Verified Reviews"])
            for d in data:
                i += 1
                print(i)
                with open('asinData12.csv', 'a+') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(
                        [i, d[1].strip(), d[2].strip(), d[3].strip(), d[4].strip(), d[5], d[6], d[7], d[8], d[9]])
                # csvFile.flush()
                # csvFile.close()

    def start_requests(self):
        notDoneItems = []
        chars = "df"
        self.write()

        with connection.cursor() as cursor:
            sql = "SELECT ID,ASIN FROM T_ASIN where done != %s"
            cursor.execute(sql, ("GOT"))
            notDoneItems = cursor.fetchall()
            connection.commit()

        for d in notDoneItems:
            # with connection.cursor() as cursor:
            #     sql = "SELECT ASIN FROM T_ASIN_DATA where ASIN= %s"
            #     cursor.execute(sql, (d[1]))
            #     ks = cursor.fetchall()
            #     connection.commit()
            #     if len(ks)>0:
            #         with connection.cursor() as cursor:
            #             sql = "UPDATE T_ASIN SET done='GOT' where ID=%s"
            #             cursor.execute(sql, (d[0]))
            #             connection.commit()
            #         continue
            header = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
                    d[0]) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }
            j = 10 - len(d[1].strip())
            if j > 0:
                asin = ''.join(['0'] * j) + d[1].strip()
            else:
                asin = d[1].strip()
            url = 'https://www.amazon.com/dp/' + asin

            with connection.cursor() as cursor:
                # print("DONE")
                sql = "UPDATE T_ASIN SET done='CALL' WHERE" \
                      " ID=%s"
                cursor.execute(sql, d[0])
                connection.commit()
            yield scrapy.Request(url, callback=self.parse, headers=header, meta={'ASIN': asin, 'ID': d[0]})

        # header = {
        #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        #     "accept-encoding": "gzip, deflate, br",
        #     "accept-language": "en-US,en;q=0.9",
        #     "upgrade-insecure-requests": "1",
        #     "user-agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
        #         34) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        # }
        # yield scrapy.Request('https://www.amazon.com/dp/B00DI8A4HU',headers=header, callback=self.parse,meta={'ASIN': 'B00DI8A4HU',"ID":1})

    def parseReview(self, response):
        t = response.body.decode('utf-8')
        # print(response.body)
        # print(t.split('Showing')[1])
        try:
            f = response.css('div.a-box:nth-child(2) > div:nth-child(1) > h4:nth-child(2)').xpath(
                './text()').extract_first().strip()
            if "Enter the characters you see below" in f:
                with connection.cursor() as cursor:
                    # print("DONE")
                    sql = "UPDATE T_ASIN SET done='ERR' WHERE" \
                          " ID=%s"
                    cursor.execute(sql, response.meta['ID'])
                    connection.commit()
                return
        except:
            pass
        count = \
            response.xpath('//*[@id="filter-info-section"]/span/text()').extract_first().split("of")[1].split(
                'reviews')[
                0].strip().replace(",", "")
        print("ddddddddddddddddddddd" + count)

        data = response.meta['data']

        data['ALL_REVIEW'] = count

        url = response.url.split('reviewerType=all')[0] + 'reviewerType=avp_only_reviews&pageNumber=1'

        header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
                data['ASIN']) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        yield scrapy.Request(url, callback=self.parseReviewVeri, meta={'data': data, 'ID': response.meta['ID']})

    def parseReviewVeri(self, response):
        t = response.body.decode('utf-8')
        # print(response.body)
        # print(t.split('Showing')[1])
        try:
            f = response.css('div.a-box:nth-child(2) > div:nth-child(1) > h4:nth-child(2)').xpath(
                './text()').extract_first().strip()
            if "Enter the characters you see below" in f:
                with connection.cursor() as cursor:
                    # print("DONE")
                    sql = "UPDATE T_ASIN SET done='ERR' WHERE" \
                          " ID=%s"
                    cursor.execute(sql, response.meta['ID'])
                    connection.commit()
                return
        except:
            pass
        try:
            count = response.xpath('//*[@id="filter-info-section"]/span/text()').extract_first().split("of")[1].split(
                'reviews')[0].strip().replace(",", "")
        except:
            # print(response.body)
            count = "0"
            # return
        print("ddddddddddddddddddeeeeeeeeeeeeeeddd" + count)

        data = response.meta['data']

        data['VERIFIED_REVIEW'] = count
        with connection.cursor() as cursor:
            sql = "INSERT INTO T_ASIN_DATA (ASIN, URL, TITLE, BY_V, VENDOR, VENDOR_ID, ALL_REVIEW,VERIFIED_REVIEW,NON_VERIFIED_REVIEW,EDITED)" \
                  " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s , %s)"
            s = int(data["ALL_REVIEW"]) - int(data["VERIFIED_REVIEW"])
            v = ''.join([i if ord(i) < 128 else '' for i in data["Vendor"]])
            rt = ''.join([i if ord(i) < 128 else '' for i in data["title"]])
            bb = ''.join([i if ord(i) < 128 else '' for i in data["By"]])
            print(v)
            print(data)
            ed = 'N'
            if v != data["Vendor"]:
                ed = 'Y'
            cursor.execute(sql,
                           (data['ASIN'], data["URL"], rt, bb, v, data["VendorID"],
                            data["ALL_REVIEW"], data["VERIFIED_REVIEW"], s, ed))
            connection.commit()

        with connection.cursor() as cursor:
            # print("DONE")
            sql = "UPDATE T_ASIN SET done='GOT' WHERE" \
                  " ID=%s"
            cursor.execute(sql, response.meta["ID"])
            connection.commit()

    def parse(self, response):
        # print("dfsssssssssss")
        # print(response.body)
        try:
            f = response.css('div.a-box:nth-child(2) > div:nth-child(1) > h4:nth-child(2)').xpath(
                './text()').extract_first().strip()
            if "Enter the characters you see below" in f:
                with connection.cursor() as cursor:
                    # print("DONE")
                    sql = "UPDATE T_ASIN SET done='ERR' WHERE" \
                          " ID=%s"
                    cursor.execute(sql, response.meta['ID'])
                    connection.commit()
                return
        except:
            pass
        try:
            title = response.css('#productTitle').xpath('./text()').extract_first().strip()
        except:
            title = response.css("#title").xpath('./text()').extract_first().strip()
        by = response.css('.author').xpath('./span/a/text()').extract_first()
        if title == '' or title == None:
            title = 'N/A'
        print(title)
        if by == '' or by == None:
            by = 'N/A'
        sellerComp = response.css('#sellerProfileTriggerId')
        vendor = 'N/A'
        vendorID = 'None'
        try:
            vendor = sellerComp.xpath('./text()').extract_first()
        except:
            pass
        if vendor == None:
            vendor = 'N/A'

        try:
            vendorID = sellerComp.xpath('./@href').extract_first().split('seller=')[1]
        except:
            pass
        if vendorID == None:
            vendorID = 'None'

        if title == 'N/A' and by == 'N/A':
            with connection.cursor() as cursor:
                print("SSSSDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
                sql = "INSERT INTO T_ASIN_DATA (ASIN, URL, TITLE, BY_V, VENDOR, VENDOR_ID, ALL_REVIEW,VERIFIED_REVIEW,NON_VERIFIED_REVIEW)" \
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql,
                               (response.meta['ASIN'], response.url, 'N/A', 'N/A', 'N/A', 'None', 'N/A', 'N/A', 'N/A'))
            connection.commit()
            return

        data = {
            "ASIN": response.meta['ASIN'],
            "URL": response.url,
            "title": title,
            "By": by,
            "Vendor": vendor,
            "VendorID": vendorID,
            "ALL_REVIEW": 0,
            "VERIFIED_REVIEW": 0
        }

        reviewLink = 'https://www.amazon.com/Prophet-Kahlil-Gibran/product-reviews/' + data[
            'ASIN'] + '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
        if reviewLink != '' and reviewLink != None:
            form = {"sortBy": "",
                    "reviewerType": "all_reviews",
                    "formatType": "",
                    "mediaType": "",
                    "filterByStar": "",
                    "pageNumber": "1",
                    "filterByLanguage": "",
                    "filterByKeyword": "",
                    "shouldAppend": "undefined",
                    "deviceType": "desktop",
                    "reftag": "cm_cr_arp_d_viewopt_rvwer",
                    "pageSize": "10",
                    "asin": data['ASIN'],
                    "scope": "reviewsAjax0"}
            chars = "fsg"

            header = {
                "accept": "text/html,*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "content-length": "244",
                "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                "origin": "https://www.amazon.com",
                "user-agent": "Mozilla/4.0 (X11; Linux x86_64)" + data[
                    'ASIN'] + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"}

            url = 'https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_arp_d_viewopt_rvwer'

            # yield FormRequest(url, callback=self.parseReviewAll, formdata=form, headers=header,meta={'data': data,'ID':response.meta['ID']})

            u = 'https://www.amazon.com' + response.xpath(
                '//*[@id="reviews-medley-footer"]/div[2]/a/@href').extract_first()
            print(u)
            header = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
                    data['ASIN']) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
            }
            yield scrapy.Request(u, callback=self.parseReview, meta={'data': data, 'ID': response.meta['ID']})

    def parseReviewAll(self, response):
        print('ssfdf')
        t = response.body.decode('utf-8')
        # print(response.body)
        # print(t.split('Showing')[1])
        try:
            f = response.css('div.a-box:nth-child(2) > div:nth-child(1) > h4:nth-child(2)').xpath(
                './text()').extract_first().strip()
            if "Enter the characters you see below" in f:
                with connection.cursor() as cursor:
                    # print("DONE")
                    sql = "UPDATE T_ASIN SET done='ERR' WHERE" \
                          " ID=%s"
                    cursor.execute(sql, response.meta['ID'])
                    connection.commit()
                return
        except:
            pass
        count = ''
        try:
            count = t.split('Showing')[1].split('of')[1].split('reviews')[0].strip().replace(',', '')
        except:
            pass
        data = response.meta['data']

        data['ALL_REVIEW'] = count

        print('ddddddddffffffffffffffffffffffffffffffffff' + count)
        print('ddddddddffffffffffffffffffffffffffffffffff' + response.url)
        # url='https://www.amazon.com/Prophet-Kahlil-Gibran/product-reviews/'+data['ASIN']+'/ref=cm_cr_arp_d_viewopt_rvwer?ie=UTF8&reviewerType=avp_only_reviews&pageNumber=1'

        form = {"sortBy": "",
                "reviewerType": "avp_only_reviews",
                "formatType": "",
                "mediaType": "",
                "filterByStar": "",
                "pageNumber": "1",
                "filterByLanguage": "",
                "filterByKeyword": "",
                "shouldAppend": "undefined",
                "deviceType": "desktop",
                "reftag": "cm_cr_arp_d_viewopt_rvwer",
                "pageSize": "10",
                "asin": data['ASIN'],
                "scope": "reviewsAjax0"}
        chars = "sd"
        header = {
            "accept": "text/html,*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-length": "244",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "origin": "https://www.amazon.com",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64)" + data[
                'ASIN'] + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"}

        url = 'https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_arp_d_viewopt_rvwer'

        yield FormRequest(url, callback=self.parseReviewVerified, formdata=form, headers=header,
                          meta={"data": data, 'ID': response.meta['ID']})

    def parseReviewVerified(self, response):
        # print(response.body)
        count = ''
        t = response.body.decode('utf-8')
        try:
            f = response.css('div.a-box:nth-child(2) > div:nth-child(1) > h4:nth-child(2)').xpath(
                './text()').extract_first().strip()
            if "Enter the characters you see below" in f:
                with connection.cursor() as cursor:
                    # print("DONE")
                    sql = "UPDATE T_ASIN SET done='ERR' WHERE" \
                          " ID=%s"
                    cursor.execute(sql, response.meta['ID'])
                    connection.commit()
                return
        except:
            pass
        try:
            count = t.split('Showing')[1].split('of')[1].split('reviews')[0].strip().replace(',', '')

        except:
            pass
        data = response.meta['data']

        data['VERIFIED_REVIEW'] = count
        with connection.cursor() as cursor:
            v = data["Vendor"].replace('//', '@@@@')
            sql = "INSERT INTO T_ASIN_DATA (ASIN, URL, TITLE, BY_V, VENDOR, VENDOR_ID, ALL_REVIEW,VERIFIED_REVIEW,NON_VERIFIED_REVIEW)" \
                  " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            s = int(data["ALL_REVIEW"]) - int(data["VERIFIED_REVIEW"])
            cursor.execute(sql,
                           (data['ASIN'], data["URL"], data["title"], data["By"], v, data["VendorID"],
                            data["ALL_REVIEW"], data["VERIFIED_REVIEW"], s))
            connection.commit()

        with connection.cursor() as cursor:
            # print("DONE")
            sql = "UPDATE T_ASIN SET done='GOT' WHERE" \
                  " ID=%s"
            cursor.execute(sql, response.meta["ID"])
            connection.commit()
