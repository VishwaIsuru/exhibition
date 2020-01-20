import scrapy
import re
import json
import csv
import pymysql.cursors
from scrapy.http import FormRequest
import random
import string
# import sys
#
# reload(sys)
# sys.setdefaultencoding('utf8')

class workspider(scrapy.Spider):
    name = "ali"

    def start_requests(self):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Cookie': 'ali_apache_id=11.227.118.144.1560243213943.170846.1; xman_us_f=x_l=0&x_locale=en_US&no_popup_today=n&x_user=LK|LK|shopper|ifm|2049466156&zero_order=y&last_popup_time=1560243260056; aep_usuc_f=region=US&site=glo&b_locale=en_US&isb=y&x_alimid=2049466156&c_tp=USD; acs_usuc_t=acs_rt=9da4f96c432e4c2c993ff89393ecae80&x_csrf=q1afm401r4rg; xman_t=YKyhSb/W0jRzf8bwWKtJDtat7VPRazUdmCWMDCw1Ubg3kqsPUayu2ztvuy3+hjXuxkxTeQQujkoF6+vKxIDMmRtYSx31mDQhLPYm8Vy6B9spQwf1Uiby7bUgutZZpz1H42lOxHEkgTaIOrVaY7R6HGgYez3KdmlIhfjUcTBKEQ4f1cBowGdFvZGLMFsc4Cxzg9D0oLZ4cbTEvSd7Q3IefDnDew6CkSxyq8TESXZNZ4sY3fY1ZxZxNViPb7Xoh5y3uYqYjmHYZuLOc+qUyn5ljNIi2CJ8SOyH6LR1hwYcthT0/1rz5i9p3qt+6ObJvr4JMYnihJLiZ3QnMvxVOWQ3lt9tg3PBwIlj3Q9Uvek2TAG/R57Yizgyul1+GZkLRj22mhrGp+EQNVW5DH401TrV6NmyMZIIoS9jm8GXe52TyxBijMh0ccVuttU7Ujcfa/4RZZ4cG7h8ZdncunmduI3JI3VWh4jTLkoTUb7CphW0tMRl5Di7MsgegXClULaiTQyFbFWI7KB0Ua84E8L6OXAdwVnlq6/aBiZ4iIEAFMtA+FoR5FBjFvVsDZukM5yNMy0W5adEeqtvuFm3HchBnfJ5y0A2A9aGh3mm8uPp0Nq3nNOg2/XdtT934ijHeAtZotgJaw6YTrsoWFWC2vGqQYuTwphOaWj/skoV; intl_locale=en_US; intl_common_forever=zIUw8IfMIypVNPxHk9TMezYRJLWSW9OZRhlzF5Wfft3TvYEQXOhb1w==; xman_f=K+COX9IAXWlEGSqkNHilfPn6lc/y6oTxEYjavIWfb4tv3OirDQxaPJiWuGvnQ1SAlQQ/0F2uTBvKXFNGhssLeQA9Wa/6ZlfH/xQ6TgBnZQ3x7C4HW0zTW+CjAR0tLjj1eBXLWprmmNDPWDsxUjxhQ8XGrkM3qOfZfBU702H3ordkcjDWVEEDgHLOrUw6vItltHi8HYGlCKpK4gqoe74eQ47Y548vVJNNQ2nAoPabUqzbBKUDE3y/jyy9am2mEdpBB+EXHvg7MvrY6stMNBgbn5WgzZSCreocgvDi3/OrCl1o4DPzUVplEoVSFXiSXwve7Xk6UQsfzkELpgwtoDmZ0SA9gs2f8OWmuvyM9tKT9DvD567eCoOfEWWUrcXCi+cVdsqwVdRek2fn3D30OLp2+z5BiF+sttR7shRJQjE0oRgpOQa/y3EAt0ONxEr5ILQP; AKA_A2=A; ali_apache_track=mt=1|ms=|mid=lk450064156kclae; ali_apache_tracktmp=W_signed=Y; _m_h5_tk=a5c7a3adf38627e0a3a6c5b92daebbfa_1560245468215; _m_h5_tk_enc=597d5ed30ff4f8cefc0b5650a9f62112; cna=E1qGFbqgoAYCAa+dLodjAxQD; isg=BNPTBKcriwV93kfRGTPm5w7uYV49IG85qlBTm4XxR_APBPCmDVnLmweWPq3Pv79C; l=bBQbFUWrvQvF0u99BOfwiuIRGh7T1IOV1kPzw4gGkIB193f32d-pZHwdmnZMI3Q6T_5I3etkzNkMzdFD--U3rt1..; _hvn_login=13; aep_common_f=XCSJruHZkxdwv6LOUeNXd8jW8D3TETzdaw8lyyCJJQVr5B4yjZZ4yg==; xman_us_t=x_lid=lk450064156kclae&sign=y&x_user=lhnMgIRAZpD7goBk9eh3gu69J0jSIoDq+5rya8Iitik=&ctoken=d9ht1ollzjjy&need_popup=y&l_source=aliexpress; aep_usuc_t=ber_l=A0; JSESSIONID=70FC800196DE6C51D18C71D25EB1589B; RT="sl=2&ss=1560243275928&tt=9287&obo=1&sh=1560243291128%3D2%3A1%3A9287%2C1560243281802%3D1%3A1%3A0&dm=aliexpress.com&si=02fd0846-8998-4c76-93c6-bea9837c35bb&se=900&bcn=%2F%2F60062f09.akstat.io%2F&ld=1560243291129&nu=https%3A%2F%2Fwww.aliexpress.com%2Fcategory%2F200003482%2Fdresses.html%3Ff7aad4af8007347c6d49fbf761a83e1f&cl=1560243346041&r=https%3A%2F%2Fwww.aliexpress.com%2Fcategory%2F200003482%2Fdresses.html%3F6992043c608675b1eca340f9e4f77946&ul=1560243346063"; _mle_tmp0=iiCGajxLJhPRfqiVFROq8v93BQJLYna1Eo3Tluzd4T7%2FDKYPoiXPxzOr3%2B9a7pr4wDbHwEW4Vu%2FccSoGwZh0XU4JNxIumMHYtFHJaX3Stg9pkqwM2W4yVqG55ApuyH1v; _ga=GA1.2.1662031661.1560243288; _gid=GA1.2.1030961734.1560243288; _fbp=fb.1.1560243288162.727386139; _gat=1',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
                   'Upgrade-Insecure-Requests': '1',
                   'DNT': '1',
                   'Host':'www.aliexpress.com'}

        yield scrapy.Request('https://www.aliexpress.com/category/200003482/dresses/5.html?site=glo&g=y&needQuery=n&tag=',headers=headers, callback=self.parse)


    def parse(self,response):
        print(response.body)