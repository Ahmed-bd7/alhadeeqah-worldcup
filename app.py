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

st.set_page_config(page_title="⚽🏆 WC26 KING", page_icon="🏆", layout="centered")

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

# 🎨 تصميم واجهة المستخدم الاحترافية والمحسنة (Premium Dark UI)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');

/* تطبيق الخط والخلفية العامة */
* {
    font-family: 'Cairo', sans-serif;
}
.stApp {
    background: radial-gradient(circle at top, #062f19, #020905);
}

/* العنوان الرئيسي الفخم */
.main-title {
    color: #FFD700 !important;
    text-align: center;
    font-size: clamp(32px, 6vw, 54px);
    font-weight: 900;
    padding: 30px 15px;
    border-radius: 35px;
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(0, 0, 0, 0.4));
    border: 1px solid rgba(255, 215, 0, 0.25);
    box-shadow: 0 20px 50px rgba(0,0,0,0.6), inset 0 0 20px rgba(255,215,0,0.1);
    margin-bottom: 35px;
    letter-spacing: 1px;
}

/* الهيدر والعناوين الفرعية */
h1, h2, h3, h4, p, label, div {
    color: white;
}

/* بطاقة المباراة المحدثة والناعمة */
.match-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
    border-radius: 24px;
    padding: 22px;
    margin: 18px 0;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 35px rgba(0,0,0,0.4);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.match-card:hover {
    transform: translateY(-4px);
    border-color: rgba(0, 230, 118, 0.4);
    box-shadow: 0 15px 40px rgba(0, 230, 118, 0.15);
    background: linear-gradient(145deg, rgba(255,255,255,0.12), rgba(255,255,255,0.04));
}

/* بادجات الحالات للمباريات */
.badge-status {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: bold;
    margin-top: 8px;
}
.badge-open { background: rgba(0, 230, 118, 0.2); color: #00e676; border: 1px solid #00e676; }
.badge-closed { background: rgba(255, 23, 68, 0.2); color: #ff1744; border: 1px solid #ff1744; }
.badge-done { background: rgba(255, 215, 0, 0.2); color: #FFD700; border: 1px solid #FFD700; }

/* أزرار الحديقة - هيبة وملمس احترافي */
.stButton button {
    width: 100%;
    height: 50px;
    border-radius: 16px;
    border: none;
    background: linear-gradient(90deg, #00b0ff, #00e676);
    color: white;
    font-weight: 700;
    font-size: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}
.stButton button:hover {
    background: linear-gradient(90deg, #FFD700, #ff9800);
    color: #000 !important;
    transform: translateY(-2px);
    box-shadow: 0 12px 25px rgba(255,215,0,0.3);
}

/* ستايل لوحة الصدارة الفاخرة */
.leaderboard-row {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 16px;
    padding: 12px 16px;
    margin: 8px 0;
    border-right: 4px solid #FFD700;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* كروت الإحصائيات الأنيقة */
.stats-container {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 25px;
    direction: rtl;
}
.stat-box {
    flex: 1;
    background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px 8px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    transition: transform 0.2s;
}
.stat-box:hover {
    transform: scale(1.03);
    border-color: rgba(255,215,0,0.3);
}
.stat-box-label {
    font-size: 13px;
    color: #b3b3b3;
    margin-bottom: 4px;
}
.stat-box-value {
    font-size: 20px;
    font-weight: bold;
    color: #FFD700;
}

/* كرت توقع بطل المونديال الأيقوني */
.champion-box-card {
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(0, 77, 43, 0.3));
    border: 1px solid rgba(255,215,0,0.3);
    border-radius: 28px;
    padding: 30px 20px;
    margin: 25px 0;
    box-shadow: 0 20px 45px rgba(0,0,0,0.5);
    text-align: center;
}
.champion-saved-badge {
    background: linear-gradient(90deg, #FFD700, #ffa726);
    color: #000000 !important;
    font-weight: 900;
    font-size: 15px;
    padding: 8px 22px;
    border-radius: 50px;
    display: inline-block;
    margin-top: 15px;
    box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
WC26 KING 🇸🇦🏆⚽️
</div>
""", unsafe_allow_html=True)

# 2. إعداد قاعدة البيانات المحلية والاتصال
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
            is_joker INTEGER DEFAULT 0,
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
    
    try: cursor.execute("ALTER TABLE predictions ADD COLUMN is_joker INTEGER DEFAULT 0")
    except sqlite3.OperationalError: pass
        
    try: cursor.execute("ALTER TABLE users ADD COLUMN champion_pred TEXT DEFAULT NULL")
    except sqlite3.OperationalError: pass

    try: cursor.execute("ALTER TABLE predictions ADD COLUMN pred_pens_winner TEXT DEFAULT NULL")
    except sqlite3.OperationalError: pass

    try: cursor.execute("ALTER TABLE processed_matches ADD COLUMN actual_pens_winner TEXT DEFAULT NULL")
    except sqlite3.OperationalError: pass
        
    conn.commit()
    return conn

db_conn = init_db()
ADMIN_PHONE = "0502518301" 

def get_internal_matches():
    return [
        {"id": 1, "team_home": "المكسيك", "team_away": "جنوب أفريقيا", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 2, "team_home": "كوريا الجنوبية", "team_away": "التشيك", "time": datetime(2026, 6, 12, 5, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 3, "team_home": "كندا", "team_away": "البوسنة والهرسك", "time": datetime(2026, 6, 12, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 4, "team_home": "الولايات المتحدة", "team_away": "باراغواي", "time": datetime(2026, 6, 13, 4, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 5, "team_home": "قطر", "team_away": "سويسرا", "time": datetime(2026, 6, 13, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 6, "team_home": "البرازيل", "team_away": "المغرب", "time": datetime(2026, 6, 14, 1, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 7, "team_home": "هايتي", "team_away": "اسكتلندا", "time": datetime(2026, 6, 14, 4, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 8, "team_home": "أستراليا", "team_away": "تركيا", "time": datetime(2026, 6, 14, 7, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 9, "team_home": "ألمانيا", "team_away": "كوراساو", "time": datetime(2026, 6, 14, 20, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 10, "team_home": "هولندا", "team_away": "اليابان", "time": datetime(2026, 6, 14, 23, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 11, "team_home": "ساحل العاج", "team_away": "الإكوادور", "time": datetime(2026, 6, 15, 2, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 12, "team_home": "السويد", "team_away": "تونس", "time": datetime(2026, 6, 15, 5, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 13, "team_home": "إسبانيا", "team_away": "الرأس الأخضر", "time": datetime(2026, 6, 15, 19, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 14, "team_home": "بلجيكا", "team_away": "مصر", "time": datetime(2026, 6, 15, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 15, "team_home": "السعودية", "team_away": "الأوروغواي", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 16, "team_home": "إيران", "team_away": "نيوزيلندا", "time": datetime(2026, 6, 16, 4, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 17, "team_home": "فرنسا", "team_away": "السنغال", "time": datetime(2026, 6, 16, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 18, "team_home": "النرويج", "team_away": "العراق", "time": datetime(2026, 6, 17, 1, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 19, "team_home": "الأرجنتين", "team_away": "الجزائر", "time": datetime(2026, 6, 17, 4, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 20, "team_home": "النمسا", "team_away": "الأردن", "time": datetime(2026, 6, 17, 7, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 21, "team_home": "البرتغال", "team_away": "الكونغو الديمقراطية", "time": datetime(2026, 6, 17, 20, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 22, "team_home": "إنجلترا", "team_away": "كرواتيا", "time": datetime(2026, 6, 17, 23, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 23, "team_home": "غانا", "team_away": "بنما", "time": datetime(2026, 6, 18, 2, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 24, "team_home": "أوزبكستان", "team_away": "كولومبيا", "time": datetime(2026, 6, 18, 5, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 25, "team_home": "التشيك", "team_away": "جنوب أفريقيا", "time": datetime(2026, 6, 18, 19, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 26, "team_home": "سويسرا", "team_away": "البوسنة والهرسك", "time": datetime(2026, 6, 18, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 27, "team_home": "كندا", "team_away": "قطر", "time": datetime(2026, 6, 19, 1, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 28, "team_home": "المكسيك", "team_away": "كوريا الجنوبية", "time": datetime(2026, 6, 19, 4, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 29, "team_home": "الولايات المتحدة", "team_away": "أستراليا", "time": datetime(2026, 6, 19, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 30, "team_home": "اسكتلندا", "team_away": "المغرب", "time": datetime(2026, 6, 20, 1, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 31, "team_home": "البرازيل", "team_away": "هايتي", "time": datetime(2026, 6, 20, 3, 30, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 32, "team_home": "تركيا", "team_away": "باراغواي", "time": datetime(2026, 6, 20, 6, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 33, "team_home": "هولندا", "team_away": "السويد", "time": datetime(2026, 6, 20, 20, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 34, "team_home": "ألمانيا", "team_away": "ساحل العاج", "time": datetime(2026, 6, 20, 23, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 35, "team_home": "الإكوادور", "team_away": "كوراساو", "time": datetime(2026, 6, 21, 3, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 36, "team_home": "اليابان", "team_away": "تونس", "time": datetime(2026, 6, 21, 7, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 37, "team_home": "إسبانيا", "team_away": "السعودية", "time": datetime(2026, 6, 21, 19, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 38, "team_home": "بلجيكا", "team_away": "إيران", "time": datetime(2026, 6, 21, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 39, "team_home": "أوروغواي", "team_away": "الرأس الأخضر", "time": datetime(2026, 6, 22, 1, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 40, "team_home": "نيوزيلندا", "team_away": "مصر", "time": datetime(2026, 6, 22, 4, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 41, "team_home": "الأرجنتين", "team_away": "النمسا", "time": datetime(2026, 6, 22, 20, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 42, "team_home": "فرنسا", "team_away": "العراق", "time": datetime(2026, 6, 23, 0, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 43, "team_home": "النرويج", "team_away": "السنغال", "time": datetime(2026, 6, 23, 3, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 44, "team_home": "الأردن", "team_away": "الجزائر", "time": datetime(2026, 6, 23, 6, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 45, "team_home": "البرتغال", "team_away": "أوزبكستان", "time": datetime(2026, 6, 23, 20, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 46, "team_home": "إنجلترا", "team_away": "غانا", "time": datetime(2026, 6, 23, 23, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 47, "team_home": "بنما", "team_away": "كرواتيا", "time": datetime(2026, 6, 24, 2, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 48, "team_home": "كولومبيا", "team_away": "الكونغو الديمقراطية", "time": datetime(2026, 6, 24, 5, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 49, "team_home": "البوسنة والهرسك", "team_away": "قطر", "time": datetime(2026, 6, 24, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 50, "team_home": "سويسرا", "team_away": "كندا", "time": datetime(2026, 6, 24, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 51, "team_home": "المغرب", "team_away": "هايتي", "time": datetime(2026, 6, 25, 1, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 52, "team_home": "اسكتلندا", "team_away": "البرازيل", "time": datetime(2026, 6, 25, 1, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 53, "team_home": "التشيك", "team_away": "المكسيك", "time": datetime(2026, 6, 25, 4, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 54, "team_home": "جنوب أفريقيا", "team_away": "كوريا الجنوبية", "time": datetime(2026, 6, 25, 4, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 55, "team_home": "كوراساو", "team_away": "ساحل العاج", "time": datetime(2026, 6, 25, 23, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 56, "team_home": "الإكوادور", "team_away": "ألمانيا", "time": datetime(2026, 6, 25, 23, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 57, "team_home": "اليابان", "team_away": "السويد", "time": datetime(2026, 6, 26, 2, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 58, "team_home": "تونس", "team_away": "هولندا", "time": datetime(2026, 6, 26, 2, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 59, "team_home": "باراغواي", "team_away": "أستراليا", "time": datetime(2026, 6, 26, 5, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 60, "team_home": "تركيا", "team_away": "الولايات المتحدة", "time": datetime(2026, 6, 26, 5, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 61, "team_home": "فرنسا", "team_away": "النرويج", "time": datetime(2026, 6, 26, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 62, "team_home": "السنغال", "team_away": "العراق", "time": datetime(2026, 6, 26, 22, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 63, "team_home": "الرأس الأخضر", "team_away": "السعودية", "time": datetime(2026, 6, 27, 3, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 64, "team_home": "أوروغواي", "team_away": "إسبانيا", "time": datetime(2026, 6, 27, 3, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 65, "team_home": "مصر", "team_away": "إيران", "time": datetime(2026, 6, 27, 6, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 66, "team_home": "نيوزيلندا", "team_away": "بلجيكا", "time": datetime(2026, 6, 27, 6, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 67, "team_home": "كرواتيا", "team_away": "غانا", "time": datetime(2026, 6, 28, 0, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 68, "team_home": "بنما", "team_away": "إنجلترا", "time": datetime(2026, 6, 28, 0, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 69, "team_home": "كولومبيا", "team_away": "البرتغال", "time": datetime(2026, 6, 28, 2, 30, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 70, "team_home": "الكونغو الديمقراطية", "team_away": "أوزبكستان", "time": datetime(2026, 6, 28, 2, 30, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 71, "team_home": "الجزائر", "team_away": "النمسا", "time": datetime(2026, 6, 28, 5, 0, tzinfo=ksa_tz), "is_knockout": False},
        {"id": 72, "team_home": "الأردن", "team_away": "الأرجنتين", "time": datetime(2026, 6, 28, 5, 0, tzinfo=ksa_tz), "is_knockout": False},
        # ===== دور الـ32 (مباريات خروج المغلوب) =====
        {"id": 73, "team_home": "كندا", "team_away": "جنوب أفريقيا", "time": datetime(2026, 6, 28, 22, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 74, "team_home": "البرازيل", "team_away": "اليابان", "time": datetime(2026, 6, 29, 20, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 75, "team_home": "ألمانيا", "team_away": "باراغواي", "time": datetime(2026, 6, 29, 23, 30, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 76, "team_home": "هولندا", "team_away": "المغرب", "time": datetime(2026, 7, 30, 4, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 77, "team_home": "النرويج", "team_away": "ساحل العاج", "time": datetime(2026, 7, 30, 20, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 78, "team_home": "فرنسا", "team_away": "السويد", "time": datetime(2026, 7, 1, 0, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 79, "team_home": "المكسيك", "team_away": "الإكوادور", "time": datetime(2026, 7, 1, 4, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 80, "team_home": "إنجلترا", "team_away": "الكونغو الديمقراطية", "time": datetime(2026, 7, 1, 19, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 81, "team_home": "بلجيكا", "team_away": "السنغال", "time": datetime(2026, 7, 1, 23, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 82, "team_home": "الولايات المتحدة", "team_away": "البوسنة والهرسك", "time": datetime(2026, 7, 2, 3, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 83, "team_home": "إسبانيا", "team_away": "النمسا", "time": datetime(2026, 7, 2, 22, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 84, "team_home": "البرتغال", "team_away": "كرواتيا", "time": datetime(2026, 7, 3, 2, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 85, "team_home": "سويسرا", "team_away": "الجزائر", "time": datetime(2026, 7, 3, 6, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 86, "team_home": "أستراليا", "team_away": "مصر", "time": datetime(2026, 7, 3, 21, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 87, "team_home": "الأرجنتين", "team_away": "الرأس الأخضر", "time": datetime(2026, 7, 4, 1, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 88, "team_home": "كولومبيا", "team_away": "غانا", "time": datetime(2026, 7, 4, 4, 30, tzinfo=ksa_tz), "is_knockout": True},
    ]

all_matches = get_internal_matches()
matches_dict = {m["id"]: m for m in all_matches}

def calculate_match_points(p_h, p_a, p_p, actual_h, actual_a, actual_p, is_knockout):
    earned = 0
    if p_h == actual_h and p_a == actual_a:
        earned += 3
        if is_knockout and p_h == p_a and p_p == actual_p:
            earned += 3  
    elif (p_h > p_a and actual_h > actual_a) or (p_h < p_a and actual_h < actual_a):
        earned += 1
    elif is_knockout and p_h == p_a and actual_h == actual_a:
        if p_p == actual_p:
            earned += 3
    return earned

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    st.session_state["user_phone"] = ""
    st.session_state["user_name"] = ""

if not st.session_state["is_logged_in"]:
    tab_auth, tab_info = st.tabs(["🔐 بوابة الأعضاء", "ℹ️ معلومات التحدي"])
    
    with tab_auth:
        choice = st.radio("إختر الإجراء للتداول داخل الحديقة:", ["تسجيل الدخول", "إنشاء حساب جديد (لأول مرة)"], horizontal=True)

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
                            st.success(f"🎉 تم إنشاء حسابك المؤمن بنجاح يا {new_name}!")
                            st.balloons()
        else:
            st.subheader("🔐 تسجيل دخول مشاركي الحديقة")
            login_phone = st.text_input("📱 رقم جوالك المعتمد:", max_chars=10)
            login_pass = st.text_input("🔐 كلمة المرور الخاصة بك:", type="password")
            
            if st.button("تسجيل الدخول ومباشرة التحدي 🚀"):
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
                        st.rerun()

else:
    login_phone = st.session_state["user_phone"]
    user_name = st.session_state["user_name"]
    
    st.sidebar.markdown(f"👤 المشارك: **{user_name}**")
    if st.sidebar.button("تسجيل الخروج 🚪"):
        st.session_state["is_logged_in"] = False
        st.session_state["user_phone"] = ""
        st.session_state["user_name"] = ""
        st.rerun()

    tabs_list = ["🏆🔥 لوحة الصدارة", "🤩 صالة التوقعات", "📅 جدول المباريات"]
    if login_phone == ADMIN_PHONE:
        tabs_list.append("⚙️ لوحة الإدارة")
        
    tabs = st.tabs(tabs_list)

    # --- 1. لوحة الصدارة وعرض الإحصائيات الحية المفتوحة ---
    with tabs[0]:
        cursor = db_conn.cursor()
        cursor.execute("SELECT name, points, phone, champion_pred FROM users ORDER BY points DESC")
        leaderboard_data = cursor.fetchall()
        
        user_rank = 0
        user_current_points = 0
        user_champ_saved = None
        for idx, row in enumerate(leaderboard_data):
            if row[2] == login_phone:
                user_rank = idx + 1
                user_current_points = row[1]
                user_champ_saved = row[3]
                break
        
        cursor.execute("""
            SELECT p.match_id, p.pred_home, p.pred_away, p.pred_pens_winner, p.is_joker, 
                   pm.actual_home, pm.actual_away, pm.actual_pens_winner 
            FROM predictions p
            JOIN processed_matches pm ON p.match_id = pm.match_id
            WHERE p.phone = ?
        """, (login_phone,))
        user_calculated_preds = cursor.fetchall()
        
        correct_count = 0
        wrong_count = 0
        for pred in user_calculated_preds:
            m_id, p_h, p_a, p_p, p_joker, a_h, a_a, a_p = pred
            is_ko = matches_dict.get(m_id, {}).get("is_knockout", False)
            earned = calculate_match_points(p_h, p_a, p_p, a_h, a_a, a_p, is_ko)
            if earned > 0: correct_count += 1
            else: wrong_count += 1
                
        total_user_preds = correct_count + wrong_count
        success_ratio = round((correct_count / total_user_preds) * 100, 1) if total_user_preds > 0 else 0.0
        
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-box">
                <div class="stat-box-label">✅ صحيحة </div>
                <div class="stat-box-value">{correct_count}</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">❌ خاطئة</div>
                <div class="stat-box-value">{wrong_count}</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">🎯 الدقة</div>
                <div class="stat-box-value">{success_ratio}%</div>
            </div>
            <div class="stat-box">
                <div class="stat-box-label">🎖️ ترتيبك</div>
                <div class="stat-box-value">#{user_rank}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
            
        share_stats_text = f"📊 *إحصائيات ملك التوقعات بالحديقة* 👑\n\n👤 *الاسم:* {user_name}\n🎖️ *الترتيب:* المركز {user_rank}\n🏆 *النقاط:* {user_current_points}\n🎯 *الدقة:* {success_ratio}%\n\n#WC26_KING 🔥⚽"
        wa_stats_link = "https://wa.me/?text=" + urllib.parse.quote(share_stats_text)
        st.link_button("📲 شارك بطاقتك وإحصائياتك فوراً", wa_stats_link)
        
        st.markdown("<h3 style='color:#FFD700;'>🥇 صدارة الترتيب العام</h3>", unsafe_allow_html=True)
        
        for idx, row in enumerate(leaderboard_data):
            p_name, p_points, p_phone, p_champ = row
            rank_icon = "🥇" if idx == 0 else ("🥈" if idx == 1 else ("🥉" if idx == 2 else f"#{idx+1}"))
            
            st.markdown(f"""
            <div class="leaderboard-row">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-size:18px;">{rank_icon}</span>
                    <span style="font-weight:bold; font-size:16px;">{p_name} {FLAGS.get(p_champ, '🏳️') if p_champ else ''}</span>
                </div>
                <div style="color:#FFD700; font-weight:bold;">🏆 {p_points} Pts</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 كشف التوقعات", key=f"rev_{p_phone}_{idx}"):
                st.session_state[f"view_predictions_for"] = p_phone
                st.session_state[f"view_predictions_name"] = p_name
                    
        if f"view_predictions_for" in st.session_state:
            target_phone = st.session_state[f"view_predictions_for"]
            target_name = st.session_state[f"view_predictions_name"]
            st.markdown(f"<div class='review-card'><b>📋 استعراض توقعات: {target_name}</b></div>", unsafe_allow_html=True)
            cursor.execute("SELECT match_id, pred_home, pred_away, pred_pens_winner FROM predictions WHERE phone = ?", (target_phone,))
            user_preds = {r[0]: (r[1], r[2], r[3]) for r in cursor.fetchall()}
            review_list = []
            for m in all_matches:
                m_desc = f"{m['team_home']} × {m['team_away']}"
                if m["id"] in user_preds:
                    txt = f"{user_preds[m['id']][0]} - {user_preds[m['id']][1]}"
                    if m["is_knockout"] and user_preds[m['id']][0] == user_preds[m['id']][1] and user_preds[m['id']][2]:
                        txt += f" (ترجيح: {user_preds[m['id']][2]})"
                else: txt = "لم يتوقع"
                review_list.append({"المباراة": m_desc, "التوقع": txt})
            st.dataframe(pd.DataFrame(review_list), hide_index=True, use_container_width=True)
            if st.button("إغلاق المراجعة ✖️"):
                del st.session_state[f"view_predictions_for"]
                st.rerun()

    # --- 2. صالة التوقعات (محدثة بالكامل بفلتر احترافي) ---
    with tabs[1]:
        cursor = db_conn.cursor()
        cursor.execute("SELECT champion_pred FROM users WHERE phone = ?", (login_phone,))
        current_champ = cursor.fetchone()[0]
        
        tournament_start_time = datetime(2026, 6, 28, 21, 0, tzinfo=ksa_tz)
        is_champ_locked = now_ksa >= tournament_start_time
        
        champ_html_badge = f"<div class='champion-saved-badge'>🎯 بطل المونديال المتوقع: {FLAGS.get(current_champ, '🔮')} {current_champ}</div>" if current_champ else "<div class='champion-saved-badge' style='background:linear-gradient(90deg, #ff5252, #ff1744); color:white !important;'>⚠️ لم تختر بطلاً بعد</div>"
        
        st.markdown(f"""
        <div class="champion-box-card">
            <h2 style="color: #FFD700; margin-bottom: 5px; font-weight: 900;">🏆 بطل كأس العالم 2026</h2>
            <p style="color: #cccccc; font-size: 14px;">حدد المنتخب الفائز باللقب قبل الإغلاق واكسب <b style="color:#FFD700;">+10 نقاط إضافية</b>!</p>
            {champ_html_badge}
        </div>
        """, unsafe_allow_html=True)
        
        all_teams = sorted(list(FLAGS.keys()))
        default_idx = all_teams.index(current_champ) if current_champ in all_teams else 0
            
        selected_champ = st.selectbox("👑 اختر البطل وعزز نقاطك:", all_teams, index=default_idx, disabled=is_champ_locked)
        
        c_champ_save, c_champ_share = st.columns(2)
        with c_champ_save:
            if not is_champ_locked:
                if st.button("🎯 اعتماد التوقع للبطل", key="save_champ"):
                    cursor.execute("UPDATE users SET champion_pred = ? WHERE phone = ?", (selected_champ, login_phone))
                    db_conn.commit()
                    st.success("تم تثبيت خيار البطل بنجاح!")
                    st.rerun()
        with c_champ_share:
            if current_champ:
                share_champ_text = f"🏆 *تحدي ملك المونديال* 👑\n\n👤 *المشارك:* {user_name}\n🏆 *توقعي لبطل كأس العالم 2026 هو: {current_champ} {FLAGS.get(current_champ, '')}* \n\n#WC26_KING 🔥"
                st.link_button("📲 مشاركة خيار البطل", "https://wa.me/?text=" + urllib.parse.quote(share_champ_text))
                
        st.markdown("<hr style='border: 1px dashed rgba(255,215,0,0.15); margin: 30px 0;'>", unsafe_allow_html=True)

        cursor.execute("SELECT COUNT(*) FROM predictions WHERE phone = ? AND is_joker = 1", (login_phone,))
        remaining_jokers = max(0, 8 - cursor.fetchone()[0])
        
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, rgba(255,215,0,0.15), rgba(0,0,0,0.2)); border: 1px solid #FFD700; border-radius: 16px; padding: 12px; text-align: center; margin-bottom: 25px;">
            <span style="font-size: 18px; font-weight: bold; color: #FFD700;">✌🏼 رصيد كروت (دبلها) المتبقي: {remaining_jokers} من 8</span>
        </div>
        """, unsafe_allow_html=True)

        # ⚡ فلتر احترافي لتنظيم تصفح المباريات
        filter_mode = st.radio("🔍 عرض وتصفية المباريات حسب الأدوار:", ["المباريات المتاحة الآن", "دور المجموعات", "الأدوار الإقصائية (خروج المغلوب)"], horizontal=True)
        hide_closed = st.toggle("🔴 إخفاء المواجهات المنتهية تماماً", value=False)
        
        for match in all_matches:
            time_until_match = match["time"] - now_ksa
            is_closed_original = now_ksa >= match["time"]
            
            # فلترة ذكية لتفادي التمرير اللانهائي
            if filter_mode == "المباريات المتاحة الآن" and is_closed_original: continue
            if filter_mode == "دور المجموعات" and match["is_knockout"]: continue
            if filter_mode == "الأدوار الإقصائية (خروج المغلوب)" and not match["is_knockout"]: continue
            if hide_closed and is_closed_original: continue
            
            cursor.execute("SELECT actual_home, actual_away, actual_pens_winner FROM processed_matches WHERE match_id = ?", (match["id"],))
            match_status_row = cursor.fetchone()
            
            home_flag = FLAGS.get(match['team_home'], '🏳️')
            away_flag = FLAGS.get(match['team_away'], '🏳️')
            
            # تحديد نوع البادج وطبيعة الكرت بصرياً
            if match_status_row and match_status_row[0] is not None:
                actual_h, actual_a, actual_p = match_status_row
                cursor.execute("SELECT pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE phone = ? AND match_id = ?", (login_phone, match["id"]))
                user_pred_row = cursor.fetchone()
                earned_pts = 0
                if user_pred_row:
                    earned_pts = calculate_match_points(user_pred_row[0], user_pred_row[1], user_pred_row[2], actual_h, actual_a, actual_p, match["is_knockout"])
                    if user_pred_row[3] == 1: earned_pts *= 2
                
                txt_p = f" (ترجيح: {actual_p})" if actual_p else ""
                badge_html = f"<span class='badge-status badge-done'>✅ انتهت | نقاطك: {earned_pts}</span>"
                score_html = f"<span style='font-size:26px; color:#FFD700;'>{actual_a} × {actual_h}</span>"
                is_calculated_and_valid = True
            else:
                if time_until_match < timedelta(minutes=10):
                    badge_html = "<span class='badge-status badge-closed'>🔒 مغلقة التوقع</span>"
                else:
                    badge_html = "<span class='badge-status badge-open'>🟢 باب التوقع مفتوح</span>"
                score_html = "<span style='font-size:22px; color:#bbb;'> VS </span>"
                is_calculated_and_valid = False
            
            match_ui_box = f"""
            <div class="match-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span style="font-size:12px; color:#aaa;">🕒 {match['time'].strftime('%d يونيو | %I:%M %p')}</span>
                    {badge_html}
                </div>
                <div style="display:flex; justify-content:center; align-items:center; gap:20px;">
                    <div style="text-align:center; flex:1;">
                        <div style="font-size:32px;">{away_flag}</div>
                        <div style="font-weight:bold; font-size:15px;">{match['team_away']}</div>
                    </div>
                    <div>{score_html}</div>
                    <div style="text-align:center; flex:1;">
                        <div style="font-size:32px;">{home_flag}</div>
                        <div style="font-weight:bold; font-size:15px;">{match['team_home']}</div>
                    </div>
                </div>
            </div>
            """
            
            st.markdown(match_ui_box, unsafe_allow_html=True)
            
            # مساحة التحكم والتفاعل تحت الكرت المطور مباشرة
            if not (time_until_match < timedelta(minutes=10) or is_calculated_and_valid):
                cursor.execute("SELECT pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE phone = ? AND match_id = ?", (login_phone, match["id"]))
                existing_pred = cursor.fetchone()
                val_home = existing_pred[0] if existing_pred else 0
                val_away = existing_pred[1] if existing_pred else 0
                val_pens = existing_pred[2] if existing_pred else match['team_home']
                is_joker_checked = bool(existing_pred[3]) if existing_pred else False
                
                c1, c2 = st.columns(2)
                with c1: h_score = st.number_input(f"أهداف {match['team_home']}", 0, 10, value=val_home, key=f"h_{match['id']}")
                with c2: a_score = st.number_input(f"أهداف {match['team_away']}", 0, 10, value=val_away, key=f"a_{match['id']}")
                
                pens_winner = None
                if match["is_knockout"] and h_score == a_score:
                    pens_winner = st.radio(f"🏆 فائز الترجيح الإلزامي:", [match['team_home'], match['team_away']], index=0 if val_pens == match['team_home'] else 1, key=f"pens_{match['id']}", horizontal=True)
                
                use_joker = st.checkbox("✌🏼 تفعيل كرت دبلها للمباراة", value=is_joker_checked, key=f"joker_{match['id']}")
                
                col_submit, col_share = st.columns(2)
                with col_submit:
                    if st.button("🚀 اعتماد التوقع", key=f"btn_{match['id']}"):
                        if use_joker and not is_joker_checked and remaining_jokers <= 0:
                            st.error("⚠️ نفذت جواكرك الـ 8 المتاحة!")
                            st.stop()
                        cursor.execute('''
                            INSERT INTO predictions (phone, match_id, pred_home, pred_away, pred_pens_winner, is_joker)
                            VALUES (?, ?, ?, ?, ?, ?)
                            ON CONFLICT(phone, match_id) DO UPDATE SET pred_home=excluded.pred_home, pred_away=excluded.pred_away, pred_pens_winner=excluded.pred_pens_winner, is_joker=excluded.is_joker
                        ''', (login_phone, match["id"], h_score, a_score, pens_winner, 1 if use_joker else 0))
                        db_conn.commit()
                        st.success("تم تأمين التوقع بالملف بنجاح!")
                        st.rerun()
                with col_share:
                    joker_tag = "✌🏼 [مباراة دبلها الكبرى]" if use_joker else ""
                    pens_tag = f" | (ترجيح: {pens_winner})" if pens_winner else ""
                    share_text = f"🏆 *ملك المونديال بالحديقة* 👑\n\n🎯 *توقعي لمواجهة: {match['team_home']} × {match['team_away']}*\n📊 النتيجة: {h_score} - {a_score} {pens_tag}\n{joker_tag}"
                    st.link_button("📲 مشاركة بالواتساب", "https://wa.me/?text=" + urllib.parse.quote(share_text), key=f"share_{match['id']}")

    # --- 3. جدول المواعيد المنظم وفترات الفتح ---
    with tabs[2]:
        st.subheader("📅 مواعيد فتح وقفل التوقعات")
        rows = []
        for match in all_matches:
            open_time = match["time"] - timedelta(hours=24)
            status = "🔴 مغلق" if now_ksa >= match["time"] else ("🟢 مفتوح الآن" if now_ksa >= open_time else "🟡 قريباً")
            rows.append({
                "المباراة": f"{match['team_home']} × {match['team_away']}",
                "فتح التوقع": open_time.strftime("%d/%m %I:%M %p"),
                "انطلاق اللقاء": match["time"].strftime("%d/%m %I:%M %p"),
                "الوضع الحلي": status
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    # --- 4. لوحة الإدارة الفاخرة والآمنة (أحمد بادحمان) ---
    if login_phone == ADMIN_PHONE:
        with tabs[3]:
            st.markdown('<div class="admin-card">⚙️ <b>لوحة القيادة والمشرف العام (أحمد بادحمان)</b></div>', unsafe_allow_html=True)
            cursor = db_conn.cursor()
            
            st.subheader("🧮 إدخال واحتساب النتائج")
            match_options = {f"{m['team_home']} × {m['team_away']}": m for m in all_matches}
            selected_match_str = st.selectbox("اختر مباراة لحسم نقاطها:", list(match_options.keys()))
            selected_match = match_options[selected_match_str]
            
            cursor.execute("SELECT actual_home, actual_away, actual_pens_winner FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
            already_calculated = cursor.fetchone()
            is_valid_old_result = already_calculated and already_calculated[0] is not None
            
            if is_valid_old_result:
                st.warning(f"المباراة محسومة سابقاً بنتيجة: {already_calculated[0]} - {already_calculated[1]}")
                if st.button("🚨 إلغاء النتيجة وسحب النقاط من الأعضاء"):
                    cursor.execute("SELECT phone, pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE match_id = ?", (selected_match["id"],))
                    for pred in cursor.fetchall():
                        old_points = calculate_match_points(pred[1], pred[2], pred[3], already_calculated[0], already_calculated[1], already_calculated[2], selected_match["is_knockout"])
                        if pred[4] == 1: old_points *= 2
                        if old_points > 0: cursor.execute("UPDATE users SET points = MAX(0, points - ?) WHERE phone = ?", (old_points, pred[0]))
                    cursor.execute("DELETE FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
                    db_conn.commit()
                    st.rerun()
            
            c_act_h, c_act_a = st.columns(2)
            with c_act_h: actual_h = st.number_input("أهداف المستضيف الفعلي", 0, 10, value=already_calculated[0] if is_valid_old_result else 0)
            with c_act_a: actual_a = st.number_input("أهداف الضيف الفعلي", 0, 10, value=already_calculated[1] if is_valid_old_result else 0)
            
            actual_p = None
            if selected_match["is_knockout"] and actual_h == actual_a:
                actual_p = st.radio("الفائز الفعلي بالبنتيات:", [selected_match['team_home'], selected_match['team_away']])
            
            if st.button("🔥 حسم النقاط وتحديث الصدارة"):
                cursor.execute("SELECT phone, pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE match_id = ?", (selected_match["id"],))
                for pred in cursor.fetchall():
                    pts = calculate_match_points(pred[1], pred[2], pred[3], actual_h, actual_a, actual_p, selected_match["is_knockout"])
                    if pred[4] == 1: pts *= 2
                    if pts > 0: cursor.execute("UPDATE users SET points = points + ? WHERE phone = ?", (pts, pred[0]))
                cursor.execute('INSERT INTO processed_matches (match_id, actual_home, actual_away, actual_pens_winner) VALUES (?, ?, ?, ?)', (selected_match["id"], actual_h, actual_a, actual_p))
                db_conn.commit()
                st.success("تم تحديث وحسم ترتيب لوحة الصدارة الملكية!")
                st.rerun()
                
    # --- 4. لوحة الإدارة الفاخرة والآمنة (أحمد بادحمان) ---
    if login_phone == ADMIN_PHONE:
        with tabs[3]:
            st.markdown('<div class="admin-card">⚙️ <b>لوحة المشرف العام والتحكم الكامل (أحمد بادحمان)</b></div>', unsafe_allow_html=True)
            cursor = db_conn.cursor()
            
            # ---------------- SECTION 1: إدارة بيانات الأعضاء والسرية ----------------
            st.markdown("<h3 style='color:#FFD700;'>👥 لوحة التحكم بالأعضاء (الأرقام والباسوردات)</h3>", unsafe_allow_html=True)
            
            cursor.execute("SELECT name, phone, password, points FROM users ORDER BY points DESC")
            all_users_rows = cursor.fetchall()
            
            users_df_list = []
            for u_row in all_users_rows:
                users_df_list.append({
                    "👨🏽 الاسم": u_row[0],
                    "📱 رقم الجوال": u_row[1],
                    "🔐 كلمة المرور": u_row[2],
                    "🏆 النقاط الحالية": u_row[3]
                })
            
            # عرض جدول البيانات بالكامل للمشرف
            st.dataframe(pd.DataFrame(users_df_list), use_container_width=True, hide_index=True)
            
            # ---------------- SECTION 2: إضافة وتعديل النقاط يدوياً ----------------
            st.markdown("<h3 style='color:#FFD700;'>✍🏼 تعديل وإضافة نقاط يدوية للمستخدمين</h3>", unsafe_allow_html=True)
            
            user_select_options = {f"{u[0]} ({u[1]})": u[1] for u in all_users_rows}
            selected_user_for_points = st.selectbox("اختر العضو المراد تعديل نقاطه:", list(user_select_options.keys()))
            target_user_phone = user_select_options[selected_user_for_points]
            
            col_pts_type, col_pts_val = st.columns(2)
            with col_pts_type:
                operation_type = st.radio("نوع العملية:", ["➕ إضافة نقاط", "➖ خصم نقاط"], horizontal=True)
            with col_pts_val:
                points_to_change = st.number_input("مقدار النقاط:", min_value=1, max_value=100, value=5)
                
            if st.button("🎯 اعتماد تعديل النقاط يدوياً"):
                cursor.execute("SELECT points, name FROM users WHERE phone = ?", (target_user_phone,))
                current_pts, target_name = cursor.fetchone()
                
                if "إضافة" in operation_type:
                    new_pts_total = current_pts + points_to_change
                else:
                    new_pts_total = max(0, current_pts - points_to_change)
                    
                cursor.execute("UPDATE users SET points = ? WHERE phone = ?", (new_pts_total, target_user_phone))
                db_conn.commit()
                st.success(f"✅ تم تحديث نقاط {target_name} بنجاح! الرصيد الجديد: {new_pts_total} نقطة.")
                st.rerun()
                
            st.markdown("<hr style='border: 1px dashed rgba(255,215,0,0.15); margin: 25px 0;'>", unsafe_allow_html=True)

            # ---------------- SECTION 3: احتساب نتائج المباريات (المنطق السابق) ----------------
            st.markdown("<h3 style='color:#FFD700;'>🧮 إدخال واحتساب نتائج المباريات</h3>", unsafe_allow_html=True)
            match_options = {f"{m['team_home']} × {m['team_away']}": m for m in all_matches}
            selected_match_str = st.selectbox("اختر مباراة لحسم نقاطها:", list(match_options.keys()))
            selected_match = match_options[selected_match_str]
            
            cursor.execute("SELECT actual_home, actual_away, actual_pens_winner FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
            already_calculated = cursor.fetchone()
            is_valid_old_result = already_calculated and already_calculated[0] is not None
            
            if is_valid_old_result:
                st.warning(f"المباراة محسومة سابقاً بنتيجة: {already_calculated[0]} - {already_calculated[1]}")
                if st.button("🚨 إلغاء النتيجة وسحب النقاط من الأعضاء"):
                    cursor.execute("SELECT phone, pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE match_id = ?", (selected_match["id"],))
                    for pred in cursor.fetchall():
                        old_points = calculate_match_points(pred[1], pred[2], pred[3], already_calculated[0], already_calculated[1], already_calculated[2], selected_match["is_knockout"])
                        if pred[4] == 1: old_points *= 2
                        if old_points > 0: cursor.execute("UPDATE users SET points = MAX(0, points - ?) WHERE phone = ?", (old_points, pred[0]))
                    cursor.execute("DELETE FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
                    db_conn.commit()
                    st.rerun()
            
            c_act_h, c_act_a = st.columns(2)
            with c_act_h: actual_h = st.number_input("أهداف المستضيف الفعلي", 0, 10, value=already_calculated[0] if is_valid_old_result else 0)
            with c_act_a: actual_a = st.number_input("أهداف الضيف الفعلي", 0, 10, value=already_calculated[1] if is_valid_old_result else 0)
            
            actual_p = None
            if selected_match["is_knockout"] and actual_h == actual_a:
                actual_p = st.radio("الفائز الفعلي بالبنتيات:", [selected_match['team_home'], selected_match['team_away']])
            
            if st.button("🔥 حسم النقاط وتحديث الصدارة"):
                cursor.execute("SELECT phone, pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE match_id = ?", (selected_match["id"],))
                for pred in cursor.fetchall():
                    pts = calculate_match_points(pred[1], pred[2], pred[3], actual_h, actual_a, actual_p, selected_match["is_knockout"])
                    if pred[4] == 1: pts *= 2
                    if pts > 0: cursor.execute("UPDATE users SET points = points + ? WHERE phone = ?", (pts, pred[0]))
                cursor.execute('INSERT INTO processed_matches (match_id, actual_home, actual_away, actual_pens_winner) VALUES (?, ?, ?, ?)', (selected_match["id"], actual_h, actual_a, actual_p))
                db_conn.commit()
                st.success("تم تحديث وحسم ترتيب لوحة الصدارة الملكية!")
                st.rerun()

