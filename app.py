import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 다운로드 및 등록 (Streamlit Cloud 대응)
font_url = "https://raw.githubusercontent.com/naver/nanumfont/master/ttf/NanumGothic.ttf"
font_path = "/tmp/NanumGothic.ttf"

if not os.path.exists(font_path):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(font_url, headers=headers)
    with open(font_path, "wb") as f:
        f.write(response.content)

font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# ✅ 앱 제목
st.title("📊 산업재해 통계 시각화 (2013–2023, 선택 항목)")

# ✅ API 키 (Streamlit Cloud의 secrets.toml에 저장되어야 함)
API_KEY = st.secrets["KOSIS_API_KEY"]

# ✅ KOSIS API 요청 정보
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

# ✅ API 요청 실행
response = requests.get(URL, params=params)

try:
    data = response.json()
except ValueError:
    st.error("❌ API 응답 파싱 실패. API Key 또는 파라미터를 확인하세요.")
    st.stop()

# ✅ 데이터프레임 변환 및 정리
if isinstance(data, list):
    df = pd.DataFrame(data)
    df = df[['PRD_DE', 'ITM_NM', 'DT']]
    df['DT'] = pd.to_numeric(df['DT'], errors='coerce')

    # ✅ 항목 선택
    item_list = df['ITM_NM'].unique().tolist()
    default_index = item_list.index("총계") if "총계" in item_list else 0
    selected_item = st.selectbox("📌 항목을 선택하세요", item_list, index=default_index)

    # ✅ 선택 항목 필터링
    df_selected = df[df['ITM_NM'] == selected_item].sort_values("PRD_DE")

    # ✅ 막대그래프 그리기
    fig, ax = plt.subplots()
    bars = ax.bar(df_selected['PRD_DE'], df_selected['DT'])

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f'{yval:.0f}',
                va='bottom', ha='center', fontsize=9)

    ax.set_xlabel("연도")
    ax.set_ylabel("사고 건수")
    ax.set_title(f"산업재해 통계: {selected_item} (연도별)")

    st.pyplot(fig)

else:
    st.error("❌ API에서 올바른 형식의 데이터가 오지 않았습니다.")
