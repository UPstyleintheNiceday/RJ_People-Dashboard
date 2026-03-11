import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้า Dashboard
st.set_page_config(page_title="Manpower Dashboard", layout="wide")
st.title("📊 Manpower Efficiency Dashboard")

# 2. โหลดข้อมูล
try:
    df = pd.read_excel('RJ Manpower/data.xlsx')
    
    # --- ส่วนสำคัญ: แก้ไขชื่อคอลัมน์ให้ตรงกับไฟล์ Excel ของคุณ ---
    # ให้ดูชื่อในไฟล์ Excel แล้วนำมาพิมพ์ใส่ใน '...' ให้เหมือนเป๊ะๆ
    col_pos = 'ชื่อตำแหน่ง'     # <--- แก้ไขจุดนี้
    col_area = 'พื้นที่ (ตร.ม.)' # <--- แก้ไขจุดนี้
    col_man = 'จำนวนพนักงาน'     # <--- แก้ไขจุดนี้
    # -----------------------------------------------------

    # ตรวจสอบว่าชื่อคอลัมน์มีอยู่จริงไหม
    if all(col in df.columns for col in [col_pos, col_area, col_man]):
        
        # 3. คำนวณประสิทธิภาพ
        # กรองเฉพาะแถวที่มีพนักงานมากกว่า 0 เพื่อป้องกัน Error หารด้วย 0
        df = df[df[col_man] > 0].copy()
        df['Area_Per_Man'] = df[col_area] / df[col_man]

        # 4. แสดงผล
        st.subheader("เปรียบเทียบพื้นที่ดูแลต่อพนักงาน 1 คน")
        
        # แสดงตาราง
        st.dataframe(df[[col_pos, col_area, col_man, 'Area_Per_Man']].style.format({"Area_Per_Man": "{:.2f}"}))

        # แสดงกราฟ
        st.subheader("กราฟเปรียบเทียบภาระงาน")
        st.bar_chart(df.set_index(col_pos)['Area_Per_Man'])
        
        st.caption("หมายเหตุ: ค่าที่แสดงคือจำนวนตารางเมตรที่พนักงาน 1 คนต้องดูแล (ยิ่งสูงยิ่งหนัก)")

    else:
        st.error("ชื่อคอลัมน์ในโค้ดไม่ตรงกับในไฟล์ Excel!")
        st.write("รายชื่อคอลัมน์ที่ระบบอ่านได้จากไฟล์คือ:", df.columns.tolist())

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
    
