"""
LIBRARY & PACKAGES 
"""
#CSV File Processing 
import csv 
import glob 
from pathlib import Path 
import os 

#Data Processing 
import pandas as pd 

def readFile():
    wd = '../Uptake/2015' #Set working directory 
    os.chdir(wd)
    df = pd.concat([pd.read_csv(f) for f in glob.glob('2015-01-*.csv')], ignore_index = True)
    return df

def explore(df): 
    # FROM 95 columns -> 81 columns: 
    df = df.dropna(axis=1,how='all') #drop all columns with all NANs records  

    #FROM 81 columns -> 43 columns after removing normalized columns: 
    index = df.head() #column names 
    normalized_columns = [] 
    for i in index: 
        if i.find('normalized') >0: 
            normalized_columns.append(i)
    df.drop([x for x in normalized_columns], axis=1, inplace=True) #df without normalized columns 
    #FROM, 43 columns -> 33 columns after removing all columns with >70% empty values 
    df = df[[column for column in df if df[column].count()/len(df) >=0.3]]
    print(df.shape) #(rows: 1293799, columns:33)
    print(df.info(memory_usage='deep')) #653.6 MB NOW 
    
    #Remove serial_number, model, capacity_bytes
    df.drop(columns =['model','capacity_bytes']) #columns not useful for now 
    print(len(df.dtypes))
    df.to_csv('filtered_2015.csv')

data = readFile()
explore(data) 




