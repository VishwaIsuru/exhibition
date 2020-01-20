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
    name = "aamz"
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["LINK","LETTER","COUNT"]
    }

    def start_requests(self):
        urls=[u'/gp/search/other/ref=sr_in_1_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=%23&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_a_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=a&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_b_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=b&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_c_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=c&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_d_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=d&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_e_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=e&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_f_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=f&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_g_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=g&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_h_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=h&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_i_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=i&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_j_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=j&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_k_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=k&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_l_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=l&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_m_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=m&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_n_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=n&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_o_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=o&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_p_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=p&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_q_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=q&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_r_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=r&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_s_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=s&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_t_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=t&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_u_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=u&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_v_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=v&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_w_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=w&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_x_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=x&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_y_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=y&ie=UTF8&qid=1571250332', u'/gp/search/other/ref=sr_in_z_-2?rh=i%3Aautomotive%2Cn%3A15684181%2Cn%3A15719731%2Ck%3Aautomotive+replacement+parts&keywords=automotive+replacement+parts&pickerToList=lbr_brands_browse-bin&indexField=z&ie=UTF8&qid=1571250332']
        i=0
        for u in urls:
            u='https://www.amazon.com'+u
            yield scrapy.Request(url=u.strip(), callback=self.parse,
                                 headers={'User-Agent': 'Mozilla Firefox 12.0'},meta={"Index":i})
            i+=1

    def parse(self,response):
        all = response.css('.a-list-item').xpath('./a/span[2]/text()').extract()
        f=0
        cur=response.xpath('/html/body/div[1]/div[2]/div/div[2]/div/div/div').css('.pagnCur').xpath('./text()').extract_first()
        for a in all:
            f += int(a.replace('(', '').replace(')', '').replace(',', ''))
        yield {
            "LINK":response.url,"LETTER":cur, "COUNT":f
        }


