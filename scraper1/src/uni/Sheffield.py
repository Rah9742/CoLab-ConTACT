from .University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class Sheffield(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = 'https://eprints.whiterose.ac.uk/cgi/search/archive/advanced?screen=Search&dataset=archive&_action_search=Search&documents_merge=ALL&documents=&title_merge=ALL&title=&creators_name_merge=ALL&creators_name=&creators_orcid=&id_number_merge=ALL&id_number=&isbn_merge=ALL&isbn=&issn_merge=ALL&issn=&abstract_merge=ALL&abstract=&keywords_merge=ALL&keywords='+keywords[i]+'&iau=Sheffield&iau_merge=ANY&editors_name_merge=ALL&editors_name=&refereed=EITHER&publication_merge=ALL&publication=&date=&funder_grant_funding_body_merge=ALL&funder_grant_funding_body=&funder_grant_grant_number_merge=ALL&funder_grant_grant_number=&satisfyall=ALL&order=-date%2Fcreators_name%2Ftitle&search_offset='+str(y*2)+'0'
                page = requests.get(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    trs = soup.find_all("tr", {"class": "ep_search_result"})

                    for x in tqdm(range(len(trs)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                        href = self.GetHref(trs[x])
                        if href != "None":
                            pageMat = requests.get(href)
                            if page.status_code == 200:
                                soupMat = BeautifulSoup(pageMat.text, "html.parser")
                                self.titleArr.append(trs[x].find("em").get_text())
                                self.hrefArr.append(href)
                                self.authorArr.append(self.GetAuthors(trs[x]))
                                self.dateArr.append(self.GetDate(soupMat).strftime("%B %Y"))
                                self.abstractArr.append(self.GetAbstract(soupMat))
                                self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("University of Sheffield")
        else:
            self.OutputCSV("University of Sheffield", "sheffield")

    def GetAuthors(self, tr):
        authorSpans = tr.find_all('span', {'class':'person_name'})
        if authorSpans != None:
            output = ''
            for x in range(len(authorSpans)):
                if x == 0:
                    output = authorSpans[x].get_text()
                else:
                    output = output + '; ' + authorSpans[x].get_text()
            return output
        else:
            return "None"


    def GetHref(self, tr):
        hrefs = tr.find_all('a', {'class': None})
        if len(hrefs) == 1:
            return hrefs[0].get("href")
        else:
            return "None"


    def GetDate(self, soup):
        #page = requests.get(href)
        #soup = BeautifulSoup(page.text, "html.parser")

        ul = soup.find("ul", {"class": "datesdatesdates"})
        
        lis = ul.find_all("li")
        dates = []

        for li in lis:
            dates.append(parse(li.get_text(), fuzzy=True))

        return dates[0]


    def GetAbstract(self, soup):
        #page = requests.get(href)
        #soup = BeautifulSoup(page.text, "html.parser")
        pAbstract = soup.find("p", {"class": "abstract"})
        if pAbstract != None:
            return pAbstract.get_text()
        else:
            return "None"