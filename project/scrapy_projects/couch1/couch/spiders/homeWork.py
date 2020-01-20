import scrapy


class WorkSpider(scrapy.Spider):
    name = 'homeWork'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["Subject",
                               "Content",
                               "Due Date",
                               "Budget",
                               "Attachment links"
                               ]
    };
    urls = [
        "https://www.homeworkmarket.com/homework-answers",

    ]
    i = 2
    while i < 10:
        ur = "https://www.homeworkmarket.com/homework-answers?page="+str(i)
        urls.append(ur)
        i += 1



    def start_requests(self):
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
                31111111111111) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Referer": "https://www.homeworkmarket.com",
            "Origin": "https://www.homeworkmarket.com",
            "Connection": "keep-alive",


        }

        for u in self.urls:
            #print ('iam here')
            yield scrapy.Request(url=u, headers=header,callback=self.parse, dont_filter=True)

    def parse(self, response):
        #print(response.body)
        #links=[]
        details = response.xpath('//div[@class ="tag-question-header"]')

        for detail in details:
            link = detail.xpath('//h3/a').xpath('./@href').extract()
            #links = 'https://www.homeworkmarket.com' + link
            #links.append(link)

            for links in link:
                l = 'https://www.homeworkmarket.com' + links
                header = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
                        563235) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                    "Referer": "https://www.homeworkmarket.com",
                    "Origin": "https://www.homeworkmarket.com",
                    "Connection": "keep-alive",
                }
                yield scrapy.Request(url=l, callback=self.parseInside,
                                     headers={'User-Agent': header},
                                     )
    def parseInside(self,response):
        header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" + str(
                563235) + " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Referer": "https://www.homeworkmarket.com",
            "Origin": "https://www.homeworkmarket.com",
            "Connection": "keep-alive",
        }

        attachedment = response.xpath('//ul[@class="attachment-list"]/li/a/@href').extract()
        try:
         sb = response.xpath('//div[@class="educational-details"]/ul/li/li./text()').extract()
        except:
            pass
        content = ''.join([x.strip() for x in response.xpath('//div[@class="question-body"]').xpath('.//text()').extract()])
        duedate = response.xpath('//div[@class= "meta question-meta"]//time/text()').extract_first()
        budget = ''.join([x.strip() for x in response.xpath('//div[@class= "meta question-meta"]/ul//li[3]').xpath('./text()').extract()])


        yield {
            "Subject" : sb,
            "Content" :content,
            "Attachment links" : attachedment,
            "Due Date" : duedate,
            "Budget" : budget

               }

