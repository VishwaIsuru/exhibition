import scrapy
import re
import json
import csv
import pymysql.cursors


connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='scrape', use_unicode=True, charset="utf8")


class workspider(scrapy.Spider):
    name = "surname"

    def start_requests(self):
        notDoneItems = []
        with connection.cursor() as cursor:
            sql = "SELECT id, url, surname FROM surnames where done = %s and id > 250000 and id <= 300000"

            cursor.execute(sql, ("N"))
            notDoneItems = cursor.fetchall()

        for i in notDoneItems:
            # s=i[1].replace('https','http')
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
            yield scrapy.Request(i[1], callback=self.parse, headers=headers, meta={'dont_redirect': True,
                                                                                   'handle_httpstatus_list': [301, 302],
                                                                                   'id': i[0], 'surname': i[2]})

    def parse(self, response):
        # print(response.body)
        if (response.status == 200):
            nationsDataTableTr = response.css('#nations-2014').css('tbody').css('tr')
            with connection.cursor() as cursor:
                for tr in nationsDataTableTr:
                    countryData = tr.css('td::text').extract()
                    frequency = tr.css('td>span::text').extract()[0]
                    country = countryData[0]
                    incidence = countryData[1]
                    rank = countryData[2]
                    sql = "INSERT INTO surname_data (country, frequency, incidence, rank, surname, url, done)" \
                          " VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql,
                                   (country, frequency, incidence, rank, response.meta['surname'], response.url, 'Y'))

            with connection.cursor() as cursor:
                similarTableTr = response.css('#similar-table').css('tbody').css('tr')
                for tr in similarTableTr:
                    similar = tr.css('a::text')[0].extract()
                    sql = "INSERT INTO simillar (surname, similar)" \
                          " VALUES (%s, %s)"
                    cursor.execute(sql, (response.meta['surname'], similar))

            with connection.cursor() as cursor:
                cursor.execute("UPDATE surnames SET done='Y1' WHERE id=%s", (response.meta['id']))

            connection.commit()
        elif response.status == 301 or response.status == 302:

            with connection.cursor() as cursor:
                cursor.execute("UPDATE surnames SET done='T' WHERE id=%s", (response.meta['id']))
            connection.commit()

            with open('not_found_1.csv', mode='a') as employee_file:
                employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                employee_writer.writerow([response.meta['surname']])
