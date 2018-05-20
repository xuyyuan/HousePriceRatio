import requests
import re
from bs4 import BeautifulSoup
import openpyxl

def get_one_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Referer':'http://news.house.qq.com/a/20170702/003985.htm?pgv_ref=aio2015&ptlang=2052'
    }
    res = requests.get(url, headers=headers)
    return res.text

def parse_one_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('p', style='TEXT-INDENT: 2em')
    items = iter(items)
    for item in items:
        if item.text.isnumeric():
            yield [
                next(items).text[1:-1],
                next(items).text[5:],
                next(items).text[5:],
                next(items).text[6:]
            ]
            # 这里用yield不是很好，因为下面save_to_data里面的参数要的是列表中的列表，所以这里直接产生想要的东西即可

def save_to_excel(data):
    wb = openpyxl.Workbook()
    wb.guess_types = True
    ws = wb.active
    ws.append(['城市', '房价', '工资', '房价工资比'])
    for each in data:
        ws.append(each)
    wb.save('2017HousePriceRatio2.xlsx')

def main():
    url = 'http://news.house.qq.com/a/20170702/003985.htm'
    html = get_one_page(url)
    data = []
    for each in parse_one_page(html):
        data.append(each)
    save_to_excel(data)
    # data=[]到data.append(each)这地方写得比较拖沓

if __name__ == '__main__':
    main()
