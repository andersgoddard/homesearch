import json
import time
import timeit
import pandas as pd
import openpyxl
from datetime import date
from datetime import datetime

dateFormat = '%d-%m-%Y'
currentTime = time.strftime(dateFormat, time.localtime())
currentDate = datetime.strptime(currentTime, dateFormat)
    
def updateSimilaritySummary(externalData, internalDataArray, similaritySummary):        
    for internalData in internalDataArray:
        start = timeit.default_timer()
        for i in range(len(externalData)):
            for j in range(len(internalData)):
                if externalData.iloc[i]['postcode'] == internalData.iloc[j]['postcode']: 
                    similarityExample = {
                        "Internal Address": internalData.iloc[j]['Address'],
                        "External Address": externalData.iloc[i]['full address'],
                        "Postcode": externalData.iloc[i]['postcode'],
                        "System Date": internalData.iloc[j]['CreationDate'],
                        "Owner": internalData.iloc[j]['ShortName'],
                        "System": internalData.iloc[j]['System'],
                        "Status": internalData.iloc[j]['Status'],
                        "Agents": externalData.iloc[i]['agency_names'],
                        "Current Price": externalData.iloc[i]['current_price'],
                        "Original Price": externalData.iloc[i]['original_price'],  
                        "Date Listed": externalData.iloc[i]['listed_at'],                          
                        "Date Last Sold": externalData.iloc[i]['last sold date'],                          
                        "Similarity": internalData.iloc[j]['Similarity']                            
                        }
                    similaritySummary.append(similarityExample)
    stop = timeit.default_timer()
    print("updateSimilaritySummary took the following time: " + str(stop-start))    
    return similaritySummary
 
def createSpreadsheet(similarityData):
    with pd.ExcelWriter('Output.xlsx', mode='w') as writer:
        similarityData.to_excel(writer, sheet_name='Similarities')