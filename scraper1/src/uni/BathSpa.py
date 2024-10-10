from .University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class BathSpa(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = 'https://researchspace.bathspa.ac.uk/cgi/search/archive/advanced?screen=Search&dataset=archive&_action_search=Search&documents_merge=ALL&documents=&title_merge=ALL&title=&creators_name_merge=ALL&creators_name=&abstract_merge=ALL&abstract=&date=&keywords_merge=ALL&keywords='+keywords[i]+'&subjects_merge=ANY&divisions_merge=ANY&un_dev_goals_merge=ANY&research_groups_merge=ANY&research_excellence_areas_merge=ANY&editors_name_merge=ALL&editors_name=&refereed=EITHER&publication_merge=ALL&publication=&datestamp=&satisfyall=ALL&order=-date%2Fcreators_name%2Ftitle&search_offset='+str(y*2)+'0'
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
                                self.titleArr.append(trs[x].find("em").get_text().replace("'", ""))
                                self.hrefArr.append(href)
                                self.authorArr.append(self.GetAuthors(trs[x]))
                                self.dateArr.append(self.GetDate(soupMat))
                                self.abstractArr.append(self.GetAbstract(soupMat))
                                self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("Bath Spa University")
        else:
            self.OutputCSV("Bath Spa University", "bathspa")


    def GetAuthors(self, tr):
        authorSpans = tr.find_all('span', {'class':'person_name'})
        if authorSpans != None:
            output = ''
            for x in range(len(authorSpans)):
                toAdd = authorSpans[x].get_text()
                toRemoveElement = authorSpans[x].find("span", {"class": "orcid-tooltip"})
                if toRemoveElement != None:
                    toRemove = toRemoveElement.get_text()
                    toAdd = toAdd.replace(toRemove, "")

                if x == 0:
                    output = toAdd
                else:
                    output = output + '; ' + toAdd
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
        tds = soup.find_all("td")
        for i in range(len(tds)):
            if self.is_date(tds[i].get_text()):
                return parse(tds[i].get_text(), fuzzy=True).strftime("%B %Y")

        return "None"



    def GetAbstract(self, soup):
        pAbstract = soup.find("p", {"style": "text-align: left; margin: 1em auto 0em auto"})
        if pAbstract != None:
            return pAbstract.get_text()
        else:
            return "None"

    def is_date(self, string, fuzzy=False):
        try: 
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False