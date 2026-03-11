import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 RJ Manpower Dashboard")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # โหลดแยกกันชัดเจน
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', header=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', header=0)

    # เลือกอาคาร
    building = st.selectbox("เลือกอาคาร:", ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร'])

    # ดึงค่าพื้นที่รวมจากตารางแรก (บรรทัด "Total Space")
    # สมมติแถวที่ "Total Space" อยู่คือแถวที่ 0 หรือ 1 ลองสังเกตจากตารางที่เคยโชว์
    total_area = df_area.loc[df_area.iloc[:, 0] == 'Total Space', building].values[0]

    # ดึงจำนวนคนรวมจากตารางสอง
    # สมมติคอลัมน์ชื่อ 'จำนวนคน' อยู่ในตาราง df_staff
    total_staff = df_staff['จำนวนคน'].sum()

    st.metric("พื้นที่รวม (ตร.ม.)", f"{total_area:,.2f}")
    st.metric("จำนวนพนักงานทั้งหมด", f"{total_staff:,.0f}")
    
    # คำนวณ
    ratio = total_area / total_staff
    st.subheader(f"ค่าเฉลี่ยพื้นที่ต่อคน: {ratio:.2f} ตร.ม./คน")

except Exception as e:
    st.write("กรุณาตรวจสอบว่าใน Sheet 'อัตรากำลัง' มีคอลัมน์ชื่อ 'จำนวนคน' อยู่จริง")
    st.error(f"Error details: {e}")
