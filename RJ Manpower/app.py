import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 Profitable Space Efficiency Dashboard")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # โหลดโดยให้คอลัมน์แรกเป็น Index
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # เลือกอาคาร
    buildings = ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร']
    selected_bldg = st.selectbox("เลือกอาคาร:", buildings)
    
    # 1. ดึงค่า Profitable Space ของอาคารที่เลือก
    # ใช้ .loc[แถว, คอลัมน์]
    prof_space = df_area.loc['Profitable Space', selected_bldg]
    
    # 2. ดึงข้อมูลพนักงานของอาคารที่เลือก
    staff_data = df_staff[[selected_bldg]].rename(columns={selected_bldg: 'จำนวนคน'})
    
    # 3. คำนวณ (ใช้ค่าเดียวหารทั้งคอลัมน์)
    staff_data['ตร.ม./คน'] = prof_space / staff_data['จำนวนคน']
    
    st.write(f"### พื้นที่ Profitable Space ของ {selected_bldg}: {prof_space:,.2f} ตร.ม.")
    
    # แสดงตารางและตัดค่าที่ไม่มีพนักงาน (0) ออก
    final_df = staff_data[staff_data['จำนวนคน'] > 0]
    st.dataframe(final_df.style.format({'ตร.ม./คน': '{:.2f}'}))
    
    st.bar_chart(final_df['ตร.ม./คน'])

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
    st.write("ตรวจสอบชื่ออาคารใน Excel ว่าตรงกับในโค้ดหรือไม่ (เช่น ประดิพัทธ์, ประชาชื่น, สาทร)")
