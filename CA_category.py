
#from fastapi import FastAPI
import pandas as pd


# app = FastAPI()
# @app.get("/CA_category")
def CA_category() :
    RO_df = pd.read_csv("RO_Data.csv", encoding='utf-8-sig')
    cafe_df = pd.read_csv("naver_cafe_Data.csv", encoding='utf-8-sig')
    ro_ca_df = pd.read_csv("CA_RO_Table.csv", encoding='utf-8-sig')

    sub_phenom_list = []
    big_phenom_list = []

    for i in range(ro_ca_df.shape[0]) :
        re_t = []
        t = ro_ca_df['ro_index'][i].replace('[' , '')
        t = t.replace(']','')
        t = t.split(' ')
        for j in range(len(t)):
            if t[j] != '' and t[j] != ' ' : 
                re_t.append(t[j])
        sub_phenom = RO_df.iloc[int(re_t[0])]['sub_phenom']
        sub_phenom_list.append(sub_phenom)
        big_phenom = RO_df.iloc[int(re_t[0])]['big_phenom']
        big_phenom_list.append(big_phenom)

    frequency_cafe_df = pd.DataFrame( {'sub_phenom' : sub_phenom_list, "big_phenom" : big_phenom_list} )

    graph = pd.Series(frequency_cafe_df['big_phenom']).value_counts()
    graph_df = pd.DataFrame(graph)
    graph_df = graph_df.sort_index()
    graph_df = graph_df.reset_index()
    graph_df = graph_df.rename(columns = {"big_phenom" : "big_phenom_count"})
    graph_df = graph_df.rename(columns = {"index" : "big_phenom"})

    graph_df=graph_df.sort_values(by=['big_phenom_count'], ascending=False)
    graph_df = graph_df.reset_index()
    graph_df = graph_df.drop(columns = 'index')
    print("graph_df : ",graph_df) # CA_bigcategory : DB저장

    big_category = ["부품 외관", "시트 작동불량 / 시트벨트_작동불량", "시트 작동 소음/이음", "작동 불량", "경고등 점등", "소음/이음", 
                "녹 발생", "진동", "냄새과다",  "조립문제", "사용/위치 불편","기타", "부품 도장", "도어 개폐불량", "기밀 불량" ]

    probability_list = []
    sub_category_count_list = []
    sub_category_list = []

    for b in big_category :
        try :
            big_category_label_count = int(graph_df[graph_df['big_phenom']==b]['big_phenom_count'])
        except :
            big_category_label_count = 0
    
        sub_category = frequency_cafe_df[frequency_cafe_df['big_phenom']==b]
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
    print("sub_category_df : ",sub_category_df)

    return {"1" : 1}

CA_category()