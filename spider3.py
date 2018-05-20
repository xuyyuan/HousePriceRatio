import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import openpyxl

def get_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def parse_page(html):
    result = []
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('#Cnt-Main-Article-QQ p[style="TEXT-INDENT: 2em"]')
    items = iter(items)
    for item in items:
        if item.get_text().isnumeric():
            result.append([
                next(items).get_text()[1:-1],
                next(items).get_text()[5:],
                next(items).get_text()[5:],
                next(items).get_text()[6:],
            ])
    return result


def save_to_excel(content): # 这里函数里面的参数是列表啊,列表中还有列表
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['城市', '房价', '工资比', '房价工资比'])
    for each in content: # 证实了参数是列表
        ws.append(each)
    wb.save('houseprice.xlsx')

def main():
    url = 'http://news.house.qq.com/a/20170702/003985.htm'
    html = get_page(url)
    result = parse_page(html)  #reuslt是列表
    save_to_excel(result)

if __name__ == '__main__':
    main()

