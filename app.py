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

            st.markdown("---")
            st.subheader("🔮 وضع توقعاتك الذكية")
            
            for match in all_matches:
                time_until_match = match["time"] - now_ksa
                
                # فحص حالة المباراة وتفاصيل نتيجتها المخزنة
                cursor.execute("SELECT actual_home, actual_away FROM processed_matches WHERE match_id = ?", (match["id"],))
                match_status_row = cursor.fetchone()
                
                # التحقق الذكي من أن القيم المسترجعة ليست فارغة
                if match_status_row and match_status_row[0] is not None and match_status_row[1] is not None:
                    match_desc = f"{match['team_home']} {match_status_row[0]} × {match_status_row[1]} {match['team_away']} (انتهت واحتُسبت ✅)"
                    is_calculated_and_valid = True
                else:
                    match_desc = f"{match['team_home']} × {match['team_away']}"
                    is_calculated_and_valid = False
                
                # شرط العرض الذكي (خلال 24 ساعة، أو مباريات يوم 11 يونيو، أو الأدمن)
                is_within_24h = (timedelta(hours=0) <= time_until_match <= timedelta(hours=24))
                is_june_11 = (match["time"].day == 11 and match["time"].month == 6)
                
                if is_within_24h or is_june_11 or is_calculated_and_valid or (login_phone == ADMIN_PHONE):
                    with st.container():
                        st.markdown(f"""
                        <div class="match-card">
                            <h4 style='color: #1e4620; margin:0;'>{match_desc}</h4>
                            <p style='color: #777; font-size:13px; margin:5px 0 0 0;'>📅 موعد اللقاء: {match['time'].strftime('%d يونيو | %I:%M %p')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if (time_until_match < timedelta(minutes=10) or is_calculated_and_valid) and login_phone != ADMIN_PHONE:
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
            
            # 🛠️ --- لوحة التحكم المتطورة والآمنة الخاصة بأحمد بادحمان ---
            if login_phone == ADMIN_PHONE:
                st.markdown("---")
                st.markdown('<div class="admin-card">⚙️ <b>لوحة تحكم الإدارة الملكية (أحمد بادحمان)</b></div>', unsafe_allow_html=True)
                
                st.subheader("🧮 إدارة وإدخل نتائج المباريات")
                match_options = {f"{m['team_home']} × {m['team_away']}": m for m in all_matches}
                selected_match_str = st.selectbox("إختر المباراة المستهدفة لإدخال/تعديل نتيجتها:", list(match_options.keys()))
                selected_match = match_options[selected_match_str]
                
                cursor.execute("SELECT actual_home, actual_away FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
                already_calculated = cursor.fetchone()
                
                # التحقق أن النتيجة القديمة ليست فارغة لمنع الـ TypeError
                is_valid_old_result = already_calculated and already_calculated[0] is not None and already_calculated[1] is not None
                
                if is_valid_old_result:
                    st.warning(f"⚠️ هذه المباراة احتُسبت سابقاً بنتيجة: {already_calculated[0]} - {already_calculated[1]}")
                    
                    # 🔴 خيار الإلغاء الآمن
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
                        st.error(f"🔄 تم إلغاء المباراة وسحب النقاط بنجاح! عادت المباراة مفتوحة الآن.")
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
                    # إذا كانت النتيجة قديمة وصحيحة، نقوم بخصمها أولاً قبل التحديث الجديد
                    if is_valid_old_result:
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
                    
                    # احتساب النقاط الجديدة وإضافتها
                    cursor.execute("SELECT phone, pred_home, pred_away FROM predictions WHERE match_id = ?", (selected_match["id"],))
                    all_preds = cursor.fetchall()
                    for pred in all_preds:
                        user_phone, p_home, p_away = pred
                        calculated_points = 0
                        if p_home == actual_h and p_away == actual_a:
                            calculated_points = 3
                        elif (p_home > p_away and actual_h > actual_a) or \
                             (p_home < p_away and actual_h < actual_a) or \
                             (p_home == p_away and actual_h == actual_a):
                            calculated_points = 1
                        if calculated_points > 0:
                            cursor.execute("UPDATE users SET points = points + ? WHERE phone = ?", (calculated_points, user_phone))
                    
                    # حفظ النتيجة الجديدة في الـ Database
                    cursor.execute('''
                        INSERT INTO processed_matches (match_id, actual_home, actual_away) 
                        VALUES (?, ?, ?)
                        ON CONFLICT(match_id) DO UPDATE SET actual_home=excluded.actual_home, actual_away=excluded.actual_away
                    ''', (selected_match["id"], actual_h, actual_a))
                    db_conn.commit()
                    st.success(f"🏆 تم اعتماد النتيجة ({actual_h} - {actual_a}) وتحديث نقاط الشباب فوراً!")
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
                            cursor.execute("DELETE FROM predictions WHERE phone = ?", (target_user_data[1],))
                            db_conn.commit()
                            st.error("تم حذف العضو!")
                            st.rerun()
