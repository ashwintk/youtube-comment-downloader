'''
      This class contains the methods
      needed to fetch the YouTube video
      metadata.
'''

import bs4
import requests
import re
import os
import httplib2
import json
import argparse
import sys

class YouTubeSearch:

      
      #Set of class attributes that are global in scope
      
      USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
      YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query={}"
      YOUTUBE_URL = "https://www.youtube.com/"
      vidInfo = {}
      vidInfo['info'] = []
      vidMetaData = {}
      
      

      def __init__(self , search_term , output_file_name):
            
            #Initialize with the user search query
            self.searchQuery = search_term
            self.YOUTUBE_SEARCH_URL = self.YOUTUBE_SEARCH_URL.format(self.searchQuery)
            self.output_file_name = output_file_name


      def setSessions(self , YOUTUBE_GEN_URL):
            #print("url: " , YOUTUBE_GEN_URL)
            with requests.Session() as s:
                  s.headers = {'User-Agent' : self.USER_AGENT}
                  self.reqObj = s.get(YOUTUBE_GEN_URL).text
                  #print(self.reqObj)
                  self.soup = bs4.BeautifulSoup(self.reqObj , "html.parser")
                  return self.soup

      def getTitle(self , youtubeVidObj):

            nextLink = ""

            div = [d for d in youtubeVidObj.find_all('div') if d.has_attr('class')]

            nextPage = youtubeVidObj.find_all('a' , class_ = 'yt-uix-button')
            #print(len(nextPage))

            for n in nextPage:
                  if n.string == 'Next »':
                        print(n['aria-label'])
                        nextLink = n['href']
                  else:
                        foundNext = False

            youtubeObj = self.setSessions(self.YOUTUBE_URL + nextLink)
            #reqObject = requests.get("https://www.youtube.com/" + nextLink).text
            #youtubeObj = bs4.BeautifulSoup(reqObject , "html.parser")

            for d in div:
                  if d.has_attr('class') and 'yt-lockup-video' in d['class']:
                        #print(d['class'])
                        if 'yt-lockup-tile' in d['class']:
                              #title = [t for t in d.find_all('a') if t.has_attr('title')]
                              for a in d.find_all('a'):
                                    if a.has_attr('title') and a.has_attr('aria-describedby') and a.has_attr('href'):
                                        self.getVidMetaData(a['title'] , "https://www.youtube.com" + a['href'])
                                        #print(ascii(a['title']) , '\t' , ascii(a['href']))



            stopCrawl = youtubeObj.find_all('div' , string = 'No more results')
            print('\n stop crawl: ' , stopCrawl)
            print('\n next link: ' , nextLink)
            if len(stopCrawl) < 1 and len(nextLink) != 0:
                  self.getTitle(youtubeObj)
            else:
                  start = False
                  print('stopping...')
                  self.writeJSON(self.vidInfo, self.output_file_name)
                  #f = open(os.path.join('C:\\Users\\akanna\\Desktop\\My Work\\Fall 2016\\Big Data Analytics\\Google API\\' , 'videoList.json' ) , 'w' , encoding = 'cp1252' , errors = 'replace')
                  #f.write(json.dumps(vidTitleID , indent = 4))
                  #f.write(str(vidTitleID))
                  #f.close()

            div.clear()
            nextPage.clear()
            stopCrawl.clear()
            
      def getVidMetaData(self , title , url):

          #print(title)
          #global vidMetaData
          vidObj = self.setSessions(url)
          self.vidMetaData['title'] = title
          #vidURL = requests.get(url).text
          #vidObj = bs4.BeautifulSoup(vidURL , "html.parser")

          div = [d for d in vidObj.find_all('div') if d.has_attr('class') and 'watch-main-col' in d['class']]

          #print(div)

          for d in div:
              for m in d.find_all('meta'):
                    if m.has_attr('itemprop') and m.has_attr('content'):
                          if m['itemprop'] == 'datePublished':
                                self.vidMetaData['datePublished'] = m['content']
                          if m['itemprop'] == 'interactionCount':
                                self.vidMetaData['views'] = m['content']
                          if m['itemprop'] == 'videoId':
                                self.vidMetaData['videoID'] = m['content']
                          if m['itemprop'] == 'duration':
                                time = re.findall('\d+' , m['content'])
                                time = int(time[0]) + float(time[1]) / 60
                                self.vidMetaData['duration'] = time
                      
                      
                      
    

          self.vidInfo['info'].append(self.vidMetaData)
          self.vidMetaData = {}
            

      def writeJSON(self , results , output_file_name):
            #f = open(os.path.join('your path' , 'videoList.json' ) , 'w' , encoding = 'cp1252' , errors = 'replace')
            f = open(self.output_file_name + '.json', 'w+' , encoding = 'cp1252' , errors = 'replace')
            f.write(json.dumps(results , indent = 4))
            #f.write(str(vidTitleID))
            f.close()
      

      def printURL(self):
            print(self.YOUTUBE_SEARCH_URL)
      


def main(argv):
      
      parser = argparse.ArgumentParser(add_help=False, description=('Get Video Metadata from YouTube'))
      parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
      parser.add_argument('--search', '-s', help='Specify search term')
      parser.add_argument('--output', '-o', help='Specify Output filename (output format is in JSON format)')

      try:
            args = parser.parse_args(argv)
            search_term = args.search
            output_file_name = args.output
            
            if not output_file_name:
                  parser.print_usage()
                  raise ValueError('you need to specify a output filename')
                  
      except Exception as e:
             print('Error:', str(e))
             sys.exit(1)


      #print('Enter Search Term: ')
      yt = YouTubeSearch(search_term , output_file_name)

      #print(yt.YOUTUBE_SEARCH_URL)
      obj = yt.setSessions(yt.YOUTUBE_SEARCH_URL)
      yt.getTitle(obj)

if __name__ == '__main__':
      main(sys.argv[1:])
