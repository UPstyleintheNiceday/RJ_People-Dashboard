import streamlit as st
import pandas as pd

st.set_page_config(page_title="RJ Manpower Dashboard", layout="wide")
st.title("📊 Manpower Efficiency Dashboard")

try:
    file_path = 'RJ Manpower/data.xlsx'
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', header=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', header=0)

    # รวมข้อมูลโดยระบุ suffixes เพื่อแยกพื้นที่กับคน
    df_combined = pd.merge(df_area, df_staff, left_on=df_area.columns[0], right_on=df_staff.columns[0], suffixes=('_พื้นที่', '_คน'))

    # เลือกอาคาร
    buildings = ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร']
    selected_bldg = st.selectbox("เลือกอาคารที่ต้องการเปรียบเทียบ:", buildings)

    # คำนวณ (ใช้ชื่อคอลัมน์ใหม่ที่ระบุชัดเจน)
    # พื้นที่มาจากตึก_พื้นที่ / จำนวนคนมาจากตึก_คน
    df_combined['ตร.ม. ต่อคน'] = df_combined[f'{selected_bldg}_พื้นที่'] / df_combined[f'{selected_bldg}_คน']

    # แสดงผล
    st.subheader(f"ประสิทธิภาพ: อาคาร {selected_bldg}")
    st.dataframe(df_combined[['สาขา', f'{selected_bldg}_พื้นที่', f'{selected_bldg}_คน', 'ตร.ม. ต่อคน']])

    # กราฟ
    st.bar_chart(df_combined.set_index('สาขา')['ตร.ม. ต่อคน'])

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
