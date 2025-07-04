import sqlite3
import csv
import os

stockList = ["MSFT", "GOOG", "NVDA", "AAPL"] 
dbFile = "stockhistory.db"
baseFolder = "C:\Projects\StockTracker"
tableCreate = """
    _no INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    price REAL NOT NULL,
    difference REAL NOT NULL,
    percent REAL NOT NULL
"""

def connectToDB(dbFile):

        stockHistory = sqlite3.connect(dbFile)
        cursor = stockHistory.cursor()
        return stockHistory, cursor

def addStock(stockName, cursor):
    print(f"Adding {stockName} table to {dbFile}")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {stockName} ({tableCreate})")
    print(f"Addition to {dbFile} successful")

def endDB(stockHistory):

    stockHistory.commit()
    stockHistory.close()

def updateTable():

    if not os.path.exists(dbFile):
        print(f"Unable to locate {dbFile}")
    else:
        stockHistory, cursor = connectToDB(dbFile)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    existingTables = [row[0] for row in cursor.fetchall()] 
    #existing_tables.remove("sqlite_sequence")
    print(f"Existing tables: {existingTables}")

    for stockName in stockList:
        for table in existingTables:
            if stockName == table:
                break
            elif table == existingTables[-1]:
                addStock(stockName, cursor)

    endDB(stockHistory)


def createTable(): #In case the db file was deleted

    stockHistory, cursor = connectToDB(dbFile)
    for stockname in stockList:
        addStock(stockname, cursor)

    endDB(stockHistory)



def addValuesToTable(stockValues: list, stockname):

    stockHistory, cursor = connectToDB(dbFile)

    date = getDate()
    cursor.execute(f"INSERT INTO {stockname} (date, price, difference, percent) VALUES (?, ?, ?, ?)", (date, *stockValues))
    endDB(stockHistory)

def getDate():
    from datetime import datetime
    date = datetime.now().strftime("%d-%m-%Y %H-%M")
    return date

def makeFolder(baseFolder, newName):
    Folder = os.path.join(baseFolder, newName)
    if not os.path.exists(Folder):
        os.makedirs(Folder)

def exportCSV(dbFile, tableName, baseFolder):


    makeFolder(baseFolder, "csv")

    baseFolder = f"{baseFolder}/csv"
    makeFolder(baseFolder, tableName)
    baseFolder = f"{baseFolder}/{tableName}"

    #Naming Convention for CSV File
    date = getDate()
    outputFile = os.path.join(baseFolder, f"{tableName}_{date}.csv")

    stockHistory, cursor = connectToDB(dbFile)

    cursor.execute(f"SELECT * FROM {"GOOG"}")
    rows = cursor.fetchall()
    print(rows)

    #Fetching only the header names of tables
    fieldNames = [desc[0] for desc in cursor.description]

    #standard code for .db --> CSV
    with open(outputFile, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fieldNames)
        writer.writerows(rows)
    print(f"Exported {tableName} to {outputFile}")

    endDB(stockHistory)

def exportMultipleCSV(dbFile, tableNames, baseFolder: str = "StockTracker"):
    for tableName in tableNames:
        exportCSV(dbFile, tableName, baseFolder)



