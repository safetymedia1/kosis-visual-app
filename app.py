import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# 제목
st.title("📊 산업재해 통계 시각화 (성별 분류)")

# API 키
API_KEY = st.secrets["KOSIS_API_KEY"]

# API 호출 파라미터
URL = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
params = {
    "method": "getList",
    "apiKey": API_KEY,
    "itmId": "16118AAD6_15118AI8AA",  # 사고자수 총계
    "objL1": "A04",  # 성별
    "format": "json",
    "jsonVD": "Y",
    "prdSe": "Y",
    "startPrdDe": "2013",
    "endPrdDe": "2023",
    "orgId": "118",
    "tblId": "DT_11806_N002"  # 성별 분류를 지원하는 통계표 ID
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
                 labels={'C1_NM': '성별', 'DT': '사고자 수'},
                 title=f"{selected_year}년 성별 산업재해 통계")
    
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-30)

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("❌ API에서 잘못된 응답이 반환되었습니다.")
