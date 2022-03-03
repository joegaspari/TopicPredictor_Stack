import pyodbc 
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from pandas import DataFrame
import pandas as pd



conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=StackOverflow;Trusted_Connection=yes;')

# query = "SELECT * FROM [StackOverflow].[dbo].[Comments] TABLESAMPLE(50000 rows);"

# cursor = conn.cursor()
# # results = cursor.execute(cmd).fetchall()
# df = pd.read_sql(query, conn)

