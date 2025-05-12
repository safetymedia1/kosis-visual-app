import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="산업재해 통계 시각화", layout="wide")

st.title("📊 산업재해 통계 시각화")

API_KEY = st.secrets["KOSIS_API_KEY"]

# API 설정
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

# 요청
response = requests.get(URL, params=params)

try:
    data = response.json()
except ValueError:
    st.error("❌ API 응답 파싱 실패")
    st.stop()

if isinstance(data, list):
    df = pd.DataFrame(data)
    df = df[['PRD_DE', 'ITM_NM', 'DT']]

    # 수치 변환 + 클린업
    df['DT'] = pd.to_numeric(df['DT'], errors='coerce')
    df = df.dropna(subset=['DT'])
    df = df[df['DT'] >= 0]

    # 항목 선택
    item_list = df['ITM_NM'].unique().tolist()
    default_item_index = item_list.index("총계") if "총계" in item_list else 0
    selected_item = st.selectbox("📌 항목을 선택하세요", item_list, index=default_item_index)

    # 연도 선택
    year_list = sorted(df['PRD_DE'].unique())
    selected_years = st.multiselect("📅 연도를 선택하세요 (복수 선택)", year_list, default=year_list[-1:])

    df_selected = df[(df['ITM_NM'] == selected_item) & (df['PRD_DE'].isin(selected_years))]
    df_selected = df_selected.sort_values("PRD_DE")

    # 단위 포맷 적용 (천 단위 쉼표)
    df_selected['DT_fmt'] = df_selected['DT'].map(lambda x: f"{x:,.0f}")

    # Plotly 그리기
    fig = px.bar(
        df_selected,
        x='PRD_DE',
        y='DT',
        text='DT_fmt',
        labels={'PRD_DE': '연도', 'DT': '사고 건수'},
        title=f"{selected_item} (연도별 비교)",
        color_discrete_sequence=['#0083B8'],  # 시각적 강조 색
        height=500
    )

    fig.update_traces(
        textposition='outside',
        marker_line_width=0.5
    )

    fig.update_layout(
        yaxis=dict(
            title="사고 건수",
            tickformat=",",  # 천 단위 쉼표
            dtick=5,
            gridcolor='lightgray'
        ),
        xaxis=dict(
            title="연도",
            tickangle=-30
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        margin=dict(t=80, l=50, r=50, b=50),
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("❌ API 데이터 형식이 잘못되었습니다.")
