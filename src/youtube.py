import pandas
import os
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

api_key = os.environ.get('GOOGLE_API_KEY') #코드상에서 키를 숨기기위해 환경변수를 이용하여 GOOGLE_API_KEY라는 변수안에 키를 담아둔 후 호출.
<<<<<<< HEAD
video_id = str(input("동영상 ID를 입력하세요: ")) 
=======
>>>>>>> 58767a0790bea09d5335fae10067c9dbeec60843
 
comments = list()
api_obj = build('youtube', 'v3', developerKey=api_key)
#build 함수를 통해 Google API 클라이언트에서 지원하는 서비스를 사용할 수 있는 API 서비스 객체를 생성
#build 함수를 실행시키기 위해 API 서비스의 이름, API의 버전, 필요한 인증정보 제공

while True:
    try:
        video_id = input("동영상 ID를 입력하세요: ")
        response = api_obj.commentThreads().list(part='snippet', videoId=video_id, maxResults=100).execute()
        #commentThreads : 특정 동영상에 연결된 댓글 스레드(thread) 목록을 검색하는 데 사용
        #위 코드에서 part 매개변수는 API 응답에 포함되어야 할 리소스의 일부를 지정합니다. 
        #여기서는 댓글 스레드와 관련된 정보를 모두 포함하도록 snippet으로 설정하였습니다. 
        #replies는 해당 댓글 스레드에 포함된 모든 댓글과 답글 목록을 가져올 수 있다. 댓글의 대댓글은 불필요하므로 지웠습니다!
        #videoId 매개변수는 검색하려는 동영상의 ID를 지정합니다.
        #commentThreads() 함수의 반환값은 JSON 형식으로 제공되며, 검색된 댓글 스레드 목록을 포함합니다. 반환된 JSON에서 필요한 정보를 추출하여 사용할 수 있습니다.
        break
    except:
        print("존재하지 않는 동영상입니다. 다시 입력해주세요.")

def video_info(): # video의 정보들 뽑아내는 함수.
    response = api_obj.videos().list(
        part='snippet,statistics',
        id=video_id
    ).execute() # 서버로 api 요청
    #statistics : 동영상의 통계 정보 요청시 사용, 영상의 조회수, 좋아요 수, 싫어요 수 등의 정보 포함
    #contentDetails : 동영상의 콘텐츠 상세 정보를 요청시 사용, 동영상의 길이, 해상도, 썸네일 URL 등의 정보 포함
    #id : 동영상의 ID를 요청할 때 사용

    for item in response['items']: #for 루프를 사용하여 딕셔너리 형태로 저장된 정보에 접근
        print("제목:", item['snippet']['title']+"\n")
        print("조회수:", item['statistics']['viewCount']+"\n")
        print("설명:", item['snippet']['description']+"\n")
        print("채널명:", item['snippet']['channelTitle']+"\n")


while response:  # 댓글이 다음페이지에도 있다면 계속 돌리고 , 이제 없으면 break
    for item in response['items']: # items(댓글데이터)를 받아서 comments list에 추가
        comment = item['snippet']['topLevelComment']['snippet']
        #topLevelComment : 해당 동영상의 최상위 댓글을 나타내는 객체로 객체 안에 댓글 작성자, 댓글 내용, 작성 시간 등의 정보가 담김
        comments.append([BeautifulSoup(comment['textDisplay'],"lxml").text])
        #textDisplay : 댓글 작성자가 본문에 HTML 태그를 사용한 경우, 
        # textDisplay 속성에는 HTML 태그가 포함되지 않은 일반 텍스트 형식으로 반환된다.
        #만약 <p>This video is amazing!</p> 이런 태그가 있다면 p태그를 적용시킨 댓글만을 반환한다.
        #하지만 일부 댓글에는 HTML 태그가 포함될 수 있고, 이를 제거하기 위해서는 
    if 'nextPageToken' in response: #댓글이 다음페이지에 있다면 넘겨서 댓글을 더 가져옴.
        response = api_obj.commentThreads().list(part='snippet', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
        #기본적으로 API는 한 번에 최대 100개의 댓글 스레드를 반환한다. 
        # 만약 전체 댓글 스레드가 100개 이상이라면, PageToken매개변수를 사용하여 다음 페이지의 결과를 요청해야함
        #nextPageToken은 이전 페이지에서 반환된 마지막 댓글 스레드의 토큰입니다. 
        # 이 토큰을 pageToken 매개변수에 지정하여 다음 페이지를 요청하면 됩니다.
        #commentThreads API에서 maxResults 매개변수는 한 페이지에 반환할 최대 결과 수를 나타냅니다.
        #기본값으로는 20이 설정되어 있지만, 최대 100까지 설정할 수 있습니다.
        #반환되는 댓글 쓰레드가 100개 미만이라면 nextPageToken이 null값을 가진다.

    else:
        break

video_info()

for i in comments:
    print(i)

