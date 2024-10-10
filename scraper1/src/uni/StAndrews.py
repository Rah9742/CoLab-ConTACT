from uni.University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class StAndrews(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = "https://research-repository.st-andrews.ac.uk/discover?rpp=10&etal=0&query=" + keywords[i] + "&scope=/&group_by=none&page=" + str(y)
                # https://research-repository.st-andrews.ac.uk/discover?rpp=10&etal=0&query=Tech&scope=/&group_by=none&page=1
                page = requests.get(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    divs = soup.find_all("div", {"class": "col-sm-12 artifact-description"})

                    for x in tqdm(range(len(divs)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                        href = "https://research-repository.st-andrews.ac.uk" + divs[x].find("a").get("href")
                        paperPage = requests.get(href)
                        paperSoup = BeautifulSoup(paperPage.text, "html.parser")

                        self.titleArr.append(divs[x].find_all("h4", {"class": None})[0].get_text())
                        self.hrefArr.append(href)
                        self.authorArr.append(self.GetAuthors(paperSoup))
                        self.dateArr.append(self.GetDate(divs[x]))
                        self.abstractArr.append(self.GetAbstract(paperSoup))
                        self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("University of St Andrews")
        else:
            self.OutputCSV("University of St Andrews", "standrews")


    def GetAbstract(self, soup):
        abstractDiv = soup.find('div', class_='simple-item-view-description item-page-field-wrapper table')
        if abstractDiv == None:
            return "None"
        
        if abstractDiv:
            abstractDiv = abstractDiv.find('div')  # Find the nested <div> within the target <div>
            return abstractDiv.get_text()


    def GetAuthors(self, soup):
        authorsDiv = soup.find("div", {"class": "simple-item-view-authors item-page-field-wrapper table"})
        spans = authorsDiv.find_all("div", {"class": None})

        authors = ""

        for x in range(len(spans)):
            if spans[x].get_text() != "":
                if x == 0:
                    authors += spans[x].get_text(strip=True)
                else:
                    authors += "; " + spans[x].get_text(strip=True)

        
        return authors


    def GetDate(self, div):
        dateUnformatted = div.find("span", {"class": "date"})
        return parse(dateUnformatted.get_text(), fuzzy=True).strftime("%B %Y")
