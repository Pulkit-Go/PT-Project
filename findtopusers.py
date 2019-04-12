import numpy as np
import time

nusers=int(input("enter no. of users : "))
t1=time.time()
f=open("kaggle_visible_evaluation_triplets.txt","r")
currentuser=0
user=f.read(40)
prevuser=user
song=f.read(19).strip()
song
currentnsongs=0
print("finding top users....\n")
allusers=np.zeros(110000)
songsheard=0
while(currentuser<110000):
    if(user==prevuser):
        freq=int(f.readline().strip())
        songsheard+=1
        user=f.read(40)
        song=f.read(19).strip()
    else:
        allusers[currentuser]=songsheard
        currentuser+=1
        songsheard=1
        if(currentuser!=110000):
            freq=int(f.readline().strip())
            user=f.read(40)
            song=f.read(19).strip()
            prevuser=user

ind=np.argpartition(allusers,-nusers)[-nusers:]
print(ind)
topfreq=allusers[ind]
print(topfreq)
topusers=ind[np.argsort(-1*topfreq)]
print(topusers)
print(allusers[topusers])
print("reading data....\n")
j=open("topusers.txt","w")
si=0
ui=0
while(ui<nusers):
    f=open("kaggle_visible_evaluation_triplets.txt","r")
    currentuser=0
    user=f.read(40)
    prevuser=user
    song=f.read(19).strip()
    currentnsongs=0
    

    while(ui<nusers and currentuser<=topusers[ui]):
        if(user==prevuser):
            freq=f.readline().strip()
            
            if(currentuser==topusers[ui]):
                j.write(user)
                j.write("\t")
                j.write(song)
                j.write("\t")
                j.write(freq)
                j.write("\n")
            
            user=f.read(40)
            song=f.read(19).strip()
        else:
            if(currentuser==topusers[ui]):
                ui+=1
            currentuser+=1
            prevuser=user
            x=0
    f.close()
    print(ui)
j.close()
print(time.time()-t1)