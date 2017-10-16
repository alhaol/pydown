
# coding: utf-8

# # This code download Youtube as mp4

# In[18]:


import youtube_dl
from tqdm import tqdm
import pandas as pd
import optparse
import os

List=['https://www.safaribooksonline.com/library/view/getting-started-with/9781788625531/video3_3.html']
Fold='Videos'
desc="""
This tool download video for a provided list of links in a csv file 
"""
parser = optparse.OptionParser(description=desc)
parser.add_option('--list', '-l',help='Enter csv file that has link of csv', dest='playlist', default="List.csv", action='store')
parser.add_option('--folder', '-f',help='Name of the folder', dest='FoldName', default="Videos", action='store')

(opts, args) = parser.parse_args()

List_path=opts.playlist
Fold=opts.FoldName

#Save the list locally
if not os.path.exists(Fold):
        os.makedirs(Fold)

URLs=pd.read_csv(List_path, header=None)[0].tolist()


# In[17]:





# # This code download Video List by providing link from any video source 

# In[43]:



os.chdir(Fold) #changing the drectory 

def VideoDownload(URLs):
    for i in tqdm(range(len(URLs))):
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(title)s.%(ext)s'})
        with ydl:
            result = ydl.extract_info(URLs[i],download=True)

VideoDownload(URLs)

os.chdir('../') #changing the drectory 


# In[22]:

