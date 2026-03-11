import streamlit as st
import pandas as pd

st.title("ตรวจสอบชื่อหัวตาราง")

# โหลดข้อมูลแบบไม่มี header ก่อน เพื่อให้เราเห็นว่าแถวไหนคือหัวตารางจริงๆ
df_area_raw = pd.read_excel('RJ Manpower/data.xlsx', sheet_name='พื้นที่', header=None)
st.write("### 5 แถวแรกของ Sheet 'พื้นที่' (หัวตารางจริงคือแถวไหน?):")
st.dataframe(df_area_raw.head(5))

# ถ้าคุณเห็นชื่อตึก 'ประดิพัทธ์' อยู่ที่แถวไหน ให้บอกผม หรือเปลี่ยน header ในโค้ด
# เช่น ถ้าตึกอยู่ที่แถวที่ 3 ให้เปลี่ยน header=2 (เพราะ index เริ่มที่ 0)
