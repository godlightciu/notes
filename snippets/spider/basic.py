# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pymysql


class Bilibili:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver,10)
        self.url = 'https://www.bilibili.com'
        self.db = pymysql.connect('localhost',
                                  'root',
                                  '3832',
                                  'bilibili',
                                charset='utf8')  # 连接数据库，如果不加charset，可能会导致乱码出现
    def create_Table(self):        #建表
        db = self.db
        cursor = db.cursor()
        table = "CREATE TABLE bilibili(Anime_name VARCHAR(255) NOT NULL,Viewing_number VARCHAR(255) NOT NULL,Barrage VARCHAR(255) NOT NULL)"
        cursor.execute(table)
        db.commit()
    def insert(self,Anime_name,Viewing_number,Barrage):      #插入方法
        db = self.db
        cursor = db.cursor()
        insert = "insert into bilibili(Anime_Name,Viewing_number,Barrage) values(%s,%s,%s);"
        cursor.execute(insert,(Anime_name,Viewing_number,Barrage))
        db.commit()
    def open_page(self):        #打开网页
        url = self.url
        self.driver.get(url)
    def get_response(self):           #寻找数据
        driver = self.driver
        wait = self.wait
        try:
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#videolist_box > div.vd-list-cnt'))
            )
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'#videolist_box > div.vd-list-cnt > ul > li:nth-child(1) > div > div.r'))
            )
        except TimeoutException:
            raise TimeoutException
        page = driver.page_source
        soup = BeautifulSoup(page,'html.parser')
        items = soup.find_all('div',class_ = 'r')
        for item in items:
            item1 = item.find_all('span',class_ = 'v-info-i')
            Anime_name = item.find('a',class_ = 'title').text
            Viewing_name = item1[0].text
            Barrage = item1[1].text
            bilibili.insert(Anime_name,Viewing_name,Barrage)
    def next_page(self):         #翻页
        try:
            button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'#videolist_box > div.vd-list-cnt > div.pager.pagination > ul > li.page-item.next > button'))
            )
        except TimeoutException:
            raise TimeoutException
        button.click()
    def main(self):
        driver = self.driver
        bilibili.open_page()
        for i in range(1,4):
            bilibili.get_response(i)
            bilibili.next_page()
        driver.quit()
if __name__ == '__main__':
    bilibili = Bilibili()
    bilibili.create_Table()
    bilibili.main()
