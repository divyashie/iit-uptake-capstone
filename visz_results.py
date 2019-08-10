"""
PACKAGES & LIBRARY 
"""
import pandas as pd 
import numpy as np

import plotly.graph_objects as go

def read_file(): #Read file 
    path = '../Uptake/random_result.txt'
    with open(path, "r") as f:
        result = [line.strip() for line in f if line.strip()] #remove all blank lines in file 
    return result 

def file_extraction(result): #Extract data from file
    data = [] 
    #header = result[0]
    for row in result[1:]: #each row is a string     
        string = row.split(",") 
        title = string[0] 
        batch_number = string[1]
        percent_x = string[2]

        #confusion matrix values 
        tn = int(string[3])
        fp = int(string[4])
        fn = int(string[5])
        tp = int(string[6])

        #eventwise accuracy 
        accuracy_list = string[7].split('/')
        accuracy = int(accuracy_list[0]) / int(accuracy_list[1])
        precision, recall = precision_recall(tp, fn, fp, tn)

        #Save data into a list of list 
        data.append([title, batch_number, percent_x, precision, recall, accuracy])
    return data 

def precision_recall(tp, fn, fp, tn):  #Calculate precision and recall 
    if (tp + fp) == 0:  
        precision = 0 
    else: 
        precision = tp/(tp + fp)
    if  (tp + fn) == 0: 
        recall = 0 
    else: 
        recall = tp/(tp + fn)
    return precision, recall 

def data_structure(data, section, x): #section is the selection of either labeled or naive 
    #Create dataframe
    df = pd.DataFrame(data, columns = (['title', 'batch_number', 'percent_x', 'precision','recall','accuracy'])) 
    df_type = df[df['title']== section].groupby('percent_x').agg(lambda x: list(x))

    return df_type[x] #x is any of the metric {'precision','recall','accuracy'}


def plot(df_section_metric, section, metric): 
    x_data = ['0%', '10%', '30%', '50%', '70%', '90%'] 
    y_data = df_section_metric.values.tolist()

    n = len(x_data) #number of boxes 
    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, n)] #generate 6 colors 

    fig = go.Figure()

    for xd, yd, cls in zip(x_data, y_data, c):
        fig.add_trace(go.Box(
            y=yd,
            name=xd,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=cls,
            marker_size=2,
            line_width=1)
        )

    fig.update_layout(
           # y_axis = metric, 
           # x_axis = "labels remaining",
            title = "XGBoost" + " " + section + " " + metric, 
            paper_bgcolor='rgb(233,233,233)',
            plot_bgcolor='rgb(233,233,233)',
    )

    fig.show()
"""
MAIN FUNCTION 
"""
data = file_extraction(read_file())
metric = ['precision', 'recall', 'accuracy']
#section = ['Naive', 'Labeled'] #RF 
section = ['Labeled']   #XG 

## PLUG N PLAY for different metric, section & model 
df_section_metric = data_structure(data, section[0], metric[2]) 
plot(df_section_metric, section[0], metric[2])
#print("Random Forest Naive")
#print("XGBoost")

