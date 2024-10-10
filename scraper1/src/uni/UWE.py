from .University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv

class UWE(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = "https://uwe-repository.worktribe.com/outputs?advanced=1&id=&Title_operator=all&Title=&Name=&ReportingDate=&Keywords_operator=all&Keywords="+keywords[i]+"&Journal_operator=all&Journal=&order=ReportingDateDesc&page=" + str(y+1)
                page = requests.get(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    divs = soup.find_all("blockquote")

                    for x in tqdm(range(len(divs)), ncols=80, ascii=True, desc=keywords[i]):
                        self.titleArr.append(divs[x].find("strong").get_text())
                        href = divs[x].find("a").get("href")
                        self.hrefArr.append(href)
                        researchPage = requests.get(href)
                        self.authorArr.append(self.GetAuthors(researchPage))
                        self.dateArr.append(self.GetDate(researchPage))
                        self.abstractArr.append(self.GetAbstract(researchPage))
                        self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("University of the West of England")
        else:
            self.OutputCSV("University of the West of England", "uwe")

    def GetAuthors(self, researchPage):
        if researchPage.status_code == 200:
            soup = BeautifulSoup(researchPage.text, "html.parser")
            output = ""

            divs = soup.find("div", {"style": "max-height: 100vh; overflow: auto;"})
            strongs = []
            if divs != None:
                strongs = divs.find_all("strong")

            for i in range(len(strongs)):
                if i != 0:
                    output += "; " + strongs[i].get_text()
                else:
                    output += strongs[i].get_text()

            if output == "":
                return "None"
            return output
        else:
            return "None";
    
    def GetDate(self, researchPage):
        if researchPage.status_code == 200:
            soup = BeautifulSoup(researchPage.text, "html.parser")
            output = "None"

            trs = soup.find_all("tr")

            for i in range(len(trs)):
                if trs[i].find("th").get_text() == "Publication Date":
                    output = trs[i].find("td").get_text()
                    break

            return output
        else:
            return "None";
    
    def GetAbstract(self, researchPage):
        if researchPage.status_code == 200:
            soup = BeautifulSoup(researchPage.text, "html.parser")
            output = "None"
            div = soup.find("div", {"class": "content abstract"})
            if div != None:
                output = div.find("p").get_text()
            return output
        else:
            return "None";