import streamlit as st
import pandas as pd

st.title("🔎 สแกนชื่อหัวตาราง (Sheet: อัตรากำลัง)")

try:
    file_path = 'RJ Manpower/data.xlsx'
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', header=0)
    
    st.write("### รายชื่อคอลัมน์ที่พบใน Sheet 'อัตรากำลัง':")
    st.write(df_staff.columns.tolist())
    
    st.write("### ข้อมูล 5 แถวแรกของ Sheet นี้:")
    st.dataframe(df_staff.head(5))

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
