import pandas
import os
from googleapiclient.discovery import build

api_key = os.environ.get('GOOGLE_API_KEY')
 
comments = list()
api_obj = build('youtube', 'v3', developerKey=api_key)
while True:
    try:
        video_id = input("동영상 ID를 입력하세요: ")
        response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()
        break
    except:
        print("존재하지 않는 동영상입니다. 다시 입력해주세요.")

def video_info():
    response = api_obj.videos().list(
        part='snippet,statistics,contentDetails,id',
        id=video_id
    ).execute()

    for item in response['items']:
        print("제목:", item['snippet']['title']+"\n")
        print("조회수:", item['statistics']['viewCount']+"\n")
        print("설명:", item['snippet']['description']+"\n")
        print("채널명:", item['snippet']['channelTitle']+"\n")


while response:
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append([comment['textDisplay']])
    
        if item['snippet']['totalReplyCount'] > 0:
            for reply_item in item['replies']['comments']:
                reply = reply_item['snippet']
                comments.append([reply['textDisplay']])
 
    if 'nextPageToken' in response:
        response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
    else:
        break
 
for i in comments:
    print(i)

video_info()