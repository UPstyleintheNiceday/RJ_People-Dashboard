import streamlit as st
import pandas as pd

# 1. โหลดข้อมูล
# ใช้ header=1 หรือ 0 ขึ้นอยู่กับว่าหัวตารางของคุณอยู่ที่แถวไหน
df = pd.read_excel('RJ Manpower/data.xlsx')

st.title("📊 Manpower Efficiency Dashboard")

# 2. เตรียมข้อมูล
# สมมติว่า Column B ของคุณคือชื่อตำแหน่ง ให้เรา set เป็น index หรือใช้กรองข้อมูล
st.subheader("เปรียบเทียบพื้นที่ดูแลต่อพนักงาน 1 คน (ตร.ม./คน)")

# เลือกเฉพาะตึกที่ต้องการ
buildings = ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร']

# สมมติว่าใน Excel มีคอลัมน์ชื่อ 'Position' (ตำแหน่ง), 'Area' (พื้นที่), 'Manpower' (จำนวนคน)
# คุณต้องเปลี่ยนชื่อในตัวแปรเหล่านี้ให้ตรงกับหัวคอลัมน์ในไฟล์ Excel ของคุณ!
col_pos = 'ชื่อตำแหน่ง'     # <--- แก้ให้ตรงกับหัว Column B
col_area = 'พื้นที่ (ตร.ม.)' # <--- แก้ให้ตรงกับหัวตารางพื้นที่
col_man = 'จำนวนพนักงาน'     # <--- แก้ให้ตรงกับหัวตารางจำนวนคน

# คำนวณอัตราส่วน: พื้นที่ / จำนวนคน
df['Area_Per_Man'] = df[col_area] / df[col_man]

# 3. แสดงผลในรูปแบบตารางและกราฟ
st.dataframe(df[[col_pos, col_area, col_man, 'Area_Per_Man']])

st.subheader("กราฟเปรียบเทียบภาระงาน (ตร.ม. ต่อคน)")
chart_data = df.set_index(col_pos)[['Area_Per_Man']]
st.bar_chart(chart_data)

st.info("หมายเหตุ: ค่าที่สูงหมายถึงพนักงาน 1 คนดูแลพื้นที่เยอะ (อาจจะเหนื่อยกว่าปกติ)")


