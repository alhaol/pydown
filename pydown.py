
from pytube import YouTube
import os 
import pandas as pd
from tqdm import tqdm
import time 

import optparse

desc="""
This tool download mp4 youtube videos to a spcific folder with a specific name given in List.csv
Name,ID,Folder:  Name is the file name, ID is the youtube unique ID adn Folder is the folder to save that video
"""
parser = optparse.OptionParser(description=desc)
parser.add_option('--list', '-l',help='File that have the list of files', dest='List', default="List.csv", action='store')
(opts, args) = parser.parse_args()


Default_List=opts.List


def DownloadLink(yt,name,fold): 
    comm='http://www.youtube.com/watch?v='
    yt = YouTube(comm+yt)
    yt.set_filename(name)

    try: 
        video = yt.get('mp4')
        print ('Format is mp4')
    except:
        try:
            video = yt.get('mp4','720p')
            print ('Format mp4/720p')
        except:
            try:
                video = yt.get('mp4','360p')
                print ('Format mp4/360p')
            except:
                print ("No mp4 720 or 360 Available")
    try:
        video.download(fold+'/')
        print (yt.filename+'.mp4 was downloaded successfully to {}'.foramt(fold))
        print('================================================\n')
    except:
        print(yt.filename+" Already Downloaded")
        print('================================================\n')


def DownloadAll(DF):
    for i in range(len(DF)):
        Name=DF.Name[i]
        ID=DF.ID[i]
        Fold=DF.Fold[i]
        DownloadLink(ID,Name,Fold)
        

def Working(x):
    print('\nWorking on {} .....'.format(x))


def DownloadLink(yt,name,fold): 
    comm='http://www.youtube.com/watch?v='
    yt = YouTube(comm+yt)
    yt.set_filename(name)

    try: 
        video = yt.get('mp4')
        print ('Format is mp4')
    except:
        try:
            video = yt.get('mp4','720p')
            print ('Format mp4/720p')
        except:
            try:
                video = yt.get('mp4','360p')
                print ('Format mp4/360p')
            except:
                print ("No mp4 720 or 360 Available")
    try:
        video.download(fold+'/',on_progress=Working(name))
        print (yt.filename+'.mp4 was downloaded successfully to {}'.foramt(fold))
        print('================================================\n')
    except:
        print(yt.filename+" Already Downloaded")
        print('================================================\n')


def DownloadAll(DF):
    for i in tqdm(range(len(DF))):
        Name=DF.Name[i]
        ID=DF.ID[i]
        Fold=DF.Fold[i]
        DownloadLink(ID,Name,Fold)
                   


# In[ ]:

# Import the list 
All_Vid=pd.read_csv(Default_List)
def CleanName(x):
    x=x.replace(' ','_').replace(':','_').replace('|','_').replace('?','')
    return x
All_Vid.Name=All_Vid.Name.apply(CleanName)

# Create Folders 
for foldName in All_Vid.Fold.tolist():
    if not os.path.exists(foldName):
        os.makedirs(foldName)

# Download all videos in the list 
Start_time=time.time()
print('=====================Start Downloading ===========================\n')
DownloadAll(All_Vid)

Req_time=round ((time.time()-Start_time)/60)
print('=====================End Downloading in {} min===========================\n'.format(Req_time))







