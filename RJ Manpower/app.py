import streamlit as st
import pandas as pd

st.title("📊 รายงานประสิทธิภาพ: พื้นที่ทำกำไรต่อคน")

try:
    # 1. โหลดข้อมูล (ปรับชื่อไฟล์ให้ตรงกับที่คุณอัปโหลด)
    df_area = pd.read_csv('data.xlsx - พื้นที่.csv', index_col=0)
    df_staff = pd.read_csv('data.xlsx - อัตรากำลัง.csv', index_col=0)
    
    # 2. ทำความสะอาดข้อมูล: ดึงเฉพาะคอลัมน์อาคารที่ต้องการ
    cols = ['ประชาชื่น', 'ประดิพัทธ์', 'สาทร']
    
    # ดึงค่า Profitable Space
    prof_space = df_area.loc['Profitable Space', cols]
    
    # ดึงข้อมูลพนักงานและบังคับเป็นตัวเลข
    df_staff = df_staff.loc[:, cols]
    df_staff = df_staff.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # 3. คำนวณ (ใช้ .div จับคู่ชื่อคอลัมน์อาคารโดยตรง)
    result_df = df_staff.div(prof_space, axis=1)
    
    # 4. ล้างแถวที่เป็น 0 ออก (ตำแหน่งที่ไม่มีพนักงานในทุกสาขา)
    result_df = result_df.replace(0, pd.NA).dropna(how='all').fillna(0)
    
    # 5. แสดงผลเป็นตารางเท่านั้น
    st.write("### ตารางประสิทธิภาพ (ตร.ม. ทำกำไรต่อพนักงาน 1 คน)")
    st.dataframe(result_df.style.format("{:.2f}"), use_container_width=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
