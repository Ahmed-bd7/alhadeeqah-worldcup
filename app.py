import streamlit as st
from datetime import datetime, timedelta
import pytz
import pandas as pd
import sqlite3

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
    .admin-card {
        background-color: #fff3cd; border-radius: 15px; padding: 20px;
        border-right: 10px solid #ffc107; margin-top: 30px; margin-bottom: 20px;
    }
    .review-card {
        background-color: #e8f5e9; border-radius: 15px; padding: 20px;
        border-right: 10px solid #00c853; margin-top: 20px; margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #2e7d32; color: white; border-radius: 10px;
        width: 100%; font-weight: bold; height: 40px; border: none;
    }
    .stButton>button:hover { background-color: #1b5e20; border: 1px solid #d4af37; }
    </style>
    <div class="main-title">🌿 بوابـة الحديقة الرقمية الذكية 🏆</div>
    """, unsafe_allow_html=True)

# 2. إنشاء وإعداد قاعدة البيانات المحلية 
def init_db():
    conn = sqlite3.connect('alhadeeqah_db.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            phone TEXT PRIMARY KEY,
            password TEXT DEFAULT '1234'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            phone TEXT,
            match_id INTEGER,
            pred_home INTEGER,
            pred_away INTEGER,
            PRIMARY KEY (phone, match_id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_matches (
            match_id INTEGER PRIMARY KEY,
            actual_home INTEGER,
            actual_away INTEGER
        )
    ''')
    try:
        cursor.execute("ALTER TABLE processed_matches ADD COLUMN actual_home INTEGER")
        cursor.execute("ALTER TABLE processed_matches ADD COLUMN actual_away INTEGER")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    return conn

db_conn = init_db()

# رقم أدمن الحديقة الثابت
ADMIN_PHONE = "0502518301" 

# 🗓️ 3. الجدول الكامل للمباريات (مترجم وبتوقيت مكة المكرمة)
def get_internal_matches():
    return [
        # --- الجولة الأولى الافتتاحية ---
        {"id": 101, "team_home": "المكسيك", "team_away": "كندا", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz)},
        {"id": 102, "team_home": "أمريكا", "team_away": "عُمان", "time": datetime(2026, 6, 12, 1, 0, tzinfo=ksa_tz)},
        {"id": 103, "team_home": "الأرجنتين", "team_away": "المغرب", "time": datetime(2026, 6, 13, 18, 0, tzinfo=ksa_tz)},
        {"id": 104, "team_home": "فرنسا", "team_away": "أستراليا", "time": datetime(2026, 6, 13, 21, 0, tzinfo=ksa_tz)},
        {"id": 105, "team_home": "إسبانيا", "team_away": "نيجيريا", "time": datetime(2026, 6, 14, 16, 0, tzinfo=ksa_tz)},
        {"id": 106, "team_home": "إنجلترا", "team_away": "الكاميرون", "time": datetime(2026, 6, 14, 19, 0, tzinfo=ksa_tz)},
        {"id": 107, "team_home": "ألمانيا", "team_away": "كوريا الجنوبية", "time": datetime(2026, 6, 14, 22, 0, tzinfo=ksa_tz)},
        {"id": 108, "team_home": "السعودية", "team_away": "أوروجواي", "time": datetime(2026, 6, 15, 20, 0, tzinfo=ksa_tz)},
        {"id": 109, "team_home": "إيطاليا", "team_away": "كولومبيا", "time": datetime(2026, 6, 15, 23, 0, tzinfo=ksa_tz)},
        {"id": 110, "team_home": "البرازيل", "team_away": "اليابان", "time": datetime(2026, 6, 16, 18, 0, tzinfo=ksa_tz)},
        {"id": 111, "team_home": "بلجيكا", "team_away": "الجزائر", "time": datetime(2026, 6, 16, 21, 0, tzinfo=ksa_tz)},
        {"id": 112, "team_home": "البرتغال", "team_away": "تونس", "time": datetime(2026, 6, 17, 16, 0, tzinfo=ksa_tz)},
        {"id": 113, "team_home": "هولندا", "team_away": "الإكوادور", "time": datetime(2026, 6, 17, 19, 0, tzinfo=ksa_tz)},
        {"id": 114, "team_home": "كرواتيا", "team_away": "مصر", "time": datetime(2026, 6, 17, 22, 0, tzinfo=ksa_tz)},
        
        # --- الجولة الثانية ---
        {"id": 201, "team_home": "المكسيك", "team_away": "الأرجنتين", "time": datetime(2026, 6, 18, 21, 0, tzinfo=ksa_tz)},
        {"id": 202, "team_home": "فرنسا", "team_away": "المغرب", "time": datetime(2026, 6, 19, 18, 0, tzinfo=ksa_tz)},
        {"id": 203, "team_home": "أمريكا", "team_away": "إسبانيا", "time": datetime(2026, 6, 19, 22, 0, tzinfo=ksa_tz)},
        {"id": 204, "team_home": "إنجلترا", "team_away": "ألمانيا", "time": datetime(2026, 6, 20, 19, 0, tzinfo=ksa_tz)},
        {"id": 205, "team_home": "السعودية", "team_away": "إيطاليا", "time": datetime(2026, 6, 21, 21, 0, tzinfo=ksa_tz)},
        {"id": 206, "team_home": "البرازيل", "team_away": "بلجيكا", "time": datetime(2026, 6, 22, 18, 0, tzinfo=ksa_tz)},
        {"id": 207, "team_home": "البرتغال", "team_away": "هولندا", "time": datetime(2026, 6, 22, 22, 0, tzinfo=ksa_tz)},
        {"id": 208, "team_home": "أوروجواي", "team_away": "كولومبيا", "time": datetime(2026, 6, 23, 20, 0, tzinfo=ksa_tz)},
        
        # --- الجولة الثالثة الحاسمة ---
        {"id": 301, "team_home": "المكسيك", "team_away": "المغرب", "time": datetime(2026, 6, 24, 21, 0, tzinfo=ksa_tz)},
        {"id
