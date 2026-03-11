import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 สรุปประสิทธิภาพ: ตร.ม. (Profitable) ต่อคน")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # 1. โหลดข้อมูล
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # 2. ทำความสะอาดชื่ออาคาร
    df_area.columns = df_area.columns.str.strip()
    df_staff.columns = df_staff.columns.str.strip()
    
    # 3. เตรียมข้อมูลพนักงาน: บังคับให้เป็นตัวเลขทั้งหมด
    df_staff = df_staff.drop(columns=['รวม'], errors='ignore')
    # ใช้ pd.to_numeric เพื่อแปลงทุกอย่างเป็นตัวเลข ถ้าเจอช่องว่างให้เป็น 0
    df_staff = df_staff.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # 4. เตรียม Profitable Space
    prof_space = df_area.loc['Profitable Space']
    
    # 5. คำนวณ
    # ตอนนี้ df_staff เป็นตัวเลขล้วนๆ สามารถหารได้ทันที
    result_df = df_staff.div(prof_space, axis=1)
    
    # 6. ลบแถวที่ไม่มีคนเลย (คือเป็น 0 ในทุกสาขา)
    result_df = result_df.loc[~(result_df == 0).all(axis=1)]
    
    st.write("### ตารางประสิทธิภาพ (ตร.ม. ทำกำไร ต่อพนักงาน 1 คน)")
    st.dataframe(result_df.style.format("{:.2f}"), use_container_width=True)
    
    st.write("### กราฟเปรียบเทียบ")
    st.bar_chart(result_df)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
