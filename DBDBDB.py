import streamlit as st
import pandas as pd

# 대시보드 제목 설정
st.title('HR 역할 구분 대시보드')

# CSV 파일 로드
file_path = 'AI분석해보자.csv'

@st.cache
def load_data():
    data = pd.read_csv(file_path)
    return data

data = load_data()

# 1. 연도별 역할 구분에 따른 분포 (남녀 구분 없이 인원수 표로 보여주기) - 2024년 데이터 포함
roles = ['M', 'P', 'R', 'S']
role_year_distribution = data[data['역할구분 (MPRS)'].isin(roles)].groupby(['년도', '역할구분 (MPRS)']).size().unstack(fill_value=0)
st.write("### 연도별 역할 구분에 따른 분포 (남녀 구분 없음)")
st.dataframe(role_year_distribution)

# 2. 연도별 여성 비율 계산 (역할구분을 열로, 년도를 행으로) - 소수점 한자리까지만 표시하고 % 추가
def calculate_female_ratio(df, role):
    role_data = df[df['역할구분 (MPRS)'] == role]
    total_counts = role_data.groupby('년도').size()
    female_counts = role_data[role_data['성별'] == '여'].groupby('년도').size()
    female_ratio = (female_counts / total_counts * 100).round(1).astype(str) + '%'
    return female_ratio

female_ratios = pd.DataFrame()

for role in roles:
    female_ratios[role] = calculate_female_ratio(data, role)

st.write("### 연도별 여성 비율 (전체 인원 중 여성 비율)")
st.dataframe(female_ratios)
