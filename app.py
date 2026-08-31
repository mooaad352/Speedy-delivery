import streamlit as st
import urllib.parse
from datetime import datetime, timezone, timedelta
import pandas as pd
import os
import json
from io import BytesIO

st.set_page_config(page_title="Speedy Delivery - מערכת ניהול משלוחים", page_icon="🚚", layout="wide")

ISRAEL_OFFSET = timedelta(hours=2)
ADMIN_PHONE = "972502616375"
CONTRACTS_FILE = "delivery_drivers_contracts.csv"
USERS_FILE = "couriers_db.json"

def get_israel_time():
    return datetime.now(timezone(ISRAEL_OFFSET)).strftime("%Y-%m-%d %H:%M")

def format_whatsapp_phone(phone_str):
    clean_phone = "".join(filter(str.isdigit, str(phone_str)))
    if clean_phone.startswith("0"):
        clean_phone = "972" + clean_phone[1:]
    elif not clean_phone.startswith("972") and len(clean_phone) > 0:
        clean_phone = "972" + clean_phone
    return clean_phone

DEFAULT_USERS = {
    "Admin": {"password": "Sma.srablove2028", "role": "מנהל מערכת ראשי (Super Admin)", "phone": ADMIN_PHONE, "company": "System", "contract_signed": True},
    "mohammad": {"password": "123", "role": "שליח", "phone": "972502616375", "company": "Independent", "contract_signed": True}
}

def load_users_db():
    users = DEFAULT_USERS.copy()
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    users.update(data)
        except Exception:
            pass
    
    users["Admin"] = {
        "password": "Sma.srablove2028", 
        "role": "מנהל מערכת ראשי (Super Admin)", 
        "phone": ADMIN_PHONE, 
        "company": "System", 
        "contract_signed": True
    }
    return users

def save_users_db(users_dict):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_dict, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

def load_contracts_data():
    if os.path.exists(CONTRACTS_FILE):
        try:
            df = pd.read_csv(CONTRACTS_FILE)
            if df is not None and not df.empty:
                return df
        except Exception:
            pass
    return pd.DataFrame(columns=["שם משתמש", "תפקיד", "חברה", "שם מלא", "ת.ז", "כתובת", "אימייל", "טלפון", "ח.פ / עוסק פטור", "תאריך רישום"])

def save_contracts_data(df):
    try:
        df.to_csv(CONTRACTS_FILE, index=False, encoding="utf-8-sig")
    except Exception:
        pass

if "couriers_db" not in st.session_state:
    st.session_state.couriers_db = load_users_db()
else:
    st.session_state.couriers_db["Admin"]["password"] = "Sma.srablove2028"
    st.session_state.couriers_db["Admin"]["role"] = "מנהל מערכת ראשי (Super Admin)"

if "saved_routes" not in st.session_state:
    st.session_state.saved_routes = {}

if "deliveries" not in st.session_state:
    st.session_state.deliveries = [{
        "ברקוד": "TEST-001", "שם לקוח": "סמר שומרי", "שם חברה": "SHEIN", "טלפון": "972502616375",
        "כביש": "רחוב ראשי", "מספר בית": "10", "קומה": "2", "עיר": "כסרא-סמיע", "הערות": "משלוח בדיקה", "status": "ממתין",
        "courier": "mohammad", "company": "Independent", "date": get_israel_time()
    }]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.company = ""

TRANSLATIONS = {
    "עברית (Hebrew)": {
        "title": "🚚 מערכת ניהול וסידור משלוחים מהירה",
        "login_title": "כניסת משתמשים ושליחים",
        "username": "שם משתמש",
        "password": "סיסמה",
        "login_btn": "התחבר למערכת",
        "login_error": "שם משתמש או סיסמה שגויים.",
        "logout": "התנתק (Logout)",
        "admin_menu": "תפריט ניהול ראשי",
        "main_sys": "מערכת משלוחים ראשית",
        "smart_route": "🗺️ סידור מסלול משלוחים (אוטומטי וידני)",
        "add_delivery": "➕ הוספת משלוח חדש",
        "add_courier": "הוספת שליח חדש",
        "add_company_admin": "הוספת מנהל חברת משלוחים",
        "manage_users": "ניהול סיסמאות ומשתמשים",
        "platform_profits": "💰 דוח עמדות והכנסות פלטפורמה (1 ₪ למשלוח)",
        "contract_menu": "📝 פנקס נרשמים וחוזים שמורים",
        "change_password": "🔐 החלפת סיסמה אישית",
        "whatsapp_btn": "📲 שלח וואטסאפ ללקוח",
        "waze_btn": "🧭 נווט ב-Waze",
        "mark_delivered": "סמן כנמסר",
        "delivered_success": "הסטטוס עודכן בהצלחה!"
    },
    "العربية (Arabic)": {
        "title": "🚚 نظام إدارة وتوصيل الشحنات السريع",
        "login_title": "تسجيل دخول المستخدمين والمندوبين",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_btn": "تسجيل الدخول",
        "login_error": "خطأ في اسم المستخدم أو كلمة المرور.",
        "logout": "تسجيل الخروج",
        "admin_menu": "قائمة الإدارة الرئيسية",
        "main_sys": "نظام الشحنات الرئيسي",
        "smart_route": "🗺️ ترتيب مسار الشحنات (تلقائي ويدوي)",
        "add_delivery": "➕ إضافة شحنة جديدة",
        "add_courier": "إضافة مندوب جديد",
        "add_company_admin": "إضافة مدير شركة توصيل",
        "manage_users": "إدارة كلمات المرور والمستخدمين",
        "platform_profits": "💰 تقرير أرباح المنصة (1 شيكل لكل شحنة)",
        "contract_menu": "📝 سجل العقود والبيانات المسجلة",
        "change_password": "🔐 تغيير كلمة المرور الشخصية",
        "whatsapp_btn": "📲 إرسال واتساب",
        "waze_btn": "🧭 التنقل عبر Waze",
        "mark_delivered": "تحديد كـ تم التسليم",
        "delivered_success": "تم تحديث الحالة بنجاح!"
    }
}

st.sidebar.markdown("---")
lang_choice = st.sidebar.selectbox("🌐 Language / שפה", ["עברית (Hebrew)", "العربية (Arabic)"], index=0)
t = TRANSLATIONS[lang_choice]

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.company = ""
    st.rerun()

if not st.session_state.logged_in:
    st.title(t["title"])
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader(t["login_title"])
        with st.form("login_form"):
            username_input = st.text_input(t["username"])
            password_input = st.text_input(t["password"], type="password")
            submit_btn = st.form_submit_button(t["login_btn"], use_container_width=True)
            
            if submit_btn:
                db = st.session_state.couriers_db
                matched_user = None
                for u_key in db.keys():
                    if u_key.lower() == username_input.strip().lower():
                        matched_user = u_key
                        break
                
                if matched_user and str(db[matched_user].get("password", "")) == str(password_input.strip()):
                    st.session_state.logged_in = True
                    st.session_state.username = matched_user
                    st.session_state.role = db[matched_user].get("role", "שליח")
                    st.session_state.company = db[matched_user].get("company", "Independent")
                    st.rerun()
                else:
                    st.error(t["login_error"])

elif st.session_state.role == "מנהל מערכת ראשי (Super Admin)":
    st.sidebar.title("מנהל ראשי (הפלטפורמה)")
    admin_menu = st.sidebar.radio(
        t["admin_menu"], 
        [
            t["main_sys"], 
            t["smart_route"],
            t["add_delivery"],
            t["add_company_admin"],
            t["add_courier"], 
            t["manage_users"],
            t["platform_profits"],
            t["contract_menu"],
            t["change_password"]
        ]
    )
    if st.sidebar.button(t["logout"]):
        logout_user()

    if admin_menu == t["main_sys"]:
        st.title(t["main_sys"])
        admin_deliveries = st.session_state.deliveries
        
        total_delivered_count = len([d for d in admin_deliveries if d.get("status") == "נמסר"])
        my_platform_revenue = total_delivered_count * 1.00

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("סך הכל משלוחים במערכת", len(admin_deliveries))
        col2.metric("פעילים / ממתינים", len([d for d in admin_deliveries if d.get("status") not in ["נמסר", "סורב על ידי הלקוח"]]))
        col3.metric("נמסרו בהצלחה", total_delivered_count)
        col4.metric("💰 הרווח שלך (לפני מע״מ)", f"{my_platform_revenue:,.2f} ₪")
        
        st.divider()
        for idx, item in enumerate(admin_deliveries):
            status_color = "🟢" if item.get("status") == "נמסר" else ("🔴" if "סורב" in item.get("status", "") else "🟠")
            full_address_str = f"כביש/רחוב: {item.get('כביש', '-')}, בית: {item.get('מספר בית', '-')}, קומה: {item.get('קומה', '-')}, יישוב: {item.get('עיר', '-')}"
            
            with st.expander(f"{status_color} 📦 {item.get('שם לקוח', '')} | {item.get('עיר', '')} | סטטוס: {item.get('status', '')}"):
                st.write(f"**ברקוד:** {item.get('ברקוד', '')} | **חברה/מותג:** {item.get('שם חברה', 'General')} | **טלפון:** {item.get('טלפון', '')}")
                st.write(f"**כתובת:** {full_address_str}")
                
                c_phone = format_whatsapp_phone(item.get('טלפון', ''))
                company_name = item.get('שם חברה', 'General')
                wa_msg = urllib.parse.quote(f"שלום לך, השליח של חברת {company_name} בדרך אליך! אנא הישאר זמין לקבל את המשלוח.")
                wa_link = f"https://wa.me/{c_phone}?text={wa_msg}"
                waze_query = urllib.parse.quote(f"{item.get('כביש', '')} {item.get('מספר בית', '')}, {item.get('עיר', '')}")
                waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                
                b1, b2, b3 = st.columns(3)
                with b1:
                    st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["whatsapp_btn"]}</button></a>', unsafe_allow_html=True)
                with b2:
                    st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["waze_btn"]}</button></a>', unsafe_allow_html=True)
                with b3:
                    if st.button(t["mark_delivered"], key=f"adm_m_{idx}"):
                        item["status"] = "נמסר"
                        st.success(t["delivered_success"])
                        st.rerun()

    elif admin_menu == t["smart_route"]:
        st.title(t["smart_route"])
        couriers_list = [u for u, i in st.session_state.couriers_db.items() if i.get("role") == "שליח"]
        selected_courier_route = st.selectbox("בחר שליח לסידור מסלול:", couriers_list if couriers_list else ["אין שליחים"])
        
        courier_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == selected_courier_route and d.get("status") not in ["נמסר", "סורב על ידי הלקוח"]] if couriers_list else []
        
        if not courier_deliveries:
            st.info("אין משלוחים פעילים לשליח זה.")
        else:
            tab_auto, tab_manual = st.tabs(["🚀 סידור אוטומטי חכם", "✏️ סידור ידני לפי בחירתך (גרירה/מספור)"])
            
            with tab_auto:
                all_cities = list(set([d.get("עיר", "אחר") for d in courier_deliveries]))
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    start_location = st.selectbox("📍 בחר נקודת התחלה (מוצא):", all_cities, key="adm_start_loc")
                with col_s2:
                    end_location = st.selectbox("🏁 בחר נקודת סיום (יעד סופי):", all_cities, key="adm_end_loc")
                
                if st.button("🚀 הפעל סידור אוטומטי של המסלול"):
                    remaining = [d for d in courier_deliveries if d.get("עיר") != end_location]
                    end_items = [d for d in courier_deliveries if d.get("עיר") == end_location]
                    
                    sorted_route = []
                    current_point = start_location
                    
                    while remaining:
                        next_item = min(remaining, key=lambda x: 0 if x.get("עיר") == current_point else len(str(x.get("עיר"))))
                        sorted_route.append(next_item)
                        current_point = next_item.get("עיר")
                        remaining.remove(next_item)
                    
                    sorted_route.extend(end_items)
                    st.session_state.saved_routes[selected_courier_route] = sorted_route
                    st.success("✅ המסלול סודר ונשמר בהצלחה!")

            with tab_manual:
                st.markdown("### ✏️ קביעת מספר סידורי ידני לכל משלוח (מיקום בתור):")
                st.info("הזן לכל משלוח את מספר התחנה הרצוי (למשל: 1 לתחנה ראשונה, 2 לשנייה וכו').")
                
                if selected_courier_route not in st.session_state.saved_routes or len(st.session_state.saved_routes[selected_courier_route]) != len(courier_deliveries):
                    st.session_state.saved_routes[selected_courier_route] = list(courier_deliveries)

                current_route_items = st.session_state.saved_routes[selected_courier_route]
                
                with st.form("manual_route_form"):
                    updated_orders = []
                    for idx, item in enumerate(current_route_items):
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            st.markdown(f"📦 **לקוח:** {item.get('שם לקוח', '')} | **כתובת:** {item.get('כביש', '')} {item.get('מספר בית', '')}, {item.get('עיר', '')} | **מותג:** {item.get('שם חברה', '')}")
                        with c2:
                            new_pos = st.number_input("מספר תחנה", min_value=1, max_value=len(current_route_items), value=idx+1, key=f"pos_{selected_courier_route}_{item.get('ברקוד', idx)}")
                        updated_orders.append((new_pos, item))
                        st.divider()
                    
                    if st.form_submit_button("💾 שמור סדר ידני מעודכן"):
                        updated_orders.sort(key=lambda x: x[0])
                        st.session_state.saved_routes[selected_courier_route] = [item[1] for item in updated_orders]
                        st.success("✅ המסלול הידני עודכן ונשמר בהצלחה!")
                        st.rerun()

            st.divider()
            st.markdown("### 📋 רשימת התחנות הסופית לשליח:")
            active_saved_route = st.session_state.saved_routes.get(selected_courier_route, courier_deliveries)
            for s_idx, s_item in enumerate(active_saved_route, 1):
                st.markdown(f"**תחנה {s_idx}. 📦 לקוח: {s_item.get('שם לקוח', '')} | מותג: {s_item.get('שם חברה', '')} | יישוב: {s_item.get('עיר', '')}**")
                waze_query = urllib.parse.quote(f"{s_item.get('כביש', '')} {s_item.get('מספר בית', '')}, {s_item.get('עיר', '')}")
                waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer;">🧭 נווט לתחנה ב-Waze</button></a>', unsafe_allow_html=True)
                st.divider()

    elif admin_menu == t["add_delivery"]:
        st.title(t["add_delivery"])
        with st.form("add_delivery_form"):
            d_barcode = st.text_input("ברקוד משלוח:", value=f"DEL-{int(datetime.now().timestamp())}")
            d_client = st.text_input("שם הלקוח:")
            d_company = st.text_input("שם חברה / מותג (לדוגמה: SHEIN, AliExpress, Amazon):", value="SHEIN")
            d_phone = st.text_input("טלפון הלקוח:")
            d_street = st.text_input("כביש / רחוב:")
            d_house = st.text_input("מספר בית:")
            d_floor = st.text_input("קומה:")
            d_city = st.text_input("עיר / יישוב:")
            d_notes = st.text_area("הערות:")
            couriers_list = [u for u, i in st.session_state.couriers_db.items() if i.get("role") == "שליח"]
            assigned_courier = st.selectbox("שיוך שליח:", couriers_list if couriers_list else ["אין שליחים"])
            
            if st.form_submit_button("הוסף משלוח למערכת 🚀") and d_client and d_phone and d_city:
                new_item = {
                    "ברקוד": d_barcode, "שם לקוח": d_client, "שם חברה": d_company if d_company else "General",
                    "טלפון": format_whatsapp_phone(d_phone), "כביש": d_street, "מספר בית": d_house, "קומה": d_floor, "עיר": d_city,
                    "הערות": d_notes, "status": "ממתין", "courier": assigned_courier, "company": "System", "date": get_israel_time()
                }
                st.session_state.deliveries.append(new_item)
                st.success("המשלוח נוסף בהצלחה!")

    elif admin_menu == t["add_company_admin"]:
        st.title(t["add_company_admin"])
        with st.form("add_comp_form"):
            cu = st.text_input("שם משתמש מנהל:")
            cp = st.text_input("סיסמה:", type="password")
            cn = st.text_input("שם חברה:")
            cph = st.text_input("טלפון:")
            if st.form_submit_button("הוסף מנהל חברה") and cu and cp and cn and cph:
                st.session_state.couriers_db[cu] = {"password": cp, "role": "מנהל חברה (Company Admin)", "phone": format_whatsapp_phone(cph), "company": cn, "contract_signed": True}
                save_users_db(st.session_state.couriers_db)
                st.success("מנהל החברה נוסף בהצלחה!")

    elif admin_menu == t["add_courier"]:
        st.title(t["add_courier"])
        with st.form("add_cour_form"):
            cu = st.text_input("שם משתמש שליח:")
            cp = st.text_input("סיסמה:", type="password")
            cph = st.text_input("טלפון:")
            comp_list = ["Independent"] + list(set([i.get("company") for u, i in st.session_state.couriers_db.items() if i.get("company") not in ["Independent", "System"]]))
            ccomp = st.selectbox("שיוך חברה:", comp_list)
            if st.form_submit_button("הוסף שליח") and cu and cp and cph:
                st.session_state.couriers_db[cu] = {"password": cp, "role": "שליח", "phone": format_whatsapp_phone(cph), "company": ccomp, "contract_signed": True}
                save_users_db(st.session_state.couriers_db)
                st.success("השליח נוסף בהצלחה!")

    elif admin_menu == t["manage_users"]:
        st.title("🔑 ניהול וצפייה בסיסמאות כל המשתמשים במערכת")
        for usr, info in list(st.session_state.couriers_db.items()):
            if usr == "Admin": 
                continue
            with st.expander(f"👤 {usr} | תפקיד: {info.get('role', '')} | חברה: {info.get('company', '')}"):
                st.markdown(f"**שם משתמש:** `{usr}`")
                st.markdown(f"**סיסמה נוכחית במערכת:** `{info.get('password', '')}`")
                st.markdown(f"**טלפון:** `{info.get('phone', '-')}`")
                
                with st.form(f"change_pwd_form_{usr}"):
                    new_admin_pwd = st.text_input("הגדר סיסמה חדשה למשתמש:", type="password", key=f"npwd_{usr}")
                    if st.form_submit_button("עדכן סיסמה"):
                        if new_admin_pwd.strip():
                            st.session_state.couriers_db[usr]["password"] = new_admin_pwd.strip()
                            save_users_db(st.session_state.couriers_db)
                            st.success(f"הסיסמה של {usr} עודכנה בהצלחה!")
                            st.rerun()
                
                if st.button(f"🗑️ מחק משתמש {usr}", key=f"del_usr_{usr}"):
                    del st.session_state.couriers_db[usr]
                    save_users_db(st.session_state.couriers_db)
                    st.warning("המשתמש נמחק.")
                    st.rerun()

    elif admin_menu == t["platform_profits"]:
        st.title(t["platform_profits"])
        st.markdown("### דוח רווחי פלטפורמה (חישוב עמלת שימוש: 1 ₪ לפני מע\"מ לכל משלוח שנמסר)")
        
        all_couriers = [u for u, i in st.session_state.couriers_db.items() if i.get("role") == "שליח"]
        
        report_data = []
        for c in all_couriers:
            delivered_by_courier = len([d for d in st.session_state.deliveries if d.get("courier") == c and d.get("status") == "נמסר"])
            fee_total = delivered_by_courier * 1.00
            report_data.append({
                "שם שליח/משתמש": c,
                "משלוחים שנמסרו": delivered_by_courier,
                "עמלה מגיעה לך (₪ לפני מע״מ)": f"{fee_total:,.2f} ₪"
            })
        
        if report_data:
            df_report = pd.DataFrame(report_data)
            st.table(df_report)
            
            total_all_delivered = sum([int(str(d.get("משלוחים שנמסרו", 0))) for d in report_data])
            total_all_revenue = total_all_delivered * 1.00
            st.metric("סך הכל הכנסות עמלות לך מכל השליחים (לפני מע״מ)", f"{total_all_revenue:,.2f} ₪")
            
            html_invoice = f"<h1>דוח עמדות פלטפורמה</h1><h3>סך הכל הכנסות: {total_all_revenue:,.2f} ₪ לפני מע״מ</h3>" + df_report.to_html(index=False)
            invoice_stream = BytesIO(html_invoice.encode("utf-8"))
            invoice_stream.seek(0)
            
            st.download_button(
                label="📥 הורד דוח הכנסות פלטפורמה (.html)",
                data=invoice_stream,
                file_name="platform_commission_report.html",
                mime="text/html"
            )
        else:
            st.info("אין עדיין נתונים להצגה.")

    elif admin_menu == t["contract_menu"]:
        st.title(t["contract_menu"])
        contracts_df = load_contracts_data()
        if contracts_df.empty:
            st.info("אין כרגע נרשמים שמורים במערכת.")
        else:
            st.dataframe(contracts_df)
            st.divider()
            st.subheader("🗑️ מחיקת נרשם או חוזה שמור")
            
            contract_options = []
            for idx, row in contracts_df.iterrows():
                display_label = f"שם: {row.get('שם מלא', 'לא ידוע')} | משתמש: {row.get('שם משתמש', '')} | טלפון: {row.get('טלפון', '')}"
                contract_options.append((idx, display_label))
            
            selected_to_delete = st.selectbox("בחר נרשם להסרה מהפנקס:", options=contract_options, format_func=lambda x: x[1])
            
            if st.button("🗑️ מחק נרשם נבחר לצמיתות", type="primary"):
                if selected_to_delete:
                    row_idx_to_drop = selected_to_delete[0]
                    contracts_df = contracts_df.drop(row_idx_to_drop).reset_index(drop=True)
                    save_contracts_data(contracts_df)
                    st.success("הנרשם נמחק בהצלחה מהפנקס!")
                    st.rerun()

    elif admin_menu == t["change_password"]:
        st.title(t["change_password"])
        with st.form("admin_change_pwd"):
            old_p = st.text_input("סיסמה נוכחית:", type="password")
            new_p = st.text_input("סיסמה חדשה:", type="password")
            if st.form_submit_button("עדכן סיסמה") and old_p == st.session_state.couriers_db["Admin"]["password"]:
                st.session_state.couriers_db["Admin"]["password"] = new_p
                save_users_db(st.session_state.couriers_db)
                st.success("הסיסמה עודכנה בהצלחה!")

else:
    my_username = st.session_state.username
    my_role = st.session_state.role
    my_company = st.session_state.company

    if my_role == "שליח":
        st.sidebar.title(f"שליח: {my_username}")
        courier_menu = st.sidebar.radio("תפריט שליח", ["📦 המשלוחים שלי", "🗺️ סידור מסלול אישי", "➕ הוספת משלוח", "🔐 החלפת סיסמה"])
        if st.sidebar.button(t["logout"]):
            logout_user()

        my_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == my_username]

        if courier_menu == "📦 המשלוחים שלי":
            st.title("📦 המשלוחים המוקצים אליך")
            if not my_deliveries:
                st.info("אין לך משלוחים מוקצים כרגע.")
            for idx, item in enumerate(my_deliveries):
                status_color = "🟢" if item.get("status") == "נמסר" else "🟠"
                with st.expander(f"{status_color} 📦 לקוח: {item.get('שם לקוח', '')} | מותג: {item.get('שם חברה', '')} | עיר: {item.get('עיר', '')} | סטטוס: {item.get('status', '')}"):
                    st.write(f"**ברקוד:** {item.get('ברקוד', '')} | **חברה/מותג:** {item.get('שם חברה', 'General')} | **טלפון:** {item.get('טלפון', '')}")
                    st.write(f"**כתובת:** {item.get('כביש', '')} {item.get('מספר בית', '')}, קומה {item.get('קומה', '-')}, {item.get('עיר', '')}")
                    
                    c_phone = format_whatsapp_phone(item.get('טלפון', ''))
                    company_name = item.get('שם חברה', 'General')
                    wa_msg = urllib.parse.quote(f"שלום לך, השליח של חברת {company_name} בדרך אליך! אנא הישאר זמין לקבל את המשלוח.")
                    wa_link = f"https://wa.me/{c_phone}?text={wa_msg}"
                    
                    waze_query = urllib.parse.quote(f"{item.get('כביש', '')} {item.get('מספר בית', '')}, {item.get('עיר', '')}")
                    waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                    
                    b1, b2, b3 = st.columns(3)
                    with b1:
                        st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["whatsapp_btn"]}</button></a>', unsafe_allow_html=True)
                    with b2:
                        st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["waze_btn"]}</button></a>', unsafe_allow_html=True)
                    with b3:
                        if st.button(t["mark_delivered"], key=f"cour_m_{idx}"):
                            item["status"] = "נמסר"
                            st.success(t["delivered_success"])
                            st.rerun()

        elif courier_menu == "🗺️ סידור מסלול אישי":
            st.title("🗺️ סידור מסלול משלוחים אישי לשליח")
            active_my_deliveries = [d for d in my_deliveries if d.get("status") not in ["נמסר", "סורב על ידי הלקוח"]]
            
            if not active_my_deliveries:
                st.info("אין לך משלוחים פעילים לסידור מסלול.")
            else:
                tab_auto, tab_manual = st.tabs(["🚀 סידור אוטומטי", "✏️ סידור ידני לפי בחירתך"])
                
                with tab_auto:
                    all_cities = list(set([d.get("עיר", "אחר") for d in active_my_deliveries]))
                    col_s1, col_s2 = st.columns(2)
                    with col_s1:
                        start_location = st.selectbox("📍 נקודת התחלה (מוצא):", all_cities, key="cour_start_loc")
                    with col_s2:
                        end_location = st.selectbox("🏁 נקודת סיום (יעד סופי):", all_cities, key="cour_end_loc")
                    
                    if st.button("🚀 סדר לי את המסלול באופן אוטומטי"):
                        remaining = [d for d in active_my_deliveries if d.get("עיר") != end_location]
                        end_items = [d for d in active_my_deliveries if d.get("עיר") == end_location]
                        
                        sorted_route = []
                        current_point = start_location
                        
                        while remaining:
                            next_item = min(remaining, key=lambda x: 0 if x.get("עיר") == current_point else len(str(x.get("עיר"))))
                            sorted_route.append(next_item)
                            current_point = next_item.get("עיר")
                            remaining.remove(next_item)
                        
                        sorted_route.extend(end_items)
                        st.session_state.saved_routes[my_username] = sorted_route
                        st.success("✅ המסלול סודר אוטומטית בהצלחה!")

                with tab_manual:
                    st.markdown("### ✏️ סידור ידני של התחנות:")
                    if my_username not in st.session_state.saved_routes or len(st.session_state.saved_routes[my_username]) != len(active_my_deliveries):
                        st.session_state.saved_routes[my_username] = list(active_my_deliveries)

                    current_my_route = st.session_state.saved_routes[my_username]

                    with st.form("courier_manual_route_form"):
                        updated_my_orders = []
                        for idx, item in enumerate(current_my_route):
                            c1, c2 = st.columns([3, 1])
                            with c1:
                                st.markdown(f"📦 **לקוח:** {item.get('שם לקוח', '')} | **כתובת:** {item.get('כביש', '')} {item.get('מספר בית', '')}, {item.get('עיר', '')}")
                            with c2:
                                new_pos = st.number_input("מספר תחנה", min_value=1, max_value=len(current_my_route), value=idx+1, key=f"c_pos_{item.get('ברקוד', idx)}")
                            updated_my_orders.append((new_pos, item))
                            st.divider()

                        if st.form_submit_button("💾 שמור את הסידור הידני"):
                            updated_my_orders.sort(key=lambda x: x[0])
                            st.session_state.saved_routes[my_username] = [item[1] for item in updated_my_orders]
                            st.success("✅ המסלול הידני שלך עודכן בהצלחה!")
                            st.rerun()

                st.divider()
                st.markdown("### המסלול שלך לפי סדר תחנות:")
                current_saved_route = st.session_state.saved_routes.get(my_username, active_my_deliveries)
                for s_idx, s_item in enumerate(current_saved_route, 1):
                    st.markdown(f"**תחנה {s_idx}. 📦 לקוח: {s_item.get('שם לקוח', '')} | מותג: {s_item.get('שם חברה', '')} | יישוב: {s_item.get('עיר', '')}**")
                    waze_query = urllib.parse.quote(f"{s_item.get('כביש', '')} {s_item.get('מספר בית', '')}, {s_item.get('עיר', '')}")
                    waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                    st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:6px 12px; border-radius:5px; cursor:pointer;">🧭 נווט לתחנה זו ב-Waze</button></a>', unsafe_allow_html=True)
                    st.divider()

        elif courier_menu == "➕ הוספת משלוח":
            st.title("➕ הוספת משלוח חדש")
            with st.form("cour_add"):
                d_client = st.text_input("שם לקוח")
                d_company = st.text_input("שם חברה / מותג (לדוגמה: SHEIN, ALIEXPRESS)", value=my_company)
                d_phone = st.text_input("טלפון")
                d_street = st.text_input("כביש / רחוב")
                d_house = st.text_input("מספר בית")
                d_city = st.text_input("עיר")
                if st.form_submit_button("הוסף משלוח") and d_client and d_phone and d_city:
                    st.session_state.deliveries.append({
                        "ברקוד": f"DEL-{int(datetime.now().timestamp())}", "שם לקוח": d_client, "שם חברה": d_company if d_company else my_company,
                        "טלפון": format_whatsapp_phone(d_phone), "כביש": d_street, "מספר בית": d_house, "עיר": d_city, "status": "ממתין", "courier": my_username, "company": my_company, "date": get_israel_time()
                    })
                    st.success("המשלוח נוסף בהצלחה!")

        elif courier_menu == "🔐 החלפת סיסמה":
            st.title("🔐 החלפת סיסמה אישית")
            with st.form("c_pwd"):
                old_p = st.text_input("סיסמה נוכחית", type="password")
                new_p = st.text_input("סיסמה חדשה", type="password")
                if st.form_submit_button("עדכן סיסמה") and old_p == st.session_state.couriers_db.get(my_username, {}).get("password", ""):
                    st.session_state.couriers_db[my_username]["password"] = new_p
                    save_users_db(st.session_state.couriers_db)
                    st.success("הסיסמה עודכנה בהצלחה!")
