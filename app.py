# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime, timedelta
import pytz
import pandas as pd
import sqlite3
import urllib.parse

# 1. إعداد المنطقة الزمنية وتنسيق الصفحة
ksa_tz = pytz.timezone('Asia/Riyadh')
now_ksa = datetime.now(ksa_tz)

st.set_page_config(page_title="⚽🏆 WC26 KING", page_icon="", layout="centered")

FLAGS = {
    "السعودية":"🇸🇦","الأرجنتين":"🇦🇷","البرازيل":"🇧🇷","فرنسا":"🇫🇷","ألمانيا":"🇩🇪",
    "إسبانيا":"🇪🇸","البرتغال":"🇵🇹","إنجلترا":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","اسكتلندا":"🏴󠁧󠁢󠁳󠁣󠁴󠁿","المغرب":"🇲🇦",
    "الجزائر":"🇩🇿","تونس":"🇹🇳","مصر":"🇪🇬","قطر":"🇶🇦","المكسيك":"🇲🇽",
    "الولايات المتحدة":"🇺🇸","كندا":"🇨🇦","أستراليا":"🇦🇺","تركيا":"🇹🇷","سويسرا":"🇨🇭",
    "التشيك":"🇨🇿","كوريا الجنوبية":"🇰🇷","باراغواي":"🇵🇾","هايتي":"🇭🇹","أوروغواي":"🇺🇾",
    "الأوروغواي":"🇺🇾","أوزبكستان":"🇺🇿","إيران":"🇮🇷","الأردن":"🇯🇴","الإكوادور":"🇪🇨",
    "البوسنة والهرسك":"🇧🇦","الرأس الأخضر":"🇨🇻","السنغال":"🇸🇳","السويد":"🇸🇪","العراق":"🇮🇶",
    "الكونغو الديمقراطية":"🇨🇩","النرويج":"🇳🇴","النمسا":"🇦🇹","اليابان":"🇯🇵","بلجيكا":"🇧🇪",
    "بنما":"🇵🇦","جنوب أفريقيا":"🇿🇦","ساحل العاج":"🇨🇮","غانا":"🇬🇭","كرواتيا":"🇭🇷",
    "كوراساو":"🇨🇼","كولومبيا":"🇨🇴","نيوزيلندا":"🇳🇿","هولندا":"🇳🇱"
}


# تصميم واجهة المستخدم (CSS) - هوية الحديقة الملكية
# Design V2 فقط
# استبدل CSS القديم بهذا

st.markdown("""
<style>
.stApp{
background:radial-gradient(circle at top,#14532d,#020806);
}

.main-title{
color:#FFD700 !important;
text-align:center;
font-size:48px;
font-weight:900;
padding:25px;
border-radius:30px;
background:rgba(255,215,0,.15);
box-shadow:0 0 35px rgba(255,215,0,.25);
}

.stApp,p,label,div{
color:white;
}

.match-card{
background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(255,255,255,.04));
border-radius:30px;
padding:25px;
margin:20px 0;
border:1px solid rgba(255,255,255,.2);
box-shadow:0 15px 40px rgba(0,0,0,.45);
}

.match-card h4{
color:#FFD700 !important;
text-align:center;
font-size:26px;
}

.stButton button{
width:100%;
height:48px;
border-radius:18px;
border:none;
background:linear-gradient(90deg,#00c853,#00e676);
color:white;
font-weight:bold;
}

.stButton button:hover{
background:linear-gradient(90deg,#FFD700,#ff9800);
color:black;
}

.admin-card{
background:linear-gradient(135deg,#5b3200,#b8860b);
border-radius:25px;
padding:25px;
}

.review-card{
background:linear-gradient(135deg,#004d2b,#00a85a);
border-radius:25px;
padding:25px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
WC26 KING 🇸🇦🏆⚽️
</div>
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
        {"id": 1, "team_home": "المكسيك", "team_away": "جنوب أفريقيا", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz)},
{"id": 2, "team_home": "كوريا الجنوبية", "team_away": "التشيك", "time": datetime(2026, 6, 12, 5, 0, tzinfo=ksa_tz)},
{"id": 3, "team_home": "كندا", "team_away": "البوسنة والهرسك", "time": datetime(2026, 6, 12, 22, 0, tzinfo=ksa_tz)},
{"id": 4, "team_home": "الولايات المتحدة", "team_away": "باراغواي", "time": datetime(2026, 6, 13, 4, 0, tzinfo=ksa_tz)},
{"id": 5, "team_home": "قطر", "team_away": "سويسرا", "time": datetime(2026, 6, 13, 22, 0, tzinfo=ksa_tz)},
{"id": 6, "team_home": "البرازيل", "team_away": "المغرب", "time": datetime(2026, 6, 14, 1, 0, tzinfo=ksa_tz)},
{"id": 7, "team_home": "هايتي", "team_away": "اسكتلندا", "time": datetime(2026, 6, 14, 4, 0, tzinfo=ksa_tz)},
{"id": 8, "team_home": "أستراليا", "team_away": "تركيا", "time": datetime(2026, 6, 14, 7, 0, tzinfo=ksa_tz)},
{"id": 9, "team_home": "ألمانيا", "team_away": "كوراساو", "time": datetime(2026, 6, 14, 20, 0, tzinfo=ksa_tz)},
{"id": 10, "team_home": "هولندا", "team_away": "اليابان", "time": datetime(2026, 6, 14, 23, 0, tzinfo=ksa_tz)},
{"id": 11, "team_home": "ساحل العاج", "team_away": "الإكوادور", "time": datetime(2026, 6, 15, 2, 0, tzinfo=ksa_tz)},
{"id": 12, "team_home": "السويد", "team_away": "تونس", "time": datetime(2026, 6, 15, 5, 0, tzinfo=ksa_tz)},
{"id": 13, "team_home": "إسبانيا", "team_away": "الرأس الأخضر", "time": datetime(2026, 6, 15, 19, 0, tzinfo=ksa_tz)},
{"id": 14, "team_home": "بلجيكا", "team_away": "مصر", "time": datetime(2026, 6, 15, 22, 0, tzinfo=ksa_tz)},
{"id": 15, "team_home": "السعودية", "team_away": "الأوروغواي", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz)},
{"id": 16, "team_home": "إيران", "team_away": "نيوزيلندا", "time": datetime(2026, 6, 16, 4, 0, tzinfo=ksa_tz)},
        
        # --- الجولة الثانية ---
{"id": 17, "team_home": "فرنسا", "team_away": "السنغال", "time": datetime(2026, 6, 16, 22, 0, tzinfo=ksa_tz)},
{"id": 18, "team_home": "النرويج", "team_away": "العراق", "time": datetime(2026, 6, 17, 1, 0, tzinfo=ksa_tz)},

{"id": 19, "team_home": "الأرجنتين", "team_away": "الجزائر", "time": datetime(2026, 6, 17, 4, 0, tzinfo=ksa_tz)},
{"id": 20, "team_home": "النمسا", "team_away": "الأردن", "time": datetime(2026, 6, 17, 7, 0, tzinfo=ksa_tz)},
{"id": 21, "team_home": "البرتغال", "team_away": "الكونغو الديمقراطية", "time": datetime(2026, 6, 17, 20, 0, tzinfo=ksa_tz)},
{"id": 22, "team_home": "إنجلترا", "team_away": "كرواتيا", "time": datetime(2026, 6, 17, 23, 0, tzinfo=ksa_tz)},
{"id": 23, "team_home": "غانا", "team_away": "بنما", "time": datetime(2026, 6, 18, 2, 0, tzinfo=ksa_tz)},
{"id": 24, "team_home": "أوزبكستان", "team_away": "كولومبيا", "time": datetime(2026, 6, 18, 5, 0, tzinfo=ksa_tz)},
{"id": 25, "team_home": "التشيك", "team_away": "جنوب أفريقيا", "time": datetime(2026, 6, 18, 19, 0, tzinfo=ksa_tz)},
{"id": 26, "team_home": "سويسرا", "team_away": "البوسنة والهرسك", "time": datetime(2026, 6, 18, 22, 0, tzinfo=ksa_tz)},
{"id": 27, "team_home": "كندا", "team_away": "قطر", "time": datetime(2026, 6, 19, 1, 0, tzinfo=ksa_tz)},
{"id": 28, "team_home": "المكسيك", "team_away": "كوريا الجنوبية", "time": datetime(2026, 6, 19, 4, 0, tzinfo=ksa_tz)},
{"id": 29, "team_home": "الولايات المتحدة", "team_away": "أستراليا", "time": datetime(2026, 6, 19, 22, 0, tzinfo=ksa_tz)},
{"id": 30, "team_home": "اسكتلندا", "team_away": "المغرب", "time": datetime(2026, 6, 20, 1, 0, tzinfo=ksa_tz)},
{"id": 31, "team_home": "البرازيل", "team_away": "هايتي", "time": datetime(2026, 6, 20, 3, 30, tzinfo=ksa_tz)},
{"id": 32, "team_home": "تركيا", "team_away": "باراغواي", "time": datetime(2026, 6, 20, 6, 0, tzinfo=ksa_tz)},
{"id": 33, "team_home": "هولندا", "team_away": "السويد", "time": datetime(2026, 6, 20, 20, 0, tzinfo=ksa_tz)},
{"id": 34, "team_home": "ألمانيا", "team_away": "ساحل العاج", "time": datetime(2026, 6, 20, 23, 0, tzinfo=ksa_tz)},
{"id": 35, "team_home": "الإكوادور", "team_away": "كوراساو", "time": datetime(2026, 6, 21, 3, 0, tzinfo=ksa_tz)},
{"id": 36, "team_home": "اليابان", "team_away": "تونس", "time": datetime(2026, 6, 21, 7, 0, tzinfo=ksa_tz)},
{"id": 37, "team_home": "إسبانيا", "team_away": "السعودية", "time": datetime(2026, 6, 21, 19, 0, tzinfo=ksa_tz)},
{"id": 38, "team_home": "بلجيكا", "team_away": "إيران", "time": datetime(2026, 6, 21, 22, 0, tzinfo=ksa_tz)},
{"id": 39, "team_home": "أوروغواي", "team_away": "الرأس الأخضر", "time": datetime(2026, 6, 22, 1, 0, tzinfo=ksa_tz)},
{"id": 40, "team_home": "نيوزيلندا", "team_away": "مصر", "time": datetime(2026, 6, 22, 4, 0, tzinfo=ksa_tz)},
{"id": 41, "team_home": "الأرجنتين", "team_away": "النمسا", "time": datetime(2026, 6, 22, 20, 0, tzinfo=ksa_tz)},
{"id": 42, "team_home": "فرنسا", "team_away": "العراق", "time": datetime(2026, 6, 23, 0, 0, tzinfo=ksa_tz)},
{"id": 43, "team_home": "النرويج", "team_away": "السنغال", "time": datetime(2026, 6, 23, 3, 0, tzinfo=ksa_tz)},
{"id": 44, "team_home": "الأردن", "team_away": "الجزائر", "time": datetime(2026, 6, 23, 6, 0, tzinfo=ksa_tz)},
{"id": 45, "team_home": "البرتغال", "team_away": "أوزبكستان", "time": datetime(2026, 6, 23, 20, 0, tzinfo=ksa_tz)},
{"id": 46, "team_home": "إنجلترا", "team_away": "غانا", "time": datetime(2026, 6, 23, 23, 0, tzinfo=ksa_tz)},

{"id": 47, "team_home": "بنما", "team_away": "كرواتيا", "time": datetime(2026, 6, 24, 2, 0, tzinfo=ksa_tz)},
{"id": 48, "team_home": "كولومبيا", "team_away": "الكونغو الديمقراطية", "time": datetime(2026, 6, 24, 5, 0, tzinfo=ksa_tz)},
{"id": 49, "team_home": "البوسنة والهرسك", "team_away": "قطر", "time": datetime(2026, 6, 24, 22, 0, tzinfo=ksa_tz)},
{"id": 50, "team_home": "سويسرا", "team_away": "كندا", "time": datetime(2026, 6, 24, 22, 0, tzinfo=ksa_tz)},

{"id": 51, "team_home": "المغرب", "team_away": "هايتي", "time": datetime(2026, 6, 25, 1, 0, tzinfo=ksa_tz)},
{"id": 52, "team_home": "اسكتلندا", "team_away": "البرازيل", "time": datetime(2026, 6, 25, 1, 0, tzinfo=ksa_tz)},
{"id": 53, "team_home": "التشيك", "team_away": "المكسيك", "time": datetime(2026, 6, 25, 4, 0, tzinfo=ksa_tz)},
{"id": 54, "team_home": "جنوب أفريقيا", "team_away": "كوريا الجنوبية", "time": datetime(2026, 6, 25, 4, 0, tzinfo=ksa_tz)},
{"id": 55, "team_home": "كوراساو", "team_away": "ساحل العاج", "time": datetime(2026, 6, 25, 23, 0, tzinfo=ksa_tz)},
{"id": 56, "team_home": "الإكوادور", "team_away": "ألمانيا", "time": datetime(2026, 6, 25, 23, 0, tzinfo=ksa_tz)},

{"id": 57, "team_home": "اليابان", "team_away": "السويد", "time": datetime(2026, 6, 26, 2, 0, tzinfo=ksa_tz)},
{"id": 58, "team_home": "تونس", "team_away": "هولندا", "time": datetime(2026, 6, 26, 2, 0, tzinfo=ksa_tz)},
{"id": 59, "team_home": "باراغواي", "team_away": "أستراليا", "time": datetime(2026, 6, 26, 5, 0, tzinfo=ksa_tz)},
{"id": 60, "team_home": "تركيا", "team_away": "الولايات المتحدة", "time": datetime(2026, 6, 26, 5, 0, tzinfo=ksa_tz)},
{"id": 61, "team_home": "فرنسا", "team_away": "النرويج", "time": datetime(2026, 6, 26, 22, 0, tzinfo=ksa_tz)},
{"id": 62, "team_home": "السنغال", "team_away": "العراق", "time": datetime(2026, 6, 26, 22, 0, tzinfo=ksa_tz)},

{"id": 63, "team_home": "الرأس الأخضر", "team_away": "السعودية", "time": datetime(2026, 6, 27, 3, 0, tzinfo=ksa_tz)},
{"id": 64, "team_home": "أوروغواي", "team_away": "إسبانيا", "time": datetime(2026, 6, 27, 3, 0, tzinfo=ksa_tz)},
{"id": 65, "team_home": "مصر", "team_away": "إيران", "time": datetime(2026, 6, 27, 6, 0, tzinfo=ksa_tz)},
{"id": 66, "team_home": "نيوزيلندا", "team_away": "بلجيكا", "time": datetime(2026, 6, 27, 6, 0, tzinfo=ksa_tz)},

{"id": 67, "team_home": "كرواتيا", "team_away": "غانا", "time": datetime(2026, 6, 28, 0, 0, tzinfo=ksa_tz)},
{"id": 68, "team_home": "بنما", "team_away": "إنجلترا", "time": datetime(2026, 6, 28, 0, 0, tzinfo=ksa_tz)},
{"id": 69, "team_home": "كولومبيا", "team_away": "البرتغال", "time": datetime(2026, 6, 28, 2, 30, tzinfo=ksa_tz)},
{"id": 70, "team_home": "الكونغو الديمقراطية", "team_away": "أوزبكستان", "time": datetime(2026, 6, 28, 2, 30, tzinfo=ksa_tz)},
{"id": 71, "team_home": "الجزائر", "team_away": "النمسا", "time": datetime(2026, 6, 28, 5, 0, tzinfo=ksa_tz)},
{"id": 72, "team_home": "الأردن", "team_away": "الأرجنتين", "time": datetime(2026, 6, 28, 5, 0, tzinfo=ksa_tz)},
    ]

all_matches = get_internal_matches()

# إدارة حالة تسجيل الدخول عبر الـ session_state لمنع اختفاء البيانات عند تحديث الصفحة
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    st.session_state["user_phone"] = ""
    st.session_state["user_name"] = ""

# إنشاء التبويبات الرئيسية في أعلى الصفحة
if not st.session_state["is_logged_in"]:
    tab_auth, tab_info = st.tabs(["🔐 بوابة الأعضاء", "ℹ️ معلومات التحدي"])
    
    with tab_auth:
        menu = ["تسجيل الدخول", "إنشاء حساب جديد (لأول مرة)"]
        choice = st.radio("إختر الإجراء:", menu, horizontal=True)

        if choice == "إنشاء حساب جديد (لأول مرة)":
            st.subheader("📝 استمارة تسجيل مشارك جديد")
            with st.form("registration_form"):
                new_name = st.text_input("👨🏽 اسمك يالشيخ :")
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
                            st.success(f"🎉 تم إنشاء حسابك المؤمن بنجاح يا {new_name}! يمكنك الآن الانتقال لتسجيل الدخول.")
                            st.balloons()

        else:
            st.subheader("🔐 تسجيل دخول مشاركي الحديقة")
            login_phone = st.text_input("📱 أدخل رقم جوالك المعتمد:", max_chars=10)
            login_pass = st.text_input("🔐 أدخل كلمة المرور الخاصة بك:", type="password")
            
            if st.button("تسجيل الدخول 🚀"):
                if login_phone and login_pass:
                    login_phone = str(login_phone).strip()
                    login_pass = str(login_pass).strip()
                    
                    cursor = db_conn.cursor()
                    cursor.execute("SELECT name, password FROM users WHERE phone = ?", (login_phone,))
                    user_row = cursor.fetchone()
                    
                    if not user_row:
                        st.error("❌ رقم الجوال هذا غير مسجل مسبقاً!")
                    elif user_row[1] != login_pass:
                        st.error("❌ كلمة المرور غير صحيحة!")
                    else:
                        st.session_state["is_logged_in"] = True
                        st.session_state["user_phone"] = login_phone
                        st.session_state["user_name"] = user_row[0]
                        st.success(f"مرحباً بعودتك يا {user_row[0]}! 😎")
                        st.rerun()
                else:
                    st.error("❌ الرجاء إدخال رقم الجوال وكلمة المرور.")
                    
    with tab_info:
        st.markdown("""
        ### ارحححبووو في تحدي كنق المونديال 😍🏆
        هذا التبويب مخصص للترحيب بأعضاء الحديقة قبل تسجيل الدخول.
        * سجل حسابك أولاً.
        * ادخل لتوقع نتائج مباريات المونديال بدقة.
        * تربع على صدارة الترتيب لتصبح **كنق المونديال**!
        """)

else:
    # شاشة التطبيق الرئيسية بعد تسجيل الدخول (تبويبات المحتوى)
    login_phone = st.session_state["user_phone"]
    user_name = st.session_state["user_name"]
    
    # إظهار زر تسجيل الخروج في الشريط الجانبي أو الأعلى لراحة المستخدم
    st.sidebar.markdown(f"👤 المشارك: **{user_name}**")
    if st.sidebar.button("تسجيل الخروج 🚪"):
        st.session_state["is_logged_in"] = False
        st.session_state["user_phone"] = ""
        st.session_state["user_name"] = ""
        st.rerun()

    # إنشاء التبويبات للمحتوى الفعلي للبطولة
    if login_phone == ADMIN_PHONE:
        tab_leaderboard, tab_predict, tab_schedule, tab_admin = st.tabs([
            "🏆🔥جدول الترتيب",
            "🤩التوقعات الحالية",
            "📅 مواعيد فتح التوقعات",
            "⚙️ الإدارة"
        ])
    else:
        tab_leaderboard, tab_predict, tab_schedule, tab_profile = st.tabs([
            "🏆🔥جدول الترتيب",
            "🤩التوقعات الحالية",
            "📅 مواعيد فتح التوقعات",
            "👤 ملفي الشخصي"
        ])

    # --- تبويب لوحة الصدارة ---
    with tab_leaderboard:
        st.markdown("### 🤩🏆 جدول الترتيب لايف")
        cursor = db_conn.cursor()
        cursor.execute("SELECT name, points, phone FROM users ORDER BY points DESC")
        leaderboard_data = cursor.fetchall()
        
        for idx, row in enumerate(leaderboard_data):
            p_name, p_points, p_phone = row
            col_rank, col_name, col_pts, col_action = st.columns([1, 4, 2, 3])
            with col_rank:
                st.markdown(f"**#{idx+1}**")
            with col_name:
                st.markdown(f"{p_name}")
            with col_pts:
                st.markdown(f"🏆 {p_points} Points")
            with col_action:
                if st.button(f"مشاهدة التوقعات", key=f"rev_{p_phone}_{idx}"):
                    st.session_state[f"view_predictions_for"] = p_phone
                    st.session_state[f"view_predictions_name"] = p_name
        
        if f"view_predictions_for" in st.session_state:
            target_phone = st.session_state[f"view_predictions_for"]
            target_name = st.session_state[f"view_predictions_name"]
            st.markdown(f"""<div class="review-card"> <b>كشف توقعات المشارك: {target_name}</b></div>""", unsafe_allow_html=True)
            
            cursor.execute("SELECT match_id, pred_home, pred_away FROM predictions WHERE phone = ?", (target_phone,))
            user_preds = {r[0]: (r[1], r[2]) for r in cursor.fetchall()}
            
            review_list = []
            for m in all_matches:
                m_desc = f"{m['team_home']} × {m['team_away']}"
                if m["id"] in user_preds:
                    ph, pa = user_preds[m["id"]]
                    review_list.append({"المباراة": m_desc, "التوقع": f"{ph} - {pa}"})
                else:
                    review_list.append({"المباراة": m_desc, "التوقع": "لم يتوقع"})
            
            st.dataframe(pd.DataFrame(review_list), hide_index=True, use_container_width=True)
            if st.button("إغلاق لوحة المراجعة ✖️"):
                del st.session_state[f"view_predictions_for"]
                st.rerun()

    # --- تبويب إدخال التوقعات للمباريات ---
    with tab_predict:
        st.subheader("⚽️⚒️ هنا التحدي يا متحدددي ")

        hide_closed = st.toggle(
            "🔴 إخفاء المباريات المنتهية",
            value=False
        )

        cursor = db_conn.cursor()
        
        for match in all_matches:
            time_until_match = match["time"] - now_ksa

            # إخفاء المباريات المنتهية عند تفعيل الخيار
            if hide_closed and now_ksa >= match["time"]:
                continue
            
            cursor.execute("SELECT actual_home, actual_away FROM processed_matches WHERE match_id = ?", (match["id"],))
            match_status_row = cursor.fetchone()
            
            home_flag = FLAGS.get(match['team_home'], '🏳️')
            away_flag = FLAGS.get(match['team_away'], '🏳️')
            if match_status_row and match_status_row[0] is not None and match_status_row[1] is not None:
                match_desc = f"<div style='display:flex;justify-content:center;align-items:center;gap:6px;white-space:nowrap;overflow-x:auto;padding:0 5px;font-size:clamp(18px,4vw,24px);font-weight:bold;color:#FFD700;'><span>{away_flag} {match['team_away']}</span><span>{match_status_row[1]} × {match_status_row[0]}</span><span>{home_flag} {match['team_home']}</span></div><div style='text-align:center;color:#FFD700;font-size:20px;'>(انتهت واحتُسبت ✅)</div>"
                is_calculated_and_valid = True
                    
        else:
                match_desc = f"<div style='display:flex;justify-content:center;align-items:center;gap:6px;white-space:nowrap;overflow-x:auto;padding:0 5px;font-size:clamp(18px,4vw,24px);font-weight:bold;color:#FFD700;'><span>{away_flag} {match['team_away']}</span><span>×</span><span>{home_flag} {match['team_home']}</span></div>"
                is_calculated_and_valid = False
                is_within_24h = (timedelta(hours=0) <= time_until_match <= timedelta(hours=24))
                is_june_11 = (match["time"].day == 11 and match["time"].month == 6)

            if (
                match["time"] <= now_ksa
                or is_within_24h
                or is_june_11
                or is_calculated_and_valid
                or (login_phone == ADMIN_PHONE)
            ):
                with st.container():
                    st.markdown(f"""
                    <div class="match-card">
                        {match_desc}
                        <p>
                            موعد اللقاء: {match['time'].strftime('%d يونيو | %I:%M %p')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    if (time_until_match < timedelta(minutes=10) or is_calculated_and_valid) and login_phone != ADMIN_PHONE:
                        st.error("🔒 مغلق! انتهى وقت التوقع أو المباراة انتهت فعلياً.")
                    else:
                        cursor.execute("SELECT pred_home, pred_away FROM predictions WHERE phone = ? AND match_id = ?", (login_phone, match["id"]))
                        existing_pred = cursor.fetchone()
                        if existing_pred:
    share_text = f"""🏆 WC26 KING

👤 {user_name}

⚽ {match['team_home']} × {match['team_away']}

🎯 توقعي:
{match['team_home']} {existing_pred[0]} - {existing_pred[1]} {match['team_away']}"""

    wa_link = "https://wa.me/?text=" + urllib.parse.quote(share_text)
    st.link_button(
        "📲 مشاركة التوقع عبر واتساب",
        wa_link,
        key=f"share_{match['id']}"
    )
                        val_home = existing_pred[0] if existing_pred else 0
                        val_away = existing_pred[1] if existing_pred else 0
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            h_score = st.number_input(f"أهداف {match['team_home']}", 0, 10, value=val_home, key=f"h_{match['id']}")
                        with c2:
                            a_score = st.number_input(f"أهداف {match['team_away']}", 0, 10, value=val_away, key=f"a_{match['id']}")
                        
                        if st.button(f"اعتماد التوقع لمباراة {match['team_home']} × {match['team_away']}", key=f"btn_{match['id']}"):
                            cursor.execute('''
                                INSERT INTO predictions (phone, match_id, pred_home, pred_away)
                                VALUES (?, ?, ?, ?)
                                ON CONFLICT(phone, match_id) DO UPDATE SET pred_home=excluded.pred_home, pred_away=excluded.pred_away
                            ''', (login_phone, match["id"], h_score, a_score))
                            db_conn.commit()
                            st.success("تم تسجيل وتأمين توقعك بنجاح! 🏁")

                            share_text = f"""🏆 WC26 KING

👤 {user_name}

⚽ {match['team_home']} × {match['team_away']}

🎯 توقعي:
{match['team_home']} {h_score} - {a_score} {match['team_away']}"""

                            wa_link = "https://wa.me/?text=" + urllib.parse.quote(share_text)
                            st.link_button("📲 مشاركة التوقع عبر واتساب", wa_link)


    with tab_schedule:
        st.subheader("📅 مواعيد فتح التوقعات")

        rows = []

        for match in all_matches:
            open_time = match["time"] - timedelta(hours=24)

            if now_ksa >= match["time"]:
                status = "🔴 مغلق"

            elif now_ksa >= open_time:
                status = "🟢 مفتوح الآن"

            else:
                remaining = open_time - now_ksa
                days = remaining.days
                hours = remaining.seconds // 3600
                status = f"🟡 بعد {days} يوم و {hours} ساعة"

            rows.append({
                "المباراة": f"{match['team_home']} × {match['team_away']}",
                "فتح التوقعات": open_time.strftime("%d/%m %I:%M %p"),
                "موعد المباراة": match["time"].strftime("%d/%m %I:%M %p"),
                "الحالة": status
            })

        st.dataframe(
            pd.DataFrame(rows),
            hide_index=True,
            use_container_width=True
        )


    with tab_profile:
        st.subheader("اوبتاالمونديال 📊")

        cursor = db_conn.cursor()
        cursor.execute("SELECT points FROM users WHERE phone = ?", (login_phone,))
        row = cursor.fetchone()
        user_points = row[0] if row else 0

        cursor.execute("""
            SELECT p.pred_home, p.pred_away,
                   pm.actual_home, pm.actual_away
            FROM predictions p
            JOIN processed_matches pm ON p.match_id = pm.match_id
            WHERE p.phone = ?
        """, (login_phone,))

        correct = 0
        wrong = 0

        for ph, pa, ah, aa in cursor.fetchall():
            pred_sign = (ph > pa) - (ph < pa)
            actual_sign = (ah > aa) - (ah < aa)

            if ph == ah and pa == aa:
                correct += 1
            elif pred_sign == actual_sign:
                correct += 1
            else:
                wrong += 1

        total = correct + wrong
        success_rate = round((correct / total) * 100, 1) if total else 0

        st.markdown(f"### {user_name}")
        st.metric("🏆 النقاط", user_points)

        c1, c2, c3 = st.columns(3)
        c1.metric("✅ توقعات صحيحة", correct)
        c2.metric("❌ توقعات خاطئة", wrong)
        c3.metric("📊 نسبة النجاح", f"{success_rate}%")


    # --- تبويب الإدارة والتحكم (يظهر للأدمن فقط) ---
    if login_phone == ADMIN_PHONE:
        with tab_admin:
            st.markdown('<div class="admin-card">⚙️ <b>لوحة تحكم الإدارة الملكية (أحمد بادحمان)</b></div>', unsafe_allow_html=True)
            cursor = db_conn.cursor()
            
            st.subheader("🧮 إدارة وإدخل نتائج المباريات")
            match_options = {f"{m['team_home']} × {m['team_away']}": m for m in all_matches}
            selected_match_str = st.selectbox("إختر المباراة المستهدفة لإدخال/تعديل نتيجتها:", list(match_options.keys()))
            selected_match = match_options[selected_match_str]
            
            cursor.execute("SELECT actual_home, actual_away FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
            already_calculated = cursor.fetchone()
            is_valid_old_result = already_calculated and already_calculated[0] is not None and already_calculated[1] is not None
            
            if is_valid_old_result:
                st.warning(f"⚠️ هذه المباراة احتُسبت سابقاً بنتيجة: {already_calculated[0]} - {already_calculated[1]}")
                if st.button("🚨 إلغاء نتيجة المباراة وسحب النقاط من الأعضاء", key="cancel_btn"):
                    old_h, old_a = already_calculated
                    cursor.execute("SELECT phone, pred_home, pred_away FROM predictions WHERE match_id = ?", (selected_match["id"],))
                    all_preds = cursor.fetchall()
                    
                    for pred in all_preds:
                        user_phone, p_home, p_away = pred
                        old_points = 0
                        if p_home == old_h and p_away == old_a:
                            old_points = 3
                        elif (p_home > p_away and old_h > old_a) or \
                             (p_home < p_away and old_h < old_a) or \
                             (p_home == p_away and old_h == old_a):
                            old_points = 1
                        if old_points > 0:
                            cursor.execute("UPDATE users SET points = MAX(0, points - ?) WHERE phone = ?", (old_points, user_phone))
                    
                    cursor.execute("DELETE FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
                    db_conn.commit()
                    st.error(f"🔄 تم إلغاء المباراة وعادت مفتوحة الآن.")
                    st.rerun()
            
            col_h, col_a = st.columns(2)
            with col_h:
                default_h = already_calculated[0] if is_valid_old_result else 0
                actual_h = st.number_input(f"النتيجة الفعلية لـ {selected_match['team_home']}", 0, 10, value=default_h, key="act_h")
            with col_a:
                default_a = already_calculated[1] if is_valid_old_result else 0
                actual_a = st.number_input(f"النتيجة الفعلية لـ {selected_match['team_away']}", 0, 10, value=default_a, key="act_a")
            
            btn_label = "📝 تحديث وتعديل النقاط الحالية" if is_valid_old_result else "🔥 احسب النقاط وحدث الصدارة فوراً!"
            
            if st.button(btn_label):
                if is_valid_old_result:
                    old_h, old_a = already_calculated
                    cursor.execute("SELECT phone, pred_home, pred_away FROM predictions WHERE match_id = ?", (selected_match["id"],))
                    all_preds = cursor.fetchall()
                    for pred in all_preds:
                        user_phone, p_home, p_away = pred
                        old_points = 0
                        if p_home == old_h and p_away == old_a: old_points = 3
                        elif (p_home > p_away and old_h > old_a) or (p_home < p_away and old_h < old_a) or (p_home == p_away and old_h == old_a): old_points = 1
                        if old_points > 0: cursor.execute("UPDATE users SET points = MAX(0, points - ?) WHERE phone = ?", (old_points, user_phone))
                    cursor.execute("DELETE FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
                
                cursor.execute("SELECT phone, pred_home, pred_away FROM predictions WHERE match_id = ?", (selected_match["id"],))
                all_preds = cursor.fetchall()
                for pred in all_preds:
                    user_phone, p_home, p_away = pred
                    calculated_points = 0
                    if p_home == actual_h and p_away == actual_a: calculated_points = 3
                    elif (p_home > p_away and actual_h > actual_a) or (p_home < p_away and actual_h < actual_a) or (p_home == p_away and actual_h == actual_a): calculated_points = 1
                    if calculated_points > 0: cursor.execute("UPDATE users SET points = points + ? WHERE phone = ?", (calculated_points, user_phone))
                
                cursor.execute('INSERT INTO processed_matches (match_id, actual_home, actual_away) VALUES (?, ?, ?)', (selected_match["id"], actual_h, actual_a))
                db_conn.commit()
                st.success(f"🏆 تم اعتماد النتيجة وتحديث نقاط الشباب فوراً!")
                st.rerun()

            st.subheader("🛠️ شاشة إدارة قاعدة البيانات الفورية")
            cursor.execute("SELECT name, phone, points, password FROM users")
            all_users_list = cursor.fetchall()
            user_options = {f"{u[0]} ({u[1]})": u for u in all_users_list}
            
            if user_options:
                selected_user_str = st.selectbox("إختر العضو المستهدف:", list(user_options.keys()))
                target_user_data = user_options[selected_user_str]
                
                c_edit, c_del = st.columns(2)
                with c_edit:
                    new_pts = st.number_input("تعديل مجموع نقاطه الكلي إلى:", 0, 500, value=target_user_data[2])
                    new_user_pass = st.text_input(f"تعديل كلمة مرور {target_user_data[0]} إلى:", value=target_user_data[3])
                    if st.button("💾 حفظ وتعديل البيانات"):
                        cursor.execute("UPDATE users SET points = ?, password = ? WHERE phone = ?", (new_pts, new_user_pass, target_user_data[1]))
                        db_conn.commit()
                        st.success("تم تحديث البيانات بنجاح!")
                        st.rerun()
                        
                with c_del:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("❌ حذف هذا العضو نهائياً"):
                        cursor.execute("DELETE FROM users WHERE phone = ?", (target_user_data[1],))
                        db_conn.commit()
                        st.error("تم حذف العضو!")
                        st.rerun()
