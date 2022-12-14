#from fastapi import FastAPI
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt
from PIL import Image
import numpy as np
import pandas as pd

# app = FastAPI()
# @app.get("/RO_wordcloud")
def RO_wordcloud() :
    RO_df = pd.read_csv("RO_Data.csv", encoding='utf-8-sig')

    text = ''
    for i in range(RO_df.shape[0]) :
        text+=RO_df['special_note'][i]

    okt = Okt()
    nouns = okt.nouns(text) # 명사만 추출

    words = [n for n in nouns if len(n) > 1] # 단어의 길이가 1개인 것은 제외
    words_processing  = words

    for j in range(len(words)-1):
        try :

            if words[j] == '전' and words[j+1] == '좌석':
                words_processing.pop(j)
                words_processing.insert(j,'전좌석')
                words_processing.pop(j+1)
                j=j+1
        
            if words[j] == '보조' and words[j+1] == '석':
                words_processing.pop(j)
                words_processing.insert(j,'보조석')
                words_processing.pop(j+1)
                j=j+1
        
            if words[j] == '운전' and words[j+1] == '석':
                words_processing.pop(j)
                words_processing.insert(j,'운전석')
                words_processing.pop(j+1)
                j=j+1
            
            if words[j] == '조' and words[j+1] == '수석':
                words_processing.pop(j)
                words_processing.insert(j,'조수석')
                words_processing.pop(j+1)
                j=j+1
            
            if words[j] == '수석':
                words_processing.pop(j)
                words_processing.insert(j,'조수석')
                words_processing.pop(j+1)
                j=j+1
        
        except :
            break

    c = Counter(words_processing) # 단어별 빈도수 형태의 딕셔너리 데이터 : DB저장 
    print("c : " , c)

    return {"1" : 1}

RO_wordcloud()