import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# 제목
st.title("📊 산업재해 통계 시각화 (2013–2023, 분류 기준 선택)")

# API 키
API_KEY = st.secrets["KOSIS_API_KEY"]

# 분류 기준 매핑 (objL1)
objL1_options = {
    "전체": "A01",
    "산업별": "A02",
    "규모별": "A03",
    "성별": "A04",
    "연령별": "A05",
    "직종별": "A06",
    "발생형태별": "A07",
    "기인물별": "A08",
    "작업지역*공정별": "A09",
    "작업내용별": "A10"
}

# 사용자 선택
selected_category_label = st.selectbox("📂 분류 기준 선택", list(objL1_options.keys()))
selected_objL1 = objL1_options[selected_category_label]

# API 호출 파라미터
URL = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
params = {
    "method": "getList",
    "apiKey": API_KEY,
    "itmId": "16118AAD6_15118AI8AA",  # 사고자수 총계
    "objL1": selected_objL1,
    "format": "json",
    "jsonVD": "Y",
    "prdSe": "Y",
    "startPrdDe": "2013",
    "endPrdDe": "2023",
    "orgId": "118",
    "tblId": "DT_11806_N000"
}

# API 요청
response = requests.get(URL, params=params)

try:
    data = response.json()
except ValueError:
    st.error("❌ API 응답 파싱 실패")
    st.stop()

if isinstance(data, list):
    df = pd.DataFrame(data)
    df = df[['PRD_DE', 'C1_NM', 'DT']]
    df['DT'] = pd.to_numeric(df['DT'], errors='coerce')
    
    # 연도 필터
    years = sorted(df['PRD_DE'].unique())
    selected_year = st.selectbox("📅 연도 선택", years, index=len(years)-1)

    # 해당 연도 필터링
    df_filtered = df[df['PRD_DE'] == selected_year]

    # 시각화
    fig = px.bar(df_filtered, x='C1_NM', y='DT',
                 text='DT',
                 labels={'C1_NM': selected_category_label, 'DT': '사고자 수'},
                 title=f"{selected_year}년 {selected_category_label}별 산업재해 통계")
    
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-30)

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("❌ API에서 잘못된 응답이 반환되었습니다.")
