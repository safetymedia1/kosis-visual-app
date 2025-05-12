import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.title("📊 2023년 산업별 산업재해 통계")

API_KEY = st.secrets["KOSIS_API_KEY"]

# 산업별 분류 코드: A02
params = {
    "method": "getList",
    "apiKey": API_KEY,
    "itmId": "16118AAD6_15118AI8AA",  # 사고자 수
    "objL1": "A02",  # 산업별
    "format": "json",
    "jsonVD": "Y",
    "prdSe": "Y",
    "startPrdDe": "2023",
    "endPrdDe": "2023",
    "orgId": "118",
    "tblId": "DT_11806_N000"
}

response = requests.get("https://kosis.kr/openapi/Param/statisticsParameterData.do", params=params)
try:
    data = response.json()
except ValueError:
    st.error("❌ API 응답 파싱 실패")
    st.stop()

if isinstance(data, list):
    df = pd.DataFrame(data)
    df = df[['C1_NM', 'DT']]
    df['DT'] = pd.to_numeric(df['DT'], errors='coerce')

    # 불필요한 합계/소계 제거
    exclude = ["소계", "총계", "합계"]
    df = df[~df['C1_NM'].isin(exclude)]
    df = df.dropna()

    # 보기 좋게 정렬
    df = df.sort_values(by='DT', ascending=False)

    # 시각화
    fig = px.bar(df, x='C1_NM', y='DT', text='DT',
                 labels={'C1_NM': '산업명', 'DT': '사고자 수'},
                 title="2023년 산업별 사고자 수")
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-30)

    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("❌ 유효한 데이터가 없습니다.")
