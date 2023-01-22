import pandas as pd
import numpy as np
import math
import sys


def topsis(f,w,im):
    data=pd.read_csv(f)
    # there should be 3 or more columns in the dataset
    if len(data.columns)<3:
        print("Error: data must contain three or more columns")
        quit()

    # There should be only numeric data
    curr=[]
    for i in data.columns:
        curr.append(i)
    curr.pop(0)
    for i in curr:
        if data[i].dtype!=np.int64 and data[i].dtype!=np.float64:
            sys.stdout.write("There is atleast one column with non-numeric data type.")
            sys.exit(0)

    # No. of weights, no. of impacts and no. of columns should be same
    if(len(data.columns)-1!=len(w) and len(w)!=len(im) and len(data.columns)!=len(im)):
        print("Error: Dimensions donot match. Cannot set a row with mismatched columns")
        quit()

    # Impacts can be only + or -
    for i in im:
        if i!='+' and i!='-':
            print("Error: '+' and '-' are accepted only")
            quit()
    
    #2. Removing the first column
    name=data.columns.values[0]
    # dataset=data.iloc[:,0]
    dataset=data.copy()
    data=data.iloc[: , 1:]
    #3. calculating RMS for each column and adding it to dataframe
    data.loc[len(data)] = 0
    for j in range(len(data.columns)):
        sum=0
        for i in range(len(data)):
            sum=sum+data.iloc[i,j]*data.iloc[i,j]
        data.iloc[len(data)-1,j]=math.sqrt(sum)
    # print(data)
    #4. Dividing each element by its RMS
    for j in range(len(data.columns)):
        for i in range(len(data)-1):
            data.iloc[i,j]=data.iloc[i,j]/data.iloc[(len(data)-1),j]
    # print(data)
    #5. Multiplying by weights
    for i in range(len(w)):
        data.iloc[0:len(data)-1,i]=data.iloc[0:len(data)-1,i].apply(lambda x: x*float(w[i]))
    # print(data)
    # 6. find ideal best and ideal worst
    data=data.iloc[:-1 , :]
    best=[]
    worst=[]
    for j in range(len(im)):
        if im[j]=='+':
            best.append(data.iloc[:,j].max())
            worst.append(data.iloc[:,j].min())
        else:
            best.append(data.iloc[:,j].min())
            worst.append(data.iloc[:,j].max())
    data.loc[len(data)]=best
    data.loc[len(data)]=worst
    # print(data)
    # 7.calculating euclidean distance
    best_dist=[]
    worst_dist=[]
    for i in range(len(data)-2):
        tot1=0
        tot2=0
        for j in range(len(data.columns)):
            tot1=tot1+math.pow((data.iloc[i,j]-data.iloc[len(data)-2,j]),2)
            tot2=tot2+math.pow((data.iloc[i,j]-data.iloc[len(data)-1,j]),2)
        best_dist.append(math.sqrt(tot1))
        worst_dist.append(math.sqrt(tot2))
    best_dist.append(0)
    best_dist.append(0)
    worst_dist.append(0)
    worst_dist.append(0)
    data['best_dist']=best_dist
    data['worst_dist']=worst_dist
    # print(data)
    # 8. Topsis Score
    per=[]
    for i in range(len(data)-2):
        neg=data.iloc[i,len(data.columns)-1]
        pos=data.iloc[i,len(data.columns)-2]
        per.append(neg/(neg+pos))
    dataset['Topsis Score']=per
    data=data.iloc[:-1 , :]
    data=data.iloc[:-1 , :]
    # print(data)
    # 9. Rank
    dataset=dataset.sort_values(by='Topsis Score',ascending=False)
    # print(data)
    rank=[]
    for i in range(len(data)):
        rank.append(i+1)
    dataset['Rank']=rank
    # print(data)
    # 10. Returning output
    data.drop(['best_dist','worst_dist'],axis=1,inplace=True)
    dataset=dataset.sort_index()
    # print(dataset)
    return dataset
    # dataset.to_csv(sys.argv[4],index=False)



