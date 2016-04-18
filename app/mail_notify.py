#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import pardir
from os.path import dirname
from os.path import sep
import logging
import configparser
import traceback
import requests
import log_control
import smtplib
from email.mime.text import MIMEText


class CheckCarried:

    def __init__(self):
        # Construct config_file path & read config file
        try:
            pardir_path = dirname(__file__) + sep + pardir
            config_file = pardir_path + "/config/config_mail.ini"
            config = configparser.ConfigParser()
            mailconfig = config.read(config_file)
            self.api_url = mailconfig.get('Mail', 'api_url')
        except:
            logging.error(traceback.format_exc())
            raise

    def get_api(self):

        # GET API
        self.get_result = requests.get(self.api_url)

        # Verify the status code.
        if self.get_result.status_code == 200:
            log_control.logging.debug(
                self.api_url + " GET API succeeded.(STATUS CODE= " + str(self.get_result.status_code) + ")")
        else:
            log_control.logging.debug(self.api_url + " GET API failed.(STATUS CODE= " + str(
                self.get_result.status_code) + ").")


    def check(self):

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
            self.smtp_host = mailconfig.smtp_host
            self.smtp_port = mailconfig.smtp_port
            self.local_host = mailconfig.local_host
            self.auth_id = mailconfig.smtpauth_id
            self.auth_pass = mailconfig.smtpauth_pass
            self.from_addr = mailconfig.from_addr
            self.to_addr = mailconfig.to_addr
            self.mail_title = mailconfig.mail_title
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
                "Sending mail has failed. ")
            return


# Create Instance and execute functions
mn = CheckCarried()
mn.get_api()
mn.check()

exit()
