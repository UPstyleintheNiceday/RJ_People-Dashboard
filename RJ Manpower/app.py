import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 ตารางสรุปพื้นที่ Profitable (ตร.ม./คน)")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # โหลดไฟล์
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # --- ขั้นตอนสำคัญ: ล้างชื่อคอลัมน์และดัชนี ---
    df_area.columns = df_area.columns.str.strip()
    df_staff.columns = df_staff.columns.str.strip()
    df_staff = df_staff.drop(columns=['รวม'], errors='ignore')
    
    # ดึงค่า Profitable Space
    prof_space = df_area.loc['Profitable Space']
    
    # คำนวณ (ใช้ .div ให้ค่าที่ตรงชื่อคอลัมน์หารกันโดยอัตโนมัติ)
    # ฟังก์ชันนี้จะเอาค่าใน df_staff หารด้วยค่าใน prof_space ตามชื่ออาคารที่ตรงกัน
    result_df = df_staff.div(prof_space, axis=1)
    
    # ตัดแถวที่เป็น 0 หรือว่างเปล่าทิ้ง
    result_df = result_df.replace(0, pd.NA).dropna(how='all')

    st.write("### ตารางประสิทธิภาพ (หน่วย: ตร.ม. ทำกำไรต่อพนักงาน 1 คน)")
    st.dataframe(result_df.style.format("{:.2f}"), use_container_width=True)
    
    st.write("---")
    st.bar_chart(result_df)

except Exception as e:
    st.error(f"Error: {e}")
    st.write("ลองเช็คว่าชื่ออาคารในไฟล์ Excel สะกดตรงกันทั้งสอง Sheet นะครับ")
