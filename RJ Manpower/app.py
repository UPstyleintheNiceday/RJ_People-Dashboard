import streamlit as st
import pandas as pd

st.title("📊 รายงานประสิทธิภาพ: พื้นที่ทำกำไรต่อคน")

try:
    # ระบุที่อยู่ไฟล์ตามโฟลเดอร์จริงที่ระบบบอกมา
    file_path = 'RJ Manpower/data.xlsx'
    
    # อ่าน Excel โดยระบุ Sheet ชื่อให้ตรงเป๊ะๆ
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # ดึงค่าเฉพาะ 3 สาขา (ลดความเสี่ยงจากชื่อคอลัมน์ที่ไม่ตรง)
    cols = ['ประชาชื่น', 'ประดิพัทธ์', 'สาทร']
    
    prof_space = df_area.loc['Profitable Space', cols]
    
    # จัดการพนักงาน: ตัดคอลัมน์ไม่จำเป็น และแปลงทุกอย่างให้เป็นเลข 0 ถ้าเป็นค่าว่าง
    df_staff = df_staff.loc[:, cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # คำนวณ (ใช้ .div จะปลอดภัยที่สุด)
    result = df_staff.div(prof_space, axis=1)
    
    # แสดงตารางแบบไม่มีค่าที่เป็น 0 (เอาแถวที่ไม่มีคนทำงานจริงออก)
    final_table = result.replace(0, pd.NA).dropna(how='all').fillna(0)
    
    st.dataframe(final_table.style.format("{:.2f}"), use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
