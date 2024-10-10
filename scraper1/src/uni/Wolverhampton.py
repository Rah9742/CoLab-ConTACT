from uni.University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class Wolverhampton(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = 'https://wlv.openrepository.com/discover?view=list&rpp=10&etal=0&group_by=none&page='+str(y + 1)+'&filtertype_0=subject&filter_relational_operator_0=contains&filter_0='+keywords[i]
                page = requests.get(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    divs = soup.find_all("div", {"class": "artifact-description discover-page"})

                    for x in tqdm(range(len(divs)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                        href = "https://wlv.openrepository.com" + divs[x].find("a").get("href")
                        paperPage = requests.get(href)
                        paperSoup = BeautifulSoup(paperPage.text, "html.parser")

                        self.titleArr.append(divs[x].find_all("div", {"class": "list-title-clamper"})[0].get_text())
                        self.hrefArr.append(href)
                        self.authorArr.append(self.GetAuthors(paperSoup))
                        self.dateArr.append(self.GetDate(divs[x]))
                        self.abstractArr.append(self.GetAbstract(paperSoup))
                        self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("University of Wolverhampton")
        else:
            self.OutputCSV("University of Wolverhampton", "wolverhampton")


    def GetAbstract(self, soup):
        abstractDiv = soup.find("span", {"id": "item-view-element-dc_description_abstract-1"})
        if abstractDiv == None:
            return "None"
        
        return abstractDiv.get_text()


    def GetAuthors(self, soup):
        authorsDiv = soup.find("div", {"class": "simple-item-view-dc.contributor.author item-page-field-wrapper table"})
        spans = authorsDiv.find_all("span", {"class": "item-view-never-hide"})

        authors = ""

        for x in range(len(spans)):
            if spans[x].get_text() != "":
                if x == 0:
                    authors += spans[x].get_text()
                else:
                    authors += "; " + spans[x].get_text()

        
        return authors


    def GetDate(self, div):
        dateUnformatted = div.find("span", {"class": "date"})
        return parse(dateUnformatted.get_text(), fuzzy=True).strftime("%B %Y")
