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
    .stButton>button {
        background-color: #2e7d32; color: white; border-radius: 10px;
        width: 100%; font-weight: bold; height: 40px; border: none;
    }
    .stButton>button:hover { background-color: #1b5e20; border: 1px solid #d4af37; }
    </style>
    <div class="main-title">🌿 بوابـة الحديقة الرقمية الذكية 🏆</div>
    """, unsafe_allow_html=True)

# 2. إنشاء وإعداد قاعدة البيانات المحلية (SQLite) تلقائياً
def init_db():
    conn = sqlite3.connect('alhadeeqah_db.db', check_same_thread=False)
    cursor = conn.cursor()
    # جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            phone TEXT PRIMARY KEY
        )
    ''')
    # جدول التوقعات
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

# 3. جدول المباريات الثابتة
matches = [
    {"id": 1, "desc": "🇲🇽 المكسيك × جنوب أفريقيا 🇿🇦", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz)},
    {"id": 2, "desc": "🇨🇭 سويسرا × قطر 🇶🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz)},
    {"id": 3, "desc": "🇧🇷 البرازيل × المغرب 🇲🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz)},
    {"id": 10, "desc": "🇸🇦 السعودية × كندا 🇨🇦 🔥", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz)}
]

# 4. بوابـة التحكم (تبديل بين تسجيل الدخول وإنشاء حساب جديد)
menu = ["تسجيل الدخول", "إنشاء حساب جديد (لأول مرة)"]
choice = st.radio("إختر الإجراء:", menu, horizontal=True)

# --- شاشة إنشاء الحساب الجديد بنظام الفرادة المحكم ---
if choice == "إنشاء حساب جديد (لأول مرة)":
    st.subheader("📝 استمارة تسجيل مشارك جديد")
    
    with st.form("registration_form"):
        new_name = st.text_input("👤 الاسم الثنائي الكريم:")
        new_phone = st.text_input("📱 رقم الجوال (10 أرقام - مثال: 05xxxxxxxx):", max_chars=10)
        submit_reg = st.form_submit_button("إرسال واعتماد الحساب في الحديقة 🚀")
        
        if submit_reg:
            new_phone = str(new_phone).strip()
            new_name = str(new_name).strip()
            
            if not new_name or not new_phone:
                st.error("❌ فضلاً، يرجى تعبئة جميع الخانات (الاسم والجوال).")
            elif len(new_phone) != 10 or not new_phone.isdigit():
                st.error("❌ رقم الجوال يجب أن يتكون من 10 أرقام فقط وبدون حروف.")
            else:
                cursor = db_conn.cursor()
                cursor.execute("SELECT phone FROM users WHERE phone = ?", (new_phone,))
                user_exists = cursor.fetchone()
                
                if user_exists:
                    st.error(f"⚠️ خطأ: رقم الجوال ({new_phone}) مسجل مسبقاً باسم مشارك آخر في القروب! لا يمكن تكراره.")
                else:
                    # إضافة الحساب الفريد بنجاح
                    cursor.execute("INSERT INTO users (name, points, phone) VALUES (?, ?, ?)", (new_name, 0, new_phone))
                    db_conn.commit()
                    st.success(f"🎉 كفو يا {new_name}! تم إنشاء حسابك المحمي بنجاح. حول الآن إلى شاشة 'تسجيل الدخول' وابدأ التحدي.")
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
            st.error("❌ رقم الجوال هذا غير مسجل مسبقاً! يرجى اختيار خيار 'إنشاء حساب جديد' أولاً.")
        else:
            user_name = user_row[0]
            st.success(f"مرحباً بعودتك يا {user_name}! 😎")
            
            # عرض لوحة الصدارة الحية
            st.markdown("### 📊 لوحة الصدارة المحدثة لايف")
            df_users = pd.read_sql_query("SELECT name AS 'المشارك', points AS 'النقاط' FROM users ORDER BY points DESC", db_conn)
            st.dataframe(df_users, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🔮 ضع توقعاتك")
            
            for match in matches:
                time_until_match = match["time"] - now_ksa
                
                # إظهار المباريات المتاحة للتوقع (قبل المباراة بـ 48 ساعة)
                if (timedelta(hours=0) <= time_until_match <= timedelta(hours=48)) or (match["id"] == 1):
                    with st.container():
                        st.markdown(f"""
                        <div class="match-card">
                            <h4 style='color: #1e4620; margin:0;'>{match['desc']}</h4>
                            <p style='color: #777; font-size:13px; margin:5px 0 0 0;'>📅 موعد اللقاء: {match['time'].strftime('%d يونيو | %I:%M %p')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if time_until_match <= timedelta(hours=1):
                            st.error("🔒 مغلق! انتهى وقت التوقع")
                        else:
                            # جلب توقع المستخدم السابق لهذه المباراة إن وجد ليعرف ماذا توقع
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
                                # حفظ التوقع أو تحديثه إذا غير رأيه (Upsert)
                                cursor.execute('''
                                    INSERT INTO predictions (phone, match_id, pred_home, pred_away)
                                    VALUES (?, ?, ?, ?)
                                    ON CONFLICT(phone, match_id) DO UPDATE SET
                                        pred_home=excluded.pred_home,
                                        pred_away=excluded.pred_away
                                ''', (login_phone, match["id"], h_score, a_score))
                                db_conn.commit()
                                st.success("تم تسجيل وتأمين توقعك الفريد بنجاح! 🏁")
                    st.markdown("<br>", unsafe_allow_html=True)
