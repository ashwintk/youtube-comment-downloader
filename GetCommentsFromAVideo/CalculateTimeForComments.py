import time, datetime

YEAR_VAR = 365*24*60*60
MONTH_VAR = 30*24*60*60
WEEK_VAR = 7*24*60*60
DAY_VAR = 24*60*60
HOUR_VAR = 60*60
MINUTE_VAR = 60
SECOND_VAR = 1


def convertStringToInt(valueToConvert):
    convertedVar = 0
    try:
        convertedVar = int(valueToConvert)
    except:
        convertedVar = -1
    return convertedVar

def getNumberOfLeapYears(numberOfYearsAgo):
    this_year = datetime.datetime.now().year
    numberOfLeapYears = 0
    for year in range(this_year-numberOfYearsAgo,this_year+1):
        if year % 4 == 0 and year % 100 != 0:
            numberOfLeapYears += 1
        elif year % 4 == 0 and year % 100 == 0 and year % 400 == 0:
            numberOfLeapYears += 1
    return numberOfLeapYears

def getNumberOfExtraDaysInAMonth(numberOfMonthsAgo):
    this_month = datetime.datetime.now().month
    numberOfExtraDays = 0
    daysInAMonthArray = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for month in range(this_month-numberOfMonthsAgo, this_month+1):
        this_index = 0
        if month < 0:
            this_index = this_month + month
        else:
            this_index = this_month - month
        if daysInAMonthArray[this_index] > 30:
            numberOfExtraDays += 1
        elif daysInAMonthArray[this_index] < 30:
            numberOfExtraDays -= 2
    return numberOfExtraDays

def calculateTime(elapsedTime_String):
    elapsedTimeArr = elapsedTime_String.strip().lstrip().split(" ")
    timeToSubtract = 0
    for i in xrange(0,len(elapsedTimeArr)):
        if elapsedTimeArr[i].strip().lstrip().lower() == "years" or elapsedTimeArr[i].strip().lstrip().lower() == "year":
            if i != 0 and convertStringToInt(elapsedTimeArr[i-1]) != -1:
                timeToSubtract += (convertStringToInt(elapsedTimeArr[i-1]) * YEAR_VAR) + \
                                  (getNumberOfLeapYears(convertStringToInt(elapsedTimeArr[i-1])) * DAY_VAR)
        elif elapsedTimeArr[i].strip().lstrip().lower() == "months" or elapsedTimeArr[i].strip().lstrip().lower() == "month":
            if i != 0 and convertStringToInt(elapsedTimeArr[i-1]) != -1:
                timeToSubtract += (convertStringToInt(elapsedTimeArr[i-1]) * MONTH_VAR)+ \
                                  (getNumberOfExtraDaysInAMonth(convertStringToInt(elapsedTimeArr[i-1])) * DAY_VAR)
        elif elapsedTimeArr[i].strip().lstrip().lower() == "weeks" or elapsedTimeArr[i].strip().lstrip().lower() == "week":
            if i != 0 and convertStringToInt(elapsedTimeArr[i-1]) != -1:
                timeToSubtract += (convertStringToInt(elapsedTimeArr[i-1]) * WEEK_VAR)
        elif elapsedTimeArr[i].strip().lstrip().lower() == "days" or elapsedTimeArr[i].strip().lstrip().lower() == "day":
            if i != 0 and convertStringToInt(elapsedTimeArr[i-1]) != -1:
                timeToSubtract += (convertStringToInt(elapsedTimeArr[i-1]) * DAY_VAR)
        elif elapsedTimeArr[i].strip().lstrip().lower() == "hours" or elapsedTimeArr[i].strip().lstrip().lower() == "hour":
            if i != 0 and convertStringToInt(elapsedTimeArr[i-1]) != -1:
                timeToSubtract += (convertStringToInt(elapsedTimeArr[i-1]) * HOUR_VAR)
        elif elapsedTimeArr[i].strip().lstrip().lower() == "minutes" or elapsedTimeArr[i].strip().lstrip().lower() == "minute":
            if i != 0 and convertStringToInt(elapsedTimeArr[i-1]) != -1:
                timeToSubtract += (convertStringToInt(elapsedTimeArr[i-1]) * MINUTE_VAR)
        elif elapsedTimeArr[i].strip().lstrip().lower() == "seconds" or elapsedTimeArr[i].strip().lstrip().lower() == "second":
            if i != 0 and convertStringToInt(elapsedTimeArr[i-1]) != -1:
                timeToSubtract += (convertStringToInt(elapsedTimeArr[i-1]) * SECOND_VAR)
        elif elapsedTimeArr[i].strip().lstrip().lower() == "just now" or elapsedTimeArr[i].strip().lstrip().lower() == "right now":
            timeToSubtract += 0
    return timeToSubtract