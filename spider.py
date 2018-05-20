import requests
import bs4
import re
import openpyxl

def open_url(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
	res = requests.get(url, headers)
	return res

def find_data(res):
	data = []
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	content = soup.find(id='Cnt-Main-Article-QQ') #注意find()函数里面的的参数
	# print(content)
	target = content.find_all('p', style='TEXT-INDENT: 2em') # 注意find_all里面的参数
	target = iter(target)
	for each in target:
		# print(each.text)
		if each.text.isnumeric():  #注意以下是形式是字符串.isnumeric()，用的isnumeric()方法
			data.append([
				re.search(r'\[(.*)\]', next(target).text).group(1),
				re.search(r'\d.*', next(target).text).group(),
				re.search(r'\d.*', next(target).text).group(),
				re.search(r'\d.*', next(target).text).group()])
				# 个人认为正则这块加上一些判断语句会比较好
	return data

def to_excel(data):
	wb = openpyxl.Workbook()
	wb.guess_types = True # excel有两种数据格式，通过guess_types来让openpyxl自动判断要弄进去的数据是文本呢还是数字
	ws = wb.active
	ws.append(['城市', '平均房价', '平均房价', '房价工资比'])
	for each in data: # 注意data是参数
		ws.append(each)
	wb.save('2017HousePriceRatio.xlsx')

def main():
	url = 'http://news.house.qq.com/a/20170702/003985.htm'
	res = open_url(url)
	data = find_data(res)
	to_excel(data)	

if __name__ == '__main__':
	main()