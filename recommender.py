import numpy as np
import pandas as pd
import math
import time

from numpy import genfromtxt

np.set_printoptions(threshold=np.inf)

def predict(ind,sim,noMatch,data,song):
    i=0#current index
    s=0#sum of similarities
    dotProd=0 
    prediction=0
    while(i<noMatch):
        if(data[ind[i]][song]>0):
            dotProd=dotProd+sim[ind[i]]*data[ind[i]][song]
            s=s+sim[ind[i]]
        i=i+1
    if(s!=0):
        prediction=dotProd/s
    return prediction

def calculateSimilarity(a,b,data):
	return np.dot(data[a],data[b])/math.sqrt( np.sum(np.square(data[a])) * np.sum(np.square(data[b])) )


def searchs(song,datas,nsongs):
    for i in range(nsongs):
        if(song==datas[i]):
            return i 
    return -1
    
def allzero(a,n):
	for i in range(n):
		if(a[i]!=0): 
			return 1
	return 0


nusers=int(input("How many users?:"))

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
    sim=np.zeros(nusers)
    for k in range(nusers):
        if(i!=k):
            sim[k]=calculateSimilarity(i,k,data)
    ind=np.argpartition(sim,-10)[-10:]
    for j in range(nsongs):
        if (data[i][j]==0):
            datacalc[i][j]=round(predict(ind,sim,noMatch,data,j),3)

nrecc=4

print("Sorting data....\n")

print("printing data...")

count=0
for i in range(nusers):
	if(allzero(datacalc[i],nsongs)):
		dat=np.array(datacalc[i])
		ind=np.argpartition(dat,-nrecc)[-nrecc:]
		print(i,"\t : \t",ind[np.argsort(-1*dat[ind])],"\t",dat[ind[np.argsort(-1*dat[ind])]])
		count+=1
	
print("Time taken:",round(time.time()-t1,3))
print("Number of recommendations made: ",count)

