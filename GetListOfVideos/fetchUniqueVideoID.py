'''
Read JSON files and extract unique
video ID's
'''

import glob
import os
import json
import argparse
import sys


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

      


def writeFILE(uniqueVideoID , output_file_name):

      #f = open(os.path.join('your path' , 'videoList.json' ) , 'w' , encoding = 'cp1252' , errors = 'replace')
      f = open(output_file_name + '.txt', 'a' , encoding = 'cp1252' , errors = 'replace')
      #f.write(json.dumps(results , indent = 4))
      f.write(uniqueVideoID  + '\n')
      f.close()


def main(argv):

      parser = argparse.ArgumentParser(add_help=False, description=('Extract Unique Video IDs from YouTube titles'))
      parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
      parser.add_argument('--output', '-o', help='Specify Output filename (output format is in text format)')

      try:
            args = parser.parse_args(argv)
            output_file_name = args.output

            if not output_file_name:
                  parser.print_usage()
                  raise ValueError('you need to specify a output filename')
      
            for file in os.listdir(os.curdir):
                  if file.endswith(".json"):
                        extractUniqueVideo(file)

            print('Count - Before removing duplicates: ',len(vidID))
            uniqueVideoID = list(set(vidID))
            print('Count - After removing duplicates: ' , len(uniqueVideoID))
            for v in uniqueVideoID:
                  writeFILE(v , output_file_name)
            print('done')
            
      except Exception as e:
             print('Error:', str(e))
             sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])



