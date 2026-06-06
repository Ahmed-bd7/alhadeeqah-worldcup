import streamlit as st
from datetime import datetime, timedelta
import pytz
import sqlite3

# --- 1. الإعدادات الأساسية ---
ksa_tz = pytz.timezone('Asia/Riyadh')
now_ksa = datetime.now(ksa_tz)

st.set_page_config(page_title="الحديقة 2026", page_icon="🌿", layout="centered")

# --- 2. التصميم الفاخر (WhatsApp Dark Mode) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b141a; color: #e9edef; }
    section[data-testid="stSidebar"] { background-color: #111b21 !important; border-right: 1px solid #222d34; }
    .main-title { color: #00a884; text-align: center; font-family: sans-serif; font-size: 30px; font-weight: bold; margin-bottom: 20px; }
    .match-card { background-color: #202c33; border-radius: 12px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #00a884; }
    div.stButton > button { background-color: #00a884 !important; color: white !important; border-radius: 20px !important; border: none !important; font-weight: bold !important; width: 100%; height: 40px; }
    .admin-panel { background-color: #182229; padding: 15px; border-radius: 10px; border: 1px solid #00a884; }
    </style>
""", unsafe_allow_html=True)

# --- 3. إدارة قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('alhadeeqah_db.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, points INTEGER DEFAULT 0, phone TEXT PRIMARY KEY, password TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS predictions (phone TEXT, match_id INTEGER, pred_home INTEGER, pred_away INTEGER, PRIMARY KEY (phone, match_id))')
    cursor.execute('CREATE TABLE IF NOT EXISTS processed_matches (match_id INTEGER PRIMARY KEY, actual_home INTEGER, actual_away INTEGER)')
    conn.commit()
    return conn

db_conn = init_db()
ADMIN_PHONE = "0502518301"

# --- 4. جدول المباريات ---
def get_matches():
    return [
        {"id": 101, "team_home": "المكسيك", "team_away": "كندا", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz)},
        {"id": 102, "team_home": "أمريكا", "team_away": "عُمان", "time": datetime(2026, 6, 12, 1, 0, tzinfo=ksa_tz)},
        {"id": 103, "team_home": "الأرجنتين", "team_away": "المغرب", "time": datetime(2026, 6, 13, 18, 0, tzinfo=ksa_tz)},
        {"id": 104, "team_home": "فرنسا", "team_away": "أستراليا", "time": datetime(2026, 6, 13, 21, 0, tzinfo=ksa_tz)},
        {"id": 105, "team_home": "إسبانيا", "team_away": "نيجيريا", "time": datetime(2026, 6, 14, 16, 0, tzinfo=ksa_tz)},
        {"id": 108, "team_home": "السعودية", "team_away": "أوروجواي", "time": datetime(2026, 6, 15, 20, 0, tzinfo=ksa_tz)},
        {"id": 110, "team_home": "البرازيل", "team_away": "اليابان", "time": datetime(2026, 6, 16, 18, 0, tzinfo=ksa_tz)},
    ]

# --- 5. القائمة الجانبية (التنقل) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg", width=50)
    st.title("الحديقة الرقمية")
    if 'logged_in' not in st.session_state:
        nav = st.radio("القائمة:", ["تسجيل الدخول", "إنشاء حساب"])
    else:
        st.write(f"مرحباً {st.session_state['user_name']}")
        nav = st.radio("التنقل:", ["🔮 التوقعات", "📊 الصدارة", "⚙️ الإدارة"])
        if st.button("خروج"): st.session_state.clear(); st.rerun()

# --- 6. الصفحات ---
if 'logged_in' not in st.session_state:
    if nav == "إنشاء حساب":
        with st.form("reg"):
            n = st.text_input("الاسم:")
            p = st.text_input("الجوال:")
            pw = st.text_input("كلمة المرور:", type="password")
            if st.form_submit_button("تسجيل"):
                try:
                    db_conn.cursor().execute("INSERT INTO users VALUES (?,0,?,?)", (n, p, pw))
                    db_conn.commit()
                    st.success("تم!")
                except: st.error("الجوال مستخدم!")
    else:
        lp = st.text_input("الجوال:")
        lpw = st.text_input("كلمة المرور:", type="password")
        if st.button("دخول"):
            c = db_conn.cursor()
            c.execute("SELECT name FROM users WHERE phone=? AND password=?", (lp, lpw))
            res = c.fetchone()
            if res:
                st.session_state.update({'logged_in': True, 'user_name': res[0], 'phone': lp})
                st.rerun()
            else: st.error("بيانات خطأ")

else:
    if nav == "🔮 التوقعات":
        st.markdown('<div class="main-title">المباريات القادمة</div>', unsafe_allow_html=True)
        for m in get_matches():
            c = db_conn.cursor()
            c.execute("SELECT actual_home, actual_away FROM processed_matches WHERE match_id=?", (m['id'],))
            res = c.fetchone()
            if (m['time'] - now_ksa < timedelta(hours=24)) or res:
                st.markdown(f'<div class="match-card"><h4>{m["team_home"]} VS {m["team_away"]}</h4><p>التوقيت: {m["time"].strftime("%H:%M")}</p></div>', unsafe_allow_html=True)
                if not res and (m['time'] - now_ksa > timedelta(minutes=10)):
                    col1, col2 = st.columns(2)
                    ph = col1.number_input(f"{m['team_home']}", 0, 10, key=f"h{m['id']}")
                    pa = col2.number_input(f"{m['team_away']}", 0, 10, key=f"a{m['id']}")
                    if st.button("تأكيد التوقع", key=f"b{m['id']}"):
                        c.execute("INSERT OR REPLACE INTO predictions VALUES (?,?,?,?)", (st.session_state['phone'], m['id'], ph, pa))
                        db_conn.commit()
                        st.toast("تم الحفظ!")

    elif nav == "📊 الصدارة":
        c = db_conn.cursor()
        c.execute("SELECT name, points FROM users ORDER BY points DESC")
        for u in c.fetchall(): st.write(f"🏆 {u[0]} - {u[1]} نقطة")

    elif nav == "⚙️ الإدارة" and st.session_state['phone'] == ADMIN_PHONE:
        st.markdown('<div class="admin-panel"><h3>لوحة الإدارة</h3>', unsafe_allow_html=True)
        m_sel = st.selectbox("المباراة:", [f"{m['id']} - {m['team_home']}" for m in get_matches()])
        mid = int(m_sel.split(' - ')[0])
        h = st.number_input("أهداف صاحب الأرض", 0, 10)
        a = st.number_input("أهداف الضيف", 0, 10)
        if st.button("اعتماد النتيجة"):
            c = db_conn.cursor()
            c.execute("SELECT phone, pred_home, pred_away FROM predictions WHERE match_id=?", (mid,))
            for p in c.fetchall():
                pts = 3 if (p[1]==h and p[2]==a) else (1 if (p[1]>p[2] and h>a) or (p[1]<p[2] and h<a) or (p[1]==p[2] and h==a) else 0)
                c.execute("UPDATE users SET points = points + ? WHERE phone=?", (pts, p[0]))
            c.execute("INSERT OR REPLACE INTO processed_matches VALUES (?,?,?)", (mid, h, a))
            db_conn.commit()
            st.success("تم التحديث!")
