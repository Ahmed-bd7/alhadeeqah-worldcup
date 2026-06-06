import requests
import streamlit as st

# دالة سحب نتائج مباريات كأس العالم تلقائياً من الإنترنت (Live)
def update_live_results_and_scores():
    # رابط السيرفر الرياضي المحدث لايف لكأس العالم 2026
    api_url = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = { "X-Auth-Token": "مفتاح_الاشتراك_المجاني_الخاص_بك" }
    
    try:
        response = requests.get(api_url, headers=headers)
        data = response.json()
        
        # الكود يمر على كل مباراة انتهت ويحدث نتيجتها تلقائياً
        for match in data.get('matches', []):
            if match['status'] == 'FINISHED':
                match_desc = f"{match['homeTeam']['name']} × {match['awayTeam']['name']}"
                actual_home = match['score']['fullTime']['home']
                actual_away = match['score']['fullTime']['away']
                
                # هنا السستم يقارن النتيجة الفعلية بتوقعات الشباب ويوزع الـ 3 نقاط والـ 1 نقطة فوراً!
                calculate_group_points(match_desc, actual_home, actual_away)
    except:
        st.warning("جاري تحديث النتائج لايف من السيرفر...")

# عرض لوحة الترتيب العام للشباب في واجهة التطبيق
st.subheader("🏆 جدول الترتيب العام لقروب الحديقة 🏆")
# هنا يعرض السستم جدول تفاعلي مرتب من الأعلى للأقل نقاط تلقائياً