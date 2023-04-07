import konlpy
from konlpy.tag import Okt       
from collections import Counter 
from youtube import YoutubeAPI   
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Cloud(YoutubeAPI):
    def __init__(self):
        super().__init__()
        super()._get_comment_list()

    def execute(self):
        self.__morpheme_analysis()

    def __morpheme_analysis(self):
        okt = Okt()
        nouns = list()             
        for comment in self.comments:
            for noun in okt.nouns(comment[0]):
                if len(noun) > 1:      
                    nouns.append(noun)

        count = Counter(nouns)       
        tags = count.most_common(50) 
        self.__generate_wordCloud(tags)

    def __generate_wordCloud(self,tags):
        wc = WordCloud(width=800, height=600, background_color='white', font_path='font/NanumSquareRoundB.ttf')   
        cloud = wc.generate_from_frequencies(dict(tags))

        plt.figure(figsize=(10, 8))     
        plt.axis('off')                  
        plt.imshow(cloud)            
        plt.show()               

