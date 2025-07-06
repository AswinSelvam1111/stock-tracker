from services.database import addValuesToTable
from services.database import exportMultipleCSV
from services.database import exportCSV
from services.graphs import lineGraph
from services.scraper import scrapeData

stockList = ["MSFT", "GOOG", "NVDA", "AAPL"] #add on if any additional stocks!
xpathList = []
for stock in stockList:
    xpathList.append(f"//h3[contains(text(), '{stock}')]")

dbFile = "stockhistory.db"
baseFolder = "C:\Projects\StockTracker"
tableCreate = """
    _no INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    price REAL NOT NULL,
    difference REAL NOT NULL,
    percent REAL NOT NULL
"""

for stockname, xpath in zip(stockList, xpathList):
    addValuesToTable(scrapeData(stockname), stockname)


option = input("""Please select which feature you would like to use:
1: Export Database as a CSV File
2: View all the Stock Data as a Line Graph          
""")

match option:
    case 1:
        option = input("""Please select which stock you would like to export:
        1:MSFT (Microsoft)
        2:GOOG (Google)
        3:NVDA (NVIDIA)
        4:AAPL (Apple)
        5:All of the above
                       """)
        match option:
            case 1:
                exportCSV(dbFile,"MSFT", baseFolder)
            case 2:
                exportCSV(dbFile,"GOOG", baseFolder)
            case 3:
                exportCSV(dbFile,"NVDA", baseFolder)
            case 4:
                exportCSV(dbFile,"AAPL", baseFolder)
            case 5:
                exportMultipleCSV(dbFile, stockList, baseFolder)
    case 2:
        option = input("""Please select which stock you would like to view as a line graph:
        1:MSFT (Microsoft)
        2:GOOG (Google)
        3:NVDA (NVIDIA)
        4:AAPL (Apple)
                       """)
        match option:
            case 1:
                lineGraph("MSFT")
            case 2:
                lineGraph("GOOG")
            case 3:
                lineGraph("NVDA")
            case 4:
                lineGraph("AAPL")