import streamlit as st
from datetime import datetime
import pytz
import sqlite3

# إعدادات الصفحة
ksa_tz = pytz.timezone('Asia/Riyadh')
st.set_page_config(page_title="الحديقة 2026", layout="centered")

# CSS التصميم الاحترافي (Modern Dark Theme)
st.markdown("""
    <style>
    .stApp { background-color: #0b141a; color: #e9edef; font-family: sans-serif; }
    .header { text-align: center; color: #00a884; font-size: 32px; font-weight: bold; margin-bottom: 20px; }
    .card { background-color: #16212a; border-radius: 20px; padding: 20px; margin-bottom: 15px; border: 1px solid #222d34; }
    .btn-green > button { background: linear-gradient(90deg, #00a884, #06cf9c) !important; color: white !important; border-radius: 15px !important; border: none !important; width: 100%; font-weight: bold !important; }
    .nav-bar { display: flex; justify-content: space-around; padding: 10px; background: #16212a; border-radius: 20px; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# قاعدة البيانات
conn = sqlite3.connect('alhadeeqah.db', check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS preds (phone TEXT, match_id INT, h INT, a INT, PRIMARY KEY(phone, match_id))')

# قائمة المباريات الكاملة
def get_all_matches():
    return [
        {"id": 101, "h": "المكسيك", "a": "كندا"},
        {"id": 102, "h": "أمريكا", "a": "عُمان"},
        {"id": 103, "h": "الأرجنتين", "a": "المغرب"},
        {"id": 108, "h": "السعودية", "a": "أوروجواي"},
        {"id": 110, "h": "البرازيل", "a": "اليابان"}
        # يمكنك إضافة بقية المباريات هنا بنفس النمط
    ]

# الواجهة
st.markdown('<div class="header">🌿 الحديقة الرقمية 2026</div>', unsafe_allow_html=True)

# التنقل (محاكاة لشريط السفلي في التطبيقات)
page = st.radio("القائمة:", ["المباريات", "الصدارة", "الإدارة"], horizontal=True)

if page == "المباريات":
    for m in get_all_matches():
        st.markdown(f'''
            <div class="card">
                <h3 style="text-align:center;">{m["h"]} VS {m["a"]}</h3>
            </div>
        ''', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        h = c1.number_input(f"أهداف {m['h']}", 0, 10, key=f"h{m['id']}")
        a = c2.number_input(f"أهداف {m['a']}", 0, 10, key=f"a{m['id']}")
        if st.button("تأكيد التوقع", key=f"b{m['id']}"):
            st.toast("تم حفظ توقعك!")

elif page == "الصدارة":
    st.write("قريباً: لوحة صدارة الأبطال")

elif page == "الإدارة":
    st.text_input("كلمة مرور الأدمن:")
    st.success("لوحة التحكم جاهزة للتفعيل")
