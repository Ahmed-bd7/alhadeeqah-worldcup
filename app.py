# 🌐 3. إعدادات الـ API الفنية المربوطة بمفتاحك وكأس العالم
API_KEY = "3a57379657b569a7a6abe3176fe85b10"  # مفتاح أحمد المعتمد
LEAGUE_ID = 1  # كود كأس العالم الرسمي
CURRENT_YEAR = 2026  # جرب تغييرها إلى 2024 أو 2025 إذا لم تظهر مباريات المجموعات فوراً

@st.cache_data(ttl=300)  # تحديث ذكي كل 5 دقائق
def fetch_matches_from_api(api_key, league_id, year):
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    # محاولة جلب مباريات البطولة
    for season in [year, year-1, year-2]: # يبحث في المواسم القريبة للتأكد من مطابقة تصنيف الفيفا بالـ API
        try:
            params = {'league': league_id, 'season': season}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()
            
            if "response" in data and len(data["response"]) > 0:
                fetched_matches = []
                for item in data["response"]:
                    fixture = item["fixture"]
                    teams = item["teams"]
                    
                    # تحويل وقت الفيفا العالمي (UTC) إلى توقيت المملكة (KSA) أوتوماتيكياً
                    utc_time = datetime.strptime(fixture["date"], "%Y-%m-%dT%H:%M:%S%z")
                    ksa_time = utc_time.astimezone(ksa_tz)
                    
                    fetched_matches.append({
                        "id": fixture["id"],
                        "team_home": teams["home"]["name"],
                        "team_away": teams["away"]["name"],
                        "time": ksa_time
                    })
                fetched_matches.sort(key=lambda x: x["time"])
                return fetched_matches
        except:
            continue
            
    # إذا فشلت كل المحاولات يرجع للجدول الاحتياطي المؤقت
    return [
        {"id": 901, "team_home": "المكسيك (احتياطي)", "team_away": "جنوب أفريقيا", "time": datetime(2026, 6, 11, 22, 0, tzinfo=ksa_tz)},
        {"id": 902, "team_home": "السعودية (احتياطي)", "team_away": "كندا", "time": datetime(2026, 6, 16, 1, 0, tzinfo=ksa_tz)}
    ]

matches = fetch_matches_from_api(API_KEY, LEAGUE_ID, CURRENT_YEAR)
