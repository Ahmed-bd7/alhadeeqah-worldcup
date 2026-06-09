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

# 🌐 3. إعدادات الـ API والمفتاح الرسمي لكأس العالم 2026
API_KEY = "3a57379657b569a7a6abe3176fe85b10"
LEAGUE_ID = 1  
CURRENT_YEAR = 2026

# 🔄 دالة جلب المباريات وأتمتة حساب النقاط تلقائياً
@st.cache_data(ttl=300)  # تحديث ذكي كل 5 دقائق
def fetch_and_process_matches(api_key, league_id, year):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    
    fetched_matches = []
    api_success = False
    
    for season in [year, year-1, year-2]:
        try:
            params = {'league': league_id, 'season': season}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            if "response" in data and len(data["response"]) > 0:
                cursor = db_conn.cursor()
                
                for item in data["response"]:
                    fixture = item["fixture"]
                    teams = item["teams"]
                    goals = item["goals"]
                    
                    utc_time = datetime.strptime(fixture["date"], "%Y-%m-%dT%H:%M:%S%z")
                    ksa_time = utc_time.astimezone(ksa_tz)
                    
                    match_id = fixture["id"]
                    status = fixture["status"]["short"]  # حالة المباراة (FT تعني انتهت)
                    
                    fetched_matches.append({
                        "id": match_id,
                        "team_home": teams["home"]["name"],
                        "team_away": teams["away"]["name"],
                        "time": ksa_time,
                        "status": status,
                        "goals_home": goals["home"],
                        "goals_away": goals["away"]
                    })
                    
                    # 🤖 [الأتمتة الذكية]: إذا انتهت المباراة ولم تحسب نقاطها بعد
                    if status == "FT" and goals["home"] is not None and goals["away"] is not None:
                        cursor.execute("SELECT match_id FROM processed_matches WHERE match_id = ?", (match_id,))
                        if not cursor.fetchone():
                            actual_h = goals["home"]
                            actual_a = goals["away"]
                            
                            # جلب توقعات الشباب لهذه المباراة
                            cursor.execute("SELECT phone, pred_home, pred_away FROM predictions WHERE match_id = ?", (match_id,))
                            all_preds = cursor.fetchall()
                            
                            for pred in all_preds:
                                user_phone, p_home, p_away = pred
                                calculated_points = 0
                                
                                # 3 نقاط للتوقع الصحيح بالملي
                                if p_home == actual_h and p_away == actual_a:
                                    calculated_points = 3
                                # نقطة واحدة لتوقع الفائز أو التعادل
                                elif (p_home > p_away and actual_h > actual_a) or \
                                     (p_home < p_away and actual_h < actual_a) or \
                                     (p_home == p_away and actual_h == actual_a):
                                    calculated_points = 1
                                    
                                if calculated_points > 0:
                                    cursor.execute("UPDATE users SET points = points + ? WHERE phone = ?", (calculated_points, user_phone))
                            
                            # قفل المباراة كمعالجة بنجاح
                            cursor.execute("INSERT INTO processed_matches (match_id) VALUES (?)", (match_id,))
                            db_conn.commit()
                            
                fetched_matches.sort(key=lambda x: x["time"])
                api_success = True
                return fetched_matches
        except Exception as e:
            continue
            
    if not api_success:
        return [
            {"id": 901, "team_home": "المكسيك (احتياطي)", "team_away": "جنوب أفريقيا", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz), "status": "NS", "goals_home": None, "goals_away": None},
            {"id": 902, "team_home": "السعودية (احتياطي)", "team_away": "كندا", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz), "status": "NS", "goals_home": None, "goals_away": None}
        ]

# تشغيل الأتمتة الفورية وحفظ القائمة المحدثة لايف
matches = fetch_and_process_matches(API_KEY, LEAGUE_ID, CURRENT_YEAR)

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
                    cursor.execute("INSERT INTO users (name, points, phone, password) VALUES (?, ?, ?, ?)", (new_name, 0, new_phone, new_pass))
                    db_conn.commit()
                    st.success(f"🎉 تم إنشاء حسابك المؤمن بنجاح يا {new_name}!")
                    st.balloons()

# --- شاشة تسجيل الدخول ---
else:
    st.subheader("🔐 تسجيل دخول مشاركي الحديقة")
    login_phone = st.text_input("📱 أدخل رقم جوالك المعتمد:", max_chars=10)
    login_pass = st.text_input("🔐 أدخل كلمة المرور الخاصة بك:", type="password")
    
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
            user_name = user_row[0]
            st.success(f"مرحباً بعودتك يا {user_name}! 😎")
            
            # عرض لوحة الصدارة
            st.markdown("### 📊 لوحة الصدارة المحدثة لايف")
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
                    st.markdown(f"🏆 {p_points} ن")
                with col_action:
                    if st.button(f"شفافية التوقعات", key=f"rev_{p_phone}_{idx}"):
                        st.session_state[f"view_predictions_for"] = p_phone
                        st.session_state[f"view_predictions_name"] = p_name
            
            if f"view_predictions_for" in st.session_state:
                target_phone = st.session_state[f"view_predictions_for"]
                target_name = st.session_state[f"view_predictions_name"]
                st.markdown(f"""<div class="review-card">🔍 <b>كشف توقعات المشارك: {target_name}</b></div>""", unsafe_allow_html=True)
                
                cursor.execute("SELECT match_id, pred_home, pred_away FROM predictions WHERE phone = ?", (target_phone,))
                user_preds = {r[0]: (r[1], r[2]) for r in cursor.fetchall()}
                
                review_list = []
                for m in matches:
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

            st.markdown("---")
            st.subheader("🔮 وضع توقعاتك الذكية")
            
            for match in matches:
                time_until_match = match["time"] - now_ksa
                
                # إظهار نتيجة المباراة الحقيقية بجانبها إذا كانت انتهت أو تلعب الآن
                if match["status"] == "FT":
                    match_desc = f"{match['team_home']} {match['goals_home']} × {match['goals_away']} {match['team_away']} (انتهت ✅)"
                else:
                    match_desc = f"{match['team_home']} × {match['team_away']}"
                
                if (timedelta(minutes=10) <= time_until_match <= timedelta(hours=48)) or (login_phone == ADMIN_PHONE) or (match["status"] == "FT"):
                    with st.container():
                        st.markdown(f"""
                        <div class="match-card">
                            <h4 style='color: #1e4620; margin:0;'>{match_desc}</h4>
                            <p style='color: #777; font-size:13px; margin:5px 0 0 0;'>📅 موعد اللقاء: {match['time'].strftime('%d يونيو | %I:%M %p')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # منع التوقع إذا انتهت أو قفل وقتها
                        if (time_until_match < timedelta(minutes=10) or match["status"] == "FT") and login_phone != ADMIN_PHONE:
                            st.error("🔒 مغلق! انتهى الوقت القانوني أو المباراة انتهت فعلياً.")
                        else:
                            cursor.execute("SELECT pred_home, pred_away FROM predictions WHERE phone = ? AND match_id = ?", (login_phone, match["id"]))
                            existing_pred = cursor.fetchone()
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
            
            # 🛠️ --- لوحة التحكم الخاصة بأحمد بادحمان (أصبحت خفيفة لإدارة السستم فقط) ---
            if login_phone == ADMIN_PHONE:
                st.markdown("---")
                st.markdown('<div class="admin-card">⚙️ <b>لوحة تحكم الإدارة الملكية (أحمد بادحمان)</b></div>', unsafe_allow_html=True)
                
                st.info("💡 النظام الآن يعمل مؤتمتاً بالكامل. النتائج تُحسب وتُوزع تلقائياً فور نهاية المباريات عبر الـ API.")
                
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
                            cursor.execute("DELETE FROM predictions WHERE phone = ?", (target_user_data[1],))
                            db_conn.commit()
                            st.error("تم حذف العضو!")
                            st.rerun()
                
                st.markdown("---")
                if st.button("🚨 تصفير قاعدة البيانات بالكامل"):
                    cursor.execute("DELETE FROM users")
                    cursor.execute("DELETE FROM predictions")
                    cursor.execute("DELETE協會 FROM processed_matches")
                    db_conn.commit()
                    st.success("تم تصفير السستم بالكامل!")
                    st.rerun()
