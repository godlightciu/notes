# -*- coding:utf-8 -*-
import threading
import multiprocessing as mp
import time

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
        self.url = "https://www.bilibili.com/anime/index/#season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=4&st=1&sort=0&page={}"
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

    def open_page(self,url):
        driver = self.driver
        driver.get(url)

    def get_response(self):           #寻找数据
        driver = self.driver
        wait = self.wait
        try:
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'a[class=bangumi-title]'))
            )
        except TimeoutException:
            raise TimeoutException
        page = driver.page_source
        #print(page)
        soup = BeautifulSoup(page,'html.parser')
        items = soup.find_all('li', class_ = 'bangumi-item')
        #print(items)
        for item in items:
            tag = item.find('a', class_ = 'bangumi-title')
            Anime_name = tag.text
            URL = 'http:'+tag['href']
            Scores = item.find('div', class_ = 'shadow-score').text

            driver.get(URL)

            try:
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'div[class=danmu-count'))
                )
            except TimeoutException:
                raise TimeoutException

            time.sleep(0.5)
            i_page = driver.page_source
            i_soup = BeautifulSoup(i_page,'html.parser')
            Viewing_number = i_soup.find('div', class_ = 'view-count').find('span').text
            Barrage = i_soup.find('div', class_ = 'danmu-count').find('span').text
            print(Anime_name,URL,Scores, Viewing_number,Barrage)

    def start(self,url):
        driver = self.driver
        self.open_page(url)
        self.get_response()
        driver.quit()


def crawl_process(url):
    bilibili = Bilibili()
    bilibili.start(url)

def sin_process():
    base_url = "https://www.bilibili.com/anime/index/#season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=4&st=1&sort=0&page={}"
    start = time.time()
    for i in range(1,20):
        url = base_url.format(i)
        crawl_process(url)
    end = time.time()
    print('单进程爬虫运行时间：{}s'.format(end-start))

def multi_process():
    base_url = "https://www.bilibili.com/anime/index/#season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=4&st=1&sort=0&page={}"
    start = time.time()
    p = mp.Pool()
    for i in range(1,5):
        url = base_url.format(i)
        p.apply_async(crawl_process,args=(url,))
        time.sleep(2)
    p.close()
    p.join()
    end = time.time()
    print('ALL crawl_jobs done!')
    print(end-start)

if __name__ == '__main__':
    sin_process()
