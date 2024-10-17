import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 로드
file_path = 'AI분석해보자.csv'

# 데이터프레임으로 CSV 파일 읽기
data = pd.read_csv(file_path)

# 1. 연도별 역할 구분에 따른 분포
role_year_distribution = data.groupby(['년도', '역할구분 (MPRS)']).size().unstack()
print("연도별 역할 구분에 따른 분포:\n", role_year_distribution)

# 2. M P R S 역할에 대한 연도별 여성의 비율 계산
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

print("\n연도별로 여성의 비율 (M, P, R, S 역할):\n", female_ratios)

# 3. 2024년 기준 M P R S 역할에 대한 성별 분포 파이 차트
data_2024 = data[data['년도'] == 2024]
role_gender_distribution_2024 = data_2024[data_2024['역할구분 (MPRS)'].isin(roles)].groupby(['역할구분 (MPRS)', '성별']).size().unstack()

print("\n2024년 기준 역할 구분에 따른 성별 분포:\n", role_gender_distribution_2024)
role_gender_distribution_2024.plot(kind='pie', subplots=True, autopct='%1.1f%%', figsize=(10, 10), legend=False)
plt.show()

export default Dashboard;
