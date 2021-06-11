# homesearch

This script does the following:

1. Creates a Pandas DataFrame from a spreadsheet of property information
2. Queries four tables in two SQL databases for all addresses with the same postcodes and creates a second DataFrame
3. Generates cosine similarities for every matching postcode in the internal and external DataFrames
4. Creates a spreadsheet of those similarities beside each other for human interaction

Notes:
1. The InternalDataRetrieval.py file has been withheld, as it contains information on how to connect to the databases
2. Related to the above, I have not included the SQL queries that create the second DataFrame
