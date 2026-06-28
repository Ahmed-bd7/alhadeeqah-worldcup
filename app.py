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

st.set_page_config(page_title="⚽🏆 WC26 KING", page_icon="⚽", layout="centered")

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

# ══════════════════════════════════════════════
#  CSS الكامل — مطابق لتصميم HTML
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

/* ── TOKENS ── */
:root {
  --gold:   #FFD700;
  --gold-d: #b8960a;
  --green:  #00c853;
  --green2: #00e676;
  --glass:  rgba(255,255,255,0.06);
  --border: rgba(255,255,255,0.10);
  --text:   #e8f5e9;
  --muted:  #7fada2;
  --red:    #ff5252;
}

/* ── BASE ── */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  font-family: 'Cairo', sans-serif !important;
  background: radial-gradient(ellipse at 30% 0%, #0d2b14 0%, #06120a 65%) !important;
  color: var(--text) !important;
}
[data-testid="stHeader"]         { background: transparent !important; }
[data-testid="stToolbar"]        { display: none !important; }
[data-testid="stSidebar"]        { background: rgba(6,18,10,0.97) !important; border-left: 1px solid var(--border); }
[data-testid="stSidebarContent"] p,
[data-testid="stSidebarContent"] div { color: var(--text) !important; }
section[data-testid="stMain"] > div { padding-top: 0 !important; }

/* force text color everywhere */
p, label, div, span, li, h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText { color: var(--text) !important; }

/* ── HERO TITLE ── */
.wc-hero {
  text-align: center;
  padding: 36px 20px 22px;
  position: relative;
}
.wc-hero::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(255,215,0,0.08) 0%, transparent 70%);
  pointer-events: none;
}
.wc-badge {
  display: inline-block;
  background: rgba(255,215,0,0.10);
  border: 1px solid rgba(255,215,0,0.28);
  border-radius: 50px;
  padding: 4px 16px;
  font-size: 11px; font-weight: 700; letter-spacing: 2px;
  color: var(--gold); margin-bottom: 12px; text-transform: uppercase;
}
.wc-title {
  font-size: clamp(30px, 8vw, 56px); font-weight: 900;
  color: var(--gold) !important; line-height: 1.1; margin: 0;
  text-shadow: 0 0 40px rgba(255,215,0,0.30);
}
.wc-sub {
  font-size: 14px; color: var(--muted) !important; margin-top: 6px;
}
.wc-line {
  width: 50px; height: 3px; margin: 14px auto 0;
  background: linear-gradient(90deg, var(--green), var(--gold));
  border-radius: 3px;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: rgba(6,18,10,0.85) !important;
  border-radius: 16px !important;
  border: 1px solid var(--border) !important;
  padding: 4px !important; gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; border-radius: 12px !important;
  color: var(--muted) !important; font-weight: 700 !important;
  font-family: 'Cairo', sans-serif !important; padding: 8px 10px !important;
  transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
  background: rgba(255,215,0,0.12) !important;
  color: var(--gold) !important;
  box-shadow: 0 0 0 1px rgba(255,215,0,0.28) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabContent { padding-top: 16px !important; }

/* ── BUTTONS ── */
.stButton > button {
  width: 100% !important; height: 46px !important;
  border-radius: 14px !important; border: none !important;
  background: linear-gradient(90deg, var(--green), var(--green2)) !important;
  color: #fff !important; font-weight: 700 !important;
  font-family: 'Cairo', sans-serif !important; font-size: 14px !important;
  transition: all .2s !important;
  box-shadow: 0 4px 16px rgba(0,200,83,0.18) !important;
}
.stButton > button:hover {
  background: linear-gradient(90deg, var(--gold-d), var(--gold)) !important;
  color: #000 !important; box-shadow: 0 4px 20px rgba(255,215,0,0.25) !important;
}
.stButton > button:active { transform: scale(0.97) !important; }

/* danger button override */
.btn-danger > button {
  background: rgba(255,82,82,0.15) !important;
  border: 1px solid rgba(255,82,82,0.30) !important;
  color: var(--red) !important;
  box-shadow: none !important;
}

/* link buttons */
.stLinkButton a {
  display: flex !important; align-items: center !important; justify-content: center !important;
  width: 100% !important; height: 46px !important; border-radius: 14px !important;
  border: 1px solid rgba(37,211,102,0.30) !important;
  background: rgba(37,211,102,0.09) !important; color: var(--green2) !important;
  font-weight: 700 !important; font-family: 'Cairo', sans-serif !important;
  font-size: 13px !important; text-decoration: none !important;
  transition: background .15s !important;
}
.stLinkButton a:hover { background: rgba(37,211,102,0.17) !important; }

/* ── INPUTS / SELECTS ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stPasswordInput"] input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid var(--border) !important; border-radius: 12px !important;
  color: var(--text) !important; font-family: 'Cairo', sans-serif !important;
  font-size: 16px !important; font-weight: 700 !important; text-align: center !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus,
[data-testid="stPasswordInput"] input:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 2px rgba(255,215,0,0.12) !important;
}
[data-testid="stSelectbox"] > div > div {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important; color: var(--text) !important;
  font-family: 'Cairo', sans-serif !important;
}
[data-testid="stCheckbox"] label span { color: var(--text) !important; }
[data-testid="stToggle"] label { color: var(--text) !important; }
[data-testid="stRadio"] label { color: var(--text) !important; }

/* ── AUTH CARD ── */
.auth-card {
  background: var(--glass);
  border: 1px solid var(--border);
  border-radius: 22px; padding: 26px 22px; margin-bottom: 16px;
}
.auth-card-title {
  font-size: 18px; font-weight: 900; color: var(--gold) !important; margin-bottom: 18px;
}
.info-box {
  background: rgba(0,200,83,0.07);
  border: 1px solid rgba(0,200,83,0.18);
  border-radius: 16px; padding: 16px;
  font-size: 13px; line-height: 1.8; color: var(--text) !important;
}
.info-box strong { color: var(--gold) !important; }

/* ── STATS BAR ── */
.stats-container {
  display: grid; grid-template-columns: repeat(4,1fr);
  gap: 8px; margin-bottom: 16px; direction: rtl;
}
.stat-box {
  background: var(--glass); border: 1px solid var(--border);
  border-radius: 14px; padding: 12px 6px; text-align: center;
}
.stat-box-label {
  font-size: clamp(10px,2.5vw,12px); color: var(--muted) !important;
  margin-bottom: 3px; white-space: nowrap;
}
.stat-box-value {
  font-size: clamp(14px,3.5vw,19px); font-weight: 900;
  color: var(--gold) !important; white-space: nowrap;
}

/* ── LEADERBOARD ROW ── */
.lb-row {
  display: flex; align-items: center; gap: 10px;
  background: var(--glass); border: 1px solid var(--border);
  border-radius: 14px; padding: 11px 14px; margin-bottom: 6px;
  transition: background .15s;
}
.lb-row:hover { background: rgba(255,255,255,0.09); }
.lb-row.me { border-color: rgba(255,215,0,0.32); background: rgba(255,215,0,0.06); }
.lb-rank { font-size: 16px; font-weight: 900; width: 32px; text-align: center; flex-shrink: 0; }
.lb-name { flex: 1; font-size: 14px; font-weight: 700; color: var(--text) !important; }
.lb-pts  { font-weight: 900; color: var(--gold) !important; font-size: 15px; white-space: nowrap; }

/* ── MATCH CARD ── */
.match-card {
  background: var(--glass); border: 1px solid var(--border);
  border-radius: 20px; padding: 16px 14px; margin: 8px 0 14px;
  position: relative; overflow: hidden;
}
.match-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, rgba(255,215,0,0.40), transparent);
}
.match-card.done  { border-color: rgba(0,200,83,0.28); }
.match-card.done::before  { background: linear-gradient(90deg, transparent, rgba(0,200,83,0.55), transparent); }
.match-card.locked { border-color: rgba(255,82,82,0.20); }

.match-teams {
  display: flex; align-items: center; justify-content: space-between;
  gap: 6px; margin-bottom: 8px; direction: rtl;
}
.team-side   { flex: 1; text-align: center; }
.team-flag   { font-size: 28px; display: block; line-height: 1.1; }
.team-name   { font-size: 11px; font-weight: 700; color: var(--text) !important; margin-top: 3px; }
.match-vs    { font-size: 20px; font-weight: 900; color: var(--gold) !important; text-align: center; flex-shrink: 0; }
.match-score { font-size: 22px; font-weight: 900; color: var(--gold) !important; text-align: center; flex-shrink: 0; white-space: nowrap; }
.match-meta  { text-align: center; font-size: 11px; color: var(--muted) !important; margin-bottom: 12px; }
.match-done-tag   { text-align: center; font-size: 12px; color: var(--green2) !important; font-weight: 700; margin-bottom: 10px; }
.match-locked-tag { text-align: center; font-size: 12px; color: var(--red) !important; font-weight: 700; margin-bottom: 10px; }

/* ── JOKER BANNER ── */
.joker-banner {
  background: rgba(255,215,0,0.07); border: 1px solid rgba(255,215,0,0.20);
  border-radius: 16px; padding: 13px 16px; text-align: center; margin-bottom: 16px;
}
.joker-banner strong { color: var(--gold) !important; font-size: 17px; }
.joker-banner small  { font-size: 11px; color: var(--muted) !important; display: block; margin-top: 2px; }

/* ── CHAMPION CARD ── */
.champion-box-card {
  background: linear-gradient(135deg, rgba(255,215,0,0.09), rgba(0,77,43,0.28));
  border: 1px solid rgba(255,215,0,0.22); border-radius: 22px;
  padding: 22px 16px; margin: 14px 0 18px; text-align: center;
}
.champion-box-card h2 {
  color: var(--gold) !important; font-size: clamp(17px,5vw,22px);
  font-weight: 900; margin-bottom: 5px;
}
.champion-saved-badge {
  background: linear-gradient(90deg, var(--gold-d), var(--gold));
  color: #000 !important; font-weight: 900; font-size: 14px;
  padding: 7px 20px; border-radius: 50px; display: inline-block;
  margin-top: 10px; box-shadow: 0 4px 14px rgba(255,215,0,0.20);
}

/* ── ADMIN / REVIEW ── */
.admin-card {
  background: linear-gradient(135deg, rgba(91,50,0,0.55), rgba(184,134,11,0.30));
  border: 1px solid rgba(184,134,11,0.28); border-radius: 18px;
  padding: 18px; margin-bottom: 14px;
}
.review-card {
  background: linear-gradient(135deg, rgba(0,77,43,0.45), rgba(0,168,90,0.22));
  border: 1px solid rgba(0,168,90,0.22); border-radius: 18px;
  padding: 16px; margin-bottom: 12px;
}

/* ── SECTION LABEL ── */
.sec-label {
  font-size: 11px; font-weight: 700; color: var(--muted) !important;
  text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px;
}

/* ── DIVIDER ── */
.wc-divider { border: none; border-top: 1px dashed rgba(255,215,0,0.18); margin: 22px 0; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: 14px !important; overflow: hidden; border: 1px solid var(--border) !important; }
[data-testid="stDataFrame"] th { background: rgba(255,215,0,0.08) !important; color: var(--gold) !important; font-weight: 700 !important; }
[data-testid="stDataFrame"] td { color: var(--text) !important; background: rgba(255,255,255,0.03) !important; }

/* ── ALERTS ── */
[data-testid="stAlert"] { border-radius: 14px !important; }
div[data-testid="stAlert"] p { color: inherit !important; }

/* ── SIDEBAR LOGOUT ── */
[data-testid="stSidebarContent"] .stButton > button {
  background: rgba(255,82,82,0.12) !important;
  border: 1px solid rgba(255,82,82,0.28) !important;
  color: var(--red) !important; box-shadow: none !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,215,0,0.20); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ══ HERO ══
st.markdown("""
<div class="wc-hero">
  <div class="wc-badge">🇸🇦 كأس العالم 2026</div>
  <div class="wc-title">WC26 KING 🏆</div>
  <div class="wc-sub">تحدي ملك المونديال في الحديقة ⚽️</div>
  <div class="wc-line"></div>
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
    
    try:
        cursor.execute("ALTER TABLE predictions ADD COLUMN is_joker INTEGER DEFAULT 0")
    except sqlite3.OperationalError: pass
        
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN champion_pred TEXT DEFAULT NULL")
    except sqlite3.OperationalError: pass

    try:
        cursor.execute("ALTER TABLE predictions ADD COLUMN pred_pens_winner TEXT DEFAULT NULL")
    except sqlite3.OperationalError: pass

    try:
        cursor.execute("ALTER TABLE processed_matches ADD COLUMN actual_pens_winner TEXT DEFAULT NULL")
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
{"id": 76, "team_home": "هولندا", "team_away": "المغرب", "time": datetime(2026, 6, 30, 4, 0, tzinfo=ksa_tz), "is_knockout": True},
{"id": 77, "team_home": "النرويج", "team_away": "ساحل العاج", "time": datetime(2026, 6, 30, 20, 0, tzinfo=ksa_tz), "is_knockout": True},
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

# دالة ذكية وموحدة لاحتساب النقاط
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

# ══════════════════════════════════════════════
#  SESSION STATE + LOGIN
# ══════════════════════════════════════════════
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    st.session_state["user_phone"] = ""
    st.session_state["user_name"] = ""

if not st.session_state["is_logged_in"]:
    tab_auth, tab_info = st.tabs(["🔐 بوابة الأعضاء", "ℹ️ معلومات التحدي"])

    with tab_auth:
        menu = ["تسجيل الدخول", "إنشاء حساب جديد (لأول مرة)"]
        choice = st.radio("إختر الإجراء:", menu, horizontal=True)

        if choice == "إنشاء حساب جديد (لأول مرة)":
            st.markdown('<div class="auth-card"><div class="auth-card-title">📝 انضم لتحدي الحديقة</div>', unsafe_allow_html=True)
            with st.form("registration_form"):
                new_name  = st.text_input("👤 اسمك")
                new_phone = st.text_input("📱 رقم الجوال (10 أرقام)", max_chars=10)
                new_pass  = st.text_input("🔐 كلمة مرور خاصة", type="password")
                submit_reg = st.form_submit_button("إنشاء الحساب 🚀")
                if submit_reg:
                    new_phone = str(new_phone).strip()
                    new_name  = str(new_name).strip()
                    new_pass  = str(new_pass).strip()
                    if not new_name or not new_phone or not new_pass:
                        st.error("❌ يرجى تعبئة جميع الخانات.")
                    elif len(new_phone) != 10 or not new_phone.isdigit():
                        st.error("❌ رقم الجوال يجب أن يتكون من 10 أرقام فقط.")
                    else:
                        cursor = db_conn.cursor()
                        cursor.execute("SELECT phone FROM users WHERE phone = ?", (new_phone,))
                        if cursor.fetchone():
                            st.error("⚠️ رقم الجوال مسجل مسبقاً!")
                        else:
                            cursor.execute("INSERT INTO users (name, points, phone, password) VALUES (?, ?, ?, ?)", (new_name, 0, new_phone, new_pass))
                            db_conn.commit()
                            st.success(f"🎉 تم إنشاء حسابك بنجاح يا {new_name}! انتقل لتسجيل الدخول.")
                            st.balloons()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="auth-card"><div class="auth-card-title">  🇸🇦👋 هلا فيكم ارحببووو</div>', unsafe_allow_html=True)
            login_phone = st.text_input("📱 رقم الجوال", max_chars=10)
            login_pass  = st.text_input("🔐 كلمة المرور", type="password")
            if st.button("تسجيل الدخول 🚀"):
                if login_phone and login_pass:
                    login_phone = str(login_phone).strip()
                    login_pass  = str(login_pass).strip()
                    cursor = db_conn.cursor()
                    cursor.execute("SELECT name, password FROM users WHERE phone = ?", (login_phone,))
                    user_row = cursor.fetchone()
                    if not user_row:
                        st.error("❌ رقم الجوال غير مسجل!")
                    elif user_row[1] != login_pass:
                        st.error("❌ كلمة المرور غير صحيحة!")
                    else:
                        st.session_state["is_logged_in"] = True
                        st.session_state["user_phone"]   = login_phone
                        st.session_state["user_name"]    = user_row[0]
                        st.success(f"مرحباً بعودتك يا {user_row[0]}! 😎")
                        st.rerun()
                else:
                    st.error("❌ أدخل رقم الجوال وكلمة المرور.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          🏆 <strong>تحدي ملك المونديال</strong><br>
          توقع نتائج مباريات كأس العالم 2026 واجمع النقاط!<br>
          ✅ توقع صحيح الفائز = <strong>1 نقطة</strong><br>
          🎯 نتيجة دقيقة = <strong>3 نقاط</strong><br>
          ✌🏼 فعّل <strong>دبلها</strong> لمضاعفة نقاطك في 8 مباريات<br>
          👑 توقع البطل الصحيح = <strong>+10 نقاط</strong>
        </div>
        """, unsafe_allow_html=True)

    with tab_info:
        st.markdown("""
        ### ارحححبووو في تحدي كنق المونديال 😍🏆
        هذا التبويب مخصص للترحيب بأعضاء الحديقة قبل تسجيل الدخول.
        """)

else:
    login_phone = st.session_state["user_phone"]
    user_name   = st.session_state["user_name"]

    st.sidebar.markdown(f"👤 **{user_name}**")
    if st.sidebar.button("تسجيل الخروج 🚪"):
        st.session_state["is_logged_in"] = False
        st.session_state["user_phone"]   = ""
        st.session_state["user_name"]    = ""
        st.rerun()

    if login_phone == ADMIN_PHONE:
        tab_leaderboard, tab_predict, tab_schedule, tab_admin = st.tabs([
            "🏆 الصدارة", "⚽ التوقعات", "📅 المواعيد", "⚙️ الإدارة"
        ])
    else:
        tab_leaderboard, tab_predict, tab_schedule = st.tabs([
            "🏆 الصدارة", "⚽ التوقعات", "📅 المواعيد"
        ])

    # ══ تبويب الصدارة ══
    with tab_leaderboard:
        cursor = db_conn.cursor()
        cursor.execute("SELECT name, points, phone, champion_pred FROM users ORDER BY points DESC")
        leaderboard_data = cursor.fetchall()

        user_rank = 0; user_current_points = 0; user_champ_saved = None
        for idx, row in enumerate(leaderboard_data):
            if row[2] == login_phone:
                user_rank = idx + 1; user_current_points = row[1]; user_champ_saved = row[3]; break

        cursor.execute("""
            SELECT p.match_id, p.pred_home, p.pred_away, p.pred_pens_winner, p.is_joker,
                   pm.actual_home, pm.actual_away, pm.actual_pens_winner
            FROM predictions p
            JOIN processed_matches pm ON p.match_id = pm.match_id
            WHERE p.phone = ?
        """, (login_phone,))
        user_calculated_preds = cursor.fetchall()

        correct_count = 0; wrong_count = 0
        for pred in user_calculated_preds:
            m_id, p_h, p_a, p_p, p_joker, a_h, a_a, a_p = pred
            is_ko = matches_dict.get(m_id, {}).get("is_knockout", False)
            earned = calculate_match_points(p_h, p_a, p_p, a_h, a_a, a_p, is_ko)
            if earned > 0: correct_count += 1
            else: wrong_count += 1

        total_user_preds = correct_count + wrong_count
        success_ratio = round((correct_count / total_user_preds) * 100, 1) if total_user_preds > 0 else 0.0

        # إحصائيات
        st.markdown(f'<div class="sec-label">📊 إحصائياتك — {user_name}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stats-container">
          <div class="stat-box"><div class="stat-box-label">✅ صحيحة</div><div class="stat-box-value">{correct_count}</div></div>
          <div class="stat-box"><div class="stat-box-label">❌ خاطئة</div><div class="stat-box-value">{wrong_count}</div></div>
          <div class="stat-box"><div class="stat-box-label">🎯 دقة</div><div class="stat-box-value">{success_ratio}%</div></div>
          <div class="stat-box"><div class="stat-box-label">🎖️ ترتيب</div><div class="stat-box-value">#{user_rank}</div></div>
        </div>
        """, unsafe_allow_html=True)

        share_stats_text = f"📊 *حصيلة ملك التوقعات في الحديقة* 👑\n\n👤 *الاسم:* {user_name}\n🎖️ *الترتيب الحالي:* المركز {user_rank}\n🏆 *مجموع النقاط:* {user_current_points} نقطة\n\n📈 *أرقام التحدي:*\n✅ التوقعات الصحيحة: {correct_count}\n❌ التوقعات الخاطئة: {wrong_count}\n🎯 نسبة دقة التوقعات: {success_ratio}%\n\n#WC26_KING 🔥⚽️"
        wa_stats_link = "https://wa.me/?text=" + urllib.parse.quote(share_stats_text)
        st.link_button("📲 شارك ترتيبك وإحصائياتك", wa_stats_link)

        st.markdown('<hr class="wc-divider">', unsafe_allow_html=True)
        st.markdown('<div class="sec-label">🏅 جدول الترتيب</div>', unsafe_allow_html=True)

        # قائمة الصدارة
        for idx, row in enumerate(leaderboard_data):
            p_name, p_points, p_phone, p_champ = row
            rank_icon = "🥇" if idx == 0 else ("🥈" if idx == 1 else ("🥉" if idx == 2 else f"#{idx+1}"))
            champ_flag = FLAGS.get(p_champ, '') if p_champ else ''
            is_me = "me" if p_phone == login_phone else ""
            st.markdown(f"""
            <div class="lb-row {is_me}">
              <div class="lb-rank">{rank_icon}</div>
              <div class="lb-name">{p_name} {champ_flag}</div>
              <div class="lb-pts">🏆 {p_points} Pts</div>
            </div>
            """, unsafe_allow_html=True)
            col_btn, _ = st.columns([1, 3])
            with col_btn:
                if st.button("🔍 مشاهدة التوقعات", key=f"rev_{p_phone}_{idx}"):
                    st.session_state["view_predictions_for"]  = p_phone
                    st.session_state["view_predictions_name"] = p_name

        if "view_predictions_for" in st.session_state:
            target_phone = st.session_state["view_predictions_for"]
            target_name  = st.session_state["view_predictions_name"]
            st.markdown(f'<div class="review-card"><b>كشف توقعات: {target_name}</b></div>', unsafe_allow_html=True)
            cursor.execute("SELECT match_id, pred_home, pred_away, pred_pens_winner FROM predictions WHERE phone = ?", (target_phone,))
            user_preds = {r[0]: (r[1], r[2], r[3]) for r in cursor.fetchall()}
            review_list = []
            for m in all_matches:
                m_desc = f"{m['team_home']} × {m['team_away']}"
                if m["id"] in user_preds:
                    txt = f"{user_preds[m['id']][0]} - {user_preds[m['id']][1]}"
                    if m["is_knockout"] and user_preds[m['id']][0] == user_preds[m['id']][1] and user_preds[m['id']][2]:
                        txt += f" (ترجيح: {user_preds[m['id']][2]})"
                else:
                    txt = "لم يتوقع"
                review_list.append({"المباراة": m_desc, "التوقع": txt})
            st.dataframe(pd.DataFrame(review_list), hide_index=True, use_container_width=True)
            if st.button("إغلاق ✖️"):
                del st.session_state["view_predictions_for"]
                st.rerun()

    # ══ تبويب التوقعات ══
    with tab_predict:
        cursor = db_conn.cursor()

        # بطل كأس العالم
        cursor.execute("SELECT champion_pred FROM users WHERE phone = ?", (login_phone,))
        current_champ = cursor.fetchone()[0]
        tournament_start_time = datetime(2026, 6, 28, 21, 0, tzinfo=ksa_tz)
        is_champ_locked = now_ksa >= tournament_start_time

        champ_html_badge = (
            f"<div class='champion-saved-badge'>🎯 توقعك: {FLAGS.get(current_champ,'🔮')} {current_champ}</div>"
            if current_champ else
            "<div class='champion-saved-badge' style='background:linear-gradient(90deg,#ff5252,#ff1744);color:white!important;'>⚠️ لم تختر بطلاً بعد</div>"
        )

        st.markdown(f"""
        <div class="champion-box-card">
          <h2>🏆 بطل كأس العالم 2026</h2>
          <p style="color:#ccc;font-size:13px;margin-bottom:5px;">توقع المنتخب الفائز واكسب <b style="color:#FFD700;">+10 نقاط</b> إضافية!</p>
          <p style="color:#ff9800;font-size:12px;font-weight:700;margin-bottom:8px;">🔒 يقفل 28 يونيو الساعة 9:00م</p>
          {champ_html_badge}
        </div>
        """, unsafe_allow_html=True)

        all_teams = sorted(list(FLAGS.keys()))
        try:
            default_idx = all_teams.index(current_champ) if current_champ in all_teams else 0
        except ValueError:
            default_idx = 0

        selected_champ = st.selectbox("👑 اختر المنتخب الفائز باللقب", all_teams, index=default_idx,
                                      disabled=is_champ_locked, key="champ_prediction_select")

        c_champ_save, c_champ_share = st.columns(2)
        with c_champ_save:
            if is_champ_locked:
                st.error("🔒 مغلق!")
            else:
                if st.button("🎯 اعتماد توقع البطل", key="save_champion_btn"):
                    cursor.execute("UPDATE users SET champion_pred = ? WHERE phone = ?", (selected_champ, login_phone))
                    db_conn.commit()
                    st.success(f"تم تثبيت {selected_champ} 🔥")
                    st.rerun()
        with c_champ_share:
            if current_champ:
                champ_flag = FLAGS.get(current_champ, '🏳️')
                share_champ_text = f"👑 *تحدي ملك المونديال في الحديقة* 👑\n\n👤 *المشارك:* {user_name}\n🏆 *توقعي لبطل كأس العالم 2026:*\n✨ *{current_champ} {champ_flag}* ✨\n\n#WC26_KING 🔥⚽️"
                wa_champ_link = "https://wa.me/?text=" + urllib.parse.quote(share_champ_text)
                st.link_button("📲 مشاركة البطل", wa_champ_link)
            else:
                st.info("💡 احفظ خيار البطل أولاً.")

        st.markdown('<hr class="wc-divider">', unsafe_allow_html=True)

        # رصيد الجوكر
        cursor.execute("SELECT COUNT(*) FROM predictions WHERE phone = ? AND is_joker = 1", (login_phone,))
        used_jokers = cursor.fetchone()[0]
        remaining_jokers = max(0, 8 - used_jokers)

        st.markdown(f"""
        <div class="joker-banner">
          <strong>✌🏼 رصيد الدبلها: {remaining_jokers} من 8</strong>
          <small>فعّل الدبلها على مباراة لمضاعفة نقاطك</small>
        </div>
        """, unsafe_allow_html=True)

        hide_closed = st.toggle("🔴 إخفاء المباريات المنتهية", value=False)

        for match in all_matches:
            time_until_match = match["time"] - now_ksa
            if hide_closed and now_ksa >= match["time"]: continue

            cursor.execute("SELECT actual_home, actual_away, actual_pens_winner FROM processed_matches WHERE match_id = ?", (match["id"],))
            match_status_row = cursor.fetchone()

            home_flag = FLAGS.get(match['team_home'], '🏳️')
            away_flag = FLAGS.get(match['team_away'], '🏳️')

            if match_status_row and match_status_row[0] is not None and match_status_row[1] is not None:
                # مباراة انتهت
                actual_h, actual_a, actual_p = match_status_row
                cursor.execute("SELECT pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE phone = ? AND match_id = ?", (login_phone, match["id"]))
                user_pred_row = cursor.fetchone()
                earned_pts = 0
                if user_pred_row:
                    p_home, p_away, p_pens, p_joker = user_pred_row
                    earned_pts = calculate_match_points(p_home, p_away, p_pens, actual_h, actual_a, actual_p, match["is_knockout"])
                    if p_joker == 1: earned_pts *= 2
                txt_p = f" (ترجيح: {actual_p})" if actual_p else ""
                st.markdown(f"""
                <div class="match-card done">
                  <div class="match-meta">📅 {match['time'].strftime('%d | %I:%M %p')}</div>
                  <div class="match-teams">
                    <div class="team-side"><span class="team-flag">{home_flag}</span><div class="team-name">{match['team_home']}</div></div>
                    <div class="match-score">{actual_h} × {actual_a}{txt_p}</div>
                    <div class="team-side"><span class="team-flag">{away_flag}</span><div class="team-name">{match['team_away']}</div></div>
                  </div>
                  <div class="match-done-tag">✅ انتهت واحتُسبت | حصلت على: {earned_pts} نقاط</div>
                </div>
                """, unsafe_allow_html=True)
                is_calculated_and_valid = True
            else:
                is_calculated_and_valid = False

            is_within_24h = (timedelta(hours=0) <= time_until_match <= timedelta(hours=24))
            is_june_11 = (match["time"].day == 11 and match["time"].month == 6)

            if is_within_24h or is_june_11 or is_calculated_and_valid or (login_phone == ADMIN_PHONE):
                if not is_calculated_and_valid:
                    # مباراة مفتوحة أو مقفلة
                    is_locked = (time_until_match < timedelta(minutes=10)) and login_phone != ADMIN_PHONE
                    card_class = "locked" if is_locked else "match-card"
                    st.markdown(f"""
                    <div class="{card_class}">
                      <div class="match-meta">📅 {match['time'].strftime('%d | %I:%M %p')}</div>
                      <div class="match-teams">
                        <div class="team-side"><span class="team-flag">{home_flag}</span><div class="team-name">{match['team_home']}</div></div>
                        <div class="match-vs">×</div>
                        <div class="team-side"><span class="team-flag">{away_flag}</span><div class="team-name">{match['team_away']}</div></div>
                      </div>
                      {"<div class='match-locked-tag'>🔒 مغلق — انتهى وقت التوقع</div>" if is_locked else ""}
                    </div>
                    """, unsafe_allow_html=True)

                    if is_locked:
                        continue

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
                        st.markdown("⚠️ **مباراة إقصائية اختر الفائز بالترجيح**")
                        pens_winner = st.radio(f"الفائز بالترجيح", [match['team_home'], match['team_away']],
                                               index=0 if val_pens == match['team_home'] else 1,
                                               key=f"pens_{match['id']}", horizontal=True)

                    use_joker = st.checkbox("✌🏼 تفعيل التدبيل لهذه المباراة (مضاعفة النقاط!)", value=is_joker_checked, key=f"joker_{match['id']}")

                    col_submit, col_share = st.columns(2)
                    with col_submit:
                        if st.button(f"✅ اعتماد التوقع", key=f"btn_{match['id']}"):
                            if use_joker and not is_joker_checked and remaining_jokers <= 0:
                                st.error("⚠️ استهلكت جميع الجواكر الـ 8!")
                                st.stop()
                            joker_val = 1 if use_joker else 0
                            cursor.execute('''
                                INSERT INTO predictions (phone, match_id, pred_home, pred_away, pred_pens_winner, is_joker)
                                VALUES (?, ?, ?, ?, ?, ?)
                                ON CONFLICT(phone, match_id) DO UPDATE SET
                                  pred_home=excluded.pred_home, pred_away=excluded.pred_away,
                                  pred_pens_winner=excluded.pred_pens_winner, is_joker=excluded.is_joker
                            ''', (login_phone, match["id"], h_score, a_score, pens_winner, joker_val))
                            db_conn.commit()
                            st.success("تم تسجيل التوقع بنجاح! 🏁")
                            st.rerun()
                    with col_share:
                        joker_tag = "✌🏼 [دبلها]" if use_joker else ""
                        pens_tag  = f" | (ترجيح: {pens_winner})" if pens_winner else ""
                        share_text = f"🏆 *WC26 KING #الحديقة_المونديال*\n\n👤 *{user_name}*\n\n⚽ {home_flag} *{match['team_home']} × {match['team_away']}* {away_flag}\n{joker_tag}\n\n🎯 *توقعي:*\n{match['team_home']} {h_score} - {a_score} {match['team_away']}{pens_tag}"
                        wa_link = "https://wa.me/?text=" + urllib.parse.quote(share_text)
                        st.link_button("📲 مشاركة التوقع", wa_link, key=f"share_{match['id']}")

    # ══ تبويب المواعيد ══
    with tab_schedule:
        st.markdown('<div class="sec-label">📅 مواعيد فتح التوقعات</div>', unsafe_allow_html=True)
        rows = []
        for match in all_matches:
            open_time = match["time"] - timedelta(hours=24)
            status = "🔴 مغلق" if now_ksa >= match["time"] else ("🟢 مفتوح الآن" if now_ksa >= open_time else f"🟡 بعد {(open_time - now_ksa).days} يوم")
            rows.append({
                "المباراة": f"{match['team_home']} × {match['team_away']}",
                "فتح التوقعات": open_time.strftime("%d/%m %I:%M %p"),
                "موعد المباراة": match["time"].strftime("%d/%m %I:%M %p"),
                "الحالة": status
            })
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    # ══ تبويب الإدارة ══
    if login_phone == ADMIN_PHONE:
        with tab_admin:
            st.markdown('<div class="admin-card">⚙️ <b>لوحة تحكم الإدارة الملكية (أحمد بادحمان)</b></div>', unsafe_allow_html=True)
            cursor = db_conn.cursor()

            st.subheader("🧮 إدخال نتائج المباريات")
            match_options = {f"{m['team_home']} × {m['team_away']}": m for m in all_matches}
            selected_match_str = st.selectbox("إختر المباراة:", list(match_options.keys()))
            selected_match = match_options[selected_match_str]

            cursor.execute("SELECT actual_home, actual_away, actual_pens_winner FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
            already_calculated = cursor.fetchone()
            is_valid_old_result = already_calculated and already_calculated[0] is not None and already_calculated[1] is not None

            if is_valid_old_result:
                txt_p_old = f" (ترجيح: {already_calculated[2]})" if already_calculated[2] else ""
                st.warning(f"⚠️ احتُسبت سابقاً: {already_calculated[0]} - {already_calculated[1]}{txt_p_old}")
                if st.button("🚨 إلغاء النتيجة وسحب النقاط", key="cancel_btn"):
                    old_h, old_a, old_p = already_calculated
                    cursor.execute("SELECT phone, pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE match_id = ?", (selected_match["id"],))
                    for pred in cursor.fetchall():
                        user_phone, p_home, p_away, p_pens, p_joker = pred
                        old_points = calculate_match_points(p_home, p_away, p_pens, old_h, old_a, old_p, selected_match["is_knockout"])
                        if p_joker == 1: old_points *= 2
                        if old_points > 0: cursor.execute("UPDATE users SET points = MAX(0, points - ?) WHERE phone = ?", (old_points, user_phone))
                    cursor.execute("DELETE FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
                    db_conn.commit(); st.rerun()

            col_h, col_a = st.columns(2)
            with col_h: actual_h = st.number_input(f"النتيجة لـ {selected_match['team_home']}", 0, 10, value=already_calculated[0] if is_valid_old_result else 0, key="act_h")
            with col_a: actual_a = st.number_input(f"النتيجة لـ {selected_match['team_away']}", 0, 10, value=already_calculated[1] if is_valid_old_result else 0, key="act_a")

            actual_p = None
            if selected_match["is_knockout"] and actual_h == actual_a:
                actual_p = st.radio("الفائز بركلات الترجيح:", [selected_match['team_home'], selected_match['team_away']],
                                    index=0 if already_calculated and already_calculated[2] == selected_match['team_home'] else 1, key="admin_act_pens")

            if st.button("🔥 احسب النقاط!" if not is_valid_old_result else "📝 تحديث النقاط"):
                if is_valid_old_result:
                    old_h, old_a, old_p = already_calculated
                    cursor.execute("SELECT phone, pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE match_id = ?", (selected_match["id"],))
                    for pred in cursor.fetchall():
                        user_phone, p_home, p_away, p_pens, p_joker = pred
                        old_points = calculate_match_points(p_home, p_away, p_pens, old_h, old_a, old_p, selected_match["is_knockout"])
                        if p_joker == 1: old_points *= 2
                        if old_points > 0: cursor.execute("UPDATE users SET points = MAX(0, points - ?) WHERE phone = ?", (old_points, user_phone))
                    cursor.execute("DELETE FROM processed_matches WHERE match_id = ?", (selected_match["id"],))

                cursor.execute("SELECT phone, pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE match_id = ?", (selected_match["id"],))
                for pred in cursor.fetchall():
                    user_phone, p_home, p_away, p_pens, p_joker = pred
                    pts = calculate_match_points(p_home, p_away, p_pens, actual_h, actual_a, actual_p, selected_match["is_knockout"])
                    if p_joker == 1: pts *= 2
                    if pts > 0: cursor.execute("UPDATE users SET points = points + ? WHERE phone = ?", (pts, user_phone))

                cursor.execute('INSERT INTO processed_matches (match_id, actual_home, actual_away, actual_pens_winner) VALUES (?, ?, ?, ?)',
                               (selected_match["id"], actual_h, actual_a, actual_p))
                db_conn.commit()
                st.success("🏆 تم احتساب النقاط بنجاح!")
                st.rerun()

            st.subheader("🛠️ إدارة قاعدة البيانات")
            cursor.execute("SELECT name, phone, points, password FROM users")
            all_users_list = cursor.fetchall()
            user_options = {f"{u[0]} ({u[1]})": u for u in all_users_list}
            if user_options:
                selected_user_str = st.selectbox("إختر العضو:", list(user_options.keys()))
                target_user_data = user_options[selected_user_str]
                c_edit, c_del = st.columns(2)
                with c_edit:
                    new_pts = st.number_input("تعديل النقاط إلى:", 0, 500, value=target_user_data[2])
                    new_user_pass = st.text_input(f"تعديل كلمة مرور {target_user_data[0]}:", value=target_user_data[3])
                    if st.button("💾 حفظ التعديلات"):
                        cursor.execute("UPDATE users SET points = ?, password = ? WHERE phone = ?", (new_pts, new_user_pass, target_user_data[1]))
                        db_conn.commit(); st.success("تم التحديث!"); st.rerun()
                with c_del:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("❌ حذف هذا العضو نهائياً"):
                        cursor.execute("DELETE FROM users WHERE phone = ?", (target_user_data[1],))
                        db_conn.commit(); st.error("تم حذف العضو!"); st.rerun()
