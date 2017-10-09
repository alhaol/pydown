
# coding: utf-8


import os 
import pandas as pd
from tqdm import tqdm
import time 
import subprocess
import optparse


desc="""
This tool download mp4 youtube videos to from yotubeplaylist
Name,ID,Folder:  Name is the file name, ID is the youtube unique ID adn Folder is the folder to save that video
"""
parser = optparse.OptionParser(description=desc)
parser.add_option('--playlist', '-p',help='Enter youtube playlist ID', dest='PlayListID', default="PLmNPvQr9Tf-ZSDLwOzxpvY-HrE0yv-8Fy", action='store')
parser.add_option('--folder', '-f',help='Name of the folder', dest='FoldName', default="Orange", action='store')
parser.add_option('--audio', '-a',help='Download Audio File', dest='AudioEnable', default="0", action='store')

(opts, args) = parser.parse_args()

List_ID=opts.PlayListID
Fold=opts.FoldName
Audio=int(opts.AudioEnable)



from bs4 import BeautifulSoup
from collections import namedtuple
import requests
 
"""This class extracts the urls and titles of a given youtube playlist"""
 
class PlayList:
	# name tuple to store outputs
    Video = namedtuple('Video', ['url', 'title'])
    
    def __init__(self, listurl):
        # get the html text
        self.__listurl = self.__makeUrl(listurl)
        htmldoc = requests.get(self.__listurl).text
        # parse the html
        soup = BeautifulSoup(htmldoc, 'html.parser')
        # get all the pl(aylist)-video-title-link(s):
        rawList = soup('a', {'class' : 'pl-video-title-link'})
        # there has to be at least 1 item in a playlist
        if len(rawList) < 1:
            raise ValueError('This might be either a private '                               'or an empty playlist.')
        else:
            # list of the raw hrefs and their anchor texts
            self.__rawList = [(x.get('href'), x.contents[0].strip())
                              for x in rawList]
 
 
    @property
    def playlist(self):
		# return the playlist as a list of named tuples
        return [PlayList.Video._make([self.__getVideoURL(x[0])] + [x[1]])
                for x in self.__rawList]
        
    def __getVideoURL(self, text):
		# helper function split extract url and add prefix
        url = text.split('&')[0]   
        url = 'https://www.youtube.com' + url
        return url
    
    def __makeUrl(self, text):
		# url validation and clean up
        if text.find('playlist?list') != -1:
            return text
        elif text.find('watch?v=') * text.find('list=') > 1:
            return self.__getListUrlfromVideoLink(text)
        else:
            raise ValueError('Playlist ID not found in URL.')
 
 
    def __getListUrlfromVideoLink(self, text):
		# helper function as its name implies
        return r'''https://www.youtube.com/playlist?''' +                [x for x in text.split('&')
                if x.startswith('list=')][0]


# In[2]:


import pandas as pd

Common='https://www.youtube.com/watch?v=HXjnDIgGDuI&list='
listurl=Common+List_ID
List =PlayList(listurl)





# In[3]:


Name=[]
ID=[]
for i in range(len(List.playlist)):
    ID.append(List.playlist[i].url.split('?v=')[1])
    Name.append(List.playlist[i].title)

for i in range(0,len(Name)):
    if i+1<10:
        Name[i]='0'+str(i+1)+'_'+Name[i]
    else:
        Name[i]=str(i+1)+'_'+Name[i]
DF=pd.DataFrame({'Name':Name,'ID':ID})
DF['Fold']=Fold
DF['Audio']=Audio


# In[4]:



from pytube import YouTube

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
#All_Vid=pd.read_csv(Default_List)
All_Vid=DF
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
print('=====================End Downloading in {} minutes ===========================\n'.format(Req_time))

