import pandas
import os
from googleapiclient.discovery import build

    
class YoutubeAPI:
    def __init__(self):
        self.__api_key = os.environ.get('GOOGLE_API_KEY')
        self.__api_obj = build('youtube', 'v3', developerKey=self.__api_key)
        self.__video_id=""
        self.comments = list()

    def _get_comment_list(self):
        while True:
            try:
                self.video_id = input("동영상 ID를 입력하세요: ")
                responseComment = self.__api_obj.commentThreads().list(part='snippet', videoId=self.video_id, maxResults=100).execute()        
                break
            except:
                print("존재하지 않는 동영상입니다. 다시 입력해주세요.") 
        self.__request_api(responseComment) 

    def __request_api(self,responseComment):
        response = self.__api_obj.videos().list(
        part='snippet,statistics',
        id=self.video_id
        ).execute() 
        self.__print_info(response)
        self.__print_comment(responseComment)
        
    
    def __print_info(self,response):
        for item in response['items']: 
            print("제목:", item['snippet']['title']+"\n")
            print("조회수:", item['statistics']['viewCount']+"\n")
            print("설명:", item['snippet']['description']+"\n")
            print("채널명:", item['snippet']['channelTitle']+"\n")

    def __print_comment(self,responseComment):
        while responseComment:  
            for item in responseComment['items']: 
                comment = item['snippet']['topLevelComment']['snippet']
                self.comments.append([comment['textDisplay']])
        
            if 'nextPageToken' in responseComment:
                responseComment = self.__api_obj.commentThreads().list(part='snippet', videoId=self.video_id, pageToken=responseComment['nextPageToken'], maxResults=100).execute()      
            else:
                break
 
        for i in self.comments:
            print(i)

