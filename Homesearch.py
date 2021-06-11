import pandas as pd
import timeit
from Functions import DataManipulation as dm 
from Functions import InternalDataRetrieval as idr
from Functions import CosineSimilarity as cos

externalPropertyDf = pd.read_excel("input.xlsx", index_col=0, encoding='cp1252')

print("Querying databases...")
postcodes = externalPropertyDf['postcode'].to_list()
salesData = idr.getData('Seller', postcodes)
lettingsData = idr.getData('Landlord', postcodes)
buyerData = idr.getData('Buyer', postcodes)
leadData = idr.getData('Lead', postcodes)

print("Getting similarities...") 
start = timeit.default_timer() 
lettingsData['Similarity'] = cos.getCosineSimilarities(lettingsData, externalPropertyDf)
lettingsData.drop(lettingsData[lettingsData.Similarity < 0.75].index, inplace=True)
salesData['Similarity'] = cos.getCosineSimilarities(salesData, externalPropertyDf)
salesData.drop(salesData[salesData.Similarity < 0.75].index, inplace=True)
buyerData['Similarity'] = cos.getCosineSimilarities(buyerData, externalPropertyDf)
buyerData.drop(buyerData[buyerData.Similarity < 0.75].index, inplace=True)
leadData['Similarity'] = cos.getCosineSimilarities(leadData, externalPropertyDf)
leadData.drop(leadData[leadData.Similarity < 0.75].index, inplace=True)
stop = timeit.default_timer()
print("Getting similarities took the following time: " + str(stop-start))

databasePostCodesDf = pd.concat([salesData["postcode"], lettingsData["postcode"], buyerData["postcode"], leadData["postcode"]])
databasePostCodesArray = list(databasePostCodesDf.values.flatten())
homesearchData = externalPropertyDf[externalPropertyDf.postcode.isin(databasePostCodesArray)]

similaritySummary = []
internalData = [salesData, lettingsData, buyerData, leadData]

print("Updating Summaries...")
dm.updateSimilaritySummary(homesearchData, internalData, similaritySummary)
print("Summaries updated...")

updateSimilaritySummaryDf = pd.DataFrame(similaritySummary)

try:
    dm.createSpreadsheet(updateSimilaritySummaryDf)
except:
    input("Close the spreadsheet and try again...")
    dm.createSpreadsheet(updateSimilaritySummaryDf)