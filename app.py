import streamlit as st
from datetime import datetime, timedelta
import pytz
import sqlite3

# --- 1. الإعدادات والتهيئة ---
ksa_tz = pytz.timezone('Asia/Riyadh')
st.set_page_config(page_title="الحديقة 2026", layout="centered", page_icon="🌿")

# --- 2. التصميم (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b141a; color: #e9edef; }
    .match-card { background-color: #16212a; border-radius: 15px; padding: 15px; border-left: 5px solid #00a884; margin-bottom: 10px; }
    .stButton>button { background-color: #00a884 !important; color: white !important; border-radius: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. قاعدة البيانات ---
conn = sqlite3.connect('alhadeeqah.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, phone TEXT PRIMARY KEY, password TEXT, points INTEGER DEFAULT 0)')
c.execute('CREATE TABLE IF NOT EXISTS predictions (phone TEXT, match_id INTEGER, h INTEGER, a INTEGER, PRIMARY KEY(phone, match_id))')
c.execute('CREATE TABLE IF NOT EXISTS results (match_id INTEGER PRIMARY KEY, h INTEGER, a INTEGER)')
conn.commit()

# --- 4. دالة المباريات ---
def get_matches():
    return [
        {"id": 101, "h": "المكسيك", "a": "كندا", "date": datetime(2026, 6, 11, 22, 0)},
        {"id": 108, "h": "السعودية", "a": "أوروجواي", "date": datetime(2026, 6, 15, 20, 0)},
        # ... (أضف بقية المباريات هنا بنفس النمط)
    ]

# --- 5. منطق البرنامج ---
menu = st.sidebar.radio("القائمة:", ["المباريات", "الصدارة", "الإدارة"])

if menu == "المباريات":
    st.title("🌿 مباريات الحديقة")
    for m in get_matches():
        st.markdown(f'<div class="match-card"><h4>{m["h"]} VS {m["a"]}</h4></div>', unsafe_allow_html=True)
        # كود التوقع...

elif menu == "الصدارة":
    st.title("🏆 جدول الصدارة")
    # عرض الترتيب من قاعدة البيانات...

elif menu == "الإدارة":
    st.title("🛠️ لوحة الأدمن")
    # كود احتساب النقاط وتعديل النتائج...
