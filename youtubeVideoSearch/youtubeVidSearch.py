import bs4
import requests



#div class = "yt-lockup yt-lockup-tile yt-lockup-video clearfix" --for videos
#div class = "yt-lockup-dismissable yt-uix-tile" --for title
      #div class = "yt-lockup-content" -- content
            #h3 class = "yt-lockup-tile"
            #yt-lockup-byline --for user name
            #yt-lockup-meta-info
                  #class="yt-lockup-meta -- meta data info like date and views

searchQuery = "mylapore kapaleeswarar temple"

reqObject = requests.get("https://www.youtube.com/results?search_query=" + searchQuery).text

#vidURL = "https://www.youtube.com/results?search_query=" + searchQuery

soup = bs4.BeautifulSoup(reqObject , "html.parser")

start = True
foundNext = True

vidTitleID = {}

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
      print('\n stop crawl: ' , stopCrawl)
      print('\n next link: ' , nextLink)
      if len(stopCrawl) < 1 and len(nextLink) != 0:
            getTitle(youtubeObj)
      else:
            start = False
            foundNext = False
            print(vidTitleID)

      div.clear()
      nextPage.clear()
      stopCrawl.clear()



def getVidMetaData(title , url):

    vidURL = requests.get(url).text
    vidObj = bs4.BeautifulSoup(vidURL , "html.parser")

    div = [d for d in vidObj.find_all('div') if d.has_attr('class') and 'watch-main-col' in d['class']]

    #print(div)

    for d in div:
        for m in d.find_all('meta'):
            if m.has_attr('itemprop') and m.has_attr('content'):
                if m['itemprop'] == 'datePublished':
                    vidTitleID[title] = m['content']





#getVidMetaData("https://www.youtube.com/watch?v=oqFreqHc0bE")


if start == True:
      print("starting...")
      getTitle(soup)


