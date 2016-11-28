'''
Read JSON files and extract unique
video ID's
'''

import glob
import os
import json



fileNames = []
vidID = []

def extractUniqueVideo(fileName):

      print(fileName)
      
      with open(fileName) as readJSON:
            jsonData = json.load(readJSON)
            #print(ascii(jsonData['info']))
      
      for vid in jsonData['info']:
            #print(vid.get('videoID'))
            if vid.get('videoID') is not None:
                  vidID.append((vid.get('videoID')))

      


def writeFILE(uniqueVideoID):
      #f = open(os.path.join('your path' , 'videoList.json' ) , 'w' , encoding = 'cp1252' , errors = 'replace')
      f = open('uniqueVideoID.txt', 'a' , encoding = 'cp1252' , errors = 'replace')
      #f.write(json.dumps(results , indent = 4))
      f.write(uniqueVideoID  + '\n')
      f.close()



for file in os.listdir(os.curdir):
      if file.endswith(".json"):
            extractUniqueVideo(file)

print('Count - Before removing duplicates: ',len(vidID))
uniqueVideoID = list(set(vidID))
print('Count - After removing duplicates: ' , len(uniqueVideoID))
for v in uniqueVideoID:
      writeFILE(v)
print('done')

 
#extractUniqueVideo('OUTPUT_FILE.json')
