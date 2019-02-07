# -*- coding: utf-8 -*-

import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailClient:
    def __init__(self, smtp_server, imap_server, smtp_port, imap_port):
        self.smtp_server = smtp_server
        self.imap_server = imap_server
        self.smtp_port = smtp_port
        self.imap_port = imap_port

    def send_mail(self):
        login = input('Enter login: ')
        password = input('Enter password: ')
        print('Optional:\n')
        recipients_member = input("Enter recipients with ',' delimiter: \n")
        subject = input('Enter subject: ')
        message = input('Enter message: ')
        message_content = MIMEMultipart()
        message_content['From'] = login
        message_content['To'] = recipients_member
        message_content['subject'] = subject
        message_content.attach(MIMEText(message))
        smtp_session = smtplib.SMTP(self.smtp_server, self.smtp_port)
        smtp_session.ehlo()
        smtp_session.starttls()
        smtp_session.ehlo()
        smtp_session.login(login, password)
        smtp_session.sendmail(login, recipients_member, message_content.as_string())
        smtp_session.quit()

    def receive_mail(self):
        imap_session = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        login = input('Enter login: ')
        password = input('Enter password: ')
        imap_session.login(login, password)
        imap_session.list()
        imap_session.select('INBOX')
        result, data = imap_session.uid('search', None, 'ALL')
        latest_email_uid = data[0].split()[-1]
        result, data = imap_session.uid('fetch', latest_email_uid, '(RFC822)')
        email_string = data[0][1].decode('utf-8')
        last_message = email.message_from_string(email_string)
        print(last_message)
        imap_session.logout()


if __name__ == '__main__':
    gmail_client = MailClient('smtp.gmail.com', 'imap.gmail.com', '587', '993')
    gmail_client.receive_mail()
#    gmail_client.send_mail()
