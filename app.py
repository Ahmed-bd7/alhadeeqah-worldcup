import streamlit as st
from datetime import datetime, timedelta
import pytz

# 1. إعداد المنطقة الزمنية وتنسيق الصفحة
ksa_tz = pytz.timezone('Asia/Riyadh')
now_ksa = datetime.now(ksa_tz)

st.set_page_config(page_title="توقعات الحديقة 2026", page_icon="🌿", layout="centered")

# --- 2. إضافة لمسات التصميم الخاصة بلوقو الحديقة (CSS) ---
st.markdown("""
    <style>
    /* تغيير خلفية الصفحة ودرجات الأخضر */
    .stApp {
        background-color: #f4f9f4;
    }
    
    /* تصميم العنوان الرئيسي */
    .main-title {
        color: #1e4620; /* أخضر غامق ملكي */
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-size: 40px;
        font-weight: bold;
        border-bottom: 3px solid #d4af37; /* خط ذهبي تحت العنوان */
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    
    /* تصميم بطاقة المباراة */
    .match-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-right: 10px solid #2e7d32; /* حافة خضراء يمين */
        margin-bottom: 25px;
    }
    
    /* تصميم الأزرار */
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        border: 1px solid #d4af37;
    }
    
    /* تصميم حقول الإدخال */
    .stNumberInput input {
        border-radius: 8px;
        border: 1px solid #2e7d32;
    }
    </style>
    <div class="main-title">🌿 سستم توقعات قروب الحديقة 2026 🏆</div>
    """, unsafe_allow_html=True)

# --- 3. جدول الـ 35 مباراة مع الأعلام ---
matches = [
    {"id": 1, "desc": "🇲🇽 المكسيك × جنوب أفريقيا 🇿🇦", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz)},
    {"id": 2, "desc": "🇨🇭 سويسرا × قطر 🇶🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz)},
    {"id": 3, "desc": "🇧🇷 البرازيل × المغرب 🇲🇦", "time": datetime(2026, 6, 13, 1, 0, tzinfo=ksa_tz)},
    {"id": 4, "desc": "🇩🇪 ألمانيا × كوراساو 🇨🇼", "time": datetime(2026, 6, 14, 20, 0, tzinfo=ksa_tz)},
    {"id": 5, "desc": "🇳🇱 هولندا × اليابان 🇯🇵", "time": datetime(2026, 6, 14, 23, 0, tzinfo=ksa_tz)},
    {"id": 6, "desc": "🇫🇷 فرنسا × مصر 🇪🇬", "time": datetime(2026, 6, 14, 18, 0, tzinfo=ksa_tz)},
    {"id": 7, "desc": "🇨🇮 كوت ديفوار × الإكوادور 🇪🇨", "time": datetime(2026, 6, 15, 2, 0, tzinfo=ksa_tz)},
    {"id": 8, "desc": "🇹🇳 تونس × السويد 🇸🇪", "time": datetime(2026, 6, 15, 5, 0, tzinfo=ksa_tz)},
    {"id": 9, "desc": "🇦🇷 الأرجنتين × إيران 🇮🇷", "time": datetime(2026, 6, 15, 21, 0, tzinfo=ksa_tz)},
    {"id": 10, "desc": "🇸🇦 السعودية × كندا 🇨🇦 🔥", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz)},
    {"id": 11, "desc": "🇪🇸 إسبانيا × الجزائر 🇩🇿", "time": datetime(2026, 6, 16, 19, 0, tzinfo=ksa_tz)},
    {"id": 12, "desc": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 إنجلترا × الأردن 🇯🇴", "time": datetime(2026, 6, 16, 22, 0, tzinfo=ksa_tz)},
    {"id": 13, "desc": "🇵🇹 البرتغال × العراق 🇮🇶", "time": datetime(2026, 6, 17, 20, 0, tzinfo=ksa_tz)},
    {"id": 14, "desc": "🇫🇷 فرنسا × غانا 🇬🇭", "time": datetime(2026, 6, 19, 20, 0, tzinfo=ksa_tz)},
    {"id": 15, "desc": "🇶🇦 قطر × كندا 🇨🇦", "time": datetime(2026, 6, 19, 1, 0, tzinfo=ksa_tz)},
    {"id": 16, "desc": "🇲🇦 المغرب × اسكتلندا 🏴", "time": datetime(2026, 6, 19, 22, 0, tzinfo=ksa_tz)},
    {"id": 17, "desc": "🇭🇹 هايتي × البرازيل 🇧🇷", "time": datetime(2026, 6, 20, 3, 30, tzinfo=ksa_tz)},
    {"id": 18, "desc": "🇦🇷 الأرجنتين × كرواتيا 🇭🇷", "time": datetime(2026, 6, 20, 22, 0, tzinfo=ksa_tz)},
    {"id": 19, "desc": "🇸🇳 السنغال × الأردن 🇯🇴", "time": datetime(2026, 6, 21, 16, 0, tzinfo=ksa_tz)},
    {"id": 20, "desc": "🇩🇪 ألمانيا × الإكوادور 🇪🇨", "time": datetime(2026, 6, 21, 11, 0, tzinfo=ksa_tz)},
    {"id": 21, "desc": "🇸🇦 السعودية × الأوروغواي 🇺🇾 🔥", "time": datetime(2026, 6, 21, 19, 0, tzinfo=ksa_tz)},
    {"id": 22, "desc": "🇪🇸 إسبانيا × كولومبيا 🇨🇴", "time": datetime(2026, 6, 21, 21, 0, tzinfo=ksa_tz)},
    {"id": 23, "desc": "🇨🇼 كوراساو × كوت ديفوار 🇨🇮", "time": datetime(2026, 6, 22, 11, 0, tzinfo=ksa_tz)},
    {"id": 24, "desc": "🇳🇱 هولندا × السويد 🇸🇪", "time": datetime(2026, 6, 21, 11, 0, tzinfo=ksa_tz)},
    {"id": 25, "desc": "🇧🇪 بلجيكا × العراق 🇮🇶", "time": datetime(2026, 6, 22, 22, 0, tzinfo=ksa_tz)},
    {"id": 26, "desc": "🇯🇵 اليابان × تونس 🇹🇳", "time": datetime(2026, 6, 23, 2, 0, tzinfo=ksa_tz)},
    {"id": 27, "desc": "🇨🇦 كندا × سويسرا 🇨🇭", "time": datetime(2026, 6, 24, 1, 0, tzinfo=ksa_tz)},
    {"id": 28, "desc": "🇪🇬 مصر × غانا 🇬🇭", "time": datetime(2026, 6, 24, 22, 0, tzinfo=ksa_tz)},
    {"id": 29, "desc": "🇶🇦 قطر × البوسنة 🇧🇦", "time": datetime(2026, 6, 24, 1, 0, tzinfo=ksa_tz)},
    {"id": 30, "desc": "🇧🇷 البرازيل × اسكتلندا 🏴", "time": datetime(2026, 6, 25, 10, 0, tzinfo=ksa_tz)},
    {"id": 31, "desc": "🇭🇹 هايتي × المغرب 🇲🇦", "time": datetime(2026, 6, 25, 10, 0, tzinfo=ksa_tz)},
    {"id": 32, "desc": "🏴 إنجلترا × السنغال 🇸🇳", "time": datetime(2026, 6, 25, 21, 0, tzinfo=ksa_tz)},
    {"id": 33, "desc": "🇩🇪 ألمانيا × كوت ديفوار 🇨🇮", "time": datetime(2026, 6, 26, 23, 0, tzinfo=ksa_tz)},
    {"id": 34, "desc": "🇳🇱 هولندا × تونس 🇹🇳", "time": datetime(2026, 6, 26, 2, 0, tzinfo=ksa_tz)},
    {"id": 35, "desc": "🇸🇦 السعودية × الرأس الأخضر 🇨🇻 🔥", "time": datetime(2026, 6, 27, 3, 0, tzinfo=ksa_tz)}
]

# --- 4. التفاعل مع المستخدم ---
user_name = st.text_input("👤 أدخل اسمك يا متحدددي للمشاركة في تحدي الحديقة:")

if user_name:
    st.write(f"مرحباً بك يا **{user_name}** في عرين الحديقة! 🌿")
    st.markdown("---")

    for match in matches:
        time_until_match = match["time"] - now_ksa
        
        # عرض المباراة الأولى دائماً + أي مباراة قبل موعدها بـ 48 ساعة
        if (timedelta(hours=0) <= time_until_match <= timedelta(hours=48)) or (match["id"] == 1):
            
            # بناء شكل بطاقة المباراة
            with st.container():
                st.markdown(f"""
                <div class="match-card">
                    <h3 style='color: #1e4620;'>{match['desc']}</h3>
                    <p style='color: #666;'>📅 موعد اللقاء: {match['time'].strftime('%d يونيو | %I:%M %p')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # فحص وقت القفل قبل المباراة بساعة
                if time_until_match <= timedelta(hours=1):
                    st.error("🔒 التوقعات مغلقة لهذه المباراة (بدأ العد التنازلي للماتش)")
                else:
                    c1, c2 = st.columns(2)
                    with c1:
                        h_score = st.number_input("أهداف صاحب الأرض", 0, 10, key=f"h_{match['id']}")
                    with c2:
                        a_score = st.number_input("أهداف الضيف", 0, 10, key=f"a_{match['id']}")
                    
                    if st.button(f"إرسال التوقع لـ {match['desc']}", key=f"btn_{match['id']}"):
                        st.success(f"كفو! تم حفظ توقعك ({h_score}-{a_score}) في سجلات الحديقة")
            st.markdown("<br>", unsafe_allow_html=True)
