
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Ensure Seaborn is imported according to the provided version in requirements.txt
try:
    import seaborn as sns
    seaborn_imported = True
except ImportError:
    seaborn_imported = False
    st.warning("Seaborn이 설치되지 않았습니다. Heatmap과 같은 시각화가 제한됩니다.")

# Load the data
file_path = 'AI를 활용한 HR솔루션 기능요건정의 (SKGC).xlsx'
xls = pd.ExcelFile(file_path)

df_skillset = pd.read_excel(xls, '직무별SkillSet')
df_self_review = pd.read_excel(xls, 'Self Review')
df_education_db = pd.read_excel(xls, '교육DB')

# Dashboard title
st.title('AI를 활용한 HR 대시보드')

# Sidebar for selecting sheets to display
option = st.sidebar.selectbox(
    '어떤 데이터를 탐색하시겠습니까?',
    ('직무별SkillSet', 'Self Review', '교육DB')
)

if option == '직무별SkillSet':
    st.header('직무별 SkillSet')
    
    st.write("각 부서별 스킬셋 데이터입니다.")
    
    # Display dataframe
    st.dataframe(df_skillset)
    
    # Heatmap of skill proficiency across departments
    st.subheader('부서별 스킬 숙련도 히트맵')
    
    if seaborn_imported:
        plt.figure(figsize=(10,6))
        sns.heatmap(df_skillset.iloc[:, 2:], annot=True, cmap="coolwarm", fmt=".1f")
        st.pyplot(plt)
    else:
        st.error("히트맵을 표시하려면 Seaborn이 필요합니다. Seaborn을 설치하세요.")

elif option == 'Self Review':
    st.header('자기 평가 (Self Review)')
    
    st.write("자기 평가 및 스킬 평가 비교 데이터입니다.")
    
    # Display dataframe
    st.dataframe(df_self_review)
    
    # Bar chart: Self review scores vs average department score
    st.subheader('자기 평가 점수 비교')
    fig, ax = plt.subplots()
    df_self_review['Self Review'].plot(kind='bar', ax=ax, color='skyblue', label='자기 평가')
    df_self_review['환산점수'].plot(kind='bar', ax=ax, color='orange', alpha=0.5, label='환산 점수')
    ax.legend()
    st.pyplot(fig)

elif option == '교육DB':
    st.header('교육 DB')
    
    st.write("교육 및 훈련 데이터 개요입니다.")
    
    # Display dataframe
    st.dataframe(df_education_db)
    
    # Bar chart of educational costs across departments
    st.subheader('부서별 교육 비용')
    df_education_db_filtered = df_education_db[df_education_db['비용(만원)'] > 0]
    fig, ax = plt.subplots()
    df_education_db_filtered.groupby('사업부')['비용(만원)'].sum().plot(kind='bar', ax=ax, color='green')
    ax.set_ylabel('비용 (만원)')
    st.pyplot(fig)
    
# Footer
st.write("Streamlit을 사용하여 생성된 대시보드입니다.")
