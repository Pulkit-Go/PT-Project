import numpy as np
import pandas as pd
import math
import time

from numpy import genfromtxt

np.set_printoptions(threshold=np.inf)

def predict(topMatch,data,song):
    i=0#current index
    s=0#sum of similarities
    dotProd=0 
    prediction=0
    while(i<10 and data[int(topMatch[1][i])][song]>0):
        dotProd=dotProd+topMatch[0][i]*data[int(topMatch[1][i])][song]
        s=s+topMatch[0][i]
        i=i+1
    if(s!=0):
        prediction=dotProd/s
    return prediction
    
def calculateSimilarity(a,b,data):
	return np.dot(data[a],data[b])/math.sqrt( np.sum(np.square(data[a])) * np.sum(np.square(data[b])) )

def match(user,s,noMatch,topMatch):
    smallest=2
    smallestIndex=-1
    for i in range(noMatch):
        if(topMatch[0][i]<smallest):
            smallest=topMatch[0][i]
            smallestIndex=i
    if(s>smallest):
        topMatch[0][smallestIndex]=s
        topMatch[1][smallestIndex]=user
def searchs(song,datas,nsongs):
    for i in range(nsongs):
        if(song==datas[i]):
            return i 
    return -1
    
def allzero(a,n):
	for i in range(n):
		if(a[i]!=0): 
			return 1;
	return 0;	


print("How many users?")
nusers=int(input())

t1=time.time()

nsongs=15*nusers
data=np.zeros((nusers,nsongs))
datas=["\0" for x in range(nsongs)]


datau=["\0" for x in range(nusers)]



f=open("kaggle_visible_evaluation_triplets.txt","r")
currentuser=0
user=f.read(40)
datau[0]=user
song=f.read(19).strip()
datas[0]=song
found=0
currentnsongs=0
print("reading data....\n")
while(currentuser<nusers):
    if(user==datau[currentuser]):
        
        ind=searchs(song,datas,currentnsongs)
        freq=int(f.readline().strip())
        if(ind==-1):
            ind=currentnsongs
            datas[currentnsongs]=song
            currentnsongs+=1
        found=found+1
        data[currentuser][ind]=freq
        #print(user,song,freq)
        user=f.read(40)
        song=f.read(19).strip()
    else:
        currentuser+=1
        if(currentuser!=nusers):
            datau[currentuser]=user
    

print("calculating recommendations....\n")
nsongs=currentnsongs+1
datacalc=np.zeros((nusers,nsongs))

for i in range(nusers):
    noMatch=10
    topMatch=np.zeros((2,noMatch))
    for k in range(nusers):
        if(i!=k):
            s=calculateSimilarity(i,k,data)
            match(k,s,noMatch,topMatch)
    for j in range(nsongs):
        if (data[i][j]==0):
            datacalc[i][j]=round(predict(topMatch,data,j),3)

nrecc=5

dataSort=np.ones(shape=(nusers,nrecc+1))*-1



print("Sorting data....\n")

print("printing data...")
'''
for i in range(nusers):np.argsort(
    for j in range(nsongs):
        if(datacalc[i][j]!=0):
            print(i,j,datacalc[i][j])'''

for i in range(nusers):
	if(allzero(datacalc[i],nsongs)):
		dat=np.array(datacalc[i])
		ind=np.argpartition(dat,-4)[-4:]
		print(i," : ",ind[np.argsort(-1*dat[ind])])
	
print("Time taken:",time.time()-t1)
