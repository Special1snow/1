import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 대시보드 제목 설정
st.title('HR Role Distribution Dashboard')

# CSV 파일 로드
file_path = 'AI분석해보자.csv'

@st.cache
def load_data():
    data = pd.read_csv(file_path)
    return data

data = load_data()

# 역할 구분의 한글을 영어로 변경
data['역할구분 (MPRS)'] = data['역할구분 (MPRS)'].replace({
    'M': 'Manager',
    'P': 'Professional',
    'R': 'Researcher',
    'S': 'Specialist'
})

# 1. 연도별 Role Distribution (남녀 구분 없이 인원수 표로 보여주기)
roles = ['Manager', 'Professional', 'Researcher', 'Specialist']
role_year_distribution = data[data['역할구분 (MPRS)'].isin(roles)].groupby(['년도', '역할구분 (MPRS)']).size().unstack(fill_value=0)
st.write("### Yearly Role Distribution")
st.dataframe(role_year_distribution)

# 2. 누적 막대그래프 추가 (연도별 Role Distribution을 시각화)
st.write("### Yearly Role Distribution (Stacked Bar Chart)")
fig, ax = plt.subplots()
role_year_distribution.plot(kind='bar', stacked=True, ax=ax)
ax.set_xlabel('Year')
ax.set_ylabel('Number of Employees')
st.pyplot(fig)

# 3. 연도별 여성 구성원 비율 계산 (역할구분을 열로, 년도를 행으로) - 소수점 한자리까지만 표시하고 % 추가
def calculate_female_ratio(df, role):
    role_data = df[df['역할구분 (MPRS)'] == role]
    total_counts = role_data.groupby('년도').size()
    female_counts = role_data[role_data['성별'] == '여'].groupby('년도').size()
    female_ratio = (female_counts / total_counts * 100).round(1).astype(str) + '%'
    return female_ratio

female_ratios = pd.DataFrame()

for role in roles:
    female_ratios[role] = calculate_female_ratio(data, role)

st.write("### Yearly Female Composition Ratio")
st.dataframe(female_ratios)

# 4. 파이차트 추가 (각 Role별로 여성구성원과 남성구성원 비율)
st.write("### Gender Composition by Role (Pie Chart)")

# 각 Role에 대해 여성과 남성 비율 계산
for role in roles:
    total_counts = data[data['역할구분 (MPRS)'] == role].groupby('성별').size()
    female_count = total_counts.get('여', 0)
    male_count = total_counts.get('남', 0)
    
    labels = ['Female', 'Male']
    sizes = [female_count, male_count]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # 파이차트를 원형으로 그리기 위한 설정
    st.write(f"### {role} Gender Composition")
    st.pyplot(fig)
