# Fetch List of YouTube Videos for a search term
This project allows you to fetch a list of YouTube videos for a search term without using the YouTube API. 


### Dependencies
* Python 3.x+
* bs4
* requests
* argparse

The python packages can be installed with

    pip install requests
    pip install bs4
	pip install argparse
 
### Usage
```
usage: YouTubeSearch.py [--help] [--search SEARCH_TERM] [--output OUTPUT_FILE]
Search for list of videos for a search term without YouTube API

optional arguments:
  --help, -h            Show this help message and exit
  --search SEARCH_TERM, -s SEARCH_TERM
                        Search term for which you'd need to get a list of videos
  --output OUTPUT, -o OUTPUT
                        Output filename (output format is line delimited JSON)
```

###Fetch Unique Video IDs
```
Filename - fetchUniqueVideoID.py
usage: fetchUniqueVideoID.py [--help] [--output OUTPUT_FILE]
optional arguments:
  --help, -h            Show this help message and exit

  --output OUTPUT, -o OUTPUT
                        Output filename (output format is text)
```

