import streamlit as st
import pandas as pd

st.set_page_config(page_title="Debug Dashboard", layout="wide")
st.title("🔎 ตรวจสอบโครงสร้างข้อมูลที่รวมกันแล้ว")

try:
    file_path = 'RJ Manpower/data.xlsx'
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', header=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', header=0)

    # เชื่อมตาราง
    df_combined = pd.merge(df_area, df_staff, left_on=df_area.columns[0], right_on=df_staff.columns[0])

    # แสดงชื่อคอลัมน์ทั้งหมดที่ Merge สำเร็จ
    st.write("### รายชื่อคอลัมน์ทั้งหมดหลังจาก Merge:")
    st.write(df_combined.columns.tolist())
    
    st.write("### 5 แถวแรกของตารางที่รวมแล้ว:")
    st.dataframe(df_combined.head(5))

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
