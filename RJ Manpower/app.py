import streamlit as st
import pandas as pd

st.title("📊 Manpower Efficiency Dashboard")

# 1. โหลดข้อมูลจาก 2 Tab
# เปลี่ยนชื่อไฟล์และชื่อ Sheet ให้ตรงกับไฟล์จริงของคุณ
file_path = 'RJ Manpower/data.xlsx'
df_area = pd.read_excel(file_path, sheet_name='พื้นที่') 
df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง')

# 2. ปรับหัวตารางให้ตรงกันเพื่อเชื่อมข้อมูล (สมมติว่าเชื่อมด้วย 'ชื่อพื้นที่')
# ให้มั่นใจว่าในทั้ง 2 Sheet มีคอลัมน์ที่ชื่อเหมือนกัน เช่น 'ชื่อพื้นที่'
df_combined = pd.merge(df_area, df_staff, on='ชื่อพื้นที่')

# 3. เลือกอาคารเพื่อแสดงผล
building = st.selectbox("เลือกอาคาร:", ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร'])

# 4. คำนวณ (สมมติคอลัมน์จำนวนคนชื่อ 'จำนวนพนักงาน')
# ผลลัพธ์ = พื้นที่ (ตึกที่เลือก) / จำนวนพนักงาน
df_combined['ตร.ม. ต่อคน'] = df_combined[building] / df_combined['จำนวนพนักงาน']

# 5. แสดงผล
st.subheader(f"ประสิทธิภาพพื้นที่ต่อคน - อาคาร{building}")
st.dataframe(df_combined[['ชื่อพื้นที่', 'ชื่อตำแหน่ง', building, 'จำนวนพนักงาน', 'ตร.ม. ต่อคน']])

# กราฟ
st.bar_chart(df_combined.set_index('ชื่อตำแหน่ง')['ตร.ม. ต่อคน'])
