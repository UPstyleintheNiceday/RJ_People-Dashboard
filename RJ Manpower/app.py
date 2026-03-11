import streamlit as st
import pandas as pd

st.set_page_config(page_title="RJ Dashboard", layout="wide")
st.title("📊 RJ Manpower & Space Dashboard")

# 1. โหลดข้อมูล
try:
    file_path = 'RJ Manpower/data.xlsx'
    # ใช้ header=0 เพราะชื่อตึกอยู่ในแถวแรกสุด (Index 0)
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', header=0)
    
    # 2. ปรับชื่อคอลัมน์ให้เรียกง่าย
    # แถวแรกคือชื่อพื้นที่, แถวสองคือหน่วย, คอลัมน์ที่เหลือคืออาคาร
    df_area = df_area.rename(columns={df_area.columns[0]: 'ประเภทพื้นที่'})
    
    st.subheader("ข้อมูลพื้นที่อาคาร (ตร.ม.)")
    st.dataframe(df_area)

    # 3. เลือกอาคาร
    buildings = ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร']
    selected_bldg = st.selectbox("เลือกอาคารที่ต้องการดู:", buildings)

    # 4. แสดงกราฟพื้นที่
    st.subheader(f"สัดส่วนพื้นที่: {selected_bldg}")
    chart_data = df_area.set_index('ประเภทพื้นที่')[selected_bldg]
    st.bar_chart(chart_data)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {e}")
