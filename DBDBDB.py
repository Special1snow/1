import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 대시보드 제목 설정
st.title('HR 역할 구분 대시보드')

# CSV 파일 로드
@st.cache_data
def load_data():
    data = pd.read_csv('AI분석해보자.csv')
    return data

data = load_data()

# 데이터 확인
st.write("### 데이터 미리보기", data.head())

# 연도별 역할 구분에 따른 분포 시각화
role_year_distribution = data.groupby(['년도', '역할구분 (MPRS)']).size().unstack()
st.write("### 연도별 역할 구분에 따른 분포")
st.line_chart(role_year_distribution)

# M P R S 역할에 대한 연도별 여성의 비율 계산
def calculate_female_ratio(df, role):
    role_data = df[df['역할구분 (MPRS)'] == role]
    total_counts = role_data.groupby('년도').size()
    female_counts = role_data[role_data['성별'] == '여'].groupby('년도').size()
    female_ratio = (female_counts / total_counts) * 100
    return female_ratio

roles = ['M', 'P', 'R', 'S']
female_ratios = pd.DataFrame()
for role in roles:
    female_ratios[role] = calculate_female_ratio(data, role)

st.write("### 연도별로 여성의 비율 (M, P, R, S 역할)")
st.line_chart(female_ratios)

# 2024년 기준 M P R S 역할에 대한 성별 분포 파이 차트
data_2024 = data[data['년도'] == 2024]
role_gender_distribution_2024 = data_2024[data_2024['역할구분 (MPRS)'].isin(roles)].groupby(['역할구분 (MPRS)', '성별']).size().unstack()

st.write("### 2024년 기준 역할 구분에 따른 성별 분포")
fig, ax = plt.subplots(1, 4, figsize=(16, 4))
role_gender_distribution_2024.plot(kind='pie', subplots=True, autopct='%1.1f%%', ax=ax)
st.pyplot(fig)

# 데이터 다운로드 기능 추가
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(data)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='hr_data.csv',
    mime='text/csv',
)
