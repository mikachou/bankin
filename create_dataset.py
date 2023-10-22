import os, glob
import csv
from bs4 import BeautifulSoup

def get_columns():
    columns = set()
    for filename in glob.glob('./mails/*.html'):
        with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
            # do your stuff
            print(filename)
            soup = BeautifulSoup(f, 'html.parser')
            table = soup.select_one('table[bgcolor="#ffffff"]')
            bank_name = ''
            for tr in table.select('tr'):
                if (not tr.has_attr('bgcolor')) and (td := tr.find('td', { 'colspan': '3', 'align': 'left' })):
                    #print(td.get_text().strip())
                    bank_name = td.get_text().strip()
                elif tr.has_attr('bgcolor'):
                    td1 = tr.find('td', { 'align': 'left' })
                    #print(td1.get_text().strip())
                    account_name = td1.get_text().strip()
                    columns.add(bank_name + ' - ' + account_name)
                    #td2 = tr.find('td', { 'align': 'right' })
                    #print(td2.get_text().strip())
                #print(tr.get_text().split('?'))
            #print(soup.prettify())

    print(columns)
get_columns()

# Bank list
# Array.from(document.querySelectorAll('tr.widthOutlook td[colspan="3"]')).map(node => node.innerText).filter(str => str.length > 0)
