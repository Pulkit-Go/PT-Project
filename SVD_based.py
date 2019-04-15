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

# searchs() - searches for a given song name in datas 
          # - return the index if found and -1 otherwise

def searchs(song,datas,nsongs):
    for i in range(nsongs):
        if(song==datas[i]):
            return i 
    return -1



nusers=int(input("Enter number of users : "))

t1=time.time()

nsongs=55*nusers    # initialized with a safe value as we don't know the actual number of songs listened to
data=np.zeros((nusers,nsongs))	# to store the number of times a user has heard a song
                                 # user represented by row number and song by column number
datas=["\0" for x in range(nsongs)]	# stores the name of all songs
datau=["\0" for x in range(nusers)]	# stores names of all users

f=open("topusers2000.txt","r")

# topusers2000.txt contains data for top 2000 users in descending order of the number of songs they have listened to
# generated using findtopusers.py

currentuser=0	 # current user we are scanning data for
user=f.read(40)
datau[0]=user
song=f.read(19).strip()
datas[0]=song
currentnsongs=0	# total songs we have come across
print("reading data....\n")
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
        data[currentuser][ind]=freq
        user=f.read(40)
        song=f.read(19).strip()
    else:
        currentuser+=1
        if(currentuser!=nusers):
            datau[currentuser]=user

# once we find the actual number of songs, we can remove the extra rows and columns

nsongs=currentnsongs+1
datas=datas[0:nsongs]
data=data[0:nusers,0:nsongs]

print("making suggestions...\n")

tdata=np.transpose(data)	#transpose of the matrix data

SVD=TruncatedSVD(n_components=int(nusers/25))	#performs singular value decomposition on the matrix with reduced dimension nusers/25

matrix=SVD.fit_transform(tdata)

warnings.filterwarnings("ignore",category=RuntimeWarning)	


corr=np.corrcoef(matrix)	# nsongs*nsongs matrix that contains correlation between each song


nrecc=50	#the number of recommendations we will make to each user
count=0	


for i in range(nusers):
	if(np.amax(data[i]>0)):		#we want to make recommendations only for the users who have rated at least 1 song
		songIndex = np.argmax(data[i])		#index of the most liked song by the user
		corr_song=corr[songIndex]		#correlation array which contains correlation of 
							#most liked song by the user with every other song
							
		ind=np.argsort(-1*corr_song)		#indices of most reated song to the most liked song by the user in decreasing order
		print("User",i,":",ind[0:nrecc])	

print(round(time.time()-t1,3),"sec")
