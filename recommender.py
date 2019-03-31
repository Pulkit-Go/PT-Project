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
    bot=0
    top=nsongs-1
    while(top>=bot):
        med=(top+bot)//2
        if(datas[med]>song):
            top=med-1
        elif(datas[med]<song):
            bot=med+1
        else:
            return med
    return -1

nusers=10000
nsongs=10000
data=[[0 for x in range(nsongs)] for y in range(nusers)]
datas=["\0" for x in range(nsongs)]

f=open("kaggle_songs.txt","r")
for i in range(nsongs):
    datas[i]=f.read(18)
    x=f.readline()

datau=["\0" for x in range(nusers)]


"""f=open("kaggle_users.txt","r")
for i in range(nsongs):
    datau[i]=f.readline().rstrip('\n')
"""
f=open("kaggle_visible_evaluation_triplets.txt","r")
currentuser=0
user=f.read(40)
datau[0]=user
found=0
while(currentuser<nusers):
    if(user==datau[currentuser]):
        song=f.read(19).strip()
        ind=searchs(song,datas,nsongs)
        freq=int(f.readline().strip())
        if(ind!=-1):
            data[currentuser][ind]=freq
            print(user,song,freq)
            found+=1
        user=f.read(40)
    else:
        currentuser+=1
        if(currentuser!=nusers):
            datau[currentuser]=user

print("found =",found)

#datacalc=[[0 for x in range(nsongs)] for y in range(nusers)]    #calculated data
#datacalc=np.array(datac)
"""
for i in range(nusers):
    noMatch=10
    topMatch=[[0 for x in range(noMatch)] for y in range(2)]
    for k in range(nusers):
        s=calculateSimilarity(i,k,data)
        match(k,s,noMatch,topMatch)
    for j in range(nsongs):
        if (data[i][j]==0):
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
"""
