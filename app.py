# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime, timedelta
import pytz
import pandas as pd
import sqlite3
import urllib.parse

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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Oswald:wght@700&display=swap');

:root {
  --gold:   #FFD700; --gold-d: #b8960a;
  --green:  #00c853; --green2: #00e676;
  --glass:  rgba(255,255,255,0.06);
  --border: rgba(255,255,255,0.10);
  --text:   #e8f5e9; --muted: #7fada2; --red: #ff5252;
}

/* ── FADE IN ── */
@keyframes fadeUp {
  from { opacity:0; transform:translateY(18px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes countUp {
  from { opacity:0; transform:scale(0.7); }
  to   { opacity:1; transform:scale(1); }
}
.fade-up { animation: fadeUp .55s ease both; }
.fade-up-d1 { animation: fadeUp .55s .08s ease both; }
.fade-up-d2 { animation: fadeUp .55s .16s ease both; }
.fade-up-d3 { animation: fadeUp .55s .24s ease both; }
.count-anim { animation: countUp .4s .3s ease both; }

/* ── BASE ── */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  font-family: 'Cairo', sans-serif !important;
  background: radial-gradient(ellipse at 30% 0%, #0d2b14 0%, #06120a 65%) !important;
  color: var(--text) !important;
}
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stSidebar"] { background: rgba(6,18,10,0.97) !important; border-left: 1px solid var(--border); }
[data-testid="stSidebarContent"] p,
[data-testid="stSidebarContent"] div { color: var(--text) !important; }
section[data-testid="stMain"] > div { padding-top: 0 !important; }
p,label,div,span,li,h1,h2,h3,h4,h5,h6,.stMarkdown,.stText { color: var(--text) !important; }

/* ── HERO ── */
.wc-hero { text-align:center; padding:36px 20px 22px; position:relative; }
.wc-hero::before {
  content:''; position:absolute; inset:0;
  background:radial-gradient(ellipse at 50% 0%, rgba(255,215,0,0.09) 0%, transparent 70%);
  pointer-events:none;
}
.wc-badge {
  display:inline-block; background:rgba(255,215,0,0.10);
  border:1px solid rgba(255,215,0,0.28); border-radius:50px;
  padding:4px 16px; font-size:11px; font-weight:700; letter-spacing:2px;
  color:var(--gold); margin-bottom:12px; text-transform:uppercase;
}
.wc-title {
  font-family:'Oswald',sans-serif !important;
  font-size:clamp(34px,9vw,62px); font-weight:700;
  color:var(--gold) !important; line-height:1.05; margin:0;
  text-shadow:0 0 50px rgba(255,215,0,0.35);
  letter-spacing:2px;
}
.wc-sub  { font-size:14px; color:var(--muted) !important; margin-top:6px; }
.wc-line { width:50px; height:3px; margin:14px auto 0; background:linear-gradient(90deg,var(--green),var(--gold)); border-radius:3px; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background:rgba(6,18,10,0.85) !important; border-radius:16px !important;
  border:1px solid var(--border) !important; padding:4px !important; gap:2px !important;
}
.stTabs [data-baseweb="tab"] {
  background:transparent !important; border-radius:12px !important;
  color:var(--muted) !important; font-weight:700 !important;
  font-family:'Cairo',sans-serif !important; padding:8px 10px !important; transition:all .2s !important;
}
.stTabs [aria-selected="true"] {
  background:rgba(255,215,0,0.12) !important; color:var(--gold) !important;
  box-shadow:0 0 0 1px rgba(255,215,0,0.28) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display:none !important; }
.stTabContent { padding-top:16px !important; }

/* ── BUTTONS ── */
.stButton > button {
  width:100% !important; height:46px !important; border-radius:14px !important;
  border:none !important; background:linear-gradient(90deg,var(--green),var(--green2)) !important;
  color:#fff !important; font-weight:700 !important; font-family:'Cairo',sans-serif !important;
  font-size:14px !important; transition:all .2s !important;
  box-shadow:0 4px 16px rgba(0,200,83,0.18) !important;
}
.stButton > button:hover {
  background:linear-gradient(90deg,var(--gold-d),var(--gold)) !important;
  color:#000 !important; box-shadow:0 4px 20px rgba(255,215,0,0.25) !important;
}
.stButton > button:active { transform:scale(0.97) !important; }
.stLinkButton a {
  display:flex !important; align-items:center !important; justify-content:center !important;
  width:100% !important; height:46px !important; border-radius:14px !important;
  border:1px solid rgba(37,211,102,0.30) !important;
  background:rgba(37,211,102,0.09) !important; color:var(--green2) !important;
  font-weight:700 !important; font-family:'Cairo',sans-serif !important;
  font-size:13px !important; text-decoration:none !important; transition:background .15s !important;
}
.stLinkButton a:hover { background:rgba(37,211,102,0.17) !important; }

/* ── INPUTS ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stPasswordInput"] input {
  background:#0d1f10 !important; border:1px solid rgba(255,215,0,0.25) !important;
  border-radius:12px !important; color:#ffffff !important;
  font-family:'Oswald',sans-serif !important; font-size:22px !important;
  font-weight:700 !important; text-align:center !important;
  -webkit-text-fill-color:#ffffff !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus,
[data-testid="stPasswordInput"] input:focus {
  border-color:var(--gold) !important; box-shadow:0 0 0 2px rgba(255,215,0,0.18) !important;
  color:#ffffff !important; -webkit-text-fill-color:#ffffff !important;
}
/* placeholder */
[data-testid="stNumberInput"] input::placeholder,
[data-testid="stTextInput"] input::placeholder,
[data-testid="stPasswordInput"] input::placeholder { color:rgba(255,255,255,0.35) !important; -webkit-text-fill-color:rgba(255,255,255,0.35) !important; }

[data-testid="stSelectbox"] > div > div {
  background:#0d1f10 !important; border:1px solid rgba(255,215,0,0.25) !important;
  border-radius:12px !important; color:#ffffff !important; font-family:'Cairo',sans-serif !important;
}
[data-testid="stCheckbox"] label span,
[data-testid="stToggle"] label,
[data-testid="stRadio"] label { color:var(--text) !important; }

/* ── AUTH ── */
.auth-card { background:var(--glass); border:1px solid var(--border); border-radius:22px; padding:26px 22px; margin-bottom:16px; }
.auth-card-title { font-size:18px; font-weight:900; color:var(--gold) !important; margin-bottom:18px; }
.info-box {
  background:rgba(0,200,83,0.07); border:1px solid rgba(0,200,83,0.18);
  border-radius:16px; padding:16px; font-size:13px; line-height:1.8; color:var(--text) !important;
}
.info-box strong { color:var(--gold) !important; }

/* ── STATS ── */
.stats-container { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-bottom:16px; direction:rtl; }
.stat-box { background:var(--glass); border:1px solid var(--border); border-radius:14px; padding:12px 6px; text-align:center; }
.stat-box-label { font-size:clamp(10px,2.5vw,12px); color:var(--muted) !important; margin-bottom:3px; white-space:nowrap; }
.stat-box-value { font-family:'Oswald',sans-serif !important; font-size:clamp(16px,4vw,22px); font-weight:700; color:var(--gold) !important; white-space:nowrap; }

/* ── PODIUM ── */
.podium-wrap {
  display:grid; grid-template-columns:1fr 1.1fr 1fr;
  gap:8px; align-items:end; margin-bottom:20px; direction:rtl;
}
.podium-card {
  background:var(--glass); border:1px solid var(--border);
  border-radius:18px; padding:16px 8px 12px; text-align:center;
  transition:transform .2s;
}
.podium-card:hover { transform:translateY(-4px); }
.podium-card.first {
  background:linear-gradient(160deg,rgba(255,215,0,0.14),rgba(255,215,0,0.03));
  border-color:rgba(255,215,0,0.40);
  box-shadow:0 0 28px rgba(255,215,0,0.12);
}
.podium-crown { font-size:24px; display:block; margin-bottom:6px; }
.podium-name  { font-size:13px; font-weight:700; color:var(--text) !important; margin-bottom:4px; }
.podium-pts   { font-family:'Oswald',sans-serif !important; font-size:22px; font-weight:700; color:var(--gold) !important; }
.podium-flag  { font-size:14px; color:var(--muted) !important; margin-top:3px; }

/* ── LB ROW ── */
.lb-row {
  display:flex; align-items:center; gap:10px;
  background:var(--glass); border:1px solid var(--border);
  border-radius:14px; padding:11px 14px; margin-bottom:6px; transition:background .15s;
}
.lb-row:hover { background:rgba(255,255,255,0.09); }
.lb-row.me { border-color:rgba(255,215,0,0.32); background:rgba(255,215,0,0.06); }
.lb-rank { font-size:15px; font-weight:900; width:28px; text-align:center; flex-shrink:0; }
.lb-name { flex:1; font-size:14px; font-weight:700; color:var(--text) !important; }
.lb-pts  { font-family:'Oswald',sans-serif !important; font-weight:700; color:var(--gold) !important; font-size:16px; white-space:nowrap; }

/* ── MATCH CARD ── */
.match-card {
  background:var(--glass); border:1px solid var(--border);
  border-radius:20px; padding:16px 14px; margin:8px 0 14px;
  position:relative; overflow:hidden; transition:border-color .2s;
}
.match-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg,transparent,rgba(255,215,0,0.40),transparent);
}
.match-card.done   { border-color:rgba(0,200,83,0.28); }
.match-card.done::before { background:linear-gradient(90deg,transparent,rgba(0,200,83,0.55),transparent); }
.match-card.locked { border-color:rgba(255,82,82,0.20); }

.match-teams {
  display:flex; align-items:center; justify-content:space-between;
  gap:6px; margin-bottom:6px; direction:rtl;
}
.team-side  { flex:1; text-align:center; }
.team-flag  { font-size:34px; display:block; line-height:1.1; }
.team-name  { font-size:11px; font-weight:700; color:var(--text) !important; margin-top:3px; }
.match-vs   { font-family:'Oswald',sans-serif !important; font-size:22px; font-weight:700; color:var(--gold) !important; text-align:center; flex-shrink:0; }
.match-score{ font-family:'Oswald',sans-serif !important; font-size:26px; font-weight:700; color:var(--gold) !important; text-align:center; flex-shrink:0; white-space:nowrap; letter-spacing:2px; }
.match-meta { text-align:center; font-size:11px; color:var(--muted) !important; margin-bottom:10px; }

/* توقع المستخدم في المباريات المنتهية */
.user-pred-tag {
  display:inline-block; background:rgba(255,255,255,0.07);
  border:1px solid rgba(255,255,255,0.12); border-radius:8px;
  padding:3px 10px; font-size:11px; color:var(--muted) !important; margin-bottom:5px;
}
.match-done-tag   { text-align:center; font-size:12px; color:var(--green2) !important; font-weight:700; margin-top:6px; }
.match-locked-tag { text-align:center; font-size:12px; color:var(--red) !important; font-weight:700; margin-bottom:10px; }

/* ── COUNTDOWN ── */
.countdown-wrap {
  display:flex; justify-content:center; gap:8px; margin-bottom:10px; direction:rtl;
}
.cd-box {
  background:rgba(255,215,0,0.08); border:1px solid rgba(255,215,0,0.18);
  border-radius:10px; padding:5px 10px; text-align:center; min-width:44px;
}
.cd-num  { font-family:'Oswald',sans-serif !important; font-size:18px; font-weight:700; color:var(--gold) !important; line-height:1; }
.cd-lbl  { font-size:9px; color:var(--muted) !important; margin-top:1px; }

/* ── JOKER PROGRESS ── */
.joker-banner {
  background:rgba(255,215,0,0.07); border:1px solid rgba(255,215,0,0.20);
  border-radius:16px; padding:14px 16px; margin-bottom:16px;
}
.joker-banner strong { color:var(--gold) !important; font-size:15px; }
.joker-banner small  { font-size:11px; color:var(--muted) !important; display:block; margin-top:4px; }
.joker-dots { display:flex; gap:5px; justify-content:center; margin-top:10px; flex-direction:row-reverse; }
.j-dot {
  width:28px; height:28px; border-radius:50%; font-size:14px;
  display:flex; align-items:center; justify-content:center;
  border:2px solid rgba(255,215,0,0.25); background:rgba(255,255,255,0.04);
  transition:all .2s;
}
.j-dot.used { background:linear-gradient(135deg,var(--gold-d),var(--gold)); border-color:var(--gold); }

/* ── CHAMPION ── */
.champion-box-card {
  background:linear-gradient(135deg,rgba(255,215,0,0.09),rgba(0,77,43,0.28));
  border:1px solid rgba(255,215,0,0.22); border-radius:22px;
  padding:22px 16px; margin:14px 0 18px; text-align:center;
}
.champion-box-card h2 { color:var(--gold) !important; font-size:clamp(17px,5vw,22px); font-weight:900; margin-bottom:5px; }
.champion-saved-badge {
  background:linear-gradient(90deg,var(--gold-d),var(--gold));
  color:#000 !important; font-weight:900; font-size:14px;
  padding:7px 20px; border-radius:50px; display:inline-block;
  margin-top:10px; box-shadow:0 4px 14px rgba(255,215,0,0.20);
}

/* ── ADMIN/REVIEW ── */
.admin-card {
  background:linear-gradient(135deg,rgba(91,50,0,0.55),rgba(184,134,11,0.30));
  border:1px solid rgba(184,134,11,0.28); border-radius:18px; padding:18px; margin-bottom:14px;
}
.review-card {
  background:linear-gradient(135deg,rgba(0,77,43,0.45),rgba(0,168,90,0.22));
  border:1px solid rgba(0,168,90,0.22); border-radius:18px; padding:16px; margin-bottom:12px;
}

/* ── MISC ── */
.sec-label { font-size:11px; font-weight:700; color:var(--muted) !important; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:10px; }
.wc-divider { border:none; border-top:1px dashed rgba(255,215,0,0.18); margin:22px 0; }
[data-testid="stDataFrame"] { border-radius:14px !important; overflow:hidden; border:1px solid var(--border) !important; }
[data-testid="stDataFrame"] th { background:rgba(255,215,0,0.08) !important; color:var(--gold) !important; font-weight:700 !important; }
[data-testid="stDataFrame"] td { color:var(--text) !important; background:rgba(255,255,255,0.03) !important; }
[data-testid="stAlert"] { border-radius:14px !important; }
div[data-testid="stAlert"] p { color:inherit !important; }
[data-testid="stSidebarContent"] .stButton > button {
  background:rgba(255,82,82,0.12) !important; border:1px solid rgba(255,82,82,0.28) !important;
  color:var(--red) !important; box-shadow:none !important;
}
::-webkit-scrollbar { width:4px; height:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:rgba(255,215,0,0.20); border-radius:4px; }
</style>
""", unsafe_allow_html=True)

# ══ HERO ══
st.markdown("""
<div class="wc-hero fade-up">
  <div class="wc-badge">🇸🇦 كأس العالم 2026</div>
  <div class="wc-title">WC26 KING 🏆</div>
  <div class="wc-sub">تحدي ملك المونديال في الحديقة ⚽️</div>
  <div class="wc-line"></div>
</div>
""", unsafe_allow_html=True)

# ══ DB ══
def init_db():
    conn = sqlite3.connect('alhadeeqah_db.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT NOT NULL, points INTEGER DEFAULT 0, phone TEXT PRIMARY KEY, password TEXT DEFAULT '1234')''')
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (phone TEXT, match_id INTEGER, pred_home INTEGER, pred_away INTEGER, is_joker INTEGER DEFAULT 0, PRIMARY KEY (phone, match_id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS processed_matches (match_id INTEGER PRIMARY KEY, actual_home INTEGER, actual_away INTEGER)''')
    for sql in [
        "ALTER TABLE predictions ADD COLUMN is_joker INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN champion_pred TEXT DEFAULT NULL",
        "ALTER TABLE predictions ADD COLUMN pred_pens_winner TEXT DEFAULT NULL",
        "ALTER TABLE processed_matches ADD COLUMN actual_pens_winner TEXT DEFAULT NULL",
    ]:
        try: c.execute(sql)
        except sqlite3.OperationalError: pass
    conn.commit()
    return conn

db_conn = init_db()
ADMIN_PHONE = "0502518301"

def get_internal_matches():
    return [
        {"id": 1,  "team_home": "المكسيك",            "team_away": "جنوب أفريقيا",        "time": datetime(2026, 6, 11, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 2,  "team_home": "كوريا الجنوبية",      "team_away": "التشيك",               "time": datetime(2026, 6, 12, 5,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 3,  "team_home": "كندا",                "team_away": "البوسنة والهرسك",       "time": datetime(2026, 6, 12, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 4,  "team_home": "الولايات المتحدة",    "team_away": "باراغواي",              "time": datetime(2026, 6, 13, 4,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 5,  "team_home": "قطر",                 "team_away": "سويسرا",               "time": datetime(2026, 6, 13, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 6,  "team_home": "البرازيل",            "team_away": "المغرب",               "time": datetime(2026, 6, 14, 1,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 7,  "team_home": "هايتي",               "team_away": "اسكتلندا",             "time": datetime(2026, 6, 14, 4,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 8,  "team_home": "أستراليا",            "team_away": "تركيا",                "time": datetime(2026, 6, 14, 7,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 9,  "team_home": "ألمانيا",             "team_away": "كوراساو",              "time": datetime(2026, 6, 14, 20, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 10, "team_home": "هولندا",              "team_away": "اليابان",              "time": datetime(2026, 6, 14, 23, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 11, "team_home": "ساحل العاج",          "team_away": "الإكوادور",            "time": datetime(2026, 6, 15, 2,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 12, "team_home": "السويد",              "team_away": "تونس",                 "time": datetime(2026, 6, 15, 5,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 13, "team_home": "إسبانيا",             "team_away": "الرأس الأخضر",         "time": datetime(2026, 6, 15, 19, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 14, "team_home": "بلجيكا",              "team_away": "مصر",                  "time": datetime(2026, 6, 15, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 15, "team_home": "السعودية",            "team_away": "الأوروغواي",           "time": datetime(2026, 6, 16, 1,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 16, "team_home": "إيران",               "team_away": "نيوزيلندا",            "time": datetime(2026, 6, 16, 4,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 17, "team_home": "فرنسا",               "team_away": "السنغال",              "time": datetime(2026, 6, 16, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 18, "team_home": "النرويج",             "team_away": "العراق",               "time": datetime(2026, 6, 17, 1,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 19, "team_home": "الأرجنتين",           "team_away": "الجزائر",              "time": datetime(2026, 6, 17, 4,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 20, "team_home": "النمسا",              "team_away": "الأردن",               "time": datetime(2026, 6, 17, 7,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 21, "team_home": "البرتغال",            "team_away": "الكونغو الديمقراطية", "time": datetime(2026, 6, 17, 20, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 22, "team_home": "إنجلترا",             "team_away": "كرواتيا",              "time": datetime(2026, 6, 17, 23, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 23, "team_home": "غانا",                "team_away": "بنما",                 "time": datetime(2026, 6, 18, 2,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 24, "team_home": "أوزبكستان",           "team_away": "كولومبيا",             "time": datetime(2026, 6, 18, 5,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 25, "team_home": "التشيك",              "team_away": "جنوب أفريقيا",         "time": datetime(2026, 6, 18, 19, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 26, "team_home": "سويسرا",              "team_away": "البوسنة والهرسك",      "time": datetime(2026, 6, 18, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 27, "team_home": "كندا",                "team_away": "قطر",                  "time": datetime(2026, 6, 19, 1,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 28, "team_home": "المكسيك",             "team_away": "كوريا الجنوبية",       "time": datetime(2026, 6, 19, 4,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 29, "team_home": "الولايات المتحدة",    "team_away": "أستراليا",             "time": datetime(2026, 6, 19, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 30, "team_home": "اسكتلندا",            "team_away": "المغرب",               "time": datetime(2026, 6, 20, 1,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 31, "team_home": "البرازيل",            "team_away": "هايتي",                "time": datetime(2026, 6, 20, 3, 30,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 32, "team_home": "تركيا",               "team_away": "باراغواي",             "time": datetime(2026, 6, 20, 6,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 33, "team_home": "هولندا",              "team_away": "السويد",               "time": datetime(2026, 6, 20, 20, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 34, "team_home": "ألمانيا",             "team_away": "ساحل العاج",           "time": datetime(2026, 6, 20, 23, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 35, "team_home": "الإكوادور",           "team_away": "كوراساو",              "time": datetime(2026, 6, 21, 3,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 36, "team_home": "اليابان",             "team_away": "تونس",                 "time": datetime(2026, 6, 21, 7,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 37, "team_home": "إسبانيا",             "team_away": "السعودية",             "time": datetime(2026, 6, 21, 19, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 38, "team_home": "بلجيكا",              "team_away": "إيران",                "time": datetime(2026, 6, 21, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 39, "team_home": "أوروغواي",            "team_away": "الرأس الأخضر",         "time": datetime(2026, 6, 22, 1,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 40, "team_home": "نيوزيلندا",           "team_away": "مصر",                  "time": datetime(2026, 6, 22, 4,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 41, "team_home": "الأرجنتين",           "team_away": "النمسا",               "time": datetime(2026, 6, 22, 20, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 42, "team_home": "فرنسا",               "team_away": "العراق",               "time": datetime(2026, 6, 23, 0,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 43, "team_home": "النرويج",             "team_away": "السنغال",              "time": datetime(2026, 6, 23, 3,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 44, "team_home": "الأردن",              "team_away": "الجزائر",              "time": datetime(2026, 6, 23, 6,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 45, "team_home": "البرتغال",            "team_away": "أوزبكستان",            "time": datetime(2026, 6, 23, 20, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 46, "team_home": "إنجلترا",             "team_away": "غانا",                 "time": datetime(2026, 6, 23, 23, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 47, "team_home": "بنما",                "team_away": "كرواتيا",              "time": datetime(2026, 6, 24, 2,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 48, "team_home": "كولومبيا",            "team_away": "الكونغو الديمقراطية", "time": datetime(2026, 6, 24, 5,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 49, "team_home": "البوسنة والهرسك",     "team_away": "قطر",                  "time": datetime(2026, 6, 24, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 50, "team_home": "سويسرا",              "team_away": "كندا",                 "time": datetime(2026, 6, 24, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 51, "team_home": "المغرب",              "team_away": "هايتي",                "time": datetime(2026, 6, 25, 1,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 52, "team_home": "اسكتلندا",            "team_away": "البرازيل",             "time": datetime(2026, 6, 25, 1,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 53, "team_home": "التشيك",              "team_away": "المكسيك",              "time": datetime(2026, 6, 25, 4,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 54, "team_home": "جنوب أفريقيا",        "team_away": "كوريا الجنوبية",      "time": datetime(2026, 6, 25, 4,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 55, "team_home": "كوراساو",             "team_away": "ساحل العاج",           "time": datetime(2026, 6, 25, 23, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 56, "team_home": "الإكوادور",           "team_away": "ألمانيا",              "time": datetime(2026, 6, 25, 23, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 57, "team_home": "اليابان",             "team_away": "السويد",               "time": datetime(2026, 6, 26, 2,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 58, "team_home": "تونس",                "team_away": "هولندا",               "time": datetime(2026, 6, 26, 2,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 59, "team_home": "باراغواي",            "team_away": "أستراليا",             "time": datetime(2026, 6, 26, 5,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 60, "team_home": "تركيا",               "team_away": "الولايات المتحدة",     "time": datetime(2026, 6, 26, 5,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 61, "team_home": "فرنسا",               "team_away": "النرويج",              "time": datetime(2026, 6, 26, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 62, "team_home": "السنغال",             "team_away": "العراق",               "time": datetime(2026, 6, 26, 22, 0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 63, "team_home": "الرأس الأخضر",        "team_away": "السعودية",             "time": datetime(2026, 6, 27, 3,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 64, "team_home": "أوروغواي",            "team_away": "إسبانيا",              "time": datetime(2026, 6, 27, 3,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 65, "team_home": "مصر",                 "team_away": "إيران",                "time": datetime(2026, 6, 27, 6,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 66, "team_home": "نيوزيلندا",           "team_away": "بلجيكا",               "time": datetime(2026, 6, 27, 6,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 67, "team_home": "كرواتيا",             "team_away": "غانا",                 "time": datetime(2026, 6, 28, 0,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 68, "team_home": "بنما",                "team_away": "إنجلترا",              "time": datetime(2026, 6, 28, 0,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 69, "team_home": "كولومبيا",            "team_away": "البرتغال",             "time": datetime(2026, 6, 28, 2, 30,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 70, "team_home": "الكونغو الديمقراطية","team_away": "أوزبكستان",            "time": datetime(2026, 6, 28, 2, 30,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 71, "team_home": "الجزائر",             "team_away": "النمسا",               "time": datetime(2026, 6, 28, 5,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 72, "team_home": "الأردن",              "team_away": "الأرجنتين",            "time": datetime(2026, 6, 28, 5,  0,  tzinfo=ksa_tz), "is_knockout": False},
        {"id": 73, "team_home": "كندا",                "team_away": "جنوب أفريقيا",         "time": datetime(2026, 6, 28, 22, 0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 74, "team_home": "البرازيل",            "team_away": "اليابان",              "time": datetime(2026, 6, 29, 20, 0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 75, "team_home": "ألمانيا",             "team_away": "باراغواي",             "time": datetime(2026, 6, 29, 23, 30, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 76, "team_home": "هولندا",              "team_away": "المغرب",               "time": datetime(2026, 6, 30, 4,  0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 77, "team_home": "النرويج",             "team_away": "ساحل العاج",           "time": datetime(2026, 6, 30, 20, 0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 78, "team_home": "فرنسا",               "team_away": "السويد",               "time": datetime(2026, 7,  1, 0,  0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 79, "team_home": "المكسيك",             "team_away": "الإكوادور",            "time": datetime(2026, 7,  1, 4,  0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 80, "team_home": "إنجلترا",             "team_away": "الكونغو الديمقراطية", "time": datetime(2026, 7,  1, 19, 0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 81, "team_home": "بلجيكا",              "team_away": "السنغال",              "time": datetime(2026, 7,  1, 23, 0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 82, "team_home": "الولايات المتحدة",    "team_away": "البوسنة والهرسك",      "time": datetime(2026, 7,  2, 3,  0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 83, "team_home": "إسبانيا",             "team_away": "النمسا",               "time": datetime(2026, 7,  2, 22, 0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 84, "team_home": "البرتغال",            "team_away": "كرواتيا",              "time": datetime(2026, 7,  3, 2,  0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 85, "team_home": "سويسرا",              "team_away": "الجزائر",              "time": datetime(2026, 7,  3, 6,  0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 86, "team_home": "أستراليا",            "team_away": "مصر",                  "time": datetime(2026, 7,  3, 21, 0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 87, "team_home": "الأرجنتين",           "team_away": "الرأس الأخضر",         "time": datetime(2026, 7,  4, 1,  0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 88, "team_home": "كولومبيا",            "team_away": "غانا",                 "time": datetime(2026, 7,  4, 4, 30,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 89, "team_home": "المغرب",     "team_away": "كندا",                "time": datetime(2026, 7, 4, 20, 0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 90, "team_home": "باراغواي",   "team_away": "فرنسا",               "time": datetime(2026, 7, 5, 0, 0,   tzinfo=ksa_tz), "is_knockout": True},
        {"id": 91, "team_home": "البرازيل",   "team_away": "النرويج",             "time": datetime(2026, 7, 5, 23, 0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 92, "team_home": "المكسيك",    "team_away": "إنجلترا",             "time": datetime(2026, 7, 6, 3, 0,   tzinfo=ksa_tz), "is_knockout": True},
        {"id": 93, "team_home": "إسبانيا",    "team_away": "البرتغال",            "time": datetime(2026, 7, 6, 22, 0,  tzinfo=ksa_tz), "is_knockout": True},
        {"id": 94, "team_home": "بلجيكا",     "team_away": "الولايات المتحدة",    "time": datetime(2026, 7, 7, 3, 0,   tzinfo=ksa_tz), "is_knockout": True},
        {"id": 95, "team_home": "مصر",      "team_away": "الأرجنتين", "time": datetime(2026, 7, 7, 19, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 96, "team_home": "سويسرا",              "team_away": "كولومبيا",              "time": datetime(2026, 7, 7, 23, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 97, "team_home": "المغرب",    "team_away": "فرنسا",     "time": datetime(2026, 7, 9, 23, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 98, "team_home": "إسبانيا",   "team_away": "بلجيكا",     "time": datetime(2026, 7, 10, 22, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 99, "team_home": "النرويج",   "team_away": "إنجلترا",    "time": datetime(2026, 7, 12, 0, 0, tzinfo=ksa_tz), "is_knockout": True},
        {"id": 101, "team_home": "الأرجنتين","team_away": "سويسرا",     "time": datetime(2026, 7, 12, 4, 0, tzinfo=ksa_tz), "is_knockout": True},
    ]

all_matches  = get_internal_matches()
matches_dict = {m["id"]: m for m in all_matches}

def calculate_match_points(p_h, p_a, p_p, actual_h, actual_a, actual_p, is_knockout):
    earned = 0
    if p_h == actual_h and p_a == actual_a:
        earned += 3
        if is_knockout and p_h == p_a and p_p == actual_p: earned += 3
    elif (
        (p_h > p_a and actual_h > actual_a)
        or (p_h < p_a and actual_h < actual_a)
        or (p_h == p_a and actual_h == actual_a)
    ):
        earned += 1
    elif is_knockout and p_h == p_a and actual_h == actual_a:
        if p_p == actual_p: earned += 3
    return earned

def make_countdown(match_time):
    diff = match_time - now_ksa
    if diff.total_seconds() <= 0: return ""
    total_s = int(diff.total_seconds())
    d = total_s // 86400; h = (total_s % 86400) // 3600
    m = (total_s % 3600) // 60; s = total_s % 60
    parts = []
    if d: parts.append(f'<div class="cd-box"><div class="cd-num">{d}</div><div class="cd-lbl">يوم</div></div>')
    parts.append(f'<div class="cd-box"><div class="cd-num">{h:02d}</div><div class="cd-lbl">ساعة</div></div>')
    parts.append(f'<div class="cd-box"><div class="cd-num">{m:02d}</div><div class="cd-lbl">دقيقة</div></div>')
    parts.append(f'<div class="cd-box"><div class="cd-num">{s:02d}</div><div class="cd-lbl">ثانية</div></div>')
    return f'<div class="countdown-wrap">{"".join(parts)}</div>'

def make_joker_dots(used, total=8):
    dots = ""
    for i in range(total):
        cls = "j-dot used" if i < used else "j-dot"
        dots += f'<div class="{cls}">{"✌🏼" if i < used else ""}</div>'
    return f'<div class="joker-dots">{dots}</div>'

# ══ SESSION ══
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
    st.session_state["user_phone"]   = ""
    st.session_state["user_name"]    = ""

if not st.session_state["is_logged_in"]:
    tab_auth, tab_info = st.tabs(["🔐 بوابة الأعضاء", "ℹ️ معلومات التحدي"])
    with tab_auth:
        menu   = ["تسجيل الدخول", "إنشاء حساب جديد (لأول مرة)"]
        choice = st.radio("إختر الإجراء:", menu, horizontal=True)
        if choice == "إنشاء حساب جديد (لأول مرة)":
            st.markdown('<div class="auth-card fade-up"><div class="auth-card-title">📝 انضم لتحدي الحديقة</div>', unsafe_allow_html=True)
            with st.form("registration_form"):
                new_name  = st.text_input("👤 اسمك")
                new_phone = st.text_input("📱 رقم الجوال (10 أرقام)", max_chars=10)
                new_pass  = st.text_input("🔐 كلمة مرور خاصة", type="password")
                if st.form_submit_button("إنشاء الحساب 🚀"):
                    new_phone = str(new_phone).strip(); new_name = str(new_name).strip(); new_pass = str(new_pass).strip()
                    if not new_name or not new_phone or not new_pass:
                        st.error("❌ يرجى تعبئة جميع الخانات.")
                    elif len(new_phone) != 10 or not new_phone.isdigit():
                        st.error("❌ رقم الجوال يجب أن يتكون من 10 أرقام.")
                    else:
                        cur = db_conn.cursor()
                        cur.execute("SELECT phone FROM users WHERE phone=?", (new_phone,))
                        if cur.fetchone():
                            st.error("⚠️ رقم الجوال مسجل مسبقاً!")
                        else:
                            cur.execute("INSERT INTO users (name,points,phone,password) VALUES (?,?,?,?)", (new_name,0,new_phone,new_pass))
                            db_conn.commit(); st.success(f"🎉 تم إنشاء حسابك يا {new_name}!"); st.balloons()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            login_phone = st.text_input("📱 رقم الجوال", max_chars=10)
            login_pass  = st.text_input("🔐 كلمة المرور", type="password")
            if st.button("تسجيل الدخول 🚀"):
                if login_phone and login_pass:
                    login_phone = str(login_phone).strip(); login_pass = str(login_pass).strip()
                    cur = db_conn.cursor()
                    cur.execute("SELECT name,password FROM users WHERE phone=?", (login_phone,))
                    row = cur.fetchone()
                    if not row:           st.error("❌ رقم الجوال غير مسجل!")
                    elif row[1]!=login_pass: st.error("❌ كلمة المرور غير صحيحة!")
                    else:
                        st.session_state["is_logged_in"] = True
                        st.session_state["user_phone"]   = login_phone
                        st.session_state["user_name"]    = row[0]
                        st.success(f"مرحباً بعودتك يا {row[0]}! 😎"); st.rerun()
                else: st.error("❌ أدخل رقم الجوال وكلمة المرور.")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box fade-up-d2">
          🏆 <strong>تحدي ملك المونديال</strong><br>
          توقع نتائج مباريات كأس العالم 2026 واجمع النقاط!<br>
          ✅ توقع صحيح الفائز = <strong>1 نقطة</strong><br>
          🎯 نتيجة دقيقة = <strong>3 نقاط</strong><br>
          ✌🏼 فعّل <strong>دبلها</strong> لمضاعفة نقاطك في 8 مباريات<br>
          👑 توقع البطل الصحيح = <strong>+10 نقاط</strong>
        </div>""", unsafe_allow_html=True)
    with tab_info:
        st.markdown("### ارحححبووو في تحدي كنق المونديال 😍🏆\nهذا التبويب مخصص للترحيب بأعضاء الحديقة قبل تسجيل الدخول.")

else:
    login_phone = st.session_state["user_phone"]
    user_name   = st.session_state["user_name"]
    st.sidebar.markdown(f"👤 **{user_name}**")
    if st.sidebar.button("تسجيل الخروج 🚪"):
        st.session_state["is_logged_in"]=False; st.session_state["user_phone"]=""; st.session_state["user_name"]=""; st.rerun()

    tabs = ["🏆 الصدارة","⚽ التوقعات","📅 المواعيد","⚙️ الإدارة"] if login_phone==ADMIN_PHONE else ["🏆 الصدارة","⚽ التوقعات","📅 المواعيد"]
    tab_tuple = st.tabs(tabs)
    tab_leaderboard = tab_tuple[0]; tab_predict = tab_tuple[1]; tab_schedule = tab_tuple[2]
    tab_admin = tab_tuple[3] if login_phone==ADMIN_PHONE else None

    # ══ LEADERBOARD ══
    with tab_leaderboard:
        cursor = db_conn.cursor()
        cursor.execute("SELECT name,points,phone,champion_pred FROM users ORDER BY points DESC")
        lb = cursor.fetchall()

        user_rank=0; user_pts=0; user_champ=None
        for i,r in enumerate(lb):
            if r[2]==login_phone: user_rank=i+1; user_pts=r[1]; user_champ=r[3]; break

        cursor.execute("""
            SELECT p.match_id,p.pred_home,p.pred_away,p.pred_pens_winner,p.is_joker,
                   pm.actual_home,pm.actual_away,pm.actual_pens_winner
            FROM predictions p JOIN processed_matches pm ON p.match_id=pm.match_id WHERE p.phone=?
        """, (login_phone,))
        calcd = cursor.fetchall()

        correct=0; wrong=0; best_pts=0
        for row in calcd:
            m_id,p_h,p_a,p_p,p_jk,a_h,a_a,a_p = row
            is_ko = matches_dict.get(m_id,{}).get("is_knockout",False)
            e = calculate_match_points(p_h,p_a,p_p,a_h,a_a,a_p,is_ko)
            if p_jk==1: e*=2
            if e>0: correct+=1
            else:   wrong+=1
            if e>best_pts: best_pts=e

        total = correct+wrong
        ratio = round((correct/total)*100,1) if total>0 else 0.0

        # إحصائيات المستخدم
        st.markdown(f'<div class="sec-label fade-up">📊 إحصائياتك — {user_name}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stats-container fade-up-d1">
          <div class="stat-box"><div class="stat-box-label">✅ صحيحة</div><div class="stat-box-value count-anim">{correct}</div></div>
          <div class="stat-box"><div class="stat-box-label">❌ خاطئة</div><div class="stat-box-value count-anim">{wrong}</div></div>
          <div class="stat-box"><div class="stat-box-label">🎯 دقة</div><div class="stat-box-value count-anim">{ratio}%</div></div>
          <div class="stat-box"><div class="stat-box-label">🎖️ ترتيب</div><div class="stat-box-value count-anim">#{user_rank}</div></div>
        </div>
        """, unsafe_allow_html=True)

        # إحصائيات إضافية
        cursor.execute("SELECT MAX(points) FROM users")
        leader_pts = cursor.execute("SELECT MAX(points) FROM users").fetchone()[0] or 0
        gap = leader_pts - user_pts if leader_pts > user_pts else 0
        st.markdown(f"""
        <div class="stats-container fade-up-d2" style="grid-template-columns:1fr 1fr;">
          <div class="stat-box"><div class="stat-box-label">⚡ أعلى نقاط مباراة</div><div class="stat-box-value">{best_pts}</div></div>
          <div class="stat-box"><div class="stat-box-label">📏 الفارق عن الصدارة</div><div class="stat-box-value">{"أنت المتصدر 👑" if gap==0 else f"{gap} نقطة"}</div></div>
        </div>
        """, unsafe_allow_html=True)

        share_text = f"📊 *حصيلة ملك التوقعات في الحديقة* 👑\n\n👤 *الاسم:* {user_name}\n🎖️ *الترتيب:* المركز {user_rank}\n🏆 *النقاط:* {user_pts}\n\n✅ صحيحة: {correct} | ❌ خاطئة: {wrong}\n🎯 دقة: {ratio}% | ⚡ أعلى مباراة: {best_pts} نقاط\n\n#WC26_KING 🔥⚽️"
        st.link_button("📲 شارك ترتيبك وإحصائياتك", "https://wa.me/?text="+urllib.parse.quote(share_text))

        st.markdown('<hr class="wc-divider">', unsafe_allow_html=True)

        # PODIUM — أول 3
        if len(lb) >= 3:
            st.markdown('<div class="sec-label">🏅 المتصدرون</div>', unsafe_allow_html=True)
            p2,p1,p3 = lb[1],lb[0],lb[2]
            def pc(r,crown,cls=""):
                f = FLAGS.get(r[3],'') if r[3] else ''
                return f'<div class="podium-card {cls}"><span class="podium-crown">{crown}</span><div class="podium-name">{r[0]}</div><div class="podium-pts">{r[1]}</div><div class="podium-flag">{f}</div></div>'
            st.markdown(f'<div class="podium-wrap fade-up">{pc(p2,"🥈")}{pc(p1,"🥇","first")}{pc(p3,"🥉")}</div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-label" style="margin-top:16px">📋 الترتيب الكامل</div>', unsafe_allow_html=True)
        for idx,row in enumerate(lb):
            p_name,p_points,p_phone,p_champ = row
            rank_icon = "🥇" if idx==0 else ("🥈" if idx==1 else ("🥉" if idx==2 else f"#{idx+1}"))
            cf = FLAGS.get(p_champ,'') if p_champ else ''
            me = "me" if p_phone==login_phone else ""
            st.markdown(f"""
            <div class="lb-row {me}">
              <div class="lb-rank">{rank_icon}</div>
              <div class="lb-name">{p_name} {cf}</div>
              <div class="lb-pts">{p_points} Pts</div>
            </div>""", unsafe_allow_html=True)
            cb,_ = st.columns([1,3])
            with cb:
                if st.button("🔍 مشاهدة التوقعات", key=f"rev_{p_phone}_{idx}"):
                    st.session_state["view_predictions_for"]  = p_phone
                    st.session_state["view_predictions_name"] = p_name

        if "view_predictions_for" in st.session_state:
            tp = st.session_state["view_predictions_for"]; tn = st.session_state["view_predictions_name"]
            st.markdown(f'<div class="review-card"><b>كشف توقعات: {tn}</b></div>', unsafe_allow_html=True)
            cursor.execute("SELECT match_id,pred_home,pred_away,pred_pens_winner FROM predictions WHERE phone=?", (tp,))
            up = {r[0]:(r[1],r[2],r[3]) for r in cursor.fetchall()}
            rl = []
            for m in all_matches:
                md = f"{m['team_home']} × {m['team_away']}"
                if m["id"] in up:
                    txt = f"{up[m['id']][0]} - {up[m['id']][1]}"
                    if m["is_knockout"] and up[m['id']][0]==up[m['id']][1] and up[m['id']][2]: txt+=f" (ترجيح: {up[m['id']][2]})"
                else: txt="لم يتوقع"
                rl.append({"المباراة":md,"التوقع":txt})
            st.dataframe(pd.DataFrame(rl), hide_index=True, use_container_width=True)
            if st.button("إغلاق ✖️"): del st.session_state["view_predictions_for"]; st.rerun()

    # ══ PREDICTIONS ══
    with tab_predict:
        cursor = db_conn.cursor()
        cursor.execute("SELECT champion_pred FROM users WHERE phone=?", (login_phone,))
        current_champ = cursor.fetchone()[0]
        is_champ_locked = now_ksa >= datetime(2026,7,14,21,0,tzinfo=ksa_tz)

        badge = (f"<div class='champion-saved-badge'>🎯 توقعك: {FLAGS.get(current_champ,'🔮')} {current_champ}</div>" if current_champ
                 else "<div class='champion-saved-badge' style='background:linear-gradient(90deg,#ff5252,#ff1744);color:white!important;'>⚠️ لم تختر بطلاً بعد</div>")
        st.markdown(f"""
        <div class="champion-box-card fade-up">
          <h2>🏆 بطل كأس العالم 2026</h2>
          <p style="color:#ccc;font-size:13px;margin-bottom:5px;">توقع المنتخب الفائز واكسب <b style="color:#FFD700;">+10 نقاط</b> إضافية!</p>
          <p style="color:#ff9800;font-size:12px;font-weight:700;margin-bottom:8px;">🔒 يقفل 28 يونيو الساعة 9:00م</p>
          {badge}
        </div>""", unsafe_allow_html=True)

        all_teams = sorted(FLAGS.keys())
        try:    di = all_teams.index(current_champ) if current_champ in all_teams else 0
        except: di = 0
        sel_champ = st.selectbox("👑 اختر المنتخب الفائز", all_teams, index=di, disabled=is_champ_locked, key="champ_sel")
        cs,csh = st.columns(2)
        with cs:
            if is_champ_locked: st.error("🔒 مغلق!")
            elif st.button("🎯 اعتماد البطل", key="save_champ"):
                cursor.execute("UPDATE users SET champion_pred=? WHERE phone=?", (sel_champ,login_phone))
                db_conn.commit(); st.success(f"تم تثبيت {sel_champ} 🔥"); st.rerun()
        with csh:
            if current_champ:
                cf = FLAGS.get(current_champ,'🏳️')
                st.link_button("📲 مشاركة البطل", "https://wa.me/?text="+urllib.parse.quote(f"👑 *تحدي ملك المونديال في الحديقة* 👑\n\n👤 *المشارك:* {user_name}\n🏆 *توقعي لبطل كأس العالم 2026:*\n✨ *{current_champ} {cf}* ✨\n\n#WC26_KING 🔥⚽️"))
            else: st.info("💡 احفظ خيار البطل أولاً.")

        st.markdown('<hr class="wc-divider">', unsafe_allow_html=True)

        cursor.execute("SELECT COUNT(*) FROM predictions WHERE phone=? AND is_joker=1", (login_phone,))
        used_jokers = cursor.fetchone()[0]
        remaining_jokers = max(0, 8-used_jokers)
        st.markdown(f"""
        <div class="joker-banner fade-up">
          <strong>✌🏼 رصيد دبلها: {remaining_jokers} من 8</strong>
          <small>فعّل دبلها على مباراة لمضاعفة نقاطك</small>
          {make_joker_dots(used_jokers)}
        </div>""", unsafe_allow_html=True)

        hide_closed = st.toggle("🔴 إخفاء المباريات المنتهية", value=False)

        for match in all_matches:
            time_until = match["time"] - now_ksa
            if hide_closed and now_ksa >= match["time"]: continue

            cursor.execute("SELECT actual_home,actual_away,actual_pens_winner FROM processed_matches WHERE match_id=?", (match["id"],))
            status_row = cursor.fetchone()
            hf = FLAGS.get(match['team_home'],'🏳️'); af = FLAGS.get(match['team_away'],'🏳️')

            if status_row and status_row[0] is not None:
                ah,aa,ap = status_row
                cursor.execute("SELECT pred_home,pred_away,pred_pens_winner,is_joker FROM predictions WHERE phone=? AND match_id=?", (login_phone,match["id"]))
                pr = cursor.fetchone(); ep=0; pred_txt=""
                if pr:
                    ph,pa,pp,pj = pr
                    ep = calculate_match_points(ph,pa,pp,ah,aa,ap,match["is_knockout"])
                    if pj==1: ep*=2
                    pred_txt = f'<div style="text-align:center;margin-bottom:4px"><span class="user-pred-tag">توقعك: {ph} – {pa}{f" (ترجيح: {pp})" if pp else ""}</span></div>'
                tp_txt = f" ✅ " if ap else ""
                st.markdown(f"""
                <div class="match-card done">
                  <div class="match-meta">📅 {match['time'].strftime('%d  | %I:%M %p')}</div>
                  <div class="match-teams">
                    <div class="team-side"><span class="team-flag">{hf}</span><div class="team-name">{match['team_home']}</div></div>
                    <div class="match-score">{ah} × {aa}{tp_txt}</div>
                    <div class="team-side"><span class="team-flag">{af}</span><div class="team-name">{match['team_away']}</div></div>
                  </div>
                  {pred_txt}
                  <div class="match-done-tag">✅ انتهت | نقاطك: {ep}</div>
                </div>""", unsafe_allow_html=True)
                continue

            is_within_24h = timedelta(hours=0) <= time_until <= timedelta(hours=24)
            is_june_11    = (match["time"].day==11 and match["time"].month==6)
            if not (is_within_24h or is_june_11 or login_phone==ADMIN_PHONE): continue

            is_locked = (time_until < timedelta(minutes=10)) and login_phone!=ADMIN_PHONE
            cd_html   = make_countdown(match["time"]) if not is_locked and time_until.total_seconds() > 0 else ""

            st.markdown(f"""
            <div class="match-card {'locked' if is_locked else ''}">
              <div class="match-meta">📅 {match['time'].strftime('%d | %I:%M %p')}</div>
              {cd_html}
              <div class="match-teams">
                <div class="team-side"><span class="team-flag">{hf}</span><div class="team-name">{match['team_home']}</div></div>
                <div class="match-vs">×</div>
                <div class="team-side"><span class="team-flag">{af}</span><div class="team-name">{match['team_away']}</div></div>
              </div>
              {"<div class='match-locked-tag'>🔒 مغلق — انتهى وقت التوقع</div>" if is_locked else ""}
            </div>""", unsafe_allow_html=True)

            if is_locked: continue

            cursor.execute("SELECT pred_home,pred_away,pred_pens_winner,is_joker FROM predictions WHERE phone=? AND match_id=?", (login_phone,match["id"]))
            ep = cursor.fetchone()
            vh = ep[0] if ep else 0; va = ep[1] if ep else 0
            vp = ep[2] if ep else match['team_home']; jk = bool(ep[3]) if ep else False

            c1,c2 = st.columns(2)
            with c1: hs = st.number_input(f"أهداف {match['team_home']}", 0, 10, value=vh, key=f"h_{match['id']}")
            with c2: as_ = st.number_input(f"أهداف {match['team_away']}", 0, 10, value=va, key=f"a_{match['id']}")

            pw = None
            if match["is_knockout"] and hs==as_:
                st.markdown("⚠️ **مباراة إقصائية — اختر الفائز بالترجيح:**")
                pw = st.radio("الفائز بالترجيح", [match['team_home'],match['team_away']], index=0 if vp==match['team_home'] else 1, key=f"pens_{match['id']}", horizontal=True)

            use_joker = st.checkbox("✌🏼 تفعيل دبلها (مضاعفة النقاط!)", value=jk, key=f"joker_{match['id']}")

            cs2,csh2 = st.columns(2)
            with cs2:
                if st.button("✅ اعتماد التوقع", key=f"btn_{match['id']}"):
                    if use_joker and not jk and remaining_jokers<=0:
                        st.error("⚠️ استهلكت جميع الجواكر الـ 8!"); st.stop()
                    cursor.execute('''
                        INSERT INTO predictions (phone,match_id,pred_home,pred_away,pred_pens_winner,is_joker)
                        VALUES (?,?,?,?,?,?)
                        ON CONFLICT(phone,match_id) DO UPDATE SET
                          pred_home=excluded.pred_home, pred_away=excluded.pred_away,
                          pred_pens_winner=excluded.pred_pens_winner, is_joker=excluded.is_joker
                    ''', (login_phone,match["id"],hs,as_,pw,1 if use_joker else 0))
                    db_conn.commit(); st.success("تم تسجيل التوقع! 🏁"); st.rerun()
            with csh2:
                jt = "✌🏼 [دبلها]" if use_joker else ""
                pt = f" | (ترجيح: {pw})" if pw else ""
                wa = "https://wa.me/?text="+urllib.parse.quote(f"🏆 *WC26 KING #الحديقة_المونديال*\n\n👤 *{user_name}*\n\n⚽ {hf} *{match['team_home']} × {match['team_away']}* {af}\n{jt}\n\n🎯 *توقعي:* {match['team_home']} {hs} - {as_} {match['team_away']}{pt}\n\n#WC26_KING 🔥⚽️")
                st.link_button("📲مشاركة التوقع ", wa, key=f"share_{match['id']}")

    # ══ SCHEDULE ══
    with tab_schedule:
        st.markdown('<div class="sec-label">📅 مواعيد فتح التوقعات</div>', unsafe_allow_html=True)
        rows=[]
        for m in all_matches:
            ot = m["time"]-timedelta(hours=24)
            st_txt = "🔴 مغلق" if now_ksa>=m["time"] else ("🟢 مفتوح" if now_ksa>=ot else f"🟡 بعد {(ot-now_ksa).days} يوم")
            rows.append({"المباراة":f"{m['team_home']} × {m['team_away']}","فتح التوقعات":ot.strftime("%d/%m %I:%M%p"),"الموعد":m["time"].strftime("%d/%m %I:%M%p"),"الحالة":st_txt})
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    # ══ ADMIN ══
    if login_phone==ADMIN_PHONE and tab_admin is not None:
        with tab_admin:
            st.markdown('<div class="admin-card">⚙️ <b>لوحة تحكم الإدارة الملكية (أحمد بادحمان)</b></div>', unsafe_allow_html=True)
            cursor = db_conn.cursor()
            st.subheader("🧮 إدخال نتائج المباريات")
            mo = {f"{m['team_home']} × {m['team_away']}":m for m in all_matches}
            sm_str = st.selectbox("إختر المباراة:", list(mo.keys()))
            sm = mo[sm_str]
            cursor.execute("SELECT actual_home,actual_away,actual_pens_winner FROM processed_matches WHERE match_id=?", (sm["id"],))
            ac = cursor.fetchone()
            vo = ac and ac[0] is not None and ac[1] is not None
            if vo:
                tp2 = f" (ترجيح: {ac[2]})" if ac[2] else ""
                st.warning(f"⚠️ احتُسبت سابقاً: {ac[0]} - {ac[1]}{tp2}")
                if st.button("🚨 إلغاء النتيجة وسحب النقاط", key="cancel_btn"):
                    oh,oa,op = ac
                    cursor.execute("SELECT phone,pred_home,pred_away,pred_pens_winner,is_joker FROM predictions WHERE match_id=?", (sm["id"],))
                    for p in cursor.fetchall():
                        up2,ph,pa,pp,pj = p; pts=calculate_match_points(ph,pa,pp,oh,oa,op,sm["is_knockout"])
                        if pj==1: pts*=2
                        if pts>0: cursor.execute("UPDATE users SET points=MAX(0,points-?) WHERE phone=?",(pts,up2))
                    cursor.execute("DELETE FROM processed_matches WHERE match_id=?",(sm["id"],)); db_conn.commit(); st.rerun()
            ch,ca = st.columns(2)
            with ch: ah2 = st.number_input(f"النتيجة لـ {sm['team_home']}", 0, 10, value=ac[0] if vo else 0, key="act_h")
            with ca: aa2 = st.number_input(f"النتيجة لـ {sm['team_away']}", 0, 10, value=ac[1] if vo else 0, key="act_a")
            ap2=None
            if sm["is_knockout"] and ah2==aa2:
                ap2=st.radio("الفائز بركلات الترجيح:",[sm['team_home'],sm['team_away']], index=0 if ac and ac[2]==sm['team_home'] else 1, key="admin_pens")
            if st.button("🔥 احسب النقاط!" if not vo else "📝 تحديث النقاط"):
                if vo:
                    oh,oa,op=ac
                    cursor.execute("SELECT phone,pred_home,pred_away,pred_pens_winner,is_joker FROM predictions WHERE match_id=?",(sm["id"],))
                    for p in cursor.fetchall():
                        up2,ph,pa,pp,pj=p; pts=calculate_match_points(ph,pa,pp,oh,oa,op,sm["is_knockout"])
                        if pj==1: pts*=2
                        if pts>0: cursor.execute("UPDATE users SET points=MAX(0,points-?) WHERE phone=?",(pts,up2))
                    cursor.execute("DELETE FROM processed_matches WHERE match_id=?",(sm["id"],))
                cursor.execute("SELECT phone,pred_home,pred_away,pred_pens_winner,is_joker FROM predictions WHERE match_id=?",(sm["id"],))
                for p in cursor.fetchall():
                    up2,ph,pa,pp,pj=p; pts=calculate_match_points(ph,pa,pp,ah2,aa2,ap2,sm["is_knockout"])
                    if pj==1: pts*=2
                    if pts>0: cursor.execute("UPDATE users SET points=points+? WHERE phone=?",(pts,up2))
                cursor.execute("INSERT INTO processed_matches (match_id,actual_home,actual_away,actual_pens_winner) VALUES (?,?,?,?)",(sm["id"],ah2,aa2,ap2))
                db_conn.commit(); st.success("🏆 تم احتساب النقاط!"); st.rerun()

            st.subheader("🛠️ إدارة قاعدة البيانات")
            cursor.execute("SELECT name,phone,points,password FROM users")
            ul = cursor.fetchall(); uo={f"{u[0]} ({u[1]})":u for u in ul}
            if uo:
                su_str = st.selectbox("إختر العضو:", list(uo.keys()))
                td = uo[su_str]; ce,cd = st.columns(2)
                with ce:
                    np2=st.number_input("تعديل النقاط إلى:", 0, 500, value=td[2])
                    npass=st.text_input(f"تعديل كلمة مرور {td[0]}:", value=td[3])
                    if st.button("💾 حفظ التعديلات"):
                        cursor.execute("UPDATE users SET points=?,password=? WHERE phone=?",(np2,npass,td[1])); db_conn.commit(); st.success("تم!"); st.rerun()
                with cd:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("❌ حذف هذا العضو نهائياً"):
                        cursor.execute("DELETE FROM users WHERE phone=?",(td[1],)); db_conn.commit(); st.error("تم الحذف!"); st.rerun()
