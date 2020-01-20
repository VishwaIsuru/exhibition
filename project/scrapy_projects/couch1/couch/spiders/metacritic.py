import scrapy
import csv

class WorkSpider(scrapy.Spider):
    name = 'metacritic'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            "Title","Network","Season","Meta Score","# of critics","User score","Genre","Genre 2","Permise Date","# of rating"

        ]
    };

    urls = [
        "https://www.metacritic.com/browse/tv/genre/date/business?view=condensed",
        "https://www.metacritic.com/browse/tv/genre/date/arts?view=condensed",
        "https://www.metacritic.com/browse/tv/genre/date/educational?view=condensed",
        "https://www.metacritic.com/browse/tv/genre/date/eventsspecials?view=condensed",
        "https://www.metacritic.com/browse/tv/genre/date/foodcooking?view=condensed",
        "https://www.metacritic.com/browse/tv/genre/date/kids?view=condensed",
        "https://www.metacritic.com/browse/tv/genre/date/news?view=condensed",
        "https://www.metacritic.com/browse/tv/genre/date/soap?view=condensed",
        "https://www.metacritic.com/browse/tv/genre/date/techgaming?view=condensed",
        "https://www.metacritic.com/browse/tv/genre/date/travel?view=condensed",
        "https://www.metacritic.com/browse/tv/genre/date/variety-shows?view=condensed"
    ]
    i = 0
    while i < 63: #63
        ur = "https://www.metacritic.com/browse/tv/genre/date/drama?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 18:#18
        ur = "https://www.metacritic.com/browse/tv/genre/date/actionadventure?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 3:
        ur = "https://www.metacritic.com/browse/tv/genre/date/animation?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 38:#38
        ur = "https://www.metacritic.com/browse/tv/genre/date/comedy?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 8:
        ur = "https://www.metacritic.com/browse/tv/genre/date/documentary?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 7:
        ur = "https://www.metacritic.com/browse/tv/genre/date/fantasy?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 5:
        ur = "https://www.metacritic.com/browse/tv/genre/date/gameshow?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 2:
        ur = "https://www.metacritic.com/browse/tv/genre/date/healthlifestyle?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 4:
        ur = "https://www.metacritic.com/browse/tv/genre/date/horror?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 10:#10
        ur = "https://www.metacritic.com/browse/tv/genre/date/moviemini-series?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 4:
        ur = "https://www.metacritic.com/browse/tv/genre/date/music?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 4:
        ur = "https://www.metacritic.com/browse/tv/genre/date/newsdocumentary?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 10:
        ur = "https://www.metacritic.com/browse/tv/genre/date/reality?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 1:
        ur = "https://www.metacritic.com/browse/tv/genre/date/science?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 9:
        ur = "https://www.metacritic.com/browse/tv/genre/date/sciencefiction?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 1:
        ur = "https://www.metacritic.com/browse/tv/genre/date/sports?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 15:
        ur = "https://www.metacritic.com/browse/tv/genre/date/suspense?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1

    i = 0
    while i < 2:
        ur = "https://www.metacritic.com/browse/tv/genre/date/talkinterview?view=condensed&page=" + str(i)
        urls.append(ur)
        i += 1



    def start_requests(self):

        i=0
        for u in self.urls:
            yield scrapy.Request(url=u, callback=self.parse,meta={'Index':i})
            i+=1
            # break
    def parse(self, response):
        details = response.xpath('//ol/li/div/div/a')
        links = details.xpath('.//@href').extract()

        # print links
        for link in links:
            l='https://www.metacritic.com'+link
            yield scrapy.Request(url=l,callback = self.parseInside, headers={'User-Agent': 'Mozilla Firefox 12.0'},meta={'A':'sd'})
        # print l

    def parseInside(self,response):
        network=response.xpath('//div[@class="details_section"]/table/tr/td/span/a/text()').extract()
        season = response.xpath('//div[@class="product_page_title oswald"]/h1/text()').extract()
        # seasons = ' '.join([x.strip() for x in season.split(':')[0]])
        title=response.xpath('//div[@class="product_page_title oswald"]/h1/a/text()').extract()
        metascore = response.xpath('//div[@class="score fl"]/div[@class="metascore_w larger tvshow mixed"]/text()').extract()
        critics = response.xpath('//div[@class="score_wrap"]/div[@class="metascore_w header_size tvshow positive indiv"][1]/text()').extract_first()
        userscr = response.xpath('//div[@class="score fl"]/div[@class="metascore_w user larger tvshow positive"]/text()').extract()
        genre = response.xpath('//div[@class="genres"]/span[2]/span[1]/text()').extract()
        genre2 = response.xpath('//div[@class="genres"]/span[2]/span[2]/text()').extract()
        permisedate =response.xpath('//div[@class="details_section"]/table/tr/td/span[2]/span[2]/text()').extract()
        # mpositv=['']
        # mmixed=['']
        # mnegtiv=['']
        mp = [0],
        up = [0],
        mm = [0],
        um = [0],
        mn = [0],
        un = [0],
        try:
            mpositv = response.xpath('//div[@class="fxdcol gu4"][1]/div[@class="distribution"]/div[@class="charts fl"]')
            if mpositv.xpath('.//a[1]/div[@class="chart positive"]/div[@class="text oswald"]'):
                mp=mpositv.xpath('.//div[@class="count fr"]/text()').extract_first()
                pass
            else :
                # mpositv.xpath('.//span/div[@class="chart positive"]/div[@class="text oswald"]/div[@class="count fr"]'):
                mp=mpositv.xpath('.//span[1]/div[@class="chart positive"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
        except:
            pass
        try:
            upositv = response.xpath('//div[@class="fxdcol gu4"][2]/div[@class="distribution"]/div[@class="charts fl"]')
            if upositv.xpath('.//a[1]/div[@class="chart positive"]/div[@class="text oswald"]'):
                up=upositv.xpath('.//div[@class="count fr"]/text()').extract_first()
                pass
            else:
                up=upositv.xpath('.//span[1]/div[@class="chart positive"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()

        except:
            pass

        try:
            mmixed= response.xpath('//div[@class="fxdcol gu4"][1]/div[@class="distribution"]/div[@class="charts fl"]')
            if mmixed.xpath('.//a[1]'):
                mm=mmixed.xpath('.//div[@class="chart mixed"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif mmixed.xpath('.//a[2]'):
                mm=mmixed.xpath('.//div[@class="chart mixed"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif mmixed.xpath('.//span[1]'):
                mm=mmixed.xpath('.//div[@class="chart mixed"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif mmixed.xpath('.//span[2]'):
                mm=mmixed.xpath('.//div[@class="chart mixed"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
        except:
            pass

        try:
            umixed = response.xpath('//div[@class="fxdcol gu4"][2]/div[@class="distribution"]/div[@class="charts fl"]')
            if umixed.xpath('.//a[1]'):
                um=umixed.xpath('.//div[@class="chart mixed"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif umixed.xpath('.//a[2]'):
                um=umixed.xpath('.//div[@class="chart mixed"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif umixed.xpath('.//span[1]'):
                um=umixed.xpath('.//div[@class="chart mixed"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif umixed.xpath('./span[2]'):
                um=umixed.xpath('.//div[@class="chart mixed"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
        except:
            pass

        try:
            mnegtiv= response.xpath('//div[@class="fxdcol gu4"][1]/div[@class="distribution"]/div[@class="charts fl"]')
            if mnegtiv.xpath('.//a[1]'):
                mn=mnegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif mnegtiv.xpath('.//a[2]'):
                mn = mnegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif mnegtiv.xpath('.//a[3]'):
                mn = mnegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif mnegtiv.xpath('./span[1]'):
                mn = mnegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif mnegtiv.xpath('./span[2]'):
                mn = mnegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif mnegtiv.xpath('./span[3]'):
                mn = mnegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
        except:
            pass

        # unegtiv= response.xpath('//div[@class="fxdcol gu4"][2]/div[@class="distribution"]/div[@class="charts fl"]/a[2]/div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract()
        try:
            unegtiv= response.xpath('//div[@class="fxdcol gu4"][2]/div[@class="distribution"]/div[@class="charts fl"]')
            if unegtiv.xpath('.//a[1]'):
                un=unegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif unegtiv.xpath('.//a[2]'):
                un = unegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif unegtiv.xpath('.//a[3]'):
                un = unegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif unegtiv.xpath('./span[1]'):
                un = unegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif unegtiv.xpath('./span[2]'):
                un = unegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
            elif unegtiv.xpath('./span[3]'):
                un = unegtiv.xpath('.//div[@class="chart negative"]/div[@class="text oswald"]/div[@class="count fr"]/text()').extract_first()
                pass
        except:
            pass
        # n1=[mnegtiv]
        # n2=[unegtiv]
        # p1=[mpositv]
        # p2=[upositv]
        # m1=[mmixed]
        # m2=[umixed]

        try:
            rating=int(mm)+int(um)+int(up)+int(mp)+int(mn)+int(un)
        except:
            rating=''




        yield {
            "Network":network,
            "Season":season,
            "Title": title,
            "Meta Score": metascore,
            "# of critics": critics,
            "User score": userscr,
            "Genre": genre,
            "Genre 2": genre2,
            "Permise Date": permisedate,
            "# of rating": rating,
            # "n1":mnegtiv,
            # "n2":unegtiv,"m1":mmixed,"m2":umixed,
            # "p1":mm,
            # "p2":um,


        }