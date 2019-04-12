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

def precision(m1, m2, n, m):
    match=0
    for i in range(n):
        for j in range(m):
            if(m1[i]==m2[j]):
                match+=1
    return (match/m)



nusers=int(input("Enter number of users : "))

t1=time.time()

nsongs=55*nusers
nrecc=50
nrecc1=3
data=np.zeros((nusers,nsongs))
datas=["\0" for x in range(nsongs)]
datau=["\0" for x in range(nusers)]

f=open("kaggle_visible_evaluation_triplets.txt","r")
currentuser=0
user=f.read(40)
prevuser=user
song=f.read(19).strip()
song
currentnsongs=0
print("finding top users....\n")
x=0
truedata=-1.*np.ones((20,nrecc1))
topusers=np.zeros(110000)
songsheard=0
while(currentuser<110000):
    if(user==prevuser):
        freq=int(f.readline().strip())
        songsheard+=1
        user=f.read(40)
        song=f.read(19).strip()
    else:
        topusers[currentuser]=songsheard
        currentuser+=1
        songsheard=1
        if(currentuser!=110000):
            freq=int(f.readline().strip())
            user=f.read(40)
            song=f.read(19).strip()
            prevuser=user

topusers=np.argpartition(topusers,-nusers)[-nusers:]
topusers=topusers[np.argsort(topusers)]
print("reading data....\n")
f=open("kaggle_visible_evaluation_triplets.txt","r")
currentuser=0
user=f.read(40)
prevuser=datau[0]=user
song=f.read(19).strip()
datas[0]=song
currentnsongs=0
si=0
ui=0

while(currentuser<=topusers[nusers-1]):
    if(user==prevuser):
        #ind=searchs(song,datas,currentnsongs)
        freq=int(f.readline().strip())
        
        if(currentuser==topusers[ui]):
            datau[ui]=user
            ind=searchs(song,datas,currentnsongs)
            if(ind==-1):
                ind=currentnsongs
                datas[ind]=song
                currentnsongs+=1
            #data[ui][ind]=freq
            if(x<nrecc1 and ui >= nusers-20 and ind!=currentnsongs-1):
                truedata[ui-nusers+19][x]=ind
                x+=1
            else:
                data[ui][ind]=freq
        
        user=f.read(40)
        song=f.read(19).strip()
    else:
        if(currentuser==topusers[ui]):
            ui+=1
        currentuser+=1
        prevuser=user
        x=0
        
print("Time taken:",round(time.time()-t1,3))

print("calculating recommendations....\n")

nsongs=currentnsongs+1
count=0
precisionsum=0
peoplehelped=0
for i in range(nusers):
    datacalc=np.zeros(nsongs)
    noMatch=10
    sim=np.zeros(nusers)
    for k in range(nusers):
        if(i!=k):
            sim[k]=calculateSimilarity(i,k,data)
    ind=np.argpartition(sim,-10)[-10:]
    for j in range(nsongs):
        if (data[i][j]==0):
            datacalc[j]=round(predict(ind,sim,noMatch,data,j),3)
    ind=np.argpartition(datacalc,-nrecc)[-nrecc:]
    ind=ind[np.nonzero(datacalc[ind])]
    if(ind.size>0):
        print("User",i," :  ",ind[np.argsort(-1*datacalc[ind])])
        count+=1
    if(i>=nusers-20):
        precisionsum+=(precision(ind[np.argsort(-1*datacalc[ind])],truedata[i-nusers+19],ind.size,nrecc1))
        peoplehelped+=1
    
print("MAP score = ",(precisionsum/peoplehelped))
print("Time taken:",round(time.time()-t1,3))
print("Number of recommendations made: ",count)
