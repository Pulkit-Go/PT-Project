import numpy as np
import pandas as pd
import math


from numpy import genfromtxt

np.set_printoptions(threshold=np.inf)

def predict(topMatch,data,song):
    i=0#current index
    s=0#sum of similarities
    dotProd=0 
    while(i<10 and topMatch[0][i]>0):
        dotProd=dotProd+topMatch[0][i]*data[topMatch[1][i],song]
        s=s+topMatch[0][i]
        i=i+1
    prediction=dotProd/s
    return prediction
    
def calculateSimilarity(a,b,data):
	return np.dot(data[a],data[b])/math.sqrt( np.sum(np.square(data[a])) * np.sum(np.square(data[b])) )

def match(user,s,noMatch,topMatch):
    for i in range(noMatch):
        if(s>topMatch[0][i]):
            topMatch[0][i]=s
            topMatch[1][i]=user
            break

#0 is considered as unrated
data = genfromtxt("dummyData.csv", delimiter=',')	#numpy 2D array stores data
                
nusers=data.shape[0]  #no. of users
nsongs=data.shape[1]   #no. of songs


datacalc=[[0 for x in range(nsongs)] for y in range(nusers)]    #calculated data
#datacalc=np.array(datac)

for i in range(nusers):
    #f=0  #flag: is similarity calculated??
    noMatch=10
    topMatch=[[0 for x in range(noMatch)] for y in range(2)]
    for k in range(nusers):
        s=calculateSimilarity(i,k,data)
        match(k,s,noMatch,topMatch)
    for j in range(nsongs):
        if (data[i][j]==0):
            
            
            avg=np.sum(data[i])/np.count_nonzero(data[i])
            datacalc[i][j]=round(predict(topMatch,data,j),3)

nrecc=5

dataSort=np.ones(shape=(nusers,nrecc+1))*-1



for i in range(0,nrecc+1):
	dataSort[0][i]=i



for i in range(1,nusers):
	dataSort[i][0]=i
	for j in range(1,nrecc+1):
		if(sorted(datacalc[i],reverse=True)[j-1]!=0):	
			dataSort[i][j]=datacalc[i].index(sorted(datacalc[i],reverse=True)[j-1])
		else:
			break
	
print(dataSort)
