import streamlit as st
import pandas as pd

st.set_page_config(page_title="Manpower Dashboard", layout="wide")
st.title("📊 พื้นที่ดูแลต่อพนักงาน 1 คน (Sq.m. per Person)")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # 1. โหลดข้อมูล
    # Sheet พื้นที่: แถวแรกคือหัวคอลัมน์ (อาคาร)
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    # Sheet อัตรากำลัง: ตำแหน่งอยู่แถวแรก
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # 2. ปรับโครงสร้างข้อมูลอัตรากำลังให้พร้อมคำนวณ
    # ใช้ .drop เพื่อเอาคอลัมน์ 'รวม' ออกก่อน
    df_staff_clean = df_staff.drop(columns=['รวม'], errors='ignore')
    
    # 3. สร้าง Dashboard
    st.subheader("เลือกอาคารที่ต้องการเปรียบเทียบ:")
    building = st.selectbox("อาคาร:", ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร'])
    
    # ดึงค่าพื้นที่รวมจาก Sheet พื้นที่ (Total Space)
    total_area_val = df_area.loc['Total Space', building]
    
    # ดึงจำนวนคนในอาคารนั้นๆ จาก Sheet อัตรากำลัง
    staff_data = df_staff_clean[[building]].rename(columns={building: 'จำนวนคน'})
    
    # 4. คำนวณ (พื้นที่อาคาร หารด้วย จำนวนคนในตำแหน่งนั้น)
    # หมายเหตุ: ในกรณีนี้เราเปรียบเทียบจากพื้นที่รวมของอาคาร
    staff_data['พื้นที่ต่อคน (ตร.ม.)'] = total_area_val / staff_data['จำนวนคน']
    
    # 5. แสดงผล
    st.write(f"### พื้นที่อาคาร {building} ทั้งหมด: {total_area_val:,.2f} ตร.ม.")
    
    # แสดงตารางผลลัพธ์
    st.dataframe(staff_data.style.format({"พื้นที่ต่อคน (ตร.ม.)": "{:.2f}"}), use_container_width=True)
    
    # แสดงกราฟ
    st.bar_chart(staff_data['พื้นที่ต่อคน (ตร.ม.)'])

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการประมวลผล: {e}")
    st.write("ตรวจสอบให้แน่ใจว่าชื่ออาคารใน Sheet ทั้งสองตรงกัน และไม่มีช่องว่างแปลกปลอมครับ")
