#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import requests
import time
import random
import config_import as ci
import log_control
import smtplib
from email.mime.text import MIMEText


class CheckCarried:

    def __init__(self):
        try:
            self.api_url = ci.api_url
            self.retry_sleep_min = ci.retry_sleep_min
            self.retry_sleep_max = ci.retry_sleep_max
            self.retry_max = ci.retry_max
        except:
            err = "Read config failed.\n"
            log_control.logging.error(err + traceback.format_exc())
            raise


    def get_api(self):

        retry_count = 0

        while True:
            # GET API
            self.get_result = requests.get(self.api_url)

            # If the status code is "200" or retry_count has reached "retry_max",
            # come out of this loop.
            if self.get_result.status_code == 200:
                log_control.logging.debug(
                    self.api_url + " GET API succeeded.(STATUS CODE= " + str(self.get_result.status_code) + ")")
                break
            elif retry_count >= self.retry_max:
                log_control.logging.error(
                    self.api_url + " It has reached retry_max. Give up getting API... ")
                break

            log_control.logging.debug(self.api_url + " GET API failed.(STATUS CODE= " + str(
                self.get_result.status_code) + "). Waiting for retry...")

            # Add 1 to "retry_count", empty "get_result", and sleep in random seconds.
            retry_count += 1
            self.get_result = ""
            time.sleep(random.randint(self.retry_sleep_min, self.retry_sleep_max))


    def check_carried(self):

        # Parse the response with json()
        json_result = self.get_result.json()

        self.date = json_result["date"]
        self.title = json_result["title"]
        self.status = json_result["status"]

        if self.status == "True":
            # Construct mail body text.
            mail_body = self.date + "\n" \
                        "『" + self.title + "』の掲載を検知しました。\n"

            # Create MailSend instance and send a mail.
            ms = MailSend()
            ms.mail_send(mail_body)
        else:
            pass


class MailSend:
    def __init__(self):
        try:
            self.smtp_host = ci.smtp_host
            self.smtp_port = ci.smtp_port
            self.local_host = ci.local_host
            self.auth_id = ci.smtpauth_id
            self.auth_pass = ci.smtpauth_pass
            self.from_addr = ci.from_addr
            self.to_addr = ci.to_addr
            self.mail_title = ci.mail_title
        except:
            err = "Read config failed.\n"
            log_control.logging.error(err + traceback.format_exc())
            raise

    def mail_send(self, mail_body):

        # Establish SMTP connection.(with SMTPAUTH)
        smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
        smtp.ehlo(self.local_host)
        smtp.login(self.auth_id, self.auth_pass)
        mail_body = MIMEText(mail_body)
        mail_body['Subject'] = self.mail_title

        try:
            smtp.sendmail(self.from_addr, self.to_addr, mail_body.as_string())
            smtp.quit()
            return
        except:
            smtp.quit()
            log_control.logging.error(
                "Sending Email has failed. ")
            return


# Create Instance and execute functions
mn = CheckCarried()
mn.get_api()
mn.check_carried()

exit()
