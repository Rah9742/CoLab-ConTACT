from .University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class Southampton(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = 'https://eprints.soton.ac.uk/cgi/search/archive/simple?exp=0%7C1%7C-date%2Fcontributors_name%2Ftitle%7Carchive%7C-%7Cq%3Aabstract%2Fdocuments%2Ftitle%3AALL%3AIN%3A'+keywords[i]+'%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AANY%3AEQ%3Ashow&_action_search=1&order=-date%2Fcontributors_name%2Ftitle&screen=Search&cache=39712837&search_offset='+str(y*20)
                # https://eprints.soton.ac.uk/cgi/search/archive/simple?exp=0%7C1%7C-date%2Fcontributors_name%2Ftitle%7Carchive%7C-%7Cq%3Aabstract%2Fdocuments%2Ftitle%3AALL%3AIN%3ATech%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AANY%3AEQ%3Ashow&_action_search=1&order=-date%2Fcontributors_name%2Ftitle&screen=Search&cache=39712837&search_offset=20
                page = requests.get(url)
                # print(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    trs = soup.find_all("tr", {"class": "ep_search_result"})

                    for x in tqdm(range(len(trs)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                        href = self.GetHref(trs[x])
                        if href != "None":
                            pageMat = requests.get(href)
                            if page.status_code == 200:
                                soupMat = BeautifulSoup(pageMat.text, "html.parser")
                                self.titleArr.append(trs[x].find("strong").get_text())
                                self.hrefArr.append(href)
                                self.authorArr.append(self.GetAuthors(trs[x]))
                                # self.dateArr.append("Test")
                                # self.abstractArr.append("Test")
                                self.dateArr.append(self.GetDate(href))
                                self.abstractArr.append(self.GetAbstract(href))
                                self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("University of Southampton")
        else:
            self.OutputCSV("University of Southampton", "southampton")


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


    def GetAbstract(self, href):
        page = requests.get(href)
        soup = BeautifulSoup(page.text, "html.parser")

        h2_element = soup.find('h2', text='Abstract')

        if h2_element:
            p_element = h2_element.find_next('p')
            if p_element:
                return p_element.get_text(strip=True)

        else:
            return "None"

    def remove_before_colon(text):
        if ':' in text:
            return text.split(':', 1)[1].strip()
        return text

    def GetDate(self, href):

        page = requests.get(href)
        soup = BeautifulSoup(page.text, "html.parser")
        
        span_element = soup.find('h2', text='More information')

        if span_element:
            div_element = span_element.find_next('div')
            if div_element:
                div_element = div_element.get_text(strip=True)
                if ':' in div_element:
                    return div_element.split(':', 1)[1].strip()
                return div_element
        else:
            return "None"