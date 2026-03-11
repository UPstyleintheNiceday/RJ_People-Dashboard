import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 รายงานประสิทธิภาพ: พื้นที่ทำกำไรต่อพนักงาน 1 คน")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # โหลดข้อมูล
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # --- ขั้นตอนสำคัญ: ล้างชื่อคอลัมน์และดัชนี ---
    df_area.columns = df_area.columns.str.strip()
    df_staff.columns = df_staff.columns.str.strip()
    
    # ดึงค่า Profitable Space ออกมาเป็น Series
    prof_space = df_area.loc['Profitable Space']
    
    # ทำความสะอาดตารางพนักงาน (ลบคอลัมน์รวม และเติม 0 ให้ช่องว่าง)
    df_staff = df_staff.drop(columns=['รวม'], errors='ignore')
    df_staff = df_staff.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # --- คำนวณด้วยการจับคู่ชื่อคอลัมน์ (อาคาร) ---
    # โค้ดนี้จะเอา 'สาทร' หาร 'สาทร', 'ประชาชื่น' หาร 'ประชาชื่น' ให้อัตโนมัติ
    result_df = pd.DataFrame()
    for bldg in prof_space.index:
        if bldg in df_staff.columns:
            result_df[bldg] = df_staff[bldg] / prof_space[bldg]
            
    # ลบแถวที่เป็น 0 ทั้งหมดออก (ตำแหน่งที่ไม่มีคน)
    result_df = result_df.replace(0, pd.NA).dropna(how='all').fillna(0)
    
    st.write("### ตารางประสิทธิภาพ (หน่วย: ตร.ม. ทำกำไรต่อพนักงาน 1 คน)")
    st.dataframe(result_df.style.format("{:.2f}"), use_container_width=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
