import pandas
import os
from googleapiclient.discovery import build

api_key = os.environ.get('GOOGLE_API_KEY') #코드상에서 키를 숨기기위해 환경변수를 이용하여 GOOGLE_API_KEY라는 변수안에 키를 담아둔 후 호출.
 
comments = list()
api_obj = build('youtube', 'v3', developerKey=api_key)

while True:
    try:
        video_id = input("동영상 ID를 입력하세요: ")
        response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()
        break
    except:
        print("존재하지 않는 동영상입니다. 다시 입력해주세요.")

def video_info(): # video의 정보들 뽑아내는 함수.
    response = api_obj.videos().list(
        part='snippet,statistics,contentDetails,id',
        id=video_id
    ).execute() # 서버로 api 요청

    for item in response['items']: #for 루프를 사용하여 딕셔너리 형태로 저장된 정보에 접근
        print("제목:", item['snippet']['title']+"\n")
        print("조회수:", item['statistics']['viewCount']+"\n")
        print("설명:", item['snippet']['description']+"\n")
        print("채널명:", item['snippet']['channelTitle']+"\n")


while response:  # 댓글이 다음페이지에도 있다면 계속 돌리고 , 이제 없으면 break
    for item in response['items']: # items(댓글데이터)를 받아서 comments list에 추가
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append([comment['textDisplay']])
 
    if 'nextPageToken' in response: #댓글이 다음페이지에 있다면 넘겨서 댓글을 더 가져옴.
        response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
    else:
        break
 
for i in comments:
    print(i)

video_info()