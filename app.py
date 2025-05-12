import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.title("📊 산업재해 통계 시각화 (항목 및 연도 비교 + 상세 표시)")

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

    # 항목 선택
    item_list = df['ITM_NM'].unique().tolist()
    default_item_index = item_list.index("총계") if "총계" in item_list else 0
    selected_item = st.selectbox("📌 항목을 선택하세요", item_list, index=default_item_index)

    # 연도 다중 선택
    year_list = sorted(df['PRD_DE'].unique())
    selected_years = st.multiselect("📅 연도를 선택하세요 (복수 선택)", year_list, default=year_list[-1:])

    df_selected = df[(df['ITM_NM'] == selected_item) & (df['PRD_DE'].isin(selected_years))]
    df_selected = df_selected.sort_values("PRD_DE")

    # 시각화: 상세 툴팁 포함
    fig = px.bar(df_selected, x='PRD_DE', y='DT',
                 text='DT',
                 hover_data={'PRD_DE': True, 'ITM_NM': True, 'DT': True},
                 labels={'PRD_DE': '연도', 'DT': '사고 건수'},
                 title=f"산업재해 통계: {selected_item} (선택 연도별 비교)")

    fig.update_traces(
        texttemplate='연도 %{x}<br>%{y:.0f}건',
        textposition='outside',
        hovertemplate='연도: %{x}<br>항목: %{customdata[1]}<br>사고 건수: %{y}건<extra></extra>'
    )

    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        xaxis_title='연도',
        yaxis_title='사고 건수'
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("❌ API 데이터 형식이 잘못되었습니다.")
