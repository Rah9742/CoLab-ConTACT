from .University import University
import json
from tqdm import tqdm
import requests
import csv

class Surrey(University):

    def ScrapeForData(self, isRaw, depth, keywords):
        responsesPerPage = 30
        for i in range(len(keywords)):
            for y in range(depth):
                responsesStartPos = y * responsesPerPage
                url = 'https://openresearch.surrey.ac.uk/esplorows/rest/research/simpleSearch/assets?institution=44SUR_INST&q=sub%2Ccontains%2C' + keywords[i] + '%2CAND&scope=Research&tab=Research&offset=' + str(responsesStartPos) + '&limit=' + str(responsesStartPos + responsesPerPage) + '&sort=date_d&lang=en&enableAsteriskSearch=false'
                response = requests.get(url)

                if (response.status_code != 200):
                    print('Unable to access page #' + str(1 + y) + ' for keyword \'' + keywords[i] + '\'')
                    continue

                jsonContent = json.loads(response.content)

                if len(jsonContent['assets']) == 0:
                    break

                for paperElement in tqdm(jsonContent['assets'], ncols=80, ascii=True, desc=keywords[i] + '; Page #' + str(1 + y)):
                    # Each paper here has a unique ID that we could use to avoid duplication in the future?
                    self.titleArr.append(paperElement['title'])
                    self.hrefArr.append('https://openresearch.surrey.ac.uk/esploro' + paperElement['permalink'])

                    # https://stackoverflow.com/a/5465334
                    self.authorArr.append(', '.join('\'%s\'' % creator['displayName'] for creator in paperElement['creators']))

                    self.dateArr.append(paperElement['date'])
                    self.abstractArr.append(paperElement['description'])
                    self.keywordsArr.append(keywords[i]) # Should try to put all of the matching keywords here instead of having separate entries?

                if jsonContent['info']['total'] == jsonContent['info']['last']:
                    # Finished processing, there are no more pages.
                    break

        if (isRaw):
            self.OutputRaw("University of Surrey")
        else:
            self.OutputCSV("University of Surrey", "surrey")
