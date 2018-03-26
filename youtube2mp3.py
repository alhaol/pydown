
from __future__ import unicode_literals
import youtube_dl


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=E7kRQAy9tho'])


# ffmpeg -i Name.mp4 Name.mp3 -n

# This will download an audio file if possible/supported. 
# If the file is not mp3 already, the downloaded file be converted 
# to mp3 using ffmpeg or avconv. For more information, 
# refer to the format and postprocessors documentation entries 
# in a current version of youtube-dl
