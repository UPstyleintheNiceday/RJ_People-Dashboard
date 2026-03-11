import streamlit as st
import pandas as pd

st.title("ตรวจสอบโครงสร้างไฟล์ Excel")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # โหลดทั้ง 2 Sheet
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่')
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง')

    st.write("### ชื่อคอลัมน์ใน Sheet 'พื้นที่':")
    st.write(df_area.columns.tolist())

    st.write("### ชื่อคอลัมน์ใน Sheet 'อัตรากำลัง':")
    st.write(df_staff.columns.tolist())
    
except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
