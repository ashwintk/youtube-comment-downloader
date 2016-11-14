import sys, re, csv

sys.path.append('./')

# This function can be used to parse a file given a delimiter, file name and key & value to select
def readFileandReturnADict(fileName, readMode, delimiter, keyIndex, valueIndex, isLower, fileDialect = None):
    mydict={}
    with open(fileName, readMode) as readHandle:
        if fileDialect is None:
            fileDialect = csv.Sniffer().sniff(readHandle.read(), delimiters=delimiter)
        readHandle.seek(0)
        reader = csv.reader(readHandle, fileDialect)
        for line in reader:
            if isLower:
                mydict.update({line[keyIndex].lower(): line[valueIndex]})
            else:
                mydict.update({line[keyIndex]: line[valueIndex]})
    readHandle.close()
    return mydict

# This function removes new line & return carriages from comments
def stripNewLineAndReturnCarriage(comment):
    return comment.replace('\n', ' ').replace('\r', '').strip().lstrip()

# This function is used to remove all the URL's in a comment
def removeURL(comment):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',comment)

# This function is used to remove user mentions in a comment
def removeUserMentions(comment):
    return re.sub('\+[^\s]+','',comment)

# This function replaces words with repeating 'n' or more same characters with a single character
def replaceRepeatedCharacters(comment):
    return re.sub(r"(.)\1{3,}",r"\1", comment)

# This function is used to convert multiple white spaces into a single white space
def convertMultipleWhiteSpacesToSingleWhiteSpace(comment):
    return re.sub('[\s]+', ' ', comment)

# This function replaces any hash tag in a comment with the word
def replaceHashTagsWithWords (comment):
    return re.sub(r'#([^\s]+)', r'\1', comment)

# This function splits a string by a character and replaces words from key of the dictionary
def replaceOccurrencesOfAString(text,splitBy,dict,lowerFlag):
    str_array=text.split(splitBy)
    return_str=""
    for word in str_array:
        key_to_Search=str(word).strip().lstrip()
        if len(key_to_Search) >1:
            if lowerFlag:
                key_to_Search=word.lower()
            if dict.has_key(key_to_Search):
                return_str+=" "+dict[key_to_Search]
            else:
                return_str += " " + word
    return return_str

# This method calls other methods to cleanse youtube comments
def cleanseComments(commentText, internet_slang_dict, contractions_dict):
    commentText = commentText.lstrip().strip()
    # Remove new line and carriage return
    commentText = stripNewLineAndReturnCarriage(commentText)
    # Remove URL's & User Mentions
    commentText = removeURL(commentText)
    commentText = removeUserMentions(commentText)
    # Replace sequence of repeated characters by three characters
    commentText = replaceRepeatedCharacters(commentText)
    # Convert multiple white spaces to a single white space
    commentText = convertMultipleWhiteSpacesToSingleWhiteSpace(commentText)
    # Replace hashtags with words
    commentText = replaceHashTagsWithWords(commentText)
    commentText = re.sub(r'([^\s\w\d]|_)', '', commentText)
    # Replace all the internet slang words
    commentText = replaceOccurrencesOfAString(commentText, ' ', internet_slang_dict, True).lstrip().strip()
    # Replace all word contractions
    commentText = replaceOccurrencesOfAString(commentText, ' ', contractions_dict, True).lstrip().strip()
    # Convert multiple white spaces to a single white space
    commentText = convertMultipleWhiteSpacesToSingleWhiteSpace(commentText)
    return commentText