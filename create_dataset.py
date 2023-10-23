import os, glob
import csv
from bs4 import BeautifulSoup
import re

def get_columns():
    columns = set()
    for filename in sorted(glob.glob('./mails/*.html')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            table = soup.select_one('table[bgcolor="#ffffff"]')
            bank_name = ''
            for tr in table.select('tr'):
                if (not tr.has_attr('bgcolor')) and (td := tr.find('td', { 'colspan': '3', 'align': 'left' })):
                    bank_name = td.get_text().strip()
                elif tr.has_attr('bgcolor'):
                    td1 = tr.find('td', { 'align': 'left' })
                    account_name = td1.get_text().strip()
                    columns.add(bank_name + ' - ' + account_name)

    return list(columns)

def build_csv(columns):
    columns.insert(0, 'Date')
    for f in glob.glob('./export/*.csv'):
        os.remove(f)
    with open('./export/export.csv', 'w') as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(columns)
        for filename in sorted(glob.glob('./mails/*.html')):
            with open(os.path.join(os.getcwd(), filename), 'r') as f:
                row = [0] * len(columns)
                d = filename.replace('./mails/', '').replace('.html', '')
                row[0] = str(d)
                soup = BeautifulSoup(f, 'html.parser')
                table = soup.select_one('table[bgcolor="#ffffff"]')
                bank_name = ''
                for tr in table.select('tr'):
                    if (not tr.has_attr('bgcolor')) and (td := tr.find('td', { 'colspan': '3', 'align': 'left' })):
                        bank_name = td.get_text().strip()
                    elif tr.has_attr('bgcolor'):
                        td1 = tr.find('td', { 'align': 'left' })
                        account_name = td1.get_text().strip()
                        column_name = bank_name + ' - ' + account_name
                        td2 = tr.find('td', { 'align': 'right' })
                        row[columns.index(column_name)] = re.sub(r'[^\d\.]', '', td2.get_text().strip().replace(',', '.'))

            writer.writerow(row)

columns = get_columns()
build_csv(columns)


# Bank list
# Array.from(document.querySelectorAll('tr.widthOutlook td[colspan="3"]')).map(node => node.innerText).filter(str => str.length > 0)
