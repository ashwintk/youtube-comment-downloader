# Fetch List of YouTube Videos for a search term
This project allows you to fetch a list of YouTube videos for a search term without using the YouTube API. 


### Dependencies
* Python 2.7+
* bs4
* requests


The python packages can be installed with

    pip install requests
    pip install bs4
 
### Usage
```
usage: SearchForVideos.py [--help] [--search SEARCH_TERM] [--output OUTPUT_FILE]
Search for list of videos for a search term without YouTube API

optional arguments:
  --help, -h            Show this help message and exit
  --search SEARCH_TERM, -s SEARCH_TERM
                        Search term for which you'd need to get a list of videos
  --output OUTPUT, -o OUTPUT
                        Output filename (output format is line delimited JSON)
```