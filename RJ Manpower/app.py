import streamlit as st
import pandas as pd

st.set_page_config(page_title="Profitable Space Dashboard", layout="wide")
st.title("📊 รายงานประสิทธิภาพพื้นที่ทำกำไร (Profitable Space Efficiency)")

try:
    file_path = 'RJ Manpower/data.xlsx'
    
    # 1. โหลดข้อมูล
    # เราใช้ index_col=0 เพื่อให้ชื่อตำแหน่ง/ชื่อพื้นที่ เป็นดัชนีของตาราง
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', index_col=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', index_col=0)
    
    # 2. ดึงค่า Profitable Space ของแต่ละพื้นที่
    # ผลลัพธ์: Series ที่มี index เป็นชื่ออาคาร
    profitable_space = df_area.loc['Profitable Space']
    
    # 3. เตรียมตารางข้อมูลพนักงาน (ลบคอลัมน์ 'รวม' ออกก่อน)
    df_staff_clean = df_staff.drop(columns=['รวม'], errors='ignore')
    
    # 4. คำนวณตารางประสิทธิภาพ (พื้นที่ทำกำไร / จำนวนพนักงาน)
    # เราจะคำนวณแยกทีละอาคารแล้วค่อยรวมเข้าด้วยกัน
    efficiency_df = pd.DataFrame()
    for col in df_staff_clean.columns:
        if col in profitable_space.index:
            # ใช้ .div เพื่อหารแบบจับคู่ตำแหน่งงาน
            efficiency_df[f'{col} (ตร.ม./คน)'] = df_staff_clean[col].div(profitable_space[col])
    
    # ลบแถวที่ไม่มีข้อมูลคนเลย (NaN) ออกเพื่อความสวยงาม
    efficiency_df = efficiency_df.dropna(how='all')
    
    # 5. แสดงผล Dashboard
    st.subheader("ประสิทธิภาพรายตำแหน่ง (พื้นที่ทำกำไรต่อพนักงาน 1 คน)")
    st.dataframe(efficiency_df.style.format("{:.2f}"), use_container_width=True)
    
    st.write("---")
    
    # 6. กราฟสรุป
    st.subheader("เปรียบเทียบพื้นที่รับผิดชอบต่อคน")
    st.bar_chart(efficiency_df)
    
    st.caption("หมายเหตุ: ค่าที่แสดงคือ จำนวนตารางเมตรของ Profitable Space ที่พนักงาน 1 คนในตำแหน่งนั้นๆ รับผิดชอบ")

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
    st.write("ตรวจสอบไฟล์ Excel: ตรวจสอบว่าชื่ออาคารในตารางพื้นที่ ตรงกับชื่ออาคารในตารางอัตรากำลัง")

