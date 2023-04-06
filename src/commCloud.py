'''
YouTube 영상의 댓글 데이터를 가져와서, 명사만 추출하여 wordcloud로 시각화하기
'''

import konlpy
from konlpy.tag import Okt          # 한글 텍스트 처리 및 형태소 분석기
from collections import Counter     # 빈도수 계산
from youtube import comments            # asd.py 파일에서 comments 리스트 불러오기
from wordcloud import WordCloud
import matplotlib.pyplot as plt

okt = Okt()
nouns = list()      # 명사 추출 후 담을 빈 리스트 생성
for comment in comments:
    for noun in okt.nouns(comment[0]):
        if len(noun) > 1:   # 명사의 길이가 1보다 작은 경우 리스트에 append하지 않음
            nouns.append(noun)

count = Counter(nouns)          # 명사의 빈도 수 계산
tags = count.most_common(50)    # 빈도 수가 높은 50개의 명사를 리스트에 저장

# 단어구름 생성
wc = WordCloud(width=800, height=600, background_color='white', font_path='font/NanumSquareRoundB.ttf')   # 사용할 폰트 경로 기입
cloud = wc.generate_from_frequencies(dict(tags))

plt.figure(figsize=(10, 8))     # 출력할 크기
plt.axis('off')
plt.imshow(cloud)             # 생성된 단어구름 출력
plt.show()

