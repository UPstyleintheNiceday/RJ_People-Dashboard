import streamlit as st
import pandas as pd

st.set_page_config(page_title="Manpower Dashboard", layout="wide")
st.title("📊 Manpower Efficiency Dashboard")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # 1. โหลดข้อมูลโดยระบุ header=1 เพื่อข้ามแถวบนสุดที่ไม่ใช่ชื่อคอลัมน์
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', header=1)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', header=1)
    
    # 2. ปรับชื่อคอลัมน์เพื่อความแม่นยำ (อ้างอิงจากลำดับ)
    # สมมติชื่อตึกคือคอลัมน์ที่ 2, 3, 4 (ดัชนี 2, 3, 4)
    buildings = ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร']
    
    # ดึงรายชื่อตำแหน่งจาก Tab อัตรากำลัง (แถวแรก)
    # เปลี่ยน 'ตำแหน่ง' ให้ตรงกับหัวตารางในแถวที่ 2 ของ Tab อัตรากำลัง
    pos_col = df_staff.columns[0] 
    man_col = df_staff.columns[1] # สมมติว่าคอลัมน์ที่ 2 คือ 'จำนวนคน'
    
    # 3. ให้ผู้ใช้เลือก
    selected_bldg = st.selectbox("เลือกอาคาร:", buildings)
    
    # 4. รวมข้อมูล (แบบง่าย: นำพื้นที่มาใส่ในตารางอัตรากำลัง)
    # เราจะสมมติว่าลำดับแถวของทั้งสองตารางเรียงตรงกัน
    df_final = df_staff.copy()
    df_final['พื้นที่ (ตร.ม.)'] = df_area[selected_bldg]
    
    # 5. คำนวณตารางเมตรต่อคน
    df_final['ตร.ม. ต่อคน'] = df_final['พื้นที่ (ตร.ม.)'] / df_final[man_col]
    
    # 6. แสดงผล
    st.subheader(f"ประสิทธิภาพพื้นที่ต่อคน: {selected_bldg}")
    st.dataframe(df_final[[pos_col, man_col, 'พื้นที่ (ตร.ม.)', 'ตร.ม. ต่อคน']])
    
    st.bar_chart(df_final.set_index(pos_col)['ตร.ม. ต่อคน'])

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
    st.write("ตรวจสอบให้แน่ใจว่าแถวที่ 2 ของ Excel คือหัวตารางจริงๆ ครับ")
