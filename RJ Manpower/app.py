import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 สรุปเปรียบเทียบประสิทธิภาพรายอาคาร")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # โหลดไฟล์
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # 1. ทำความสะอาดชื่ออาคาร
    df_area.columns = df_area.columns.str.strip()
    df_staff.columns = df_staff.columns.str.strip()
    
    # 2. ดึง Profitable Space (มี 3 ค่า)
    prof_space = df_area.loc['Profitable Space']
    
    # 3. เตรียมตารางพนักงาน
    df_staff = df_staff.drop(columns=['รวม'], errors='ignore')
    
    # *** เติม 0 แทนช่องว่าง เพื่อให้คำนวณได้ ***
    df_staff = df_staff.fillna(0)
    
    # 4. คำนวณ (ใช้ .div จับคู่ชื่ออาคาร)
    # ถ้าตำแหน่งไหนไม่มีคน (เป็น 0) ผลลัพธ์จะเป็น 0 หรือ inf แทนที่จะหายไป
    result_df = df_staff.div(prof_space, axis=1)
    
    # 5. ล้างแถวที่เป็น 0 ทั้งหมดออก (ตำแหน่งที่ไม่มีคนในทุกสาขา)
    result_df = result_df.replace(0, pd.NA).dropna(how='all').fillna(0)
    
    st.write("### ตารางประสิทธิภาพ (ตร.ม. ทำกำไร ต่อพนักงาน 1 คน)")
    st.dataframe(result_df.style.format("{:.2f}"), use_container_width=True)
    
    st.bar_chart(result_df)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
