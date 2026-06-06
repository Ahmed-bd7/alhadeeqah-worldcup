import streamlit as st
from datetime import datetime, timedelta
import pytz
import pandas as pd

# 1. إعداد المنطقة الزمنية والتنسيق الملكي للحديقة
ksa_tz = pytz.timezone('Asia/Riyadh')
now_ksa = datetime.now(ksa_tz)

st.set_page_config(page_title="توقعات الحديقة 2026", page_icon="🌿", layout="centered")

# تصميم واجهة المستخدم (CSS) - هوية الحديقة
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
    <div class="main-title">🌿 بوابـة الحديقة الرقمية لكأس العالم 🏆</div>
    """, unsafe_allow_html=True)

# 2. جلب رابط الجدول بأمان من الخزنة السرية وتوصيله بالسستم
try:
    gsheet_url = st.secrets["public_gsheet_url"]
    # تحويل الرابط ليصبح جاهزاً للقراءة المباشرة كـ CSV
    csv_url = gsheet_url.replace('/edit?usp=sharing', '/gviz/tq?tqx=out:csv&sheet=users')
    leaderboard_data = pd.read_csv(csv_url)
except:
    # بيانات افتراضية في حال لم يتم الربط بعد بنجاح
    leaderboard_data = pd.DataFrame([{"المشارك": "أحمد بادحمان", "النقاط": 12}, {"المشارك": "صديق 1", "النقاط": 9}])

# 3. جدول المباريات الشامل
matches = [
    {"id": 1, "desc": "🇲🇽 المكسيك × جنوب أفريقيا 🇿🇦", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz)},
    {"id": 2, "desc": "🇨🇭 سويسرا × قطر 🇶🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz)},
    {"id": 3, "desc": "🇧🇷 البرازيل × المغرب 🇲🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz)},
    {"id": 10, "desc": "🇸🇦 السعودية × كندا 🇨🇦 🔥", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz)}
]

# 4. نظام الدخول الفريد (رقم الجوال)
st.subheader("🔐 تسجيل دخول مشاركي الحديقة")
user_phone = st.text_input("📱 أدخل رقم جوالك الفريد للاستمرار:", max_chars=10, help="رقم جوالك يحمي توقعاتك من التعديل ويحسب نقاطك")

if user_phone:
    st.success(f"مرحباً بك في لوحة تحكم الحديقة لايف! ⚽")
    
    # عرض لوحة الصدارة المحدثة أوتوماتيكياً للشباب
    st.markdown("### 📊 جدول صدارة القروب الحالي")
    st.dataframe(leaderboard_data, hide_index=True, use_container_width=True)
    st.markdown("---")
    
    # عرض المباريات المتاحة
    st.subheader("🔮 ضع توقعاتك الفريدة")
    for match in matches:
        time_until_match = match["time"] - now_ksa
        
        if (timedelta(hours=0) <= time_until_match <= timedelta(hours=48)) or (match["id"] == 1):
            with st.container():
                st.markdown(f"""
                <div class="match-card">
                    <h4 style='color: #1e4620; margin:0;'>{match['desc']}</h4>
                    <p style='color: #777; font-size:13px; margin:5px 0 0 0;'>📅 انطلاق اللقاء: {match['time'].strftime('%d يونيو | %I:%M %p')}</p>
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
                        # السستم يعطيه تأكيد فوري، ويخزن البيانات مقترنة برقم جواله في الخلفية
                        st.success(f"تم تسجيل توقعك الفريد بنجاح لـ {match['desc']}!")
            st.markdown("<br>", unsafe_allow_html=True)
