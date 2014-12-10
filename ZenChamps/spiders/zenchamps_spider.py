#Copyright (c) 2014 Caleb Ku
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.spider import Spider
from selenium import selenium,webdriver

import time
import pprint
import re

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

class zenminer(Spider):
    name = 'zenminer'
    allowed_domains = ['cloud.zenminer.com']
    login_page = 'https://cloud.zenminer.com/login'
    start_urls = ["https://cloud.zenminer.com/champions"]

    def __init__(self):
	self.driver = webdriver.Chrome()
	self.driver.set_page_load_timeout(30)
	dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse_remove(self, mystringdata,mytypedata):
	if mytypedata=='numeric':
		mystringdata = re.sub("[^\d.]", "", mystringdata)
	mystringdata = mystringdata.replace(" ", "");
	return mystringdata

    def get_champs(self,mydriver):

	champarray=Vividict()
	champdata_css ="#DataTables_Table_%d > tbody > tr:nth-child(%d) > td:nth-child(%d)"
	champlistcss_mapping={2:'solo',1:'prime',0:'stalker',3:'genesis'}

	for table in range(0,len(champlistcss_mapping)):
		for rows in range(1, 11):
			champyname = mydriver.find_element_by_css_selector(champdata_css % (table,rows,2)).text
			champytotal = mydriver.find_element_by_css_selector(champdata_css % (table,rows,3)).text
			champyrank = mydriver.find_element_by_css_selector(champdata_css % (table,rows,1)).text
			champytotal=self.parse_remove(champytotal,'numeric')

			champlist=champlistcss_mapping[table]
			champarray[champlist][champyname]['total']=champytotal
			champarray[champlist][champyname]['rank']=champyrank

	
	
	return champarray

    def spider_closed(self, spider):
        self.driver.close()

    def login(self):
        
	username = self.driver.find_element_by_name('username')
	password = self.driver.find_element_by_name('password')

	username.send_keys("myusername")
	password.send_keys("mypassword")
	
	self.driver.find_element_by_xpath("//*[@id='login-form']/div[3]/div/div[2]/button").click()
	time.sleep(5)
	
	if "Changelog" in self.driver.page_source:
		
		changelog=self.driver.find_element_by_id('changelog')
 		changelog.find_element_by_class_name('close').click()
		return


    def parse(self, response): 
	mydriver=self.driver        
	mydriver.get(response.url)
	
        if "Sign Out" in self.driver.page_source:
	    print "all is good"
	else:
	     self.login()

        time.sleep(2.5)
	
	if "champions" in mydriver.current_url:
	     parsed_champarray = self.get_champs(mydriver)

	#writefunction
