import streamlit as st
import pandas as pd

st.set_page_config(page_title="Manpower Dashboard", layout="wide")
st.title("📊 Manpower Efficiency Dashboard")

try:
    # 1. โหลดข้อมูลทั้ง 2 Sheet
    file_path = 'RJ Manpower/data.xlsx'
    # ปรับ header ให้ตรงกับที่สแกนได้จากภาพก่อนหน้า
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', header=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', header=1) # สมมติว่า header อยู่แถว 2

    # 2. ปรับแต่งข้อมูล
    # สมมติว่าคอลัมน์ชื่อตำแหน่งใน tab อัตรากำลัง ชื่อว่า 'ชื่อตำแหน่ง'
    # และใน tab พื้นที่ มีชื่อพื้นที่/ตำแหน่งที่ตรงกัน
    # ให้เปลี่ยน 'ชื่อตำแหน่ง' เป็นชื่อหัวตารางจริงใน Excel ของคุณ
    pos_col = 'ชื่อตำแหน่ง' 
    man_col = 'จำนวนพนักงาน' 

    # 3. รวมข้อมูล (Merge)
    # เชื่อมด้วยชื่อตำแหน่ง/พื้นที่
    df_combined = pd.merge(df_area, df_staff, left_on=df_area.columns[0], right_on=pos_col)

    # 4. เลือกอาคาร
    buildings = ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร']
    selected_bldg = st.selectbox("เลือกอาคาร:", buildings)

    # 5. คำนวณประสิทธิภาพ
    # สูตร: พื้นที่อาคาร / จำนวนคนในตำแหน่งนั้น
    df_combined['ตร.ม. ต่อคน'] = df_combined[selected_bldg] / df_combined[man_col]

    # 6. แสดงผล Dashboard
    st.subheader(f"ประสิทธิภาพกำลังคน: อาคาร{selected_bldg}")
    st.dataframe(df_combined[[pos_col, selected_bldg, man_col, 'ตร.ม. ต่อคน']])

    # กราฟแท่ง
    st.bar_chart(df_combined.set_index(pos_col)['ตร.ม. ต่อคน'])

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการคำนวณ: {e}")
    st.write("ตรวจสอบให้แน่ใจว่าชื่อคอลัมน์ในโค้ดตรงกับหัวตารางใน Excel (โดยเฉพาะคอลัมน์ 'ชื่อตำแหน่ง' และ 'จำนวนพนักงาน')")

