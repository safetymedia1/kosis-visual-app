import streamlit as st
import pandas as pd
import requests

st.title("📊 산업재해 통계 시각화 (2013–2023)")

# API KEY를 secrets.toml에서 가져오기
API_KEY = st.secrets["KOSIS_API_KEY"]

# API 호출 URL 구성
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

# API 요청
response = requests.get(URL, params=params)
data = response.json()

# 응답이 리스트인지 확인
if isinstance(data, list):
    df = pd.DataFrame(data)
    df = df[['PRD_DE', 'ITM_NM', 'DT']]  # 연도, 항목명, 값
    df['DT'] = pd.to_numeric(df['DT'], errors='coerce')

    # Streamlit select box로 항목 선택
    selected_item = st.selectbox("항목을 선택하세요", df['ITM_NM'].unique())

    df_selected = df[df['ITM_NM'] == selected_item].sort_values("PRD_DE")

    st.line_chart(df_selected.set_index('PRD_DE')['DT'])

    st.write("📌 선택 항목:", selected_item)
else:
    st.error("❌ API 응답이 올바르지 않습니다. API 키나 파라미터를 다시 확인하세요.")
