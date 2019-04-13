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
        user=f.read(40)
        song=f.read(19).strip()
    else:
        currentuser+=1
        if(currentuser!=nusers):
            datau[currentuser]=user

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



tdata=np.transpose(data)

SVD=TruncatedSVD(n_components=int(nusers/25),random_state=17)

matrix=SVD.fit_transform(tdata)

warnings.filterwarnings("ignore",category=RuntimeWarning)

corr=np.corrcoef(matrix)


nrecc=6
count=0


for i in range(nusers):
	count=0
	reccsong=["\0" for k in range(nrecc)]
	if(np.amax(datacalc[i]>0)):
		songIndex = np.argmax(datacalc[i])	
		corr_song=corr[songIndex]

		for j in range(nsongs):
			if(corr_song[j]>0.999 and corr_song[j]<1 and data[i][j]==0):
				if(count<nrecc):
					reccsong[count]=datas[j]
					count=count+1;	
					
		if(count==nrecc):
			print("User",i,":",reccsong)

print(round(time.time()-t1,3),"sec")
