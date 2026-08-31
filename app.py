import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import json
import os

# --- הגדרות בסיסיות של העמוד ---
st.set_page_config(page_title="Speedy Delivery System", page_icon="🚚", layout="wide")

# --- פונקציות עזר לזמן ופורמטים ---
def get_israel_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_whatsapp_phone(phone_str):
    if not phone_str:
        return ""
    clean_p = "".join(filter(str.isdigit, phone_str))
    if clean_p.startswith("0"):
        clean_p = "972" + clean_p[1:]
    return clean_p

# --- מילון שפות (תמיכה בעברית, אנגלית וערבית) ---
TRANSLATIONS = {
    "Hebrew": {
        "title": "מערכת ניהול משלוחים מתקדמת",
        "login": "התחברות למערכת",
        "username": "שם משתמש",
        "password": "סיסמה",
        "login_btn": "התחבר",
        "logout": "התנתק מהמערכת",
        "main_sys": "ניהול משלוחים ראשי",
        "smart_route": "מסלול חכם (אופטימיזציה)",
        "add_delivery": "הוספת משלוח חדש",
        "monthly_report": "דוח חודשי וחשבוניות",
        "change_password": "שינוי סיסמה",
        "whatsapp_btn": "שלח הודעת וואטסאפ ללקוח",
        "waze_btn": "נווט עם Waze",
        "mark_delivered": "סמן כנמסר ✅",
        "delivered_success": "המשלוח עודכן בהצלחה כנמסר!",
        "add_courier": "הוסף שליח חדש",
        "active_users": "צפייה במשתמשים מחוברים"
    },
    "English": {
        "title": "Advanced Delivery Management System",
        "login": "System Login",
        "username": "Username",
        "password": "Password",
        "login_btn": "Login",
        "logout": "Logout",
        "main_sys": "Main Deliveries",
        "smart_route": "Smart Route (Optimization)",
        "add_delivery": "Add New Delivery",
        "monthly_report": "Monthly Report & Invoices",
        "change_password": "Change Password",
        "whatsapp_btn": "WhatsApp Client",
        "waze_btn": "Navigate with Waze",
        "mark_delivered": "Mark as Delivered ✅",
        "delivered_success": "Delivery successfully marked as delivered!",
        "add_courier": "Add New Courier",
        "active_users": "Active Users Monitor"
    }
}

# בחירת שפה בברירת מחדל
lang = st.sidebar.selectbox("Language / שפה", ["Hebrew", "English"])
t = TRANSLATIONS[lang]

# --- ניהול Session State (בדיקת נתונים ראשונית) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "company" not in st.session_state:
    st.session_state.company = ""
if "deliveries" not in st.session_state:
    st.session_state.deliveries = []
if "couriers_db" not in st.session_state:
    # משתמשים ראשוניים לדוגמה במערכת
    st.session_state.couriers_db = {
        "admin": {"password": "admin", "role": "מנהל ראשי", "phone": "972500000000", "company": "System"},
        "company1": {"password": "123", "role": "מנהל חברה", "phone": "972511111111", "company": "חברת שליחויות א"},
        "courier1": {"password": "123", "role": "שליח", "phone": "972522222222", "company": "חברת שליחויות א"}
    }
if "active_sessions" not in st.session_state:
    st.session_state.active_sessions = {}

def save_users_db(db):
    pass

def save_location_data(username, loc):
    pass

def generate_monthly_invoice_html(u_name, u_hp, is_exempt, count, price):
    html_content = f"<html><body><h1>Invoice for {u_name}</h1><p>Total Deliveries: {count}</p><p>Total Amount: {count * price} NIS</p></body></html>"
    return html_content.encode("utf-8")

def logout_user():
    if st.session_state.username in st.session_state.active_sessions:
        del st.session_state.active_sessions[st.session_state.username]
    st.session_state.logged_in = False
    format_whatsapp_phone("")
    st.rerun()

# --- מסך התחברות ---
if not st.session_state.logged_in:
    st.title(t["login"])
    with st.form("login_form"):
        u_input = st.text_input(t["username"])
        p_input = st.text_input(t["password"], type="password")
        submit_login = st.form_submit_button(t["login_btn"])
        
        if submit_login:
            if u_input in st.session_state.couriers_db and st.session_state.couriers_db[u_input]["password"] == p_input:
                st.session_state.logged_in = True
                st.session_state.username = u_input
                st.session_state.role = st.session_state.couriers_db[u_input]["role"]
                st.session_state.company = st.session_state.couriers_db[u_input]["company"]
                # רישום המשתמש כמחובר פעיל במערכת
                st.session_state.active_sessions[u_input] = {
                    "role": st.session_state.role,
                    "company": st.session_state.company,
                    "login_time": get_israel_time()
                }
                st.success("התחברת בהצלחה!")
                st.rerun()
            else:
                st.error("שם משתמש או סיסמה שגויים.")
    st.stop()

# ==========================================
# אזור מנהל ראשי (Admin)
# ==========================================
if st.session_state.role == "מנהל ראשי":
    st.sidebar.title("פאנל מנהל ראשי")
    admin_menu = st.sidebar.radio("תפריט מנהל ראשי", [t["main_sys"], t["active_users"], t["add_courier"], t["change_password"]])
    if st.sidebar.button(t["logout"]):
        logout_user()

    if admin_menu == t["active_users"]:
        st.title("👥 משתמשים מחוברים כעת למערכת (כללי)")
        if not st.session_state.active_sessions:
            st.info("אין משתמשים מחוברים כרגע.")
        else:
            for usr, details in st.session_state.active_sessions.items():
                st.markdown(f"🟢 **משתמש:** {usr} | **תפקיד:** {details.get('role')} | **חברה:** {details.get('company')} | **התחבר ב:** {details.get('login_time')}")

    elif admin_menu == t["main_sys"]:
        st.title("📋 כל המשלוחים במערכת (מנהל ראשי)")
        # כאן יוצגו כלל המשלוחים של המערכת...
        st.info("צפייה וניהול של כלל משלוחי החברות במערכת.")

    elif admin_menu == t["add_courier"]:
        st.title("הוספת משתמש/חברה חדשה")
        # טופס הוספה...

# ==========================================
# אזור מנהל חברה (Company Admin)
# ==========================================
elif st.session_state.role == "מנהל חברה":
    st.sidebar.title(f"ניהול חברה: {st.session_state.company}")
    comp_admin_menu = st.sidebar.radio(
        "תפריט מנהל חברה",
        [
            t["main_sys"],
            t["smart_route"],
            t["add_delivery"],
            t["active_users"], # הוספת זיהוי מחוברים השייכים לחברה
            t["add_courier"],
            "👥 ניהול השליחים שלי",
            t["monthly_report"],
            "📍 עדכן את המיקום החי שלי (GPS)",
            t["change_password"]
        ]
    )
    if st.sidebar.button(t["logout"]):
        logout_user()

    if comp_admin_menu == t["active_users"]:
        st.title("👥 השליחים והעובדים המחוברים לחברה שלי")
        my_company = st.session_state.company
        company_active = {u: d for u, d in st.session_state.active_sessions.items() if d.get("company") == my_company or u == st.session_state.username}
        if not company_active:
            st.info("אין כרגע שליחים מחוברים מהחברה שלך.")
        else:
            for usr, details in company_active.items():
                st.markdown(f"🟢 **שליח/משתמש:** {usr} | **תפקיד:** {details.get('role')} | **זמן התחברות:** {details.get('login_time')}")

    elif comp_admin_menu == t["main_sys"]:
        st.title(f"📦 משלוחי חברת {st.session_state.company}")
        my_company_deliveries = [d for d in st.session_state.deliveries if d.get("company") == st.session_state.company]
        
        if not my_company_deliveries:
            st.info("אין משלוחים פעילים לחברה שלך כרגע.")
        else:
            for idx, item in enumerate(my_company_deliveries):
                status_color = "🟢" if item.get("status") == "נמסר" else ("🔴" if "סורב" in item.get("status", "") else "🟠")
                full_address_str = f"כביש/רחוב: {item.get('כביש', '-')}, בית: {item.get('מספר בית', '-')}, קומה: {item.get('קומה', '-')}, יישוב/כפר: {item.get('עיר', '-')}"
                
                with st.expander(f"{status_color} 📦 לקוח: {item.get('שם לקוח', '')} | שליח מבצע: {item.get('courier', '')} | סטטוס: {item.get('status', '')}"):
                    st.write(f"**ברקוד:** {item.get('ברקוד', '')} | **טלפון:** {item.get('טלפון', '')} | **כתובת:** {full_address_str} | **הערות:** {item.get('הערות', 'אין')}")
                    
                    c_phone = format_whatsapp_phone(item.get('טלפון', ''))
                    wa_msg = urllib.parse.quote(f"שלום {item.get('שם לקוח', '')}, אני השליח בדרך אליך! יש לי משלוח מ{item.get('שם חברה', '')}.")
                    wa_link = f"https://wa.me/{c_phone}?text={wa_msg}"
                    waze_query = urllib.parse.quote(f"{item.get('כביש', '')} {item.get('מספר בית', '')}, {item.get('עיר', '')}")
                    waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                    
                    b1, b2, b3, b4, b5 = st.columns(5)
                    with b1:
                        st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["whatsapp_btn"]}</button></a>', unsafe_allow_html=True)
                    with b2:
                        st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["waze_btn"]}</button></a>', unsafe_allow_html=True)
                    with b3:
                        if st.button(t["mark_delivered"], key=f"comp_m_{idx}"):
                            item["status"] = "נמסר"
                            st.success(t["delivered_success"])
                            st.rerun()
                    with b4:
                        if st.button("🔄 דחה למחר", key=f"comp_p_{idx}"):
                            item["status"] = "נדחה למחר על ידי הלקוח"
                            st.success("עודכן כנדחה למחר!")
                            st.rerun()
                    with b5:
                        if st.button("❌ סורב", key=f"comp_r_{idx}"):
                            item["status"] = "סורב על ידי הלקוח"
                            st.warning("עודכן כסורב ולא ייחשב בתשלום.")
                            st.rerun()

    elif comp_admin_menu == t["add_delivery"]:
        st.title(t["add_delivery"])
        with st.form("comp_add_delivery_form"):
            d_barcode = st.text_input("ברקוד משלוח:", value=f"DEL-{int(datetime.now().timestamp())}")
            d_client = st.text_input("שם הלקוח:")
            d_phone = st.text_input("טלפון הלקוח:")
            d_street = st.text_input("כביש / רחוב:")
            d_house = st.text_input("מספר בית:")
            d_floor = st.text_input("קומה:")
            d_city = st.text_input("עיר / יישוב:")
            d_notes = st.text_area("הערות:")
            
            my_company_name = st.session_state.company
            comp_couriers = [u for u, i in st.session_state.couriers_db.items() if i.get("company") == my_company_name or u == st.session_state.username]
            assigned_to = st.selectbox("שיוך משלוח לשליח:", comp_couriers)
            
            if st.form_submit_button("הוסף משלוח לחברה 🚀") and d_client and d_phone and d_city:
                new_item = {
                    "ברקוד": d_barcode, "שם לקוח": d_client, "שם חברה": my_company_name,
                    "טלפון": format_whatsapp_phone(d_phone), "כביש": d_street, "מספר בית": d_house, "קומה": d_floor, "עיר": d_city,
                    "הערות": d_notes, "status": "ממתין", "courier": assigned_to, "company": my_company_name,
                    "date": get_israel_time()
                }
                st.session_state.deliveries.append(new_item)
                st.success("המשלוח נוסף בהצלחה למערכת החברה!")

    elif comp_admin_menu == t["smart_route"]:
        # ניהול מסלול חכם למנהל חברה
        st.title(t["smart_route"])
        # (קוד מסלול חכם קיים)

    elif comp_admin_menu == t["monthly_report"]:
        st.title(t["monthly_report"])
        # (קוד דוח חודשי קיים)

    elif comp_admin_menu == t["change_password"]:
        st.title(t["change_password"])
        # (קוד שינוי סיסמה קיים)

# ==========================================
# אזור שליח (Courier) - כולל הוספה ועריכה
# ==========================================
elif st.session_state.role == "שליח":
    st.sidebar.title(t["courier_menu"] if "courier_menu" in t else "תפריט שליח")
    courier_menu = st.sidebar.radio(
        "תפריט שליח",
        [
            t["main_sys"],
            t["add_delivery"],  # אפשרות לשליח להוסיף משלוחים חדשים
            t["smart_route"],
            "📍 עדכן את המיקום החי שלי (GPS)",
            t["change_password"]
        ]
    )
    if st.sidebar.button(t["logout"]):
        logout_user()

    if courier_menu == t["main_sys"]:
        st.title(f"🚚 משלוחים המשוייכים אליך - {st.session_state.username}")
        my_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == st.session_state.username]
        
        if not my_deliveries:
            st.info("אין לך משלוחים פעילים כרגע. באפשרותך להוסיף משלוח חדש מהתפריט בצד.")
        else:
            for idx, item in enumerate(my_deliveries):
                status_color = "🟢" if item.get("status") == "נמסר" else ("🔴" if "סורב" in item.get("status", "") else "🟠")
                full_address_str = f"כביש/רחוב: {item.get('כביש', '-')}, בית: {item.get('מספר בית', '-')}, קומה: {item.get('קומה', '-')}, יישוב/כפר: {item.get('עיר', '-')}"
                
                with st.expander(f"{status_color} 📦 לקוח: {item.get('שם לקוח', '')} | עיר: {item.get('עיר', '')} | סטטוס: {item.get('status', '')}"):
                    
                    # --- הרשאה לשליח לערוך את פרטי המשלוח ---
                    with st.form(f"edit_delivery_courier_{idx}"):
                        st.markdown("### ✏️ עריכת פרטי משלוח")
                        ed_client = st.text_input("שם הלקוח:", value=item.get("שם לקוח", ""))
                        ed_phone = st.text_input("טלפון לקוח:", value=item.get("טלפון", ""))
                        ed_street = st.text_input("רחוב/כביש:", value=item.get("כביש", ""))
                        ed_house = st.text_input("מספר בית:", value=item.get("מספר בית", ""))
                        ed_city = st.text_input("עיר/יישוב:", value=item.get("עיר", ""))
                        ed_notes = st.text_area("הערות:", value=item.get("הערות", ""))
                        
                        if st.form_submit_button("שמור שינויים במשלוח 💾"):
                            item["שם לקוח"] = ed_client
                            item["טלפון"] = format_whatsapp_phone(ed_phone)
                            item["כביש"] = ed_street
                            item["מספר בית"] = ed_house
                            item["עיר"] = ed_city
                            item["הערות"] = ed_notes
                            st.success("פרטי המשלוח עודכנו בהצלחה!")
                            st.rerun()

                    st.write(f"**ברקוד:** {item.get('ברקוד', '')} | **טלפון:** {item.get('טלפון', '')} | **כתובת:** {full_address_str} | **הערות:** {item.get('הערות', 'אין')}")
                    
                    c_phone = format_whatsapp_phone(item.get('טלפון', ''))
                    wa_msg = urllib.parse.quote(f"שלום {item.get('שם לקוח', '')}, אני השליח בדרך אליך עם המשלוח שלך.")
                    wa_link = f"https://wa.me/{c_phone}?text={wa_msg}"
                    waze_query = urllib.parse.quote(f"{item.get('כביש', '')} {item.get('מספר בית', '')}, {item.get('עיר', '')}")
                    waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                    
                    b1, b2, b3, b4, b5 = st.columns(5)
                    with b1:
                        st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["whatsapp_btn"]}</button></a>', unsafe_allow_html=True)
                    with b2:
                        st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["waze_btn"]}</button></a>', unsafe_allow_html=True)
                    with b3:
                        if st.button(t["mark_delivered"], key=f"cour_m_{idx}"):
                            item["status"] = "נמסר"
                            st.success(t["delivered_success"])
                            st.rerun()
                    with b4:
                        if st.button("🔄 דחה למחר", key=f"cour_p_{idx}"):
                            item["status"] = "נדחה למחר על ידי הלקוח"
                            st.success("עודכן כנדחה למחר!")
                            st.rerun()
                    with b5:
                        if st.button("❌ סורב", key=f"cour_r_{idx}"):
                            item["status"] = "סורב על ידי הלקוח"
                            st.warning("עודכן כסורב!")
                            st.rerun()

    elif courier_menu == t["add_delivery"]:
        st.title("➕ הוספת משלוח חדש על ידי שליח")
        with st.form("courier_add_delivery_form"):
            d_barcode = st.text_input("ברקוד משלוח:", value=f"DEL-C-{int(datetime.now().timestamp())}")
            d_client = st.text_input("שם הלקוח:")
            d_phone = st.text_input("טלפון הלקוח:")
            d_street = st.text_input("כביש / רחוב:")
            d_house = st.text_input("מספר בית:")
            d_floor = st.text_input("קומה:")
            d_city = st.text_input("עיר / יישוב:")
            d_notes = st.text_area("הערות:")
            
            if st.form_submit_button("הוסף משלוח אליי 🚀") and d_client and d_phone and d_city:
                new_item = {
                    "ברקוד": d_barcode, "שם לקוח": d_client, "שם חברה": st.session_state.company,
                    "טלפון": format_whatsapp_phone(d_phone), "כביש": d_street, "מספר בית": d_house, "קומה": d_floor, "עיר": d_city,
                    "הערות": d_notes, "status": "ממתין", "courier": st.session_state.username, "company": st.session_state.company,
                    "date": get_israel_time()
                }
                st.session_state.deliveries.append(new_item)
                st.success("המשלוח נוסף בהצלחה והוצמד אליך!")

    elif courier_menu == t["smart_route"]:
        st.title(t["smart_route"])
        # (קוד מסלול חכם לשליח)

    elif courier_menu == "📍 עדכן את המיקום החי שלי (GPS)":
        st.title("📍 עדכן מיקום חי")
        with st.form("cour_loc_form"):
            loc_input = st.text_input("הכנס כתובת נוכחית או קישור מיקום:")
            if st.form_submit_button("עדכן מיקום במערכת 📍") and loc_input:
                save_location_data(st.session_state.username, loc_input)
                st.success("המיקום עודכן בהצלחה!")

    elif courier_menu == t["change_password"]:
        st.title(t["change_password"])
        with st.form("change_cour_pwd_form"):
            old_p = st.text_input("סיסמה נוכחית:", type="password")
            new_p = st.text_input("סיסמה חדשה:", type="password")
            if st.form_submit_button("עדכן סיסמה") and old_p == st.session_state.couriers_db[st.session_state.username]["password"]:
                st.session_state.couriers_db[st.session_state.username]["password"] = new_p
                save_users_db(st.session_state.couriers_db)
                st.success("הסיסמה עודכנה בהצלחה!")
