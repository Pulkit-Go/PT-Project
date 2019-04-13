import numpy as np
import pandas as pd
import math
import time
import scipy 
import sklearn

from numpy import genfromtxt
import warnings

from scipy.sparse import csr_matrix

from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing


np.set_printoptions(threshold=np.inf)


# Code starts here #  


def searchs(song,datas,nsongs):
    for i in range(nsongs):
        if(song==datas[i]):
            return i 
    return -1

def calculateSimilarity(a,b,data):
	return np.dot(data[a],data[b])/math.sqrt( np.sum(np.square(data[a])) * np.sum(np.square(data[b])) )

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


print("How many users?")
nusers=int(input())

t1=time.time()

nsongs=55*nusers
data=np.zeros((nusers,nsongs))
datas=["\0" for x in range(nsongs)]
datau=["\0" for x in range(nusers)]

f=open("topusers2000.txt","r")
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

nsongs=currentnsongs+1
datacalc=np.zeros((nusers,nsongs))

tdata=np.transpose(data)

SVD=TruncatedSVD(n_components=int(nusers/25),random_state=17)

matrix=SVD.fit_transform(tdata)

#print(matrix)

warnings.filterwarnings("ignore",category=RuntimeWarning)

corr=np.corrcoef(matrix)


nrecc=5
count=0


for i in range(nusers):
	count=0
	reccsong=["\0" for k in range(nrecc)]
	if(np.amax(data[i]>0)):
		songIndex = np.argmax(data[i])	
		corr_song=corr[songIndex]

		for j in range(nsongs):
			if(corr_song[j]>0.99 and corr_song[j]<1.00 and data[i][j]==0):
				if(count<nrecc):
					reccsong[count]=datas[j]
					count=count+1;	
					
		if(count==nrecc):
			print("User",i,":",reccsong)

print(round(time.time()-t1,3),"sec")
