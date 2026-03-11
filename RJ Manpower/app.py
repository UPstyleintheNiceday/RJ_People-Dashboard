import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 สรุปประสิทธิภาพ: ตร.ม. (Profitable) ต่อคน")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # 1. โหลดข้อมูล
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # 2. ทำความสะอาดชื่อคอลัมน์ (ลบช่องว่าง)
    df_area.columns = df_area.columns.str.strip()
    df_staff.columns = df_staff.columns.str.strip()
    
    # 3. เตรียมข้อมูล
    # ลบคอลัมน์ 'รวม' ออก
    df_staff = df_staff.drop(columns=['รวม'], errors='ignore')
    
    # *** จุดสำคัญ: เติมเลข 0 แทนช่องว่าง (NaN) ในตารางพนักงาน ***
    df_staff = df_staff.fillna(0)
    
    # ดึงค่า Profitable Space
    prof_space = df_area.loc['Profitable Space']
    
    # 4. คำนวณ (ใช้ชื่อคอลัมน์จับคู่กันเอง)
    # เราเลือกเฉพาะอาคารที่ชื่อตรงกับในตารางพื้นที่
    common_cols = [c for c in df_staff.columns if c in prof_space.index]
    result_df = df_staff[common_cols].div(prof_space[common_cols], axis=1)
    
    # 5. แสดงผล (เอาเลข 0 ออกให้ดูสะอาดตา)
    final_display = result_df.replace(0, pd.NA).dropna(how='all')
    
    st.write("### ตารางประสิทธิภาพ (ตร.ม. ทำกำไรต่อพนักงาน 1 คน)")
    st.dataframe(final_display.style.format("{:.2f}"), use_container_width=True)
    
    st.write("### กราฟเปรียบเทียบ")
    st.bar_chart(final_display)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
    st.write("ลองตรวจสอบว่าชื่ออาคารในตารางพนักงาน ตรงกับตารางพื้นที่")
