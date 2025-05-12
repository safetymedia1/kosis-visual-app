import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.title("📊 산업재해 통계 시각화 (2013–2023, 막대 그래프)")

# API KEY를 secrets.toml에서 가져오기
API_KEY = st.secrets["KOSIS_API_KEY"]

# API 요청 파라미터 설정
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

# 응답 처리
if isinstance(data, list):
    df = pd.DataFrame(data)
    df = df[['PRD_DE', 'ITM_NM', 'DT']]
    df['DT'] = pd.to_numeric(df['DT'], errors='coerce')

    # 항목 선택
    selected_item = st.selectbox("📌 항목을 선택하세요", df['ITM_NM'].unique())
    df_selected = df[df['ITM_NM'] == selected_item].sort_values("PRD_DE")

    # 그래프
    fig, ax = plt.subplots()
    bars = ax.bar(df_selected['PRD_DE'], df_selected['DT'])

    # 값 라벨 추가
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.0f}', va='bottom', ha='center', fontsize=9)

    ax.set_xlabel("연도")
    ax.set_ylabel("값")
    ax.set_title(f"{selected_item} 연도별 통계")

    st.pyplot(fig)
else:
    st.error("❌ API 응답이 올바르지 않습니다. API 키나 파라미터를 확인해주세요.")
