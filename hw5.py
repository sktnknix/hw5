# -*- coding: utf-8 -*-

import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailClient:
    def __init__(self, smtp_server, imap_server, login, password,
                 smtp_port=smtplib.SMTP_SSL_PORT,
                 imap_port=imaplib.IMAP4_SSL_PORT):
        self.smtp_server = smtp_server
        self.imap_server = imap_server
        self.smtp_port = smtp_port
        self.imap_port = imap_port
        self.login = login
        self.password = password

    def send_mail(self, subject, message, recipients):
        message_content = MIMEMultipart()
        message_content['From'] = self.login
        message_content['To'] = ', '.join(recipients)
        message_content['subject'] = subject
        message_content.attach(MIMEText(message))
        smtp_session = smtplib.SMTP(self.smtp_server, self.smtp_port)
        smtp_session.ehlo()
        smtp_session.starttls()
        smtp_session.ehlo()
        smtp_session.login(self.login, self.password)
        smtp_session.sendmail(self.login, recipients,
                              message_content.as_string())
        smtp_session.quit()

    def receive_mail(self):
        imap_session = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        imap_session.login(self.login, self.password)
        imap_session.list()
        imap_session.select('INBOX')
        result, data = imap_session.uid('search', None, 'ALL')
        latest_email_uid = data[0].split()[-1]
        result, data = imap_session.uid('fetch', latest_email_uid, '(RFC822)')
        email_string = data[0][1]
        last_message = email.message_from_bytes(email_string)
        imap_session.logout()
        return last_message


if __name__ == '__main__':
    login = input('Enter login: ')
    password = input('Enter password: ')
    gmail_client = MailClient('smtp.gmail.com', 'imap.gmail.com',
                              login, password)
    gmail_client.receive_mail()
#    recipients = input("Enter recipients with ',' delimiter: \n")
#    subject = input('Enter subject: ')
#    message = input('Enter message: ')
#    gmail_client.send_mail(subject, message, recipients)
