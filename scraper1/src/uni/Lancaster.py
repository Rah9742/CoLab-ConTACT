from .University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class Lancaster(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = 'https://www.research.lancs.ac.uk/portal/en/publications/search.html?publicationYearsFrom=&publicationstatus=published&advanced=true&documents=%20&ordering=researchOutputOrderByPublicationYear&pageSize=25&language=%20&publicationYearsTo=&type=%20&uri=&descending=true&search='+keywords[i]+'&organisationName=&organisations=&publicationcategory=&peerreview=&page='+str(y)
                page = requests.get(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    lis = soup.find_all("li", {"class": "portal_list_item"})

                    for x in tqdm(range(len(lis)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                        self.titleArr.append(lis[x].find("h2", {"class": "title"}).get_text())
                        href = lis[x].find("h2", {"class": "title"}).find("a").get("href")
                        self.hrefArr.append(href)
                        self.authorArr.append(self.GetAuthors(lis[x]))
                        self.dateArr.append(lis[x].find("span", {"class": "date"}).get_text())
                        self.abstractArr.append(self.GetAbstract(href))
                        self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("University of Lancaster")
        else:
            self.OutputCSV("University of Lancaster", "lancaster")

    def GetAuthors(self, li):
        persons = li.find_all("a", {"class": "link person"})
        output = ''
        for x in range(len(persons)):
            if x == 0:
                output = persons[x].find("span").get_text()
            else:
                output = output + '; ' + persons[x].find("span").get_text()

        if output == '':
            return "None"

        return output

    def GetAbstract(self, href):
        page = requests.get(href)
        soup = BeautifulSoup(page.text, "html.parser")
        div = soup.find("div", {"class": "view_container publication_view"})

        divSpec = soup.find("div", {"class": "textblock"})
        if divSpec != None:
            p = divSpec.find("p")
            if p != None:
                return p.get_text()
            else:
                return divSpec.get_text()

        return "None"