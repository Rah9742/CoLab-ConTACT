#Author: Rahil Shah

from .University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class Swansea(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = "https://cronfa.swan.ac.uk/Search/Results?lookfor=" + keywords[i] + "&type=AllFields&page=" + str(1+y)
                # https://cronfa.swan.ac.uk/Search/Results?lookfor=Tech&type=AllFields&page=1
                page = requests.get(url)
                # print(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    divs = soup.find_all("div", {"class": "col-md-8 middle"})

                    for x in tqdm(range(0,len(divs)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                        if x >= 0:
                            self.titleArr.append(divs[x].find('a', class_='title getFull', href=True).get_text(strip=True))
                            href = "https://cronfa.swan.ac.uk" + divs[x].find("a").get("href")
                            self.hrefArr.append(href)
                            self.authorArr.append(self.GetAuthors(divs[x]))
                            self.dateArr.append(self.GetDate(href))
                            self.abstractArr.append(self.GetAbstract(href))
                            self.keywordsArr.append(keywords[i])
                            
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw("Swansea University")
        else:
            self.OutputCSV("Swansea University", "swansea")


    def GetAuthors(self, currentDiv):
        authorString = ""
        spans = currentDiv.find_all("span")
        for x in range(len(spans)):
            if x != 0:
                if spans[x].get("class") == ['date']:
                    break;
                if spans[x].get("class") == None:
                    if x != 1:
                        authorString += "; " + spans[x].get_text()
                    else:
                        authorString += spans[x].get_text()

        return authorString

    def GetDate(self, href):
        page = requests.get(href)
        soup = BeautifulSoup(page.text, "html.parser")

        spans = soup.find_all('span', {"property": "publicationDate"})
        for span in spans:
            date_text = span.get_text().strip()
            try:
                parsed_date = parse(date_text, fuzzy=True)
                return parsed_date.strftime("%Y")
            except (ValueError, OverflowError) as e:
                # print(f"Error parsing date '{date_text}': {e}")
                pass

        return "None"

    def GetAbstract(self, href):
        page = requests.get(href)
        soup = BeautifulSoup(page.text, "html.parser")

        th_element = soup.find('th', text='Abstract: ')

        if th_element:
            td_element = th_element.find_next('td')
            if td_element:
                return td_element.get_text(strip=True)

        else:
            return "None"