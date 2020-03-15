from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import re
import datetime

binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary)
url='https://coronavirus-monitor.ru/'

def get_data():
    driver.get(url)
    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, "html.parser")
    countries = soup.find_all("div", class_="statistics-row")
    for country in countries:
        name=country.find("div", class_="country")
        text_name=name.get_text()
        if re.search('Казахстан', text_name):
            stat_kz=country.find_all("div", class_="cell")
            infected=stat_kz[0].get_text().strip()
            deaths=stat_kz[1].get_text().strip()
            heals=stat_kz[2].get_text().strip()
            f=open("stats.txt", "a+")
            d = datetime.datetime.today()
            f.write(f'\n{d.strftime("%d-%B-%Y %H:%M")}|{infected}|{deaths}|{heals}')
    driver.close()

get_data()
