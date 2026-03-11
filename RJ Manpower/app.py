import streamlit as st
import pandas as pd

st.set_page_config(page_title="RJ Manpower Dashboard", layout="wide")
st.title("📊 Manpower Efficiency Dashboard")

try:
    file_path = 'RJ Manpower/data.xlsx'
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', header=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', header=0)

    # รวมข้อมูลโดยระบุ suffixes เพื่อแยกพื้นที่กับคน
    df_combined = pd.merge(df_area, df_staff, left_on=df_area.columns[0], right_on=df_staff.columns[0], suffixes=('_พื้นที่', '_คน'))

    # เลือกอาคาร
    buildings = ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร']
    selected_bldg = st.selectbox("เลือกอาคารที่ต้องการเปรียบเทียบ:", buildings)

    # คำนวณ (ใช้ชื่อคอลัมน์ใหม่ที่ระบุชัดเจน)
    # พื้นที่มาจากตึก_พื้นที่ / จำนวนคนมาจากตึก_คน
    df_combined['ตร.ม. ต่อคน'] = df_combined[f'{selected_bldg}_พื้นที่'] / df_combined[f'{selected_bldg}_คน']

    # แสดงผล
    st.subheader(f"ประสิทธิภาพ: อาคาร {selected_bldg}")
    st.dataframe(df_combined[['สาขา', f'{selected_bldg}_พื้นที่', f'{selected_bldg}_คน', 'ตร.ม. ต่อคน']])

    # กราฟ
    st.bar_chart(df_combined.set_index('สาขา')['ตร.ม. ต่อคน'])

except Exception as e:
    st.error(f"เกิดข้อผิดพลาด: {e}")
import streamlit as st
import pandas as pd

st.set_page_config(page_title="RJ Manpower Dashboard", layout="wide")
st.title("📊 Manpower Efficiency Dashboard")

try:
    # 1. โหลดข้อมูล (ใช้ header=0 เพราะหัวตารางอยู่ที่แถวแรกสุด)
    file_path = 'RJ Manpower/data.xlsx'
    df_area = pd.read_excel(file_path, sheet_name='พื้นที่', header=0)
    df_staff = pd.read_excel(file_path, sheet_name='อัตรากำลัง', header=0)

    # 2. ทำความสะอาดข้อมูล
    # เปลี่ยนชื่อคอลัมน์แรกให้เป็น 'ชื่อพื้นที่' เพื่อใช้ Merge
    df_area = df_area.rename(columns={df_area.columns[0]: 'ชื่อพื้นที่'})
    # ตรวจสอบชื่อตำแหน่งใน Sheet อัตรากำลัง (สมมติว่าคอลัมน์แรกชื่อ 'ชื่อตำแหน่ง')
    df_staff = df_staff.rename(columns={df_staff.columns[0]: 'ชื่อตำแหน่ง'})

    # 3. รวมข้อมูล (Merge)
    # เชื่อมตารางด้วยคอลัมน์ชื่อตำแหน่ง/พื้นที่ (คุณอาจต้องตรวจสอบว่าคอลัมน์ไหนที่เหมือนกัน)
    df_combined = pd.merge(df_area, df_staff, left_on='ชื่อพื้นที่', right_on='ชื่อตำแหน่ง')

    # 4. เลือกอาคาร
    buildings = ['ประดิพัทธ์', 'ประชาชื่น', 'สาทร']
    selected_bldg = st.selectbox("เลือกอาคารที่ต้องการเปรียบเทียบ:", buildings)

    # 5. คำนวณประสิทธิภาพ (พื้นที่ / จำนวนคน)
    # สมมติคอลัมน์จำนวนคนชื่อ 'จำนวนคน'
    col_man = 'จำนวนคน'
    df_combined['ตร.ม. ต่อคน'] = df_combined[selected_bldg] / df_combined[col_man]

    # 6. แสดงผล Dashboard
    st.subheader(f"ประสิทธิภาพพื้นที่ต่อคน: อาคาร {selected_bldg}")
    st.dataframe(df_combined[['ชื่อตำแหน่ง', selected_bldg, col_man, 'ตร.ม. ต่อคน']].style.format({"ตร.ม. ต่อคน": "{:.2f}"}))

    # 7. กราฟเปรียบเทียบ
    st.bar_chart(df_combined.set_index('ชื่อตำแหน่ง')['ตร.ม. ต่อคน'])
    
    st.caption("หมายเหตุ: ค่าสูงแสดงถึงภาระพื้นที่ต่อพนักงาน 1 คนที่สูงกว่า")

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดหรือคำนวณ: {e}")
    st.write("ลองตรวจสอบว่าชื่อคอลัมน์ในไฟล์ Excel ตรงกับที่ระบุในโค้ด (เช่น 'จำนวนคน') หรือไม่")
