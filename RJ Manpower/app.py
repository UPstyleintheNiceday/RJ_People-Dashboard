import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 รายงานประสิทธิภาพการใช้พื้นที่")

try:
    # 1. ใช้ pd.read_csv ตามประเภทไฟล์ที่คุณอัปโหลดเข้ามา
    df_area = pd.read_csv('data.xlsx - พื้นที่.csv', index_col=0)
    df_staff = pd.read_csv('data.xlsx - อัตรากำลัง.csv', index_col=0)
    
    # 2. ทำความสะอาดชื่อคอลัมน์
    df_area.columns = df_area.columns.str.strip()
    df_staff.columns = df_staff.columns.str.strip()
    
    # 3. ดึงค่า Profitable Space
    # ลองพิมพ์ df_area ออกมาดูจะเห็นว่าอยู่ใน index แรก
    prof_space = df_area.loc['Profitable Space']
    
    # 4. ลบ 'รวม' ออก และจัดการค่าว่าง
    df_staff = df_staff.drop(columns=['รวม'], errors='ignore')
    df_staff = df_staff.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # 5. คำนวณรายสาขาโดยตรง (ป้องกันปัญหาการจับคู่คอลัมน์อัตโนมัติ)
    # เราจะสร้างตารางผลลัพธ์ใหม่โดยหารทีละอาคาร
    result_df = pd.DataFrame(index=df_staff.index)
    
    for bldg in ['ประชาชื่น', 'ประดิพัทธ์', 'สาทร']:
        if bldg in df_staff.columns and bldg in prof_space.index:
            # พื้นที่ทำกำไร / จำนวนคน (ถ้าจำนวนคนเป็น 0 ผลลัพธ์จะเป็น inf)
            # เราจะเปลี่ยน inf เป็น 0 หรือค่าว่างเพื่อให้แสดงผลได้
            val = df_staff[bldg] / prof_space[bldg]
            result_df[bldg] = val.replace([float('inf'), -float('inf')], 0)

    # 6. ลบแถวที่ไม่มีข้อมูลเลยออก
    final_df = result_df.loc[~(result_df == 0).all(axis=1)]
    
    st.write("### ตารางประสิทธิภาพ (ตร.ม. ต่อคน)")
    st.dataframe(final_df.style.format("{:.2f}"), use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
    # ใช้เพื่อ Debug ว่าโปรแกรมมองเห็นชื่ออะไรบ้าง
    st.write("เช็คชื่อคอลัมน์ในตารางพนักงาน:", df_staff.columns.tolist())
    st.write("เช็คชื่อคอลัมน์ในตารางพื้นที่:", df_area.columns.tolist())
