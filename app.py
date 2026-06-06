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
        border-right: 10px solid #ffc107; margin-top: 30px;
    }
    .stButton>button {
        background-color: #2e7d32; color: white; border-radius: 10px;
        width: 100%; font-weight: bold; height: 40px; border: none;
    }
    .stButton>button:hover { background-color: #1b5e20; border: 1px solid #d4af37; }
    </style>
    <div class="main-title">🌿 بوابـة الحديقة الرقمية الذكية 🏆</div>
    """, unsafe_allow_html=True)

# 2. إنشاء وإعداد قاعدة البيانات المحلية (SQLite)
def init_db():
    conn = sqlite3.connect('alhadeeqah_db.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            phone TEXT PRIMARY KEY
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
    conn.commit()
    return conn

db_conn = init_db()

# 🚨 تم تثبيت رقم أدمن الحديقة الخاص بك بنجاح
ADMIN_PHONE = "0502518301" 

# 3. جدول المباريات الثابتة
matches = [
    {"id": 1, "desc": "🇲🇽 المكسيك × جنوب أفريقيا 🇿🇦", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz)},
    {"id": 2, "desc": "🇨🇭 سويسرا × قطر 🇶🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz)},
    {"id": 3, "desc": "🇧🇷 البرازيل × المغرب 🇲🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz)},
    {"id": 10, "desc": "🇸🇦 السعودية × كندا 🇨🇦 🔥", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz)}
]

# 4. بوابـة التحكم
menu = ["تسجيل الدخول", "إنشاء حساب جديد (لأول مرة)"]
choice = st.radio("إختر الإجراء:", menu, horizontal=True)

# --- شاشة إنشاء الحساب الجديد ---
if choice == "إنشاء حساب جديد (لأول مرة)":
    st.subheader("📝 استمارة تسجيل مشارك جديد")
    
    with st.form("registration_form"):
        new_name = st.text_input("👤 الاسم الثنائي الكريم:")
        new_phone = st.text_input("📱 رقم الجوال (10 أرقام):", max_chars=10)
        submit_reg = st.form_submit_button("إرسال واعتماد الحساب في الحديقة 🚀")
        
        if submit_reg:
            new_phone = str(new_phone).strip()
            new_name = str(new_name).strip()
            
            if not new_name or not new_phone:
                st.error("❌ فضلاً، يرجى تعبئة جميع الخانات.")
            elif len(new_phone) != 10 or not new_phone.isdigit():
                st.error("❌ رقم الجوال يجب أن يتكون من 10 أرقام فقط.")
            else:
                cursor = db_conn.cursor()
                cursor.execute("SELECT phone FROM users WHERE phone = ?", (new_phone,))
                if cursor.fetchone():
                    st.error(f"⚠️ خطأ: رقم الجوال ({new_phone}) مسجل مسبقاً!")
                else:
                    cursor.execute("INSERT INTO users (name, points, phone) VALUES (?, ?, ?)", (new_name, 0, new_phone))
                    db_conn.commit()
                    st.success(f"🎉 تم إنشاء حسابك بنجاح يا {new_name}! تستطيع الآن التوجه لصفحة تسجيل الدخول.")
                    st.balloons()

# --- شاشة تسجيل الدخول المعتمدة ---
else:
    st.subheader("🔐 تسجيل دخول مشاركي الحديقة")
    login_phone = st.text_input("📱 أدخل رقم جوالك المعتمد للدخول:", max_chars=10)
    
    if login_phone:
        login_phone = str(login_phone).strip()
        cursor = db_conn.cursor()
        cursor.execute("SELECT name FROM users WHERE phone = ?", (login_phone,))
        user_row = cursor.fetchone()
        
        if not user_row:
            st.error("❌ رقم الجوال هذا غير مسجل مسبقاً! يرجى إنشاء حساب جديد أولاً.")
        else:
            user_name = user_row[0]
            st.success(f"مرحباً بعودتك يا {user_name}! 😎")
            
            # عرض لوحة الصدارة الحية
            st.markdown("### 📊 لوحة الصدارة المحدثة لايف")
            df_users = pd.read_sql_query("SELECT name AS 'المشارك', points AS 'النقاط' FROM users ORDER BY points DESC", db_conn)
            st.dataframe(df_users, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🔮 وضع توقعاتك")
            
            for match in matches:
                time_until_match = match["time"] - now_ksa
                
                # تظهر دائماً للأدمن للتجربة أو للمستخدمين قبل المباراة بـ 48 ساعة
                if (timedelta(hours=0) <= time_until_match <= timedelta(hours=48)) or (match["id"] == 1) or (login_phone == ADMIN_PHONE):
                    with st.container():
                        st.markdown(f"""
                        <div class="match-card">
                            <h4 style='color: #1e4620; margin:0;'>{match['desc']}</h4>
                            <p style='color: #777; font-size:13px; margin:5px 0 0 0;'>📅 موعد اللقاء: {match['time'].strftime('%d يونيو | %I:%M %p')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        cursor.execute("SELECT pred_home, pred_away FROM predictions WHERE phone = ? AND match_id = ?", (login_phone, match["id"]))
                        existing_pred = cursor.fetchone()
                        val_home = existing_pred[0] if existing_pred else 0
                        val_away = existing_pred[1] if existing_pred else 0
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            h_score = st.number_input("أهداف الأول", 0, 10, value=val_home, key=f"h_{match['id']}")
                        with c2:
                            a_score = st.number_input("أهداف الثاني", 0, 10, value=val_away, key=f"a_{match['id']}")
                        
                        if st.button(f"اعتماد التوقع للمباراة", key=f"btn_{match['id']}"):
                            cursor.execute('''
                                INSERT INTO predictions (phone, match_id, pred_home, pred_away)
                                VALUES (?, ?, ?, ?)
                                ON CONFLICT(phone, match_id) DO UPDATE SET pred_home=excluded.pred_home, pred_away=excluded.pred_away
                            ''', (login_phone, match["id"], h_score, a_score))
                            db_conn.commit()
                            st.success("تم تسجيل وتأمين توقعك بنجاح! 🏁")
            
            # 🛠️ --- لوحة التحكم السرية لأحمد بادحمان فقط ---
            if login_phone == ADMIN_PHONE:
                st.markdown("---")
                st.markdown('<div class="admin-card">⚙️ <b>لوحة تحكم الإدارة الملكية (أحمد بادحمان)</b></div>', unsafe_allow_html=True)
                st.subheader("🧮 إدخال النتائج الفعلية وحساب النقاط")
                
                selected_match_desc = st.selectbox("إختر المباراة التي انتهت:", [m["desc"] for m in matches])
                selected_match = next(m for m in matches if m["desc"] == selected_match_desc)
                
                col_h, col_a = st.columns(2)
                with col_h:
                    actual_h = st.number_input("النتيجة الفعلية (الفريق الأول)", 0, 10, key="act_h")
                with col_a:
                    actual_a = st.number_input("النتيجة الفعلية (الفريق الثاني)", 0, 10, key="act_a")
                
                if st.button("🔥 احسب النقاط وحدث الصدارة فوراً!"):
                    cursor.execute("SELECT phone, pred_home, pred_away FROM predictions WHERE match_id = ?", (selected_match["id"],))
                    all_preds = cursor.fetchall()
                    
                    for pred in all_preds:
                        user_phone, p_home, p_away = pred
                        calculated_points = 0
                        
                        # 1. التوقع الصحيح بالملي (النتيجة دقيقة) -> 3 نقاط
                        if p_home == actual_h and p_away == actual_a:
                            calculated_points = 3
                        # 2. توقع الفائز أو التعادل صحيح لكن الأرقام تختلف -> نقطة واحدة
                        elif (p_home > p_away and actual_h > actual_a) or \
                             (p_home < p_away and actual_h < actual_a) or \
                             (p_home == p_away and actual_h == actual_a):
                            calculated_points = 1
                        
                        if calculated_points > 0:
                            cursor.execute("UPDATE users SET points = points + ? WHERE phone = ?", (calculated_points, user_phone))
                    
                    db_conn.commit()
                    st.success(f"🏆 تم بنجاح معالجة توقعات مباراة ({selected_match_desc}) وتوزيع النقاط على الشباب وتحديث لوحة الصدارة!")
                    st.rerun()
