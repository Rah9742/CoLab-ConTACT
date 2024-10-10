from bs4 import BeautifulSoup
from tqdm import tqdm
from SentenceCase import GetSentenceCase
import requests
import csv
import os


class MTCScraper():
    titleArr = []
    challengeArr = []
    solutionArr = []
    outcomeArr = []
    benefitsArr = []
    hrefArr = []

    def ScrapeForData(self):
        challengeTitleVariations = ["THE CHALLENGE", "The Challenge", "the challenge", "The challenge", "tHE CHALLENGE", "ABOUT THIS PROJECT"]
        solutionTitleVariations = ["THE SOLUTION", "The Solution", "the solution", "The solution", "MTC'S SOLUTION", "MTC's Solution", "mtc's solution", "MTC's solution", "MTC'S Solution", "THE MTC'S SOLUTION"]
        outcomeTitleVariations = ["THE OUTCOME", "The Outcome", "the outcome", "The outcome", "THE PROJECT OUTCOME", "The Project Outcome"]
        benefitsTitleVariations = ["THE BENEFITS", "The Benefits", "the benefits", "The benefits", "BENEFITS TO THE CLIENT", "Benefits To The Client", "benefits to the client", "Benefits to the client", "Benefits to the Client", "tHE BENEFITS"]

        for n in range(9):
            url = 'https://www.the-mtc.org/case-studies/?page=' + str(n + 1)
            page = requests.get(url)

            if page.status_code == 200:
                soup = BeautifulSoup(page.text, "html.parser")

                articles = soup.find_all("article", {"class": "col-lg-4 col-md-6 col-sm-6"})
                
                for i in tqdm(range(len(articles)), ncols=80, ascii=True, desc="Page " + str(n + 1)):
                    href = "https://www.the-mtc.org" + articles[i].find("a").get("href")
                    materialPage = requests.get(href)
                    materialSoup = BeautifulSoup(materialPage.text, "html.parser")

                    self.titleArr.append(articles[i].get_text())
                    self.challengeArr.append(self.GetDesciption(materialSoup, challengeTitleVariations));
                    self.solutionArr.append(self.GetDesciption(materialSoup, solutionTitleVariations));
                    self.outcomeArr.append(self.GetDesciption(materialSoup, outcomeTitleVariations));
                    self.benefitsArr.append(self.GetDesciption(materialSoup, benefitsTitleVariations));

                    self.hrefArr.append(href)

        self.OutputCSV();


    def OutputCSV(self):
        filename = "out/mtc.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', newline='', encoding='utf-8') as csvFile:
            headerList = ['Title', 'Href', 'Challenge', 'Solution', 'Outcome', 'Benefits', 'Institution']
            writer = csv.DictWriter(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, fieldnames=headerList)
            writer.writeheader()
            for x in range(len(self.titleArr)):
                title = self.titleArr[x].strip()

                challenge = self.FormatParagraph(self.challengeArr[x]);
                solution = self.FormatParagraph(self.solutionArr[x]);
                outcome = self.FormatParagraph(self.outcomeArr[x]);
                benefits = self.FormatParagraph(self.benefitsArr[x]);

                writer.writerow({'Title': title, 'Href': self.hrefArr[x], 'Challenge': challenge, 'Solution': solution, 'Outcome': outcome, 'Benefits': benefits, 'Institution': 'MTC'})

    def FormatParagraph(self, paragraph):
        paragraph = paragraph.replace('\n', '.').replace('\r', '')
        # this is a bit weird, we iterate this an arbitrary number of times to remove all the repeating periods.
        for y in range(12):
            paragraph = paragraph.replace('..', '.')
        paragraph = paragraph.strip()

        if paragraph == "":
            return "None"

        if (paragraph[0] == '.'):
            paragraph = paragraph[1:]
        paragraph = GetSentenceCase(paragraph)
        paragraph = paragraph.replace('.', '. ')
        return paragraph
    
    def GetDesciption(self, soup, headingTextVariations):
        heading = None
        for i in range(len(headingTextVariations)):
            heading = soup.find(text=headingTextVariations[i])
            if heading != None:
                break

        if heading == None:
            return "None"

        tagsBetween = []
        currentTag = heading.find_next()

        while True:
            if currentTag == None:
                break

            if currentTag.name == "h1" or currentTag.name == "h2" or currentTag.name == "h3":
                break
            
            if currentTag.get("class") != None:
                if currentTag.name == "div" and currentTag.get("class")[0] == "spacer-block":
                    currentTag = currentTag.find_next()
                    continue

            if currentTag.get("class") != None:
                if currentTag.name == "div" and currentTag.get("class")[0] != "":
                    break

            potentialH1 = currentTag.find("h1")
            potentialH2 = currentTag.find("h2")
            potentialH3 = currentTag.find("h3")

            if potentialH1 is not None or potentialH2 is not None or potentialH3 is not None:
                break

            tagsBetween.append(currentTag)
            currentTag = currentTag.find_next()

        output = ""
        for i in range(len(tagsBetween)):
            output += tagsBetween[i].get_text()
        
        return output

    