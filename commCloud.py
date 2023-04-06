import konlpy
from konlpy.tag import Okt
from collections import Counter

from asd import comments
from wordcloud import WordCloud
import matplotlib.pyplot as plt

okt = Okt()
nouns = list()
for comment in comments:
    for noun in okt.nouns(comment[0]):
        if len(noun) > 1:
            nouns.append(noun)

count = Counter(nouns)
tags = count.most_common(50)    # 빈도 수 높은 상위 50개 단어 추출

wc = WordCloud(width=800, height=600, background_color='white', font_path='nanum-square-round/NanumSquareRoundB.ttf') # 본인 폰트 경로 기입하시면 됩니다.
cloud = wc.generate_from_frequencies(dict(tags))

plt.figure(figsize=(10, 8))
plt.axis('off')
plt.imshow(cloud)
plt.show()

