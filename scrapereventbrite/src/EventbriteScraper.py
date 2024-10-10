from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver 
from dateutil.parser import parse
import requests
import csv
import time
import os


class EventbriteScraper():
    titleArr = []
    timeArr = []
    hrefArr = []

    def ScrapeForData(self, depth):
        for i in range(depth):
            url = 'https://www.eventbrite.com/d/united-kingdom--portsmouth/university-of-portsmouth/?page=' + str(i + 1)
            options = webdriver.FirefoxOptions() 
            options.headless = True 
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            time.sleep(5)
            htmlSource = driver.page_source
            driver.close()

            soup = BeautifulSoup(htmlSource, "html.parser")

            sections = soup.find_all("section", {"class": "discover-horizontal-event-card"})

            for i in tqdm(range(len(sections)), ncols=80, ascii=True, desc="Page " + str(1 + i)):
                href = sections[i].find("a").get("href")
                materialPage = requests.get(href)
                materialSoup = BeautifulSoup(materialPage.text, "html.parser")

                self.titleArr.append(sections[i].find("h2").get_text())
                self.timeArr.append(self.GetTime(materialSoup))
                self.hrefArr.append(sections[i].find("a").get("href"))

        self.OutputCSV();


    def OutputCSV(self):
        filename = "out/portsmouth_eb.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', newline='', encoding='utf-8') as csvFile:
            headerList = ['Title', 'Date', 'Href', 'Location']
            writer = csv.DictWriter(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, fieldnames=headerList)
            writer.writeheader()
            for x in range(len(self.titleArr)):
                title = self.titleArr[x].strip()
                writer.writerow({'Title': title, 'Date': self.timeArr[x], 'Href': self.hrefArr[x], 'Location': 'Portsmouth'})


    def GetTime(self, soup):
        date = soup.find("span", {"class": "date-info__full-datetime"})
        return date.get_text()

    

    