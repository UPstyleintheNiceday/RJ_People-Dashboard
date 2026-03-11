import streamlit as st
import pandas as pd
import os

st.title("📊 รายงานประสิทธิภาพ: พื้นที่ทำกำไรต่อคน")

# 1. ให้โปรแกรมแสดงชื่อไฟล์ทั้งหมดที่มีในโฟลเดอร์ เพื่อยืนยันว่าเราเรียกชื่อถูก
files_in_folder = os.listdir('.')
st.write("ไฟล์ที่โปรแกรมมองเห็นในระบบตอนนี้คือ:", files_in_folder)

try:
    # 2. ใส่ชื่อไฟล์ตามที่ปรากฏในรายการข้างบนเป๊ะๆ
    # (หากใน list ของคุณมีช่องว่างหรืออักขระแปลกๆ ต้องใส่ให้ครบตามนั้น)
    area_file = 'data.xlsx - พื้นที่.csv'
    staff_file = 'data.xlsx - อัตรากำลัง.csv'
    
    df_area = pd.read_csv(area_file, index_col=0)
    df_staff = pd.read_csv(staff_file, index_col=0)
    
    # 3. เตรียมข้อมูล (กำจัดช่องว่างในชื่ออาคาร)
    cols = ['ประชาชื่น', 'ประดิพัทธ์', 'สาทร']
    df_area.columns = df_area.columns.str.strip()
    df_staff.columns = df_staff.columns.str.strip()
    
    # 4. ดึงข้อมูล
    prof_space = df_area.loc['Profitable Space', cols]
    df_staff = df_staff.loc[:, cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # 5. คำนวณ (ใช้ .div ให้หารกันตรงๆ ตามชื่อคอลัมน์)
    result_df = df_staff.div(prof_space, axis=1)
    
    # 6. ลบแถวที่เป็น 0 ออก (ตำแหน่งที่ไม่มีคน)
    final_df = result_df.replace(0, pd.NA).dropna(how='all').fillna(0)
    
    st.write("### ตารางประสิทธิภาพ (ตร.ม. ต่อพนักงาน 1 คน)")
    st.dataframe(final_df.style.format("{:.2f}"), use_container_width=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
    st.write("คำแนะนำ: โปรดเช็คชื่อไฟล์ในรายการที่โปรแกรมแสดงด้านบน ให้ตรงกับชื่อในบรรทัดที่ 12-13")
