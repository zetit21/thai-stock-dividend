import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="Dividend Run-up Tracker", layout="wide")

# ข้อมูลหุ้นที่คัดมาแล้วว่า Win Rate > 80% ในรอบ 5 ปี
# (จำลองข้อมูล XD โดยประมาณของปี 2026 เพื่อใช้แสดงผลบน Dashboard)
data = [
    {"Symbol": "LH", "Estimated_XD": "2026-08-25", "Win_Rate": "90%", "Avg_Runup": "6.2%"},
    {"Symbol": "ADVANC", "Estimated_XD": "2026-08-15", "Win_Rate": "85%", "Avg_Runup": "5.5%"},
    {"Symbol": "KKP", "Estimated_XD": "2026-09-10", "Win_Rate": "80%", "Avg_Runup": "7.1%"},
    {"Symbol": "SPALI", "Estimated_XD": "2026-08-20", "Win_Rate": "80%", "Avg_Runup": "6.8%"},
    {"Symbol": "TISCO", "Estimated_XD": "2026-04-28", "Win_Rate": "95%", "Avg_Runup": "5.0%"}, # ผ่านไปแล้ว
]

df = pd.DataFrame(data)
df['Estimated_XD'] = pd.to_datetime(df['Estimated_XD'])
df['Entry_Date'] = df['Estimated_XD'] - timedelta(days=60)
df['Exit_Before'] = df['Estimated_XD'] - timedelta(days=1)

# --- DASHBOARD UI ---
st.title("📈 Dividend Run-up Dashboard (Thailand 2026)")
st.markdown(f"**Current Date:** {datetime.now().strftime('%d %B 2026')}")
st.divider()

# สร้างแถวสำหรับการแจ้งเตือน (Alerts)
col1, col2, col3 = st.columns(3)

# คำนวณสถานะ
today = datetime.now()

with col1:
    # หุ้นที่อยู่ในช่วง "ควรซื้อ" (Entry Window)
    to_buy = df[(df['Entry_Date'] <= today) & (today < df['Estimated_XD'])]
    st.success(f"🟢 BUY ZONE ({len(to_buy)} Stocks)")
    for s in to_buy['Symbol']:
        st.write(f"**{s}** - เป้าหมายกำไร 5-7%")

with col2:
    # หุ้นที่ใกล้จะ XD (เตรียมขาย)
    to_sell = df[(df['Estimated_XD'] - timedelta(days=7) <= today) & (today < df['Estimated_XD'])]
    st.warning(f"🟡 TAKE PROFIT ZONE ({len(to_sell)} Stocks)")
    for s in to_sell['Symbol']:
        st.write(f"**{s}** - ขายก่อน XD 1 วัน")

with col3:
    st.info("📊 Strategy Rule")
    st.write("1. เข้าซื้อล่วงหน้า 60 วัน")
    st.write("2. ตั้ง TP 5-7% ทันที")
    st.write("3. ขายทิ้งก่อนวัน XD เสมอ")

st.divider()

# --- ตารางแผนการลงทุนตลอดปี 2026 ---
st.subheader("📅 แผนการปฏิบัติงาน (Dividend Calendar 2026)")

# ปรับแต่งตารางให้ดูง่าย
display_df = df.copy()
display_df['Entry_Date'] = display_df['Entry_Date'].dt.strftime('%d/%m/%Y')
display_df['Estimated_XD'] = display_df['Estimated_XD'].dt.strftime('%d/%m/%Y')
display_df = display_df[['Symbol', 'Win_Rate', 'Entry_Date', 'Estimated_XD', 'Avg_Runup']]
display_df.columns = ['ชื่อหุ้น', 'ความแม่นยำ', 'วันที่เริ่มเก็บ (60 วันก่อน)', 'วันที่ขึ้น XD', 'กำไรเฉลี่ยในอดีต']

st.table(display_df.sort_values(by='วันที่ขึ้น XD'))

st.caption("หมายเหตุ: ข้อมูลวันที่ XD เป็นการประมาณการจากสถิติย้อนหลัง 5 ปี โปรดตรวจสอบวันประกาศจริงจาก SET อีกครั้ง")
