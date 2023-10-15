import imaplib
import time
from dotenv import dotenv_values
import sys
import email
import codecs
from datetime import datetime, date
import os
import glob

start = time.time()
try:
    imap_ssl = imaplib.IMAP4_SSL(host='imap.gmail.com', port=993)
except Exception as e:
    print('ErrorType : {}, Error : {}'.format(type(e).__name__, e))
    imap_ssl = None
    sys.exit()

print('Connection Object : {}'.format(imap_ssl))
print('Total Time Taken  : {:,.2f} Seconds'.format(time.time() - start))

config = dotenv_values('.env')

print(config)

with imaplib.IMAP4_SSL(host='imap.gmail.com', port=imaplib.IMAP4_SSL_PORT) as imap_ssl:
    print('Connection Object : {}'.format(imap_ssl))

    print('Logging into mailbox...')
    resp_code, response = imap_ssl.login(config['EMAIL'], config['PASSWORD'])

    print('Response Code : {}'.format(resp_code))
    print('Response      : {}\n'.format(response[0].decode()))

    imap_ssl.select()
    resp_code, mail_ids = imap_ssl.search(None, r'X-GM-RAW "from:\"{}\" subject:\"{}\""'.format(config['MAIL_FROM'], config['MAIL_SUBJECT']))

    mail_ids = mail_ids[0].decode().split()
    total = len(mail_ids)
    print('Total : {}'.format(total))

    i = 1
    #for mail_id in mail_ids[-20:]:

    # remove existing files
    files = glob.glob('mails/*.html')
    for f in files:
        os.remove(f)

    for mail_id in mail_ids:

        print('process mail : {} / {}'.format(i, total))

        resp_code, mail_data = imap_ssl.fetch(mail_id, '(RFC822)') ## Fetch mail data.

        message = email.message_from_bytes(mail_data[0][1]) ## Construct Message from mail data
        #print("From       : {}".format(message.get("From")))
        #print("To         : {}".format(message.get("To")))
        #print("Bcc        : {}".format(message.get("Bcc")))
        #print("Date       : {}".format(message.get("Date")))
        #print("Subject    : {}".format(message.get("Subject")))

        date_obj = datetime.strptime(message.get('Date'), '%a, %d %b %Y %X %z')

        date_str = date_obj.strftime('%Y%m%d%H%M%S')

        file1 = open('mails/{}.html'.format(date_str), 'a')
        for part in message.walk():
            if part.get_content_type() == config['MAIL_CONTENT_TYPE']:
                body_lines = part.as_string().split("\n")
                str_lines = "\n".join(body_lines)
                bytes_lines = bytes(str_lines, 'utf-8')
                decoded_lines = codecs.decode(bytes_lines, 'quopri').decode('utf-8')

                file1.write(decoded_lines)
        file1.close()

        i = i + 1
