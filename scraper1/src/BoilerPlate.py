from uni.University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class BoilerPlate(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = ''
                page = requests.get(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    trs = soup.find_all("", {"class": ""})

                    for x in tqdm(range(len(trs)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                        self.titleArr.append(" ")
                        self.hrefArr.append(" ")
                        self.authorArr.append(" ")
                        self.dateArr.append(" ")
                        self.abstractArr.append(" ")
                        self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("University of Boiler")
        else:
            self.OutputCSV("University of Boiler", "boiler")
