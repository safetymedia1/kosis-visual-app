import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.title("📊 KOSIS 산업재해 통계 시각화")

API_KEY = "당신의_API_키"
URL = "https://kosis.kr/openapi/statisticsData.do"

params = {
    "method": "getList",
    "apiKey": API_KEY,
    "format": "json",
    "jsonVD": "Y",
    "orgId": "118",
    "tblId": "DT_11806_N000",
    "itmId": "16118AAD6_15118AI8AA",
    "objL1": "ALL",
    "prdSe": "Y",
    "startPrdDe": "2013",
    "endPrdDe": "2023"
}

response = requests.get(URL, params=params)
data = response.json()

df = pd.DataFrame(data)
df = df[['PRD_DE', 'C1_NM', 'DT']]
df['DT'] = df['DT'].astype(float)

st.line_chart(df.set_index('PRD_DE')['DT'])
