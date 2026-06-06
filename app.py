import streamlit as st
from datetime import datetime, timedelta
import pytz
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. إعداد المنطقة الزمنية وتنسيق الصفحة
ksa_tz = pytz.timezone('Asia/Riyadh')
now_ksa = datetime.now(ksa_tz)

st.set_page_config(page_title="توقعات الحديقة 2026", page_icon="🌿", layout="centered")

# تصميم واجهة المستخدم (CSS) - هوية الحديقة الملكية
st.markdown("""
    <style>
    .stApp { background-color: #f4f9f4; }
    .main-title {
        color: #1e4620; text-align: center; font-family: 'Arial', sans-serif;
        font-size: 36px; font-weight: bold; border-bottom: 3px solid #d4af37;
        padding-bottom: 10px; margin-bottom: 30px;
    }
    .match-card {
        background-color: #ffffff; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-right: 10px solid #2e7d32;
        margin-bottom: 25px;
    }
    .stButton>button {
        background-color: #2e7d32; color: white; border-radius: 10px;
        width: 100%; font-weight: bold; height: 40px; border: none;
    }
    .stButton>button:hover { background-color: #1b5e20; border: 1px solid #d4af37; }
    </style>
    <div class="main-title">🌿 بوابـة الحديقة الرقمية الذكية 🏆</div>
    """, unsafe_allow_html=True)

# 2. إنشاء الاتصال التلقائي بـ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def get_sheet_data(worksheet_name):
    try:
        return conn.read(spreadsheet=st.secrets["public_gsheet_url"], worksheet=worksheet_name, ttl=0)
    except:
        return pd.DataFrame()

df_users = get_sheet_data("users")
df_preds = get_sheet_data("predictions")

# 3. جدول المباريات الثابتة
matches = [
    {"id": 1, "desc": "🇲🇽 المكسيك × جنوب أفريقيا 🇿🇦", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz), "actual_home": None, "actual_away": None},
    {"id": 2, "desc": "🇨🇭 سويسرا × قطر 🇶🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz), "actual_home": None, "actual_away": None},
    {"id": 3, "desc": "🇧🇷 البرازيل × المغرب 🇲🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz), "actual_home": None, "actual_away": None},
    {"id": 10, "desc": "🇸🇦 السعودية × كندا 🇨🇦 🔥", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz), "actual_home": None, "actual_away": None}
]

# 4. بوابـة التحكم (تبديل بين تسجيل الدخول وإنشاء حساب جديد)
menu = ["تسجيل الدخول", "إنشاء حساب جديد (لأول مرة)"]
choice = st.radio("إ
