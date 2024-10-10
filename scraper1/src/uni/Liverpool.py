#Author: Rahil Shah

from .University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class Liverpool(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = 'https://livrepository.liverpool.ac.uk/cgi/search/simple?exp=0%7C1%7C%7Carchive%7C-%7Cq%3Aabstract%2Fcreators_name%2Fdate%2Fdocuments%2Ftitle%3AALL%3AIN%3A'+keywords[i]+'%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AANY%3AEQ%3Ashow&screen=Search&cache=170532&_action_search=1&search_offset='+str(y*2)+'0'
                #https://livrepository.liverpool.ac.uk/cgi/search/simple?exp=0%7C1%7C%7Carchive%7C-%7Cq%3Aabstract%2Fcreators_name%2Fdate%2Fdocuments%2Ftitle%3AALL%3AIN%3ATech%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AANY%3AEQ%3Ashow&screen=Search&cache=170532&_action_search=1&search_offset=0
                page = requests.get(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    trs = soup.find_all("tr", {"class": "ep_search_result"})
                    # print(trs)

                    for x in tqdm(range(len(trs)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                        # print(trs[x])
                        href = self.GetHref(trs[x])
                        # print(href)
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
            self.OutputRaw("University of Liverpool")
        else:
            self.OutputCSV("University of Liverpool", "liverpool")


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
        if not hrefs[2].get("href").startswith("http://livrepository."):  #To deal with et all link after list of authors
            if len(hrefs) in {2, 3, 4}:
                return hrefs[3].get("href")
        if len(hrefs) in {1, 2, 3, 4}:
            return hrefs[2].get("href")
        else:
            return "None"


    def GetDate(self, soup):
        tds = soup.find_all('td', string=lambda text: text and "Date Deposited:" not in text)
        for td in tds:
            date_text = td.get_text().strip()
            try:
                parsed_date = parse(date_text, fuzzy=True)
                return parsed_date.strftime("%B %Y")
            except (ValueError, OverflowError) as e:
                # print(f"Error parsing date '{date_text}': {e}")
                pass

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