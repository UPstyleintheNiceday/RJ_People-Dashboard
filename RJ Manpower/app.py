import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 สรุปประสิทธิภาพ: ตร.ม. (Profitable) ต่อคน")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # 1. โหลดข้อมูลโดยให้คอลัมน์แรกเป็น Index (ชื่อตำแหน่ง/ชื่อพื้นที่)
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # 2. ดึงค่า Profitable Space ของทั้ง 3 อาคาร
    prof_space = df_area.loc['Profitable Space']
    
    # 3. ลบคอลัมน์ 'รวม' ออกจากตารางพนักงาน (ถ้ามี)
    df_staff_clean = df_staff.drop(columns=['รวม'], errors='ignore')
    
    # 4. คำนวณ (ใช้ .div จับคู่ชื่ออาคารโดยอัตโนมัติ)
    # ฟังก์ชันนี้จะเอาค่าใน df_staff หารด้วย prof_space ตามชื่อคอลัมน์
    result_df = df_staff_clean.div(prof_space, axis=1)
    
    # 5. ทำความสะอาดตาราง (ลบแถวที่ไม่มีข้อมูลพนักงานออก)
    result_df = result_df.replace(0, pd.NA).dropna(how='all')

    st.write("### ตารางประสิทธิภาพ (หน่วย: ตร.ม. ทำกำไรต่อพนักงาน 1 คน)")
    st.dataframe(result_df.style.format("{:.2f}"), use_container_width=True)
    
    st.write("### กราฟเปรียบเทียบแต่ละอาคาร")
    st.bar_chart(result_df)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
