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
if(nusers<=20):
    print("please enter a greater number.")
    exit()
t1=time.time()

nsongs=55*nusers
nrecc=50
nrecc1=3
data=np.zeros((nusers,nsongs))
datas=["\0" for x in range(nsongs)]
datau=["\0" for x in range(nusers)]

f=open("topusers.txt","r")
currentuser=0
user=f.read(40)
datau[0]=user
song=f.read(19).strip()
datas[0]=song
found=0
currentnsongs=0
print("reading data....\n")
x=0
truedata=np.zeros((20,nrecc1))
while(currentuser<nusers):
    if(user==datau[currentuser]):
        ind=searchs(song,datas,currentnsongs)
        freq=int(f.readline().strip())
        if(ind==-1):
            ind=currentnsongs
            datas[currentnsongs]=song
            currentnsongs+=1
        found=found+1
        if(x<nrecc1 and currentuser >= nusers-20 and ind!=currentnsongs-1):
            truedata[currentuser-nusers+19][x]=ind
            x+=1
        else:
            data[currentuser][ind]=freq
        user=f.read(40)
        song=f.read(19).strip()
    else:
        currentuser+=1
        x=0
        if(currentuser!=nusers):
            datau[currentuser]=user
nsongs=currentnsongs+1
datas=datas[0:nsongs]
data=data[0:nusers,0:nsongs]
print("Time taken:",round(time.time()-t1,3))

print("calculating recommendations....\n")

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
