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

# 🌐 3. إعدادات الـ API الفنية المربوطة بمفتاحك وكأس العالم 2026
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
    params = {
        'league': league_id,
        'season': year
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        fetched_matches = []
        if "response" in data and len(data["response"]) > 0:
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
            return fetched_matches
        else:
            raise Exception("No data found")
    except Exception as e:
        # جدول احتياطي لأول مباراتين لضمان عدم توقف السستم إطلاقاً
        return [
            {"id": 1, "team_home": "المكسيك", "team_away": "جنوب أفريقيا", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz)},
            {"id": 10, "team_home": "السعودية", "team_away": "كندا", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz)}
        ]

matches = fetch_matches_from_api(API_KEY, LEAGUE_ID, CURRENT_YEAR)

# 4. بوابـة التحكم للمستخدمين
menu = ["تسجيل الدخول", "إنشاء حساب جديد (لأول مرة)"]
choice = st.radio("إختر الإجراء:", menu, horizontal=True)

# --- شاشة إنشاء الحساب الجديد ---
if choice == "إنشاء حساب جديد (لأول مرة)":
    st.subheader("📝 استمارة تسجيل مشارك جديد")
    with st.form("registration_form"):
        new_name = st.text_input("👤 الاسم الثنائي الكريم:")
        new_phone = st.text_input("📱 رقم الجوال (10 أرقام):", max_chars=10)
        new_pass = st.text_input("🔐 اختر كلمة مرور خاصة بحسابك (سرية):", type="password")
        submit_reg = st.form_submit_button("إرسال واعتماد الحساب في الحديقة 🚀")
        
        if submit_reg:
            new_phone = str(new_phone).strip()
            new_name = str(new_name).strip()
            new_pass = str(new_pass).strip()
            
            if not new_name or not new_phone or not new_pass:
                st.error("❌ فضلاً، يرجى تعبئة جميع الخانات.")
            elif len(new_phone) != 10 or not new_phone.isdigit():
                st.error("❌ رقم الجوال يجب أن يتكون من 10 أرقام فقط.")
            else:
                cursor = db_conn.cursor()
                cursor.execute("SELECT phone FROM users WHERE phone = ?", (new_phone,))
                if cursor.fetchone():
                    st.error(f"⚠️ خطأ: رقم الجوال مسجل مسبقاً!")
                else:
                    cursor.execute("INSERT INTO users (name, points, phone, password) VALUES (?, ?, ?,
