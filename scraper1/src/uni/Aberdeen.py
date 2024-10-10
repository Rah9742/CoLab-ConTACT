from .University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class Aberdeen(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = 'https://aura.abdn.ac.uk/discover?rpp=20&etal=0&scope=/&group_by=none&page='+str(y+1)+'&sort_by=dc.date.issued_dt&order=desc&filtertype_0=subject&filter_relational_operator_0=contains&filter_0=' + keywords[i]
                page = requests.get(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    divs = soup.find_all("div", {"class": "row ds-artifact-item"})

                    for x in tqdm(range(len(divs)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                        href = divs[x].find("a").get("href")
                        if href != None:
                            pageMat = requests.get("https://aura.abdn.ac.uk/" + href)
                            if pageMat.status_code == 200:
                                soup = BeautifulSoup(pageMat.text, "html.parser")
                                self.titleArr.append(self.GetTitle(soup))
                                self.hrefArr.append("https://aura.abdn.ac.uk/" + href)
                                self.authorArr.append(self.GetAuthors(soup))
                                self.dateArr.append(self.GetDate(soup))
                                self.abstractArr.append(self.GetAbstract(soup))
                                self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("University of Aberdeen")
        else:
            self.OutputCSV("University of Aberdeen", "aberdeen")


    def GetTitle(self, soup):
        title = soup.find("h2", {"class": "page-header first-page-header"}).get_text()
        return title


    def GetAuthors(self, soup):
        authorDiv = soup.find("div", {"class": "simple-item-view-authors item-page-field-wrapper table"}).find_all("div")

        for x in range(len(authorDiv)):
            if x == 0:
                output = authorDiv[x].find("a").get_text()
            else:
                output = output + '; ' + authorDiv[x].find("a").get_text()
        return output


    def GetDate(self, soup):
        dateDiv = soup.find("div", {"class": "simple-item-view-date word-break item-page-field-wrapper table"})
        return parse(dateDiv.get_text(), fuzzy=True).strftime("%B %Y")


    def GetAbstract(self, soup):
        doiDiv = soup.find("div", {"class": "simple-item-view-doi item-page-field-wrapper table"})

        if doiDiv == None:
            return "None"

        doiA = doiDiv.find("a").get("href")
        doiPage = requests.get(doiA)
        soupDoi = BeautifulSoup(doiPage.text, "html.parser")

        abstractDiv = soupDoi.find("blockquote", {"class": "abstract mathjax"})

        if abstractDiv == None:
            return "None"

        finalString = abstractDiv.get_text()
        finalString = finalString.replace(" Abstract:  ", "")

        return finalString
