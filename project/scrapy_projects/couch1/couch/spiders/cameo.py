# -*- coding: utf-8 -*-
import scrapy
import re
import json
import csv
import pymysql.cursors
from scrapy.http import FormRequest
import random
import string
import sys
# -*- coding: utf-8 -*-
reload(sys)
sys.setdefaultencoding('utf8')
# import pandas
from difflib import SequenceMatcher


class workspider(scrapy.Spider):
    name = "cameo"
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["Link",
                               "Category",
                               "Name",
                               "Subtitle",
                               "Price",
                               "Review",
                               "Rating",
                               "Response Hours",
                               "Other Tags",
                               "Wiki Link",
                               "Age",
                               "Birthday",
                               "Birth Place",
                               "Residence",
                               "Occupation"
                               ]
    };

    liste = ['https://www.cameo.com/c/bloggers']

    def start_requests(self):
        # yield {
        #     'link':'https://www.cameo.com/c/bloggers'
        # }
        # yield scrapy.Request(url='https://www.cameo.com/c/bloggers', callback=self.find_cat, headers={'User-Agent': 'Mozilla Firefox 12.0'
        #                                                                })
        f = open("cameo1.csv", "r")
        contents = f.read().split('\n')
        i = 0
        # contents=['','https://www.cameo.com/c/actors']
        for c in contents:
            i += 1
            if i == 1:
                continue
            yield scrapy.Request(url=c.strip(), callback=self.parse,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'})
            # break

    def parse(self, response):
        cat = response.css('._3UyICHtWDCeNGzm_sAmyWc').xpath('./text()').extract_first().split('(')[0]
        boxes = response.css('._3MIlewVA4cdAuM4ng32tde')
        chars = []
        for box in boxes:
            chr = 'https://www.cameo.com' + box.css('._3yEJGdKwGboMQH4nTumQvk').css('a').xpath(
                './@href').extract_first()
            chars.append(chr)

        for l in chars:
            yield scrapy.Request(url=l, callback=self.character,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'}, meta={'cat': cat}, dont_filter=True)

    def character(self, response):
        cat = response.meta['cat']
        name = response.css('#profile-bio-name').xpath('./text()').extract_first()
        prof = response.css('#profile-bio-profession').xpath('./text()').extract_first()

        if prof == None or prof.strip() == '':
            prof = response.css('.profile-bio-text').xpath('./text()').extract_first()
        # prof=prof.strip().split('-')[0].strip()
        price = '$' + response.css('#bookButton').xpath('./text()').extract_first().strip().split('$')[-1]
        ratingVal = ''
        try:
            ratingVal = response.css('#profile-ratings').css('b').xpath('./text()').extract_first()
        except:
            pass
        rate = ''
        try:
            rate = response.css('._3f6X2oCJ0q5_HCpRbtxAsh').xpath('./text()').extract_first().replace('stars',
                                                                                                      '').strip()
        except:
            pass
        time = ''
        try:
            time = response.css('._389SsIExyylqjHRdDu3qPH').xpath('./b//text()').extract()
            time = ''.join(time)
            time=time.strip()
        except:
            pass
        if time!=None and 'day' in time:
            time=str(int(time.split('day')[0].strip())*24)
        elif time!=None and 'hours' in time:
            time = str(int(time.split('hours')[0].strip()) * 24)
        tagStr = ''
        try:
            tags = response.css('._3UyICHtWDCeNGzm_sAmyWc')

            for t in tags:
                tagStr += '|' + t.xpath('./text()').extract_first()
            try:
                tagStr = tagStr[1:]
            except:
                pass
        except:
            pass

        # if name!='Thomas Jones':Forms
        #     return

        if prof==None:
            prof=''
        ob = {
            "Link": response.url,
            "Category": cat,
            "Name": name,
            "Subtitle": prof,
            "Price": price,
            "Review": ratingVal,
            "Rating": rate,
            "Response Hours": time,
            "Other Tags": tagStr
        }

        add = name.strip() + ' ' + prof.split('-')[0].strip()
        add = add.replace(' ', '+')
        url = 'https://en.wikipedia.org/w/index.php?sort=relevance&search='+add+'&title=Special:Search&profile=advanced&fulltext=1&advancedSearch-current=%7B%7D&ns0=1'
        yield scrapy.Request(url=url, callback=self.wikipedia_search,
                             headers={'User-Agent': 'Mozilla Firefox 12.0'}, meta={'ob': ob}, dont_filter=True)

    def wikipedia_search(self, response):
        ob = response.meta['ob']
        ob['Wiki Link']=response.url
        name=ob['Name']
        searchText=None
        searchRes=None
        try:
            searchText = response.css('.mw-search-result-heading')[0].xpath('./a//text()').extract()
            searchText=' '.join(searchText)
            searchRes = response.css('.mw-search-result-heading')[0].xpath('./a/@href').extract_first()

            if 'List of' in searchText:
                searchText = response.css('.mw-search-result-heading')[1].xpath('./a//text()').extract()
                searchText = ' '.join(searchText)
                searchRes = response.css('.mw-search-result-heading')[1].xpath('./a/@href').extract_first()

        except:
            pass
        # print(searchText+"llllllllllllllllllll")
        # print(searchText+"  "+name+"  "+str(self.similar(name.lower(),searchText.lower())))
        if searchText==None:
            searchText=''
        else:
            searchText=searchText.split('(')[0]
        if searchRes != None and self.similar(name.lower(),searchText.lower())>0.25:
            url = 'https://en.wikipedia.org' + searchRes

            print('ddddddddddddd  ' + url)

            yield scrapy.Request(url=url, callback=self.wiki_inside,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'}, meta={'ob': ob}, dont_filter=True)
        else:
            print("I am here")
            yield {
                "Link": ob['Link'],
                "Category": ob['Category'],
                "Name": ob['Name'],
                "Subtitle": ob['Subtitle'],
                "Price": ob['Price'],
                "Review": ob['Review'],
                "Rating": ob['Rating'],
                "Response Hours": ob['Response Hours'],
                "Other Tags": ob['Other Tags'],
                "Wiki Link": '',
                "Age": '',
                "Birthday": '',
                "Birth Place": '',
                "Residence": '',
                "Occupation": ''
            }

    def wiki_inside(self, response):
        ob = response.meta['ob']
        bio = response.css('.biography')

        if bio==None or len(bio)==0:
            bio=response.css('.infobox')
        bdy = ''
        age = ''
        birthPlace = ''
        try:
            bdy = response.css('.bday').xpath('./text()').extract_first()
        except:
            pass
        try:
            age = response.css('.ForceAgeToShow').xpath('./text()').extract_first().split('age')[1].split(')')[
                0].strip()
        except:
            pass
        try:
            birthPlace = response.css('.birthplace').xpath('.//text()').extract()
            birthPlace=''.join(birthPlace)
        except:
            pass

        trs = bio.css('tr')
        residence = ''
        occupation = ''
        for tr in trs:
            hed = tr.css('th').xpath('.//text()').extract()
            hed = ' '.join(hed).strip()
            val = tr.css('td').xpath('.//text()').extract()
            val = ' '.join(val).strip()
            vals = tr.css('td').xpath('.//text()').extract()
            vals = '|'.join(vals)
            vals=vals.encode('utf-8')
            vals = vals.replace(',', '').replace('•','')
            print('Hed:'+hed+":::")
            if 'Residence' == hed:
                residence = val
            elif 'Occupation' in hed:
                occupation = vals.strip().replace('\n','')
            elif ('Born' in hed or 'Birth' in hed) and (birthPlace=='' or birthPlace==None):
                print('bith'+vals)
                try:
                    birthPlace = tr.css('td').css('a').xpath('./text()').extract_first().replace('|', ',')+vals.split(',')[-1].split("|")[-1]
                except:
                    birthPlace=vals.split(')')[-1].replace('|',',')
            elif 'Origin'== hed and (birthPlace==None or birthPlace==''):
                birthPlace=val


        try:
            birthPlace = birthPlace.strip().split('[')[0]
            if birthPlace[0]==',':
                birthPlace=birthPlace[1:]
                birthPlace=birthPlace.strip()
        except:
            pass

        yield {
            "Link": ob['Link'],
            "Category": ob['Category'],
            "Name": ob['Name'],
            "Subtitle": ob['Subtitle'],
            "Price": ob['Price'],
            "Review": ob['Review'],
            "Rating": ob['Rating'],
            "Response Hours": ob['Response Hours'],
            "Other Tags": ob['Other Tags'],
            "Wiki Link": response.url,
            "Age": age,
            "Birthday": bdy,
            "Birth Place": birthPlace,
            "Residence": residence,
            "Occupation": occupation
        }

    def find_cat(self, response):
        aas = response.css('._2UVgbrIGQxRzzAieNCcwdQ')
        links = []
        for aa in aas:
            p = 'https://www.cameo.com' + aa.xpath('./@href').extract_first()
            if p not in self.liste:
                self.liste.append(p)
                links.append(p)

                yield {
                    'link': p
                }

        for l in links:
            yield scrapy.Request(url=l, callback=self.find_cat,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'
                                          })

    def similar(self,a, b):
        return SequenceMatcher(None, a, b).ratio()