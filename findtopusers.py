import numpy as np
import time
nusers=int(input("enter no. of users : "))
t1=time.time()
f=open("kaggle_visible_evaluation_triplets.txt","r")    #this is the file that contains actual user history
currentuser=0
user=f.read(40)
prevuser=user
song=f.read(19).strip()
currentnsongs=0
print("finding top users....\n")
allusers=np.zeros(110000)       #this array will finally contain total no. of songs listened to by each user
songsheard=0
while(currentuser<110000):
    freq=int(f.readline().strip())
    if(user==prevuser):
        songsheard+=1
    else:
        allusers[currentuser]=songsheard
        currentuser+=1
        songsheard=1
        if(currentuser==110000-1):
            break
        prevuser=user
    user=f.read(40)
    song=f.read(19).strip()

ind=np.argpartition(allusers,-nusers)[-nusers:]     #indices of top nusers
topusers=ind[np.argsort(-1*allusers[ind])]          #indices of top users in descending order of no. of songs heard
print("compiling file....\n")
j=open("topusers.txt","w")          
si=0        #current song index
ui=0        #current user index
while(ui<nusers):
    #we will read the file multiple times until we get all the required users
    f=open("kaggle_visible_evaluation_triplets.txt","r")
    currentuser=0
    user=f.read(40)
    prevuser=user
    song=f.read(19).strip()
    currentnsongs=0
    

    while(ui<nusers and currentuser<=topusers[ui]):
        #if our current user is the required top user, we write his history to the new file
        #otherwise we go to the next line and continue the process
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
j.close()
print("time taken=",round(time.time()-t1,3))