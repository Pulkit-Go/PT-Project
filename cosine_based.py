import numpy as np
import pandas as pd
import math
import time

from numpy import genfromtxt

np.set_printoptions(threshold=np.inf)

# predict() - predicts the score for a given song and user using top 10 similar user's scores

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

# calculateSimilarity() - calculates similarity between two users a and b

def calculateSimilarity(a,b,data):
	return np.dot(data[a],data[b])/math.sqrt( np.sum(np.square(data[a])) * np.sum(np.square(data[b])) )

# searchs() - searches for a given song name in datas 
          # - return the index if found and -1 otherwise

def searchs(song,datas,nsongs):
    for i in range(nsongs):
        if(song==datas[i]):
            return i 
    return -1

# precision() - calculates the precision (i.e., to what extent there are similar values) in m1 and m2
def precision(m1, m2, n, m):
    match=0
    for i in range(n):
        for j in range(m):
            if(m1[i]==m2[j]):
                match+=1
    return (match/m)



nusers=int(input("Enter number of users : "))

if(nusers<=20):  # if we have less number of users, it is not possible to give good recommendations
    print("please enter a greater number.")
    exit()
t1=time.time()
nsongs=55*nusers # initialized with a safe value as we don't know the actual number of songs listened to
nrecc=50
nrecc1=3
data=np.zeros((nusers,nsongs))   # to store the number of times a user has heard a song
                                 # user represented by row number and song by column number
datas=["\0" for x in range(nsongs)]   # stores the name of all songs
datau=["\0" for x in range(nusers)]   # stores names of all users

f=open("topusers2000.txt","r")   

# topusers2000.txt contains data for top 2000 users in descending order of the number of songs they have listened to
# generated using findtopusers.py

currentuser=0    # current user we are scanning data for
user=f.read(40)
datau[0]=user
song=f.read(19).strip()
datas[0]=song
currentnsongs=0    # total songs we have come across
print("reading data....\n")
x=0
truedata=np.zeros((20,nrecc1))
while(currentuser<nusers):
    if(user==datau[currentuser]):
        ind=searchs(song,datas,currentnsongs)

        # if the song is found in the current array, we will update the number of times it has been listened to by the user
        # if it is not found, we create a new entr in datas and update the value at the correspomnding address

        freq=int(f.readline().strip())
        if(ind==-1):
            ind=currentnsongs
            datas[currentnsongs]=song
            currentnsongs+=1
        
        # we will mask nrecc1 number of songs from the data for the last 20 users for evaluation

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

# once we find the actual number of songs, we can remove the extra rows and columns

nsongs=currentnsongs+1
datas=datas[0:nsongs]
data=data[0:nusers,0:nsongs]

print("calculating recommendations....\n")

count=0
precisionsum=0
peoplehelped=0
for i in range(nusers):
    datacalc=np.zeros(nsongs)   # the data corresponding to each song we will calculate for user i
    noMatch=10  # the number of similar users we will find
    sim=np.zeros(nusers) # similarity of user i with each user k users
    for k in range(nusers):
        if(i!=k):    # this is done so that same users are given 0 similarity and not used in prediction
            sim[k]=calculateSimilarity(i,k,data)
    ind=np.argpartition(sim,-noMatch)[-noMatch:]   # indexes of top 10 similar users
    for j in range(nsongs):
        if (data[i][j]==0):
            datacalc[j]=round(predict(ind,sim,noMatch,data,j),3)
    ind=np.argpartition(datacalc,-nrecc)[-nrecc:]   #indexes of top nrecc songs
    ind=ind[np.nonzero(datacalc[ind])]   # eliminating songs with score 0
    if(ind.size>0):
        # printing song indexes in descending order of their score
        print("User",i," :  ",ind[np.argsort(-1*datacalc[ind])])   
        count+=1
    if(i>=nusers-20):
        # precision is calculated for last 20 users for whom some data was masked
        precisionsum+=(precision(ind[np.argsort(-1*datacalc[ind])],truedata[i-nusers+19],ind.size,nrecc1))
        peoplehelped+=1
    
print("MAP score = ",(precisionsum/peoplehelped))
print("Time taken:",round(time.time()-t1,3))
print("Number of recommendations made: ",count)
