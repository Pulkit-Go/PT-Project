import numpy as np
import pandas as pd
import math
import time
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



nusers=int(input("Enter number of users : "))

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
        data[currentuser][ind]=freq
        user=f.read(40)
        song=f.read(19).strip()
    else:
        currentuser+=1
        if(currentuser!=nusers):
            datau[currentuser]=user

nsongs=currentnsongs+1
datas=datas[0:nsongs]
data=data[0:nusers,0:nsongs]

print("making suggestions...\n")

tdata=np.transpose(data)

SVD=TruncatedSVD(n_components=int(nusers/25))

matrix=SVD.fit_transform(tdata)

warnings.filterwarnings("ignore",category=RuntimeWarning)


corr=np.corrcoef(matrix)


nrecc=50
count=0


for i in range(nusers):
	reccsong=["\0" for k in range(nrecc)]
	if(np.amax(data[i]>0)):
		songIndex = np.argmax(data[i])	
		corr_song=corr[songIndex]
		ind=np.argsort(-1*corr_song)
		print("User",i,":",ind[0:nrecc])

print(round(time.time()-t1,3),"sec")
