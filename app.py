import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="산업재해 산업별 통계", layout="wide")
st.title("📊 산업재해 통계 시각화 (산업별)")

API_KEY = st.secrets["KOSIS_API_KEY"]

URL = "https://kosis.kr/openapi/Param/statisticsParameterData.do"
params = {
    "method": "getList",
    "apiKey": API_KEY,
    "itmId": "16118AAD6_15118AI8AA",  # 기본: 사고자 수 (원하면 선택 가능)
    "objL1": "A02",  # ✅ 산업별
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
    df = df[['PRD_DE', 'C1_NM', 'DT']]
    df['DT'] = pd.to_numeric(df['DT'], errors='coerce')
    df = df.dropna(subset=['DT'])
    df = df[df['DT'] >= 0]

    # ✅ 연도 선택
    year_list = sorted(df['PRD_DE'].unique())
    selected_years = st.multiselect("📅 연도를 선택하세요 (복수 선택)", year_list, default=[year_list[-1]])

    df_selected = df[df['PRD_DE'].isin(selected_years)]

    # ✅ 산업명이 y축이 되도록 정렬
    df_selected = df_selected.sort_values("DT", ascending=False)
    df_selected['DT_fmt'] = df_selected['DT'].map(lambda x: f"{x:,.0f}")

    # ✅ 그래프 생성 (x: 연도, y: 산업명)
    fig = px.bar(
        df_selected,
        x='DT',
        y='C1_NM',
        color='PRD_DE',
        orientation='h',  # ✅ 수평 막대
        text='DT_fmt',
        labels={'DT': '사고자 수', 'C1_NM': '산업명', 'PRD_DE': '연도'},
        title="연도별 산업별 사고자 수"
    )

    fig.update_traces(
        textposition='outside'
    )

    fig.update_layout(
        yaxis=dict(title='산업명'),
        xaxis=dict(title='사고자 수', tickformat=','),
        height=600,
        margin=dict(t=70, l=120, r=40, b=40),
        legend_title_text="연도"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("❌ API 데이터 형식이 잘못되었습니다.")
