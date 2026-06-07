import streamlit as st
from datetime import datetime, timedelta
import pytz
import pandas as pd
import sqlite3

# 1. إعداد المنطقة الزمنية وتنسيق الصفحة
ksa_tz = pytz.timezone('Asia/Riyadh')
now_ksa = datetime.now(ksa_tz)

st.set_page_config(page_title="كينق_الحديقة_المونديال#", page_icon="🌿", layout="centered")

# ✨ تصميم واجهة المستخدم (CSS) - هوية الحديقة الرقمية الفخمة (Dark Mode / Modern Sports UI)
st.markdown("""
    <style>
    /* تغيير خلفية التطبيق بالكامل للون الداكن */
    .stApp { background-color: #0b141a; color: #e9edef; }
    
    /* العنوان الرئيسي المطور */
    .main-title {
        color: #00a884; text-align: center; font-family: 'Arial', sans-serif;
        font-size: 38px; font-weight: bold; border-bottom: 3px solid #d4af37;
        padding-bottom: 15px; margin-bottom: 35px;
    }
    
    /* كروت المباريات بتصميم داكن وحواف مضيئة */
    .match-card {
        background-color: #16212a; border-radius: 18px; padding: 22px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4); border-right: 8px solid #00a884;
        margin-bottom: 25px; border-top: 1px solid #222d34; border-left: 1px solid #222d34;
    }
    
    /* لوحة الأدمن الملكية */
    .admin-card {
        background-color: #232d36; border-radius: 18px; padding: 22px;
        border-right: 8px solid #d4af37; margin-top: 35px; margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    /* كارت كشف التوقعات للشفافية */
    .review-card {
        background-color: #1f2c34; border-radius: 18px; padding: 22px;
        border-right: 8px solid #00a884; margin-top: 25px; margin-bottom: 25px;
    }
    
    /* تخصيص الأزرار لتصبح باللون الأخضر المميز وحواف دائرية */
    .stButton>button {
        background: linear-gradient(90deg, #00a884, #06cf9c) !important; 
        color: white !important; border-radius: 12px !important;
        width: 100% !important; font-weight: bold !important; height: 45px !important; 
        border: none !important; font-size: 16px !important;
        box-shadow: 0 4px 10px rgba(0, 168, 132, 0.3);
    }
    .stButton>button:hover { 
        background: linear-gradient(90deg, #06cf9c, #00a884) !important;
        border: 1px solid #d4af37 !important; 
    }
    
    /* نصوص العناوين والفقرات داخل الكروت */
    h3, h4, p, label { color: #e9edef !important; }
    .stMarkdown p { color: #e9edef; }
    
    /* تحسين شكل جداول البيانات الـ Dataframes لتهيئة وضع الدارك مود */
    .stDataFrame { background-color: #16212a; border-radius: 12px; overflow: hidden; }
    
    /* تخصيص حقول الإدخال لتتناسب مع الدارك مود */
    div[data-baseweb="input"] { background-color: #222d34 !important; border-radius: 10px !important; color: white !important; }
    input { color: white !important; }
    </style>
    <div class="main-title"> challenge_king_alhadeeqah_wc2026# 🏆</div>
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
        {"id": 302, "team_home": "الأرجنتين", "team_away": "كندا", "time": datetime(2026, 6, 24, 21, 0, tzinfo=ksa_tz)},
        {"id": 303, "team_home": "فرنسا", "team_away": "أستراليا", "time": datetime(2026, 6, 25, 18, 0, tzinfo=ksa_tz)},
        {"id": 304, "team_home": "إسبانيا", "team_away": "عُمان", "time": datetime(2026, 6, 25, 22, 0, tzinfo=ksa_tz)},
        {"id": 305, "team_home": "إنجلترا", "team_away": "كوريا الجنوبية", "time": datetime(2026, 6, 26, 19, 0, tzinfo=ksa_tz)},
        {"id": 306, "team_home": "ألمانيا", "team_away": "الكاميرون", "time": datetime(2026, 6, 26, 19, 0, tzinfo=ksa_tz)},
        {"id": 307, "team_home": "السعودية", "team_away": "كولومبيا", "time": datetime(2026, 6, 27, 21, 0, tzinfo=ksa_tz)},
        {"id": 308, "team_home": "إيطاليا", "team_away": "أوروجواي", "time": datetime(2026, 6, 27, 21, 0, tzinfo=ksa_tz)},
        {"id": 309, "team_home": "البرازيل", "team_away": "الجزائر", "time": datetime(2026, 6, 28, 18, 0, tzinfo=ksa_tz)},
        {"id": 310, "team_home": "البرتغال", "team_away": "كرواتيا", "time": datetime(2026, 6, 28, 22, 0, tzinfo=ksa_tz)},
    ]

all_matches = get_internal_matches()

# 4. بوابـة التحكم للمستخدمين
menu = ["تسجيل الدخول", "إنشاء حساب جديد (لأول مرة)"]
choice = st.radio("إختر الإجراء:", menu, horizontal=True)

# --- شاشة إنشاء الحساب الجديد ---
if choice == "إنشاء حساب جديد (لأول مرة)":
    st.subheader("📝 استمارة تسجيل مشارك جديد")
    with st.form("registration_form"):
        new_name = st.text_input("👤 الاسم :")
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
                    cursor.execute("INSERT INTO users (name, points, phone, password) VALUES (?, ?, ?, ?)", (new_name, 0, new_phone, new_pass))
                    db_conn.commit()
