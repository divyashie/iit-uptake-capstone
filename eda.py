"""
LIBRARY & PACKAGES 
"""
import os 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import savefig

#Set working directory 
wd = '../Uptake/2015' 
os.chdir(wd)

def data_extract(): 
    data = pd.read_csv("filtered_2015.csv")
    #relevant Smart stats: 1, 3, 5, 9, 192, 194, 197, 198
    df = data[["failure", "smart_1_raw", "smart_3_raw", "smart_5_raw", "smart_9_raw", "smart_192_raw", "smart_194_raw","smart_197_raw", "smart_198_raw"]]
    df.rename(columns=lambda x: x.replace('smart_',''), inplace=True)
    print(df.columns)
    return df

#see the failure with each smart stats 
def data_manipulate(df): 
    corr = df.corr()
    ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
    )
    ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
    )
    figure = ax.get_figure()
    return figure.savefig("output.png")

data_extract()
#data_manipulate(data_extract())
