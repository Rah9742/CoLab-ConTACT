from .University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class Exeter(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = 'https://ore.exeter.ac.uk/repository/discover?rpp=20&etal=0&group_by=none&page='+str(y+1)+'&sort_by=dc.date.issued_dt&order=desc&filtertype_0=subject&filter_relational_operator_0=contains&filter_0=' + keywords[i]
                page = requests.get(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    table = soup.find("table", {"class": "table table-bordered table-hover"})
                    if table != None:
                        trs = table.find("tbody").find_all("tr")

                        for x in tqdm(range(len(trs)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                            self.titleArr.append(trs[x].find("a").get_text())
                            href = 'https://ore.exeter.ac.uk/' + trs[x].find("a").get("href")
                            self.hrefArr.append(href)
                            self.authorArr.append(self.GetAuthors(trs[x]))
                            self.dateArr.append(self.GetDate(trs[x].find("span", {"class": "date"})))
                            self.abstractArr.append(self.GetAbstract(href))
                            self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("University of Exeter")
        else:
            self.OutputCSV("University of Exeter", "exeter")


    def GetDate(self, span):
        return parse(span.get_text(), fuzzy=True).strftime("%B %Y")


    def GetAuthors(self, tr):
        tds = tr.find_all("td")
        return tds[2].get_text()

    def GetAbstract(self, href):
        page = requests.get(href)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "html.parser")
            div = soup.find("div", {"id": "abstract-text"})
            if div == None:
                return "None"

            finalAbstract = div.find("div", {"class": "hidden-overflow"})
            if finalAbstract == None:
                return "None"
            
            return finalAbstract.get_text()
        else:
            return "None"

