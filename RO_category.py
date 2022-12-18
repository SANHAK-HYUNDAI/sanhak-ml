#from fastapi import FastAPI
import pandas as pd

# app = FastAPI()
# @app.get("/RO_category")
def RO_category() :
    RO_df = pd.read_csv("RO_Data.csv", encoding='utf-8-sig')

    graph = pd.Series(RO_df['big_phenom']).value_counts()
    graph_df = pd.DataFrame(graph)
    graph_df = graph_df.sort_index()
    graph_df = graph_df.reset_index()
    graph_df = graph_df.rename(columns = {"big_phenom" : "big_phenom_count"})
    graph_df = graph_df.rename(columns = {"index" : "big_phenom"})

    graph_df=graph_df.sort_values(by=['big_phenom_count'], ascending=False)
    graph_df = graph_df.reset_index()
    graph_df = graph_df.drop(columns="index")
    print("graph_df : ",graph_df) # RO big_category : DB 저장

    probability_list = []
    sub_category_count_list = []
    sub_category_list = []

    big_category = ["부품 외관", "시트 작동불량 / 시트벨트_작동불량", "시트 작동 소음/이음", "작동 불량", "경고등 점등", "소음/이음", 
                "녹 발생", "진동", "냄새과다",  "조립문제", "사용/위치 불편","기타", "부품 도장", "도어 개폐불량", "기밀 불량" ]

    for b in big_category :
        big_category_label_count = int(graph_df[graph_df['big_phenom']==b]['big_phenom_count'])
    
        sub_category = RO_df[RO_df['big_phenom']==b]
        sub_category = pd.Series(sub_category['sub_phenom']).value_counts()
        sub_category_df = pd.DataFrame(sub_category)
        sub_category_df = sub_category_df.sort_index()
        sub_category_df = sub_category_df.reset_index()
        sub_category_df = sub_category_df.rename(columns = {"sub_phenom" : "sub_phenom_count"})
        sub_category_df = sub_category_df.rename(columns = {"index" : "sub_phenom"})
        for t in list(sub_category_df['sub_phenom_count']) :
            sub_category_count_list.append(t)
        for t in list(sub_category_df['sub_phenom']) :
            sub_category_list.append(t)
    
        for j in range(sub_category_df.shape[0]) :
            result = round(float(sub_category_df['sub_phenom_count'][j]/big_category_label_count)*100,2)
            probability_list.append(result)
    
    sub_category_df = pd.DataFrame()
    sub_category_df['sub_phenom'] = sub_category_list
    sub_category_df['sub_phenom_count'] = sub_category_count_list
    sub_category_df['sub_phenom_probability'] = probability_list
    sub_category_df = sub_category_df.sort_values(by=['sub_phenom_count'], ascending=False)
    sub_category_df = sub_category_df.reset_index()
    sub_category_df = sub_category_df.drop(columns = 'index')
    print("sub_category_df : " , sub_category_df) # RO sub_category : DB저장

    return {"1" : 1}

RO_category()