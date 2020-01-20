import scrapy


class WorkSpider(scrapy.Spider):
    name = 'amazonData'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            # "TopUrl","Item","d",
            "Description url",
            "Main Name"
            # DetailsOf"

        ]
    };

    def start_requests(self):
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
                31111111111111) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Referer": "https://www.amazon.com",
            "Origin": "https://www.amazon.com",
            "Connection": "keep-alive",
        }
        # for uall in url:
        url = 'https://www.amazon.com/gp/search/other/ref=sr_in_c_A?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=c&ie=UTF8&qid=1574672143'

        yield scrapy.Request(url=url, headers=header, callback=self.parse, dont_filter=True,meta={'page':1})

    def parse(self, response):
        # print(response.body)
        details = response.css('.a-list-item > a').xpath('//a[@class="a-link-normal"]')
        # print (response.css('.a-link-normal >a').xpath('./@href').extract())
        # print details

        links = []
        # print links
        # yield {
        #    d : details
        # }
        for detail in details:
            link = 'https://www.amazon.com' + detail.xpath('./@href').extract_first()
            links.append(link)

        # x=[]
        # my_new_list = [ string for x in links +x]

        for l in links:
            # print(l)
            header = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
                    563235) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "Referer": "https://www.amazon.com",
                "Origin": "https://www.amazon.com",
                "Connection": "keep-alive",
            }
            yield scrapy.Request(url=l, callback=self.parseInside, headers=header, meta={'page': 1})
            # break

    def parseInside(self, response):
        next_page = response.meta['page'] + 1

        description = response.xpath('//a[@class= "a-link-normal a-text-normal"]')
        # i =[]
        # try:
        # for desc in description:

        for descriptonur in description.xpath('./@href').extract():
            descriptonur = 'https://www.amazon.com' + descriptonur
            yield {"Description url": descriptonur, "Main Name": response.url}
            # print('data found')

        # print(response.body)
        pages = response.css('.a-pagination').xpath('.//li[@class="a-normal"]')
        print next_page
        print(pages)
        for page in pages:
            print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWww")
            text = page.css('a').xpath('./text()').extract_first()
            pageNum = int(text)
            if pageNum == next_page:
                header = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
                        pageNum) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                    "Referer": "https://www.amazon.com",
                    "Origin": "https://www.amazon.com",
                    "Connection": "keep-alive",
                }

                l='https://www.amazon.com' +page.xpath('./a/@href').extract_first()
                yield scrapy.Request(url=l, callback=self.parseInside, headers=header, meta={'page': next_page})
                break
