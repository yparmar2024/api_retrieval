from datetime import datetime

def start():
    print(getTime())
    print(getDate())

def getTime():
    now = datetime.now()
    currentTime = now.strftime("%I:%M %p").lstrip("0")
    return f"It is currently {currentTime}."

def getDate():
    now = datetime.now()
    month = now.strftime("%B")
    day = now.day
    year = now.year
    
    if 11 <= day <= 13:
        ordinal = "th"
    elif day % 10 == 1:
        ordinal = "st"
    elif day % 10 == 2:
        ordinal = "nd"
    elif day % 10 == 3:
        ordinal = "rd"
    else:
        ordinal = "th"
    
    return f"Today's date is {month} {day}{ordinal}, {year}."