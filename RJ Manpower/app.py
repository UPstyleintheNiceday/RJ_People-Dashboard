import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 สรุปประสิทธิภาพ: ตร.ม. (Profitable) ต่อคน")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # 1. โหลดข้อมูล
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # 2. ดึงค่า Profitable Space ของทั้ง 3 อาคาร
    # ใช้ .loc ดึงค่าตรงๆ จากแถว 'Profitable Space'
    prof_space = df_area.loc['Profitable Space']
    
    # 3. จัดการข้อมูลพนักงาน
    # ลบคอลัมน์ 'รวม' ออก และลบแถวที่เป็นค่าว่าง (NaN) ออกทั้งหมด
    df_staff_clean = df_staff.drop(columns=['รวม'], errors='ignore').dropna(how='all')
    
    # 4. คำนวณ (ใช้ .div จับคู่ชื่ออาคารให้อัตโนมัติ)
    # result_df จะได้ตารางที่มี อาคารเป็นคอลัมน์ และตำแหน่งเป็นแถว
    result_df = df_staff_clean.div(prof_space)
    
    # แทนค่า 0 หรือค่าว่างที่เกิดจากการไม่มีพนักงาน ให้เป็น NaN เพื่อไม่ให้กราฟเพี้ยน
    result_df = result_df.replace(0, pd.NA).dropna(how='all')

    # 5. แสดงผลตารางสรุป
    st.subheader("ตารางสรุป: ตร.ม. ต่อคน (ตามตำแหน่ง)")
    st.dataframe(result_df.style.format("{:.2f}"), use_container_width=True)
    
    # 6. แสดงกราฟเปรียบเทียบ
    st.subheader("กราฟเปรียบเทียบ 3 พื้นที่")
    st.bar_chart(result_df)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
    st.write("คำแนะนำ: ตรวจสอบว่าในไฟล์ Excel ทั้งสอง Sheet มีหัวคอลัมน์เป็น 'สาทร', 'ประดิพัทธ์', 'ประชาชื่น' ตรงกัน")
