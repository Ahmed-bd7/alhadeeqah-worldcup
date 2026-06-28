    # --- 4. لوحة الإدارة الفاخرة والآمنة (أحمد بادحمان) ---
    if login_phone == ADMIN_PHONE:
        with tabs[3]:
            st.markdown('<div class="admin-card">⚙️ <b>لوحة المشرف العام (أحمد بادحمان)</b></div>', unsafe_allow_html=True)
            cursor = db_conn.cursor()
            
            # ---------------- كشف بيانات الأعضاء وتعديل نقاطهم (الكونسبت القديم) ----------------
            st.markdown("<h3 style='color:#FFD700;'>👥 إدارة الحسابات والأعضاء</h3>", unsafe_allow_html=True)
            
            cursor.execute("SELECT name, phone, password, points FROM users ORDER BY points DESC")
            admin_users_data = cursor.fetchall()
            
            for idx, u_row in enumerate(admin_users_data):
                u_name, u_phone, u_pass, u_points = u_row
                
                # استخدام الـ Expander المألوف لك لعرض البيانات بشكل منظم ونظيف
                with st.expander(f"👤 {u_name} — (🏆 {u_points} نقطة)"):
                    st.markdown(f"""
                    * **رقم الجوال:** `{u_phone}`
                    * **كلمة المرور:** `{u_pass}`
                    * **النقاط الحالية:** `{u_points}`
                    """, unsafe_allow_html=True)
                    
                    # أزرار التحكم السريع بالنقاط لكل مستخدم بشكل منفصل
                    col_add, col_sub = st.columns(2)
                    with col_add:
                        if st.button(f"➕ إضافة 5 نقاط لـ {u_name}", key=f"add_5_{u_phone}_{idx}"):
                            cursor.execute("UPDATE users SET points = points + 5 WHERE phone = ?", (u_phone,))
                            db_conn.commit()
                            st.success(f"تم إضافة 5 نقاط لـ {u_name}")
                            st.rerun()
                    with col_sub:
                        if st.button(f"➖ خصم 5 نقاط من {u_name}", key=f"sub_5_{u_phone}_{idx}"):
                            cursor.execute("UPDATE users SET points = MAX(0, points - 5 WHERE phone = ?", (u_phone,))
                            db_conn.commit()
                            st.success(f"تم خصم 5 نقاط من {u_name}")
                            st.rerun()
            
            st.markdown("<hr style='border: 1px dashed rgba(255,215,0,0.15); margin: 25px 0;'>", unsafe_allow_html=True)

            # ---------------- احتساب نتائج المباريات وحسم النقاط ----------------
            st.markdown("<h3 style='color:#FFD700;'>🧮 إدخال واحتساب نتائج المباريات</h3>", unsafe_allow_html=True)
            match_options = {f"{m['team_home']} × {m['team_away']}": m for m in all_matches}
            selected_match_str = st.selectbox("اختر مباراة لحسم نقاطها:", list(match_options.keys()))
            selected_match = match_options[selected_match_str]
            
            cursor.execute("SELECT actual_home, actual_away, actual_pens_winner FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
            already_calculated = cursor.fetchone()
            is_valid_old_result = already_calculated and already_calculated[0] is not None
            
            if is_valid_old_result:
                st.warning(f"المباراة محسومة سابقاً بنتيجة: {already_calculated[0]} - {already_calculated[1]}")
                if st.button("🚨 إلغاء النتيجة وسحب النقاط من الأعضاء"):
                    cursor.execute("SELECT phone, pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE match_id = ?", (selected_match["id"],))
                    for pred in cursor.fetchall():
                        old_points = calculate_match_points(pred[1], pred[2], pred[3], already_calculated[0], already_calculated[1], already_calculated[2], selected_match["is_knockout"])
                        if pred[4] == 1: old_points *= 2
                        if old_points > 0: cursor.execute("UPDATE users SET points = MAX(0, points - ?) WHERE phone = ?", (old_points, pred[0]))
                    cursor.execute("DELETE FROM processed_matches WHERE match_id = ?", (selected_match["id"],))
                    db_conn.commit()
                    st.rerun()
            
            c_act_h, c_act_a = st.columns(2)
            with c_act_h: actual_h = st.number_input("أهداف المستضيف الفعلي", 0, 10, value=already_calculated[0] if is_valid_old_result else 0)
            with c_act_a: actual_a = st.number_input("أهداف الضيف الفعلي", 0, 10, value=already_calculated[1] if is_valid_old_result else 0)
            
            actual_p = None
            if selected_match["is_knockout"] and actual_h == actual_a:
                actual_p = st.radio("الفائز الفعلي بالبنتيات:", [selected_match['team_home'], selected_match['team_away']])
            
            if st.button("🔥 حسم النقاط وتحديث الصدارة"):
                cursor.execute("SELECT phone, pred_home, pred_away, pred_pens_winner, is_joker FROM predictions WHERE match_id = ?", (selected_match["id"],))
                for pred in cursor.fetchall():
                    pts = calculate_match_points(pred[1], pred[2], pred[3], actual_h, actual_a, actual_p, selected_match["is_knockout"])
                    if pred[4] == 1: pts *= 2
                    if pts > 0: cursor.execute("UPDATE users SET points = points + ? WHERE phone = ?", (pts, pred[0]))
                cursor.execute('INSERT INTO processed_matches (match_id, actual_home, actual_away, actual_pens_winner) VALUES (?, ?, ?, ?)', (selected_match["id"], actual_h, actual_a, actual_p))
                db_conn.commit()
                st.success("تم تحديث وحسم ترتيب لوحة الصدارة الملكية!")
                st.rerun()
