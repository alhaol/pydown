from pytube import YouTube
import os 
import pandas as pd

from tqdm import tqdm


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
                   
        


# In[192]:

All_Vid=pd.read_csv('List.csv')
def CleanName(x):
    x=x.replace(' ','_').replace(':','_').replace('|','_').replace('?','')
    return x
All_Vid.Name=All_Vid.Name.apply(CleanName)

# Create Folders 
for foldName in All_Vid.Fold.tolist():
    if not os.path.exists(foldName):
        os.makedirs(foldName)


# Download all videos 


print('================================================\n')
DownloadAll(All_Vid)






