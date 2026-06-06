import streamlit as st
from datetime import datetime, timedelta
import pytz
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. إعداد المنطقة الزمنية وتنسيق الصفحة
ksa_tz = pytz.timezone('Asia/Riyadh')
now_ksa = datetime.now(ksa_tz)

st.set_page_config(page_title="توقعات الحديقة 2026", page_icon="🌿", layout="centered")

# تصميم واجهة المستخدم (CSS)
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

# 2. إنشاء الاتصال التلقائي بـ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# دالة قراءة البيانات مع إلغاء الكاش لضمان التحديث اللحظي المتبادل
def load_live_data(sheet_name):
    try:
        return conn.read(worksheet=sheet_name, ttl=0)
    except:
        return pd.DataFrame()

df_users = load_live_data("users")
df_preds = load_live_data("predictions")

# 3. جدول المباريات الثابتة
matches = [
    {"id": 1, "desc": "🇲🇽 المكسيك × جنوب أفريقيا 🇿🇦", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz), "actual_home": None, "actual_away": None},
    {"id": 2, "desc": "🇨🇭 سويسرا × قطر 🇶🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz), "actual_home": None, "actual_away": None},
    {"id": 3, "desc": "🇧🇷 البرازيل × المغرب 🇲🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz), "actual_home": None, "actual_away": None},
    {"id": 10, "desc": "🇸🇦 السعودية × كندا 🇨🇦 🔥", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz), "actual_home": None, "actual_away": None}
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
                is_duplicate = False
                if not df_users.empty and "الجوال" in df_users.columns:
                    df_users["الجوال"] = df_users["الجوال"].astype(str).str.strip()
                    if new_phone in df_users["الجوال"].values:
                        is_duplicate = True
                
                if is_duplicate:
                    st.error(f"⚠️ خطأ: رقم الجوال ({new_phone}) مسجل مسبقاً!")
                else:
                    new_user_df = pd.DataFrame([{"المشارك": new_name, "النقاط": 0, "الجوال": new_phone}])
                    df_users = pd.concat([df_users, new_user_df], ignore_index=True)
                    
                    try:
                        conn.update(worksheet="users", data=df_users)
                        st.success(f"🎉 تم إنشاء حسابك بنجاح يا {new_name}! حول الآن إلى شاشة 'تسجيل الدخول' للبدء.")
                        st.rerun()
                    except Exception as e:
                        st.error("⚠️ تأكد من تغيير صلاحية الرابط في قوقل شيت إلى Editor (محرر) وليس عارض.")

# --- شاشة تسجيل الدخول المعتمدة ---
else:
    st.subheader("🔐 تسجيل دخول مشاركي الحديقة")
    login_phone = st.text_input("📱 أدخل رقم جوالك المعتمد للدخول:", max_chars=10)
    
    if login_phone:
        login_phone = str(login_phone).strip()
        is_found = False
        user_name = ""
        
        if not df_users.empty and "الجوال" in df_users.columns:
            df_users["الجوال"] = df_users["الجوال"].astype(str).str.strip()
            user_row = df_users[df_users["الجوال"] == login_phone]
            if not user_row.empty:
                is_found = True
                user_name = user_row.iloc[0]["المشارك"]
        
        if not is_found:
            st.error("❌ رقم الجوال هذا غير مسجل مسبقاً! يرجى اختيار خيار 'إنشاء حساب جديد' أولاً.")
        else:
            st.success(f"مرحباً بعودتك يا {user_name}! 😎")
            
            st.markdown("### 📊 لوحة الصدارة المحدثة لايف")
            if not df_users.empty and "النقاط" in df_users.columns:
                df_display = df_users[["المشارك", "النقاط"]].sort_values(by="النقاط", ascending=False)
                st.dataframe(df_display, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🔮 ضع توقعاتك")
            
            for match in matches:
                time_until_match = match["time"] - now_ksa
                
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
                            c1, c2 = st.columns(2)
                            with c1:
                                h_score = st.number_input("أهداف الأول", 0, 10, key=f"h_{match['id']}")
                            with c2:
                                a_score = st.number_input("أهداف الثاني", 0, 10, key=f"a_{match['id']}")
                            
                            if st.button(f"اعتماد التوقع للمباراة", key=f"btn_{match['id']}"):
                                new_pred = pd.DataFrame([{"الجوال": login_phone, "المباراة": match["id"], "توقع_1": h_score, "توقع_2": a_score}])
                                df_preds = pd.concat([df_preds, new_pred], ignore_index=True)
                                
                                try:
                                    conn.update(worksheet="predictions", data=df_preds)
                                    st.success("تم تسجيل توقعك الفريد بأمان في السيرفر! 🏁")
                                    st.rerun()
                                except Exception as e:
                                    st.error("خطأ أثناء حفظ التوقع. يرجى مراجعة الصلاحيات.")
                    st.markdown("<br>", unsafe_allow_html=True)
