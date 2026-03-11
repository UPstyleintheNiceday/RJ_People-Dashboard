import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 Dashboard สรุปประสิทธิภาพรายตำแหน่ง (Profitable Space)")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # โหลดข้อมูล
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # ดึงค่า Profitable Space ของทั้ง 3 อาคาร
    prof_space = df_area.loc['Profitable Space'] # ได้ค่า 3 อาคาร
    
    # ทำความสะอาดข้อมูลพนักงาน (ลบคอลัมน์ 'รวม' ออก)
    df_staff_clean = df_staff.drop(columns=['รวม'], errors='ignore')
    
    # คำนวณตารางประสิทธิภาพ (พื้นที่ทำกำไร / จำนวนพนักงาน)
    # ใช้ฟังก์ชัน div หารแบบจับคู่ชื่อคอลัมน์ (อาคาร) อัตโนมัติ
    result_df = df_staff_clean.div(prof_space)
    
    st.subheader("เปรียบเทียบพื้นที่ทำกำไรต่อพนักงาน 1 คน (ตร.ม./คน)")
    
    # แสดงตารางแบบจัดรูปแบบ (ไม่แสดงตำแหน่งที่พนักงานเป็น 0)
    st.dataframe(result_df.replace(0, pd.NA).dropna(how='all').style.format("{:.2f}"), use_container_width=True)
    
    st.write("---")
    st.subheader("กราฟเปรียบเทียบแต่ละอาคาร")
    st.bar_chart(result_df.replace(0, pd.NA).dropna(how='all'))

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
