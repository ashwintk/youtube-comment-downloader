# Youtube Comments Downloader
This project allows you to download comments for a YouTube Video without using the YouTube API. 
This project was adopted from the original project https://github.com/egbertbouman/youtube-comment-downloader

### Dependencies
* Python 2.7+
* requests
* lxml
* cssselect


The python packages can be installed with

    pip install requests
    pip install lxml
    pip install cssselect
    
  
### Usage
```
usage: GetCommentsFromVideos.py [--help] [--youtubeid YOUTUBEID] [--output OUTPUT]
Download Youtube comments without using the Youtube API

optional arguments:
  --help, -h            Show this help message and exit
  --youtubeid YOUTUBEID, -y YOUTUBEID
                        ID of Youtube video for which to download the comments
  --output OUTPUT, -o OUTPUT
                        Output filename (output format is line delimited JSON)
```

### Modifications done from the original project
* Computed elapsed time so that the output JSON contains the timestamp of when the comment was published instead of "XX hours/minutes/seconds ago"
* Cleaned the comments by doing the following
    1. Removing new line and carriage return
    2. Removing URL's & User Mentions
    3. Replacing sequence of repeated characters by maximum of three characters (E.g. toooo -> tooo)
    4. Converting multiple white spaces to a single white space
    5. Replacing any hashtags with words
    6. Replacing all the internet slang words with their full form
    7. Replacing all word contractions
    8. Removing all characters but non-alphanumeric characters