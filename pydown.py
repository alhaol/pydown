
# coding: utf-8

# In[20]:


from pytube import YouTube
import os 
import pandas as pd
from tqdm import tqdm
import time 
import subprocess
import optparse

desc="""
This tool download mp4 youtube videos to a spcific folder with a specific name given in List.csv
Name,ID,Folder:  Name is the file name, ID is the youtube unique ID adn Folder is the folder to save that video
"""
parser = optparse.OptionParser(description=desc)
parser.add_option('--list', '-l',help='File that have the list of files', dest='List', default="List.csv", action='store')

(opts, args) = parser.parse_args()

Default_List=opts.List


def DownloadLink(yt,name,fold,audio): 
    comm='http://www.youtube.com/watch?v='
    yt = YouTube(comm+yt)
    yt.set_filename(name)
    os.chdir(fold) #changing the drectory 

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
        video.download('.',on_progress=Working(name))
        if audio==1:
            subprocess.call(['ffmpeg','-i',name+'.mp4',name+'.mp3','-n'])  
            print ('\n<<{0}.mp3>> was downloaded successfully to {1} \n'.format(name,fold))
        print ('\n<<{0}.mp4>> was downloaded successfully to {1} \n'.format(name,fold))
        print('================================================\n')
        
    except:
        
        if audio==1:
            FF=subprocess.call(['ffmpeg','-i',name+'.mp4',name+'.mp3','-n']) 
            if FF!=0:
                print ('\n<<{0}.mp3>> Already downloaded to {1} \n'.format(name,fold))
            else:
                print ('\n<<{0}.mp3>> was downloaded successfully to {1} \n'.format(name,fold))
        
        print ('\n<<{0}.mp4>> Already downloaded to {1} \n'.format(name,fold))
        
    
        print('================================================\n')

    os.chdir('../') #changing the drectory 


def DownloadAll(DF):
    for i in range(len(DF)):
        Name=DF.Name[i]
        ID=DF.ID[i]
        Fold=DF.Fold[i]
        DownloadLink(ID,Name,Fold)
        

def Working(x):
    print('\nWorking on {} .....'.format(x))



def DownloadAll(DF):
    for i in tqdm(range(len(DF))):
        Name=DF.Name[i]
        ID=DF.ID[i]
        Fold=DF.Fold[i]
        Audio=DF.Audio[i]
        DownloadLink(ID,Name,Fold,Audio)
                   


# In[21]:


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
print('=====================End Downloading in {} ===========================\n'.format(Req_time))

