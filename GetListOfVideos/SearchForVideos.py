#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bs4, argparse, requests, re, json, sys, time

start = True
# Dictionary to store search results
searchResults = {}
searchResults['results'] = []
# Initialize variables for Youtube URL's, search terms & user agent
YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query={SEARCH_TERM}"
YOUTUBE_URL = "https://www.youtube.com/"
SEARCH_TERM = ""
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"

def ajax_request(session, url, params, data, retries=10, sleep=20):
    for _ in range(retries):
        response = session.post(url, params=params, data=data)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            return response_dict.get('page_token', None), response_dict['html_content']
        else:
            time.sleep(sleep)

''' This function fetches the titles of all
      youtube videos for the given search query
      The output file is written by this function after fetching video titles from
      all the pages'''

def getTitle(youtubeVidObj):
    nextLink = ""
    div = [d for d in youtubeVidObj.find_all('div') if d.has_attr('class')]
    nextPage = youtubeVidObj.find_all('a', class_='yt-uix-button')
    for n in nextPage:
        if "Next" in n.string:
            print(n['aria-label'])
            nextLink = n['href']
        else:
            foundNext = False

    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    response = session.get(YOUTUBE_URL + nextLink)
    reqObject = response.text
    youtubeObj = bs4.BeautifulSoup(reqObject, "html.parser")

    for d in div:
        if d.has_attr('class') and 'yt-lockup-video' in d['class']:
            if 'yt-lockup-tile' in d['class']:
                for a in d.find_all('a'):
                    if a.has_attr('title') and a.has_attr('aria-describedby') and a.has_attr('href'):
                        getVidMetaData(a['title'], YOUTUBE_URL + a['href'])
    stopCrawl = youtubeObj.find_all('div', string='No more results')
    if len(stopCrawl) < 1 and len(nextLink) != 0:
        getTitle(youtubeObj)
    else:
        start = False
        with open(OUTPUT_FILE, "w+") as writeHandle:
            writeHandle.write(json.dumps(searchResults, indent = 2))
        writeHandle.close()
    div.clear()
    nextPage.clear()
    stopCrawl.clear()


'''This function gives the following meta-data content for each YouTube Video

      a) Date published
      b) # of Views
      c) Duration of the video
'''


def getVidMetaData(title, url):
    vidMetaData = {}
    vidURL = requests.get(url).text
    vidObj = bs4.BeautifulSoup(vidURL, "html.parser")

    div = [d for d in vidObj.find_all('div') if d.has_attr('class') and 'watch-main-col' in d['class']]
    vidMetaData['title'] = str(title)
    for d in div:
        for m in d.find_all('meta'):
            if m.has_attr('itemprop') and m.has_attr('content'):
                if m['itemprop'] == 'datePublished':
                    vidMetaData['datePublished'] = str(m['content'])
                if m['itemprop'] == 'interactionCount':
                    vidMetaData['numberOfViews'] = str(m['content'])
                if m['itemprop'] == 'duration':
                    time = re.findall('\d+', m['content'])
                    time = int(time[0]) + float(time[1]) / 60
                    vidMetaData['duration'] = time
    searchResults['results'].append(vidMetaData)
    vidMetaData = {}


''' The code sequence starts here. The user is prompted for a search query.
    The final list of titles and the meta-data content is saved in a JSON file.'''


def main(argv):
    parser = argparse.ArgumentParser(add_help=False, description=('Get list of Videos for a search term'))
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit')
    parser.add_argument('--search', '-s', help='Search Term')
    parser.add_argument('--output', '-o', help='Output file (output format is line delimited JSON)')
    global OUTPUT_FILE
    try:
        args = parser.parse_args(argv)

        SEARCH_TERM = args.search
        OUTPUT_FILE = args.output

        if not SEARCH_TERM or not OUTPUT_FILE:
            parser.print_usage()
            raise ValueError("you need to specify a Search term & an output file")
        print 'Searching videos for search term:', SEARCH_TERM
        if start == True:
            session = requests.Session()
            session.headers['User-Agent'] = USER_AGENT
            response = session.get(YOUTUBE_SEARCH_URL.format(SEARCH_TERM=SEARCH_TERM))
            reqObject = response.text
            soup = bs4.BeautifulSoup(reqObject, "html.parser")
            vidTitleID = {}
            vidMetaData = []
            getTitle(soup)
        print '\nDone!'
    except Exception, e:
        print 'Error:', str(e)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
