import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 สรุปประสิทธิภาพ: ตร.ม. (Profitable) ต่อคน")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # 1. โหลดข้อมูล
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # 2. ล้างชื่อคอลัมน์ให้สะอาด (ลบช่องว่าง)
    df_area.columns = df_area.columns.str.strip()
    df_staff.columns = df_staff.columns.str.strip()
    
    # 3. กำหนดอาคารที่เราต้องการ
    target_buildings = ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร']
    
    # 4. ดึงข้อมูลมาเฉพาะอาคารที่เราสนใจ และเรียงลำดับให้เหมือนกัน
    prof_space = df_area.loc['Profitable Space', target_buildings]
    df_staff_clean = df_staff[target_buildings]
    
    # 5. คำนวณ (ตอนนี้ชื่อคอลัมน์ตรงกันเป๊ะ ลำดับตรงกันเป๊ะ ตัวเลขจะออกมาแน่นอน)
    result_df = df_staff_clean.div(prof_space, axis=1)
    
    # 6. ลบแถวที่ว่างเปล่าทิ้ง
    result_df = result_df.dropna(how='all')
    # แทนค่า 0 ด้วยค่าว่างเพื่อความสวยงาม
    result_df = result_df.replace(0, pd.NA).dropna(how='all')

    st.write("### ตารางเปรียบเทียบ ตร.ม. (Profitable) ต่อพนักงาน 1 คน")
    st.dataframe(result_df.style.format("{:.2f}"), use_container_width=True)
    
    st.write("### กราฟเปรียบเทียบ")
    st.bar_chart(result_df)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
    st.write("ตรวจสอบไฟล์: ให้แน่ใจว่าในทั้งสอง Sheet มีชื่ออาคาร 'ประดิพัทธ์', 'ประชาชื่น', และ 'สาทร' อยู่ครบ")
