import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Manpower Dashboard", layout="wide")

st.title("📊 Manpower Analysis Dashboard")

# 2. ฟังก์ชันสำหรับโหลดข้อมูล
@st.cache_data
def load_data():
    # ตรวจสอบว่าชื่อไฟล์ตรงกับไฟล์ของคุณในโฟลเดอร์เดียวกันหรือไม่
    df = pd.read_excel('data.xlsx') 
    return df

try:
    df = load_data()
    
    # 3. ส่วนแสดงผลหลัก
    st.subheader("ตารางข้อมูล")
    st.dataframe(df) # โชว์ตารางข้อมูลดิบ
    
    # 4. ตัวอย่างการสร้างกราฟเบื้องต้น
    st.subheader("กราฟเปรียบเทียบ")
    if st.checkbox("แสดงกราฟแท่ง"):
        st.bar_chart(df) # เปลี่ยนชื่อคอลัมน์ให้ตรงกับไฟล์ของคุณถ้าต้องการระบุแกน
        
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {e}")
    st.info("ตรวจสอบให้แน่ใจว่าไฟล์ data.xlsx อยู่ในโฟลเดอร์เดียวกับ app.py")

