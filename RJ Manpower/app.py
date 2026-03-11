import streamlit as st
import pandas as pd

st.set_page_config(page_title="Debug", layout="wide")
st.title("🔎 ตรวจสอบข้อมูลดิบในตาราง")

try:
    file_path = 'RJ Manpower/data.xlsx'
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', header=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', header=0)

    # เชื่อมตาราง
    df_combined = pd.merge(df_area, df_staff, left_on=df_area.columns[0], right_on=df_staff.columns[0], suffixes=('_พื้นที่', '_คน'))

    st.write("### นี่คือข้อมูลทั้งหมดที่มีในตารางหลังรวมกันแล้ว:")
    st.dataframe(df_combined)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
