import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드 함수
def load_data():
    try:
        data = pd.read_csv("AI분석해보자.csv")
        return data
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다.")
    except pd.errors.EmptyDataError:
        st.error("파일이 비어 있습니다.")
    except pd.errors.ParserError:
        st.error("파일 형식에 문제가 있습니다. 파일을 확인하세요.")
    return None

# 데이터 처리 함수
def process_data(data):
    if data is None or data.empty:
        st.error("데이터가 없거나 비어 있습니다.")
        return None

    # 필요한 열이 있는지 확인
    required_columns = ['Role', 'Year', 'Female_Ratio']
    if not all(column in data.columns for column in required_columns):
        st.error(f"필수 열이 누락되었습니다: {required_columns}")
        return None

    try:
        female_ratio = data.groupby('Role')['Female_Ratio'].mean()
    except ZeroDivisionError:
        st.error("여성 비율 계산 중 제로 나누기 오류가 발생했습니다.")
        return None

    return female_ratio

# 파일 업로드 및 시각화
st.title("HR 대시보드")

data = load_data()
if data is not None:
    female_ratio = process_data(data)

    if female_ratio is not None:
        st.line_chart(female_ratio)

        if 'Year' in data.columns and 2024 in data['Year'].values:
            year_2024_data = data[data['Year'] == 2024]
            st.pie_chart(year_2024_data['Female_Ratio'])
