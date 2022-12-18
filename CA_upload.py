#from fastapi import FastAPI
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re 
from hanspell import spell_checker
import nltk
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer


# app = FastAPI()
# @app.get("/CA_upload")
def CA_upload() :
    # 기존의 RO_CA mapping된 데이터
    RO_CA_df = pd.read_csv("CA_RO_TABLE.csv", encoding='utf-8-sig')

    CA_df = pd.read_csv("naver_cafe_Data_test.csv", encoding='utf-8-sig')
    CA_df_number = CA_df.shape[0]
    print("CA_df_number : ",CA_df_number)

    stop_words_github = pd.read_csv('https://raw.githubusercontent.com/cranberryai/todak_todak_python/master/machine_learning_text/clean_korean_documents/korean_stopwords.txt', header=None)
    stop_words_github[0] = stop_words_github[0].apply(lambda x: x.strip())
    stopwords = stop_words_github[0].to_numpy()
    nltk.download('punkt')

    if CA_df_number >= 2207 :
        for i in range(2206,CA_df_number) :
            try :
                # html태그 제거
                result = BeautifulSoup(CA_df['content'][i], 'html.parser').text
                CA_df['content'][i] = result
        
              # 특수기호 제거
                result = re.sub(r'[^ ㄱ-ㅣ가-힣]', '',CA_df['content'][i])
                CA_df['content'][i] = result

                # 고장/불량과 관련없는 사용자 정의 단어 제거
                if ( "투표" in CA_df['content'][i] or "추천" in CA_df['content'][i] or "색상" in CA_df['content'][i]  
                or "할인" in CA_df['content'][i] or "이벤트" in CA_df['content'][i] or "#일산썬팅" in CA_df['content'][i] 
                or "인천 실내크리닝 전문 제로맥스입니다" in CA_df['content'][i] or "TJ모터스" in CA_df['content'][i] 
                or "촬영팀입니다" in CA_df['content'][i] or "오닉스코리아 인천점입니다" in CA_df['content'][i] 
                or "#대구" in CA_df['content'][i] or "비바아우토" in CA_df['content'][i] or "비터스윗" in CA_df['content'][i]
                or "구매 링크" in CA_df['content'][i] or "모드개러지" in CA_df['content'][i] 
                or "카핏 김포본점" in CA_df['content'][i] or "로펌 법무법인" in CA_df['content'][i] 
                or "공구장 입니다" in CA_df['content'][i] or  "인천 모터스 맥스카입니다" in CA_df['content'][i] 
                or  "라인튜닝" in CA_df['content'][i] or "카스페이스 소사역곡점입니다" in CA_df['content'][i]
                or "두꺼비입니다" in CA_df['content'][i] or "모터스테이션입니다" in CA_df['content'][i] ):
                    CA_df = CA_df.drop(index = i , axis = 0)

                # py-hansell 맞춤법 검사
                spelled_sent = spell_checker.check(CA_df['content'][i])
                hanspell_sent = spelled_sent.checked
                CA_df['content'][i] = hanspell_sent
        
                # 불용어 제거
                clean_words=[]
                for word in nltk.tokenize.word_tokenize(CA_df['content'][i]) :
                    if word not in stopwords: #불용어 제거
                        clean_words.append(word)
                        result = ' '.join(clean_words)
                        CA_df['content'][i] = result
    
                result = CA_df['content'][i]
                if 'ㅜ' in CA_df['content'][i] :
                    result = result.replace('ㅜ','')
                if 'ㅠ' in CA_df['content'][i] :
                    result = result.replace('ㅠ','')
                if 'ᅲ' in CA_df['content'][i] :
                    result = result.replace('ᅲ','')
                if 'ㅎ' in CA_df['content'][i] :
                    result = result.replace('ㅎ','')
                if 'ㅋ' in CA_df['content'][i] :
                    result = result.replace('ㅋ','')
                if 'ㅡ' in CA_df['content'][i] :
                    result = result.replace('ㅡ','')
                if 'ᄒ' in CA_df['content'][i] :
                    result = result.replace('ᄒ','')
                if 'ᅮ' in CA_df['content'][i] :
                    result = result.replace('ᅮ','')
                if 'ㅅ' in CA_df['content'][i] :
                    result = result.replace('ㅅ','')
                if 'ㅇ' in CA_df['content'][i] :
                    result = result.replace('ㅇ','')
                if 'ㄱ' in CA_df['content'][i] :
                    result = result.replace('ㄱ','')
                if 'ᅳ' in CA_df['content'][i] :
                    result = result.replace('ᅳ','')
                if 'ᄏ' in CA_df['content'][i] :
                    result = result.replace('ᄏ','')
                if 'ㄷ' in CA_df['content'][i] :
                    result = result.replace('ㄷ','')
                if 'ㅂ' in CA_df['content'][i] :
                    result = result.replace('ㅂ','')
                if '안녕하세요' in CA_df['content'][i] :
                    result = result.replace('안녕하세요','')
                if '다름이 아니라' in CA_df['content'][i] :
                    result = result.replace('다름이 아니라','')
                if '다름이' in CA_df['content'][i] :
                    result = result.replace('다름이','')
                if '안녕하신가요' in CA_df['content'][i] :
                    result = result.replace('안녕하신가요','')
                if '안녕하십니까' in CA_df['content'][i] :
                    result = result.replace('안녕하십니까','')
                if '안녕하시고' in CA_df['content'][i] :
                    result = result.replace('안녕하시고','')
        
                CA_df['content'][i] = result
        
                # 짧은 문장 제거
                if len(CA_df['content'][i]) < 20 :
                    CA_df = CA_df.drop(index = i , axis = 0)
            
            except :
                print("not" , i)

        CA_df.reset_index(inplace=True)
        CA_df = CA_df.drop(columns="index")
        CA_df = CA_df.drop(columns="ca_id")
        CA_df.reset_index(inplace=True)
        CA_df = CA_df.rename(columns = {"index" : "ca_id"})
        print("CA_df_number : ",CA_df.shape[0])

        # keyword 추출 과정
        model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens') #SBERT 모델 불러오기
        okt = Okt() #형태소 분석

        basic_list=[]
        not_countvectorizer_list = [] 

        for i in range(2206, CA_df.shape[0]) :
            try : 
                tokenized_doc = okt.pos(CA_df['content'][i])
                tokenized_nouns = ' '.join([word[0] for word in tokenized_doc if word[1] == 'Noun']) # 명사만 추출
    
                test = tokenized_nouns.split(' ')
                preprocessing_test = test
    
                for j in range(len(test)-1):
                    try :

                        if test[j] == '전' and test[j+1] == '좌석':
                            preprocessing_test.pop(j)
                            preprocessing_test.insert(j,'전좌석')
                            preprocessing_test.pop(j+1)
                            j=j+1
        
                        if test[j] == '보조' and test[j+1] == '석':
                            preprocessing_test.pop(j)
                            preprocessing_test.insert(j,'보조석')
                            preprocessing_test.pop(j+1)
                            j=j+1
        
                        if test[j] == '운전' and test[j+1] == '석':
                            preprocessing_test.pop(j)
                            preprocessing_test.insert(j,'운전석')
                            preprocessing_test.pop(j+1)
                            j=j+1
            
                        if test[j] == '조' and test[j+1] == '수석':
                            preprocessing_test.pop(j)
                            preprocessing_test.insert(j,'조수석')
                            preprocessing_test.pop(j+1)
                            j=j+1
            
                        if test[j] == '수석':
                            preprocessing_test.pop(j)
                            preprocessing_test.insert(j,'조수석')
                            preprocessing_test.pop(j+1)
                            j=j+1
        
                    except :
                        break
        
                tokenized_nouns = ' '.join(preprocessing_test)
                n_gram_range = (2, 3) # biagram #trigram 추출

                count = CountVectorizer(ngram_range=n_gram_range).fit([tokenized_nouns])
                candidates = count.get_feature_names_out()
    
                doc_embedding = model.encode([CA_df['content'][i]]) # encoding 수치화
                candidate_embeddings = model.encode(candidates) # 후보군 encoding 수치화
        
                top_n = 5
                distances = cosine_similarity(doc_embedding, candidate_embeddings)
                keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
                basic_list.append(keywords)

            except : 
                basic_list.append([])
                not_countvectorizer_list.append(i)
            
        tem_basic_list = list(CA_df['keywords'][:2206])
        tem_basic_list.extend(basic_list)
        
        CA_df['keywords'] = tem_basic_list
        CA_df = CA_df.drop(not_countvectorizer_list)
        CA_df = CA_df.drop(columns="ca_id")
        CA_df.reset_index(inplace = True)
        CA_df = CA_df.drop(columns="index")
        CA_df.reset_index(inplace = True)
        CA_df = CA_df.rename(columns = {"index" : "ca_id"})
        
        print("CA_df : " , CA_df)
    
        # 가장 상위 "현상" column mapping
        # 기존의 RO데이터 불러오기
        RO_df = pd.read_csv("RO_Data.csv",encoding='utf-8-sig')

        tfidf = TfidfVectorizer(ngram_range = (1, 5), min_df = 3,  max_df = 0.9 )

        RO_index = []
        CA_id = []

        for i in range(2206, CA_df.shape[0] ) :
            RO_df.loc[8496] = ['naver_cafe','naver_cafe','naver_cafe','naver_cafe','naver_cafe' ,'naver_cafe' ,'naver_cafe', 'naver_cafe' ,CA_df['content'][i],'naver_cafe' ,'naver_cafe' ,'naver_cafe' ,'naver_cafe']
            tfidf.fit(RO_df['special_note'])
            tfidf_matrix = tfidf.fit_transform(RO_df['special_note'])
            cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
            recommendation_need = cosine_sim[-1]
    
            #첫 번째 문서와 타 문서 간 유사도가 큰 순으로 정렬한 인덱스를 추출하되 자기 자신은 제외
            sorted_index = np.argsort(recommendation_need)[::-1]
            recommend_index= sorted_index[3:11]
            RO_index.append(recommend_index)
            CA_id.append(i)
    
        new_RO_index = pd.DataFrame()
        new_RO_index['ca_id'] = CA_id
        new_RO_index['ro_index'] = RO_index
    
        print("RO_CA_df" , RO_CA_df)

    return {"1" : 1}

CA_upload()