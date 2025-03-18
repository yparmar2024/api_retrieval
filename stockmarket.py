import requests

"""
STOCK MARKET DOCUMENTATION:
https://www.alphavantage.co/documentation/
"""

user = ""
timing = ""
symbol = ""
interval = 0
marketKey = "ZPU1WOD7GQHXOX3I"
validStock = False
topMatches = []

def start():
    global user

    user = input("Hello, what's your name?\n").strip()
    if getTiming() == "TIME_SERIES_INTRADAY":
        getInterval()
    getSymbol()
    getData()

def getTiming(userInput = ""):
    global timing

    validTimings = ["INTRADAY", "DAILY", "WEEKLY", "MONTHLY"]
    while userInput not in validTimings:
        userInput = input("Would you like the information in intraday, daily, weekly or monthly?\n").strip().upper()
        if userInput not in validTimings:
            print("Incorrect input, try again.\n")
    timing = userInput
    return f"TIME_SERIES_{timing}"

def getInterval(userInput = ""):
    global interval

    validIntervals = ["1", "5", "15", "30", "60"]
    while userInput not in validIntervals:
        userInput = input("Which minute time interval would you like: 1, 5, 15, 30 or 60?\n").strip()
        if userInput not in validIntervals:
            print("Incorrect input, try again.\n")
    interval = userInput
    return f"{interval}min"

def getSymbol(userInput = ""):
    global symbol
    global timing
    global interval
    global marketKey
    global validStock
    global topMatches
    
    userInput = input("What stock would you like to look at today?\n").strip().upper()
    print()

    if timing == "INTRADAY":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{timing}&symbol={userInput}&interval={interval}&apikey={marketKey}'
    else:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{timing}&symbol={userInput}&apikey={marketKey}'
    
    validStock, topMatches = validSymbol(userInput, url)

    while not validStock:
        print("Invalid stock symbol. Did you mean one of these?")
        
        for i, match in enumerate(topMatches[:3]):
            print(f"{i + 1}. {match[0]} - {match[1]}")
        userInput = input("Please enter a valid stock.\n")

        if timing == "INTRADAY":
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{timing}&symbol={userInput}&interval={interval}&apikey={marketKey}'
        else:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{timing}&symbol={userInput}&apikey={marketKey}'

        validStock, topMatches = validSymbol(userInput, url)
    
    symbol = userInput
    print(symbol)
    return symbol

def validSymbol(userSymbol, url):
    global marketKey
    global validStock
    global topMatches

    response = requests.get(url)
    data = response.json()

    if "Meta Data" in data:
        validStock = True
    elif "Information" in data:
        return f"All API Requests are used at the moment, please try again in 24 hours."
    else:
        validStock = False

    topMatches = []

    if not validStock:
        searchURL = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={userSymbol}&apikey={marketKey}"
        searchResponse = requests.get(searchURL)
        searchData = searchResponse.json()

        if "bestMatches" in searchData:
            for match in range(len(searchData["bestMatches"])):
                topMatches.append([searchData["bestMatches"][match]["1. symbol"], searchData["bestMatches"][match]["2. name"]])
        elif "Information" in searchData:
            return f"All API Requests are used at the moment, please try again in 24 hours."
    return [validStock, topMatches]

def getData():
    global timing
    global interval
    global symbol
    global marketKey
    
    if timing == "INTRADAY":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{timing}&symbol={symbol}&interval={interval}&apikey={marketKey}'
        timeSeries = data[f"Time Series ({interval})"]
    elif timing == "DAILY":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{timing}&symbol={symbol}&apikey={marketKey}'
        timeSeries = data[f"Time Series ({timing.capitalize()}"]
    elif timing == "WEEKLY":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{timing}&symbol={symbol}&apikey={marketKey}'
        timeSeries = data[f"{timing.capitalize()} Time Series"]
    elif timing == "MONTHLY":
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_{timing}&symbol={symbol}&apikey={marketKey}'
        timeSeries = data[f"{timing.capitalize()} Time Series"]
    
    response = requests.get(url)
    data = response.json()

    if "Information" in data:
        return f"All API Requests are used at the moment, please try again in 24 hours."

    firstTimeStamp = list(timeSeries.keys())[0]
    firstIntervalData = timeSeries[firstTimeStamp]

    openPrice = firstIntervalData["1. open"]
    highPrice = firstIntervalData["2. high"]
    lowPrice = firstIntervalData["3. low"]
    closePrice = firstIntervalData["4. close"]
    volume = firstIntervalData["5. volume"]

    print(f"Open Price: {openPrice}")
    print(f"High Price: {highPrice}")
    print(f"Low Price: {lowPrice}")
    print(f"Close Price: {closePrice}")
    print(f"Volume: {volume}")