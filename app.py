import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 다운로드 (정상 작동하는 CDN 주소 사용)
font_url = "https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2307@1.0/NanumSquareNeo-aLt.ttf"
font_path = "/tmp/NanumSquareNeo-aLt.ttf"

if not os.path.exists(font_path):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(font_url, headers=headers)
    with open(font_path, "wb") as f:
        f.write(response.content)

# ✅ matplotlib에 한글 폰트 등록
try:
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
except Exception as e:
    st.error(f"❌ 한글 폰트 설정 실패: {e}")
    st.stop()
