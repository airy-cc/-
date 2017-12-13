# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 09:32:38 2017

@author: 1707498
"""
# 搜狐销售数据
#http://db.auto.sohu.com/cxdata/

#from urllib import request
from bs4 import BeautifulSoup
import requests
import xlsxwriter

#import pymysql.cursors



page = 1
#url = 'http://db.auto.sohu.com/carsales/'
#url='http://db.auto.sohu.com/cxdata/xml/sales/brand/brand191sales.xml'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
headers = { 'User-Agent' : user_agent }
#re=requests(url,headers = headers)
#resp=re.read().decode('UTF-8')
#print(resp.get())


url='http://db.auto.sohu.com/cxdata/xml/basic/modelList.xml'
def get_conn_url(url,headers):
    try:
        res = requests.get(url,headers=headers)
    except:
        print('get website erre')
    soup = BeautifulSoup(res.text,'html5lib')
    return soup
    
soup=get_conn_url(url,headers)
models=soup.find_all('model')

# 创建一个excel表格
workbook = xlsxwriter.Workbook('F:\work\Data\爬虫\data_crawler\souhuSaleData.xlsx')

# 为创建的excel表格添加一个工作表
worksheet = workbook.add_worksheet()

#表格标签栏    
worksheet.write(0, 0, 'brandid')
worksheet.write(0, 1, 'brandName')
worksheet.write(0, 2, 'corpid')
worksheet.write(0, 3, 'corpname')
worksheet.write(0, 4, 'idtype')
worksheet.write(0, 5, 'name')
worksheet.write(0, 6, 'saledate')
worksheet.write(0, 7, 'salenum') 

# 从第二行开始写入数据
row = 1 
for model in models:
    brandid=model.get('brandid')
    brandName=model.get('brandname')
    corpid=model.get('corpid')
    corpname=model.get('corpname')
    name=model.get('name')
    idtype=model.get('id')

    #每个型号车辆销售情况
    car_type_url="http://db.auto.sohu.com/cxdata/xml/sales/model/model"+idtype+"sales.xml"
    print(car_type_url)
    car_type_soup = get_conn_url(car_type_url,headers)
    sales=car_type_soup.find_all("sales")
    
    for sale in sales:
        saledate=sale.get("date")
        salenum=sale.get('salesNum')
        worksheet.write(row,0,brandid)
        worksheet.write(row,1,brandName)
        worksheet.write(row,2,corpid)
        worksheet.write(row,3,corpname)
        worksheet.write(row,4,idtype)
        worksheet.write(row,5,name)
        worksheet.write(row,6,saledate)
        worksheet.write(row,7,salenum)
        row=row+1
        print(str(row)+" "+idtype+" "+name)
workbook.close()
