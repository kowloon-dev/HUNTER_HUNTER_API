#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config_import as ci
import log_control
import requests
import time
from bs4 import BeautifulSoup
import random
import traceback


class GetWebsite:

    def __init__(self):
        try:
            self.url = ci.url
            self.title_tag = ci.title_tag
            self.title_class = ci.title_class
            self.title = ci.title
            self.retry_sleep_min = ci.retry_sleep_min
            self.retry_sleep_max = ci.retry_sleep_max
            self.retry_max = ci.retry_max
            self.result_file = ci.result_file
        except:
            err = "Read config failed.\n"
            log_control.logging.error(err + traceback.format_exc())
            raise

    def get_website(self):

        retry_count = 0
        while True:
            # GET Website
            self.get_result = requests.get(self.url)

            # Change encoding
            # "ISO-8859-1"(default) to "UTF-8"
            self.get_result.encoding = 'UTF-8'

            # If the status code is "200" or retry_count has reached "retry_max",
            # come out of this loop.
            if self.get_result.status_code == 200:
                log_control.logging.debug(self.url + " GET succeeded.(STATUS CODE= " + str(self.get_result.status_code) + ")")
                break
            elif retry_count >= self.retry_max:
                log_control.logging.error(self.url + " It has reached retry_max. Give up getting website... ")
                break

            log_control.logging.debug(self.url + " GET failed.(STATUS CODE= " + str(self.get_result.status_code) + "). Waiting for retry...")

            # Add 1 to "retry_count", empty "get_result", and sleep in random seconds.
            retry_count += 1
            self.get_result = ""
            time.sleep(random.randint(self.retry_sleep_min,self.retry_sleep_max))

    def scraping(self):
        # Parse the html code.
        soup = BeautifulSoup(self.get_result.text, "html.parser")

        # Find the title class.
        scraped_code = soup.findAll(self.title_tag, class_=self.title_class)

        # Seek textline which contains target title.
        for line in scraped_code:
            if self.title in line:
                title_check_result = 1
                log_control.logging.info("Title found! (Relevant HTML code= " + str(line) + ")")
                break
            else:
                title_check_result = 0

        # Open a result file.
        result_file = open(self.result_file, 'w')

        # Write the result of scraping to result_file.
        result_file.write("%s" % (title_check_result))

        result_file.close()

        # degug
        print(self.title)
        print(title_check_result)

gw = GetWebsite()
gw.get_website()
gw.scraping()
