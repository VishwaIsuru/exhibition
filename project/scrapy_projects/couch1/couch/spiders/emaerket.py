import scrapy
import csv

csv.register_dialect('myDialect', delimiter='/', quoting=csv.QUOTE_NONE)


class workspider(scrapy.Spider):
    name = "emarket"




    def start_requests(self):

        with open('notdonedata.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(
                ["URL","Title", "Make", "Model", "Variant", "Price", "Warranty", "Year", "km", "City", "Transmission",
                 "Doors", "CV", "Color", "Fuel", "Seller", "Post code", "Address1", "Address2", "Link", "Full Address"])

        starts = []
        with open('not_run.csv') as f:
            starts = [url.strip() for url in f.readlines()]

        # start = "https://www.coches.net/citroen-grand-c4-picasso-16-hdi-cmp-sx-5p-diesel-2009-en-madrid-38540612-covo.aspx"

        for i in range(0, len(starts)):
            s=starts[i]
            # s=
            yield scrapy.Request(url=s, callback=self.parseMain, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                   'Accept-Encoding': 'gzip, deflate, br',
                                    'Accept-Language':'en-US,en;q=0.5',
                                    'Connection':'keep-alive','TE':'Trailers','Upgrade-Insecure-Requests':1,
                                    'Host':'www.coches.net', 'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'})

    def parseMain(self, response):

        price = response.css('.mt-AdPrice-amount > strong:nth-child(1)').css('::text').extract()
        if len(price)==1:
            price= response.css('.mt-AdPrice-amount > strong:nth-child(1)').css('::text').extract_first()
            title = response.css('h1.t-h2').css('::text').extract()
            title="".join(title).strip()

            make=response.css('.js-Breadcrumb').xpath('.//a[@data-tagging="c_detail_bread_ad_brand"]').xpath('.//text()').extract_first()
            model=response.css('.js-Breadcrumb').xpath('.//a[@data-tagging="c_detail_bread_ad_model"]').xpath('.//text()').extract_first()
            variant=response.css('.js-Breadcrumb').xpath('.//span[@class="mt-Breadcrumb-link mt-Breadcrumb-link--active"]').xpath('.//text()').extract_first()
            city_head=response.css('.js-Breadcrumb').xpath('.//a[@data-tagging="c_detail_bread_ad_province"]').xpath('.//text()').extract_first()

            year = response.css('li.mt-DataGrid-item:nth-child(1) > b:nth-child(1)').css('::text').extract_first()


            seller = response.css('.mt-ProfileCard-title').css('::text').extract()
            seller="".join(seller).strip()
            address1=response.css('.mt-ProfileCard-content > p:nth-child(2)').css('::text').extract_first()
            full_address = response.css('.mt-ProfileCard-content > p:nth-child(3)').css('::text').extract_first()
            post_code=""
            address2=""
            try:
                post_code=full_address.split(" ")[0]
                o = full_address.split(" ")[1:]
                address2=" ".join(o)
            except:
                pass
            p = "https://www.coches.net"
            link=response.css('#_ctl0_ContentPlaceHolder1_AdSeller_sellerLogo').xpath('.//@href').extract_first()
            link=p+str(link)

            q = response.css('#_ctl0_ContentPlaceHolder1_AdInfo__ctl0_ul_infoItems').css('::text').extract()
            km=''
            transmission=''
            doors=''
            cv=''
            fuel=''
            warranty=''
            a = []
            for i in range(0, len(q)):
                if '\n' not in q[i]:
                    a.append(q[i])
            b=[]
            c = []
            for i in range(0, len(b)):
                try:
                    int(b[i])
                except ValueError:
                    c.append(b[i])
            try:
                color=c[0]
            except IndexError:
                color="@@@@@@@@@@@@"

            for i in range(0,len(q)):
                        if 'km' in q[i] and 'gr' not in q[i]:
                            km=str(q[i - 1])
                        elif 'Cambio' in q[i]:
                            transmission=q[i+1]
                        elif 'Puertas' in q[i]:
                            doors =(q[i - 1] + q[i]).strip()
                        elif 'cv' in q[i] :
                            cv=(q[i-1]+q[i]).strip()


            # with open('notdonedata.csv', 'a+') as csvFile:
            #     writer = csv.writer(csvFile, csv.register_dialect('myDialect', delimiter='/', quoting=csv.QUOTE_NONE))
            #     writer.writerow([response.url,title,make,model,variant,price,warranty,year,km,city_head,transmission,doors,cv,color,fuel,seller,post_code,address1,address2,link,full_address])





