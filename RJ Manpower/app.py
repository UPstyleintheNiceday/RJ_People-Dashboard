import streamlit as st
import pandas as pd

st.title("📊 รายงานประสิทธิภาพ: ตร.ม. (Profitable) ต่อคน")

try:
    # ระบุชื่อไฟล์หลักของคุณ
    file_path = 'data.xlsx'
    
    # โหลดแต่ละ Sheet แยกกัน โดยระบุชื่อ sheet_name
    # ตรวจสอบให้แน่ใจว่าชื่อ Tab ใน Excel ของคุณคือ 'พื้นที่' และ 'อัตรากำลัง' จริงๆ
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # 1. ทำความสะอาดชื่อคอลัมน์ (ลบช่องว่าง)
    df_area.columns = df_area.columns.str.strip()
    df_staff.columns = df_staff.columns.str.strip()
    
    # 2. ดึง Profitable Space (จาก Tab พื้นที่)
    prof_space = df_area.loc['Profitable Space']
    
    # 3. เตรียมตารางพนักงาน (ลบคอลัมน์ 'รวม' ออก)
    df_staff = df_staff.drop(columns=['รวม'], errors='ignore')
    # บังคับให้ข้อมูลเป็นตัวเลข ถ้าช่องไหนว่างให้เป็น 0
    df_staff = df_staff.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # 4. คำนวณ (ใช้ชื่ออาคารจับคู่กันหาร)
    # ผลลัพธ์ที่ได้จะเป็นตารางที่เปรียบเทียบทุกสาขาในหน้าเดียว
    result_df = df_staff.div(prof_space, axis=1)
    
    # 5. แสดงผลตาราง (ลบแถวที่เป็น 0 ทั้งหมดออกเพื่อให้ดูง่าย)
    final_display = result_df.replace(0, pd.NA).dropna(how='all').fillna(0)
    
    st.write("### ตารางประสิทธิภาพ (ตร.ม. ต่อพนักงาน 1 คน)")
    st.dataframe(final_display.style.format("{:.2f}"), use_container_width=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
    st.write("คำแนะนำ: ตรวจสอบว่าชื่อ Tab ในไฟล์ Excel ตรงกับ 'พื้นที่' และ 'อัตรากำลัง' (สะกดให้เป๊ะ)")
