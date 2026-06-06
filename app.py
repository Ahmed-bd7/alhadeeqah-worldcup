import streamlit as st
from datetime import datetime, timedelta
import pytz
import pandas as pd
import sqlite3
import requests

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
            match_id INTEGER PRIMARY KEY
        )
    ''')
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN password TEXT DEFAULT '1234'")
        conn.commit()
    except sqlite3.OperationalError:
        pass 
    return conn

db_conn = init_db()

# رقم أدمن الحديقة الثابت
ADMIN_PHONE = "0502518301" 

# 🌐 3. إعدادات الـ API الفنية المربوطة بمفتاحك وكأس العالم
API_KEY = "3a57379657b569a7a6abe3176fe85b10"  # مفتاح أحمد المعتمد
LEAGUE_ID = 1  # كود كأس العالم الرسمي
CURRENT_YEAR = 2026

@st.cache_data(ttl=300)  # تحديث ذكي كل 5 دقائق
def fetch_matches_from_api(api_key, league_id, year):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    
    # حلقة ذكية للبحث في تصنيفات المواسم المختلفة لتأكيد جلب مباريات الـ 48 فريق كاملة
    for season in [year, year-1, year-2]:
        try:
            params = {'league': league_id, 'season': season}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            if "response" in data and len(data["response"]) > 0:
                fetched_matches = []
                for item in data["response"]:
                    fixture = item["fixture"]
                    teams = item["teams"]
                    
                    # تحويل وقت الفيفا العالمي (UTC) إلى توقيت المملكة (KSA) أوتوماتيكياً
                    utc_time = datetime.strptime(fixture["date"], "%Y-%m-%dT%H:%M:%S%z")
                    ksa_time = utc_time.astimezone(ksa_tz)
                    
                    fetched_matches.append({
                        "id": fixture["id"],
                        "team_home": teams["home"]["name"],
                        "team_away": teams["away"]["name"],
                        "time": ksa_time
                    })
                fetched_matches.sort(key=lambda x: x["time"])
                return fetched
