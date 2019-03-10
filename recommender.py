import numpy as np
import pandas as pd
import math


np.set_printoptions(threshold=np.inf)

def sum(row):
    s=[0,0]   #s[0] stores sum of elements and s[1] stores no. of non zero elements
    for i in row:
        s[0]=s[0]+i
        if i!=0:
            s[1]=s[1]+1
    return s

def normalize(data,nusers,nsongs):
    datan=[[0 for x in range(nsongs)] for y in range(nusers)]
    for i in range(nusers):
        s=sum(data[i])
        avg=s[0]/s[1]
        for j in range(nsongs):
            if(data[i][j]!=0):
                datan[i][j]=data[i][j]-avg
    return datan

def mod(i,nsongs):
    m=0
    for j in range(nsongs):
        m=m+datan[i][j]*datan[i][j]
    m=math.sqrt(m)
    return m

def calcSimilarity(datan,user,similarity,nusers,nsongs):
    for i in range(nusers):
        if(similarity[i][user]==0):
            dotProd=0
            for j in range(nsongs):
                dotProd=dotProd+datan[user][j]*datan[i][j]
            similarity[i][user]=similarity[user][i]=dotProd/(mod(i,nsongs)*mod(user,nsongs))
            

def findSimilarUsers(data, datan, nusers, similarity, user, song):
    topMatch=[[0 for x in range(10)] for y in range(2)] #1st row contains similarity and second contains song rating of corresponding user
    usedUsers=[0 for x in range(nusers)]
    for i in range(10):
        b=0  #current biggest similarity. we want only similarities>0 to be considered
        ind=0 #user index of current biggest entry
        f=0 #flag variable: does another similar user exist??
        for j in range(nusers):
            if(data[j][song]!=0 and similarity[user][j]>b and usedUsers[j]==0):
                b=similarity[user][j]
                ind=j
                f=1
        if(f==0):
            break
        usedUsers[ind]=1
        topMatch[0][i]=b
        topMatch[1][i]=datan[ind][song]
    return topMatch


def predict(topMatch):
    i=0#current index
    s=0#sum of similarities
    dotProd=0 
    while(i<10 and topMatch[0][i]>0):
        dotProd=dotProd+topMatch[0][i]*topMatch[1][i]
        s=s+topMatch[0][i]
        i=i+1
    prediction=dotProd/s
    return prediction


#0 is considered as unrated

data=pd.read_csv("dummyData.csv")    #input data
data=data.values

                 
                 
nusers=data.shape[0]  # no. of users
nsongs=data.shape[1]   #no. of songs


datan=normalize(data,nusers,nsongs) #normalized data set

similarity=[[0 for x in range(nusers)] for y in range(nusers)]

datacalc=[[0 for x in range(nsongs)] for y in range(nusers)]    #calculated data

for i in range(nusers):
    f=0  #flag: is similarity calculated??
    for j in range(nsongs):
        if (data[i][j]==0):
            if(f==0):
                calcSimilarity(datan,i,similarity,nusers,nsongs)
                f=1
            topMatch=findSimilarUsers(data,datan,nusers,similarity,i,j)
            s=sum(data[i])
            avg=s[0]/s[1]
            datacalc[i][j]=round(predict(topMatch)+avg,3)

nrecc=5

dataSort=np.zeros(shape=(nusers,nrecc+1))

for i in range(nusers):
	dataSort[i][0]=i
	for j in range(1,nrecc+1):
		if(max(datacalc[i])!=0):	
			dataSort[i][j]=datacalc[i].index(sorted(datacalc[i],reverse=True)[j-1])
		else:
			dataSort[i][j]=-1
	
print(dataSort)
