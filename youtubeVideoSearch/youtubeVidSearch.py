import bs4
import requests
import re
import os
import httplib2
import json



#div class = "yt-lockup yt-lockup-tile yt-lockup-video clearfix" --for videos
#div class = "yt-lockup-dismissable yt-uix-tile" --for title
      #div class = "yt-lockup-content" -- content
            #h3 class = "yt-lockup-tile"
            #yt-lockup-byline --for user name
            #yt-lockup-meta-info
                  #class="yt-lockup-meta -- meta data info like date and views


start = True
vidMetaData = []
vidTitleID = {}

''' This function fetches the titles of all
      youtube videos for the given search query'''

def getTitle(youtubeVidObj):

      nextLink = ""

      div = [d for d in youtubeVidObj.find_all('div') if d.has_attr('class')]

      nextPage = youtubeVidObj.find_all('a' , class_ = 'yt-uix-button')
      print(len(nextPage))

      for n in nextPage:
            if n.string == 'Next »':
                  print(n['aria-label'])
                  nextLink = n['href']
            else:
                  foundNext = False

      reqObject = requests.get("https://www.youtube.com/" + nextLink).text
      youtubeObj = bs4.BeautifulSoup(reqObject , "html.parser")

      for d in div:
            if d.has_attr('class') and 'yt-lockup-video' in d['class']:
                  #print(d['class'])
                  if 'yt-lockup-tile' in d['class']:
                        #title = [t for t in d.find_all('a') if t.has_attr('title')]
                        for a in d.find_all('a'):
                              if a.has_attr('title') and a.has_attr('aria-describedby') and a.has_attr('href'):
                                  getVidMetaData(a['title'] , "https://www.youtube.com" + a['href'])
                                  #print(a['title'] , '\t' , a['aria-describedby'] , '\t' , a['href'])



      stopCrawl = youtubeObj.find_all('div' , string = 'No more results')
      #print('\n stop crawl: ' , stopCrawl)
      #print('\n next link: ' , nextLink)
      if len(stopCrawl) < 1 and len(nextLink) != 0:
            getTitle(youtubeObj)
      else:
            start = False
            print('stopping...')
            f = open(os.path.join('C:\\Users\\akanna\\Desktop\\My Work\\Fall 2016\\Big Data Analytics\\Google API\\' , 'videoList.json' ) , 'w' , encoding = 'cp1252' , errors = 'replace')
            f.write(json.dumps(vidTitleID , indent = 4))
            #f.write(str(vidTitleID))
            f.close()

      div.clear()
      nextPage.clear()
      stopCrawl.clear()




'''This function gives the following meta-data content for each YouTube Video

      a) Date published
      b) # of Views
      c) Duration of the video
'''
def getVidMetaData(title , url):

    print(title)
    global vidMetaData
    vidURL = requests.get(url).text
    vidObj = bs4.BeautifulSoup(vidURL , "html.parser")

    div = [d for d in vidObj.find_all('div') if d.has_attr('class') and 'watch-main-col' in d['class']]

    #print(div)

    for d in div:
        for m in d.find_all('meta'):
            if m.has_attr('itemprop') and m.has_attr('content'):
                if m['itemprop'] == 'datePublished':
                    vidMetaData.append(m['content'])
                if m['itemprop'] == 'interactionCount':
                      vidMetaData.append(m['content'])
                if m['itemprop'] == 'duration':
                      time = re.findall('\d+' , m['content'])
                      time = int(time[0]) + float(time[1]) / 60
                      vidMetaData.append(time)





    vidTitleID[title] = vidMetaData
    vidMetaData = []



#getVidMetaData("Arulmigu Kapaleeswarar Temple in Mylapore,Chennai,Tamilnadu" , "https://www.youtube.com/watch?v=XCzBnciokJI")



''' The code sequence starts here. The user is prompted for a search query.
    The final list of titles and the meta-data content is saved in a JSON file.'''

if start == True:
      print("starting...")
      print('Enter serach query....')

      searchQuery = input()

      reqObject = requests.get("https://www.youtube.com/results?search_query=" + searchQuery).text

      #vidURL = "https://www.youtube.com/results?search_query=" + searchQuery

      soup = bs4.BeautifulSoup(reqObject , "html.parser")

      vidTitleID = {}
      vidMetaData = []

      getTitle(soup)



