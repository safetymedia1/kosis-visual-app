import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.title("📊 산업재해 통계 시각화 (선택 항목 및 연도별 보기)")

API_KEY = st.secrets["KOSIS_API_KEY"]

URL = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
params = {
    "method": "getList",
    "apiKey": API_KEY,
    "itmId": "16118AAD6_15118AI8AA+16118AAD6_15118AI8AB+16118AAD6_15118AI8AC+16118AAD6_15118AI8ACAC+16118AAD6_15118AI8ACAB+16118AAD6_15118AI8ACAD+",
    "objL1": "ALL",
    "format": "json",
    "jsonVD": "Y",
    "prdSe": "Y",
    "startPrdDe": "2013",
    "endPrdDe": "2023",
    "orgId": "118",
    "tblId": "DT_11806_N000"
}

response = requests.get(URL, params=params)

try:
    data = response.json()
except ValueError:
    st.error("❌ API 응답 파싱 실패")
    st.stop()

if isinstance(data, list):
    df = pd.DataFrame(data)
    df = df[['PRD_DE', 'ITM_NM', 'DT']]
    df['DT'] = pd.to_numeric(df['DT'], errors='coerce')

    # 선택 가능한 항목 (사고자수, 사망자수 등)
    item_list = df['ITM_NM'].unique().tolist()
    default_item_index = item_list.index("총계") if "총계" in item_list else 0
    selected_item = st.selectbox("📌 항목을 선택하세요", item_list, index=default_item_index)

    # 선택 가능한 연도
    year_list = sorted(df['PRD_DE'].unique())
    selected_year = st.selectbox("📅 연도를 선택하세요", year_list, index=len(year_list)-1)

    # 선택된 항목 + 연도 기준으로 필터링
    df_selected = df[(df['ITM_NM'] == selected_item) & (df['PRD_DE'] == selected_year)]

    # 시각화
    fig = px.bar(df_selected, x='PRD_DE', y='DT',
                 text='DT',
                 labels={'PRD_DE': '연도', 'DT': '사고 건수'},
                 title=f"{selected_year}년 산업재해 통계: {selected_item}")

    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("❌ API 데이터 형식이 잘못되었습니다.")
