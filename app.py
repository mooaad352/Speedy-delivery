import streamlit as st
import urllib.parse
from datetime import datetime, timezone, timedelta
import pandas as pd
import os
import json
from io import BytesIO

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

ISRAEL_OFFSET = timedelta(hours=2)
ADMIN_PHONE = "972502616375"
APP_URL = "https://speedy-delivery-app.streamlit.app/"

def get_israel_time():
    return datetime.now(timezone(ISRAEL_OFFSET)).strftime("%Y-%m-%d %H:%M")

def format_whatsapp_phone(phone_str):
    clean_phone = "".join(filter(str.isdigit, str(phone_str)))
    if clean_phone.startswith("0"):
        clean_phone = "972" + clean_phone[1:]
    elif not clean_phone.startswith("972") and len(clean_phone) > 0:
        clean_phone = "972" + clean_phone
    return clean_phone

def generate_html_contract_form():
    """
    יוצר קובץ HTML מעוצב לטופס ההתרשמות והחוזה של השליח/המשתמש כולל הגנות משפטיות מלאות
    """
    html_content = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speedy Delivery - טופס התרשמות וחוזה התקשרות</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; direction: rtl; text-align: right; color: #333; }
        .container { max-width: 750px; margin: 30px auto; background: #ffffff; padding: 35px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }
        h2 { color: #1f2937; text-align: center; margin-bottom: 25px; }
        .contract-box { background: #f9fafb; border: 1px solid #d1d5db; padding: 15px; border-radius: 6px; height: 220px; overflow-y: scroll; font-size: 13px; margin-bottom: 20px; line-height: 1.6; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 6px; font-weight: bold; color: #374151; }
        input[type="text"], input[type="tel"], input[type="email"] { width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; box-sizing: border-box; font-size: 15px; background-color: #f9fafb; }
        .checkbox-group { display: flex; align-items: center; gap: 10px; margin: 20px 0; font-weight: bold; }
        button { background-color: #2563eb; color: white; padding: 12px 20px; border: none; border-radius: 6px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
        button:hover { background-color: #1d4ed8; }
    </style>
</head>
<body>
<div class="container">
    <h2>📝 טופס התרשמות וחוזה התקשרות - Speedy Delivery</h2>
    
    <div class="contract-box">
        <strong>תנאי שימוש, הצהרה ופטור מלא מאחריות משפטית:</strong><br><br>
        1. <strong>מהות הפלטפורמה:</strong> מערכת "Speedy Delivery" משמשת כפלטפורמה טכנולוגית עצמאית לקישור בין משתמשים לבין נותני שירות (שליחים), ואינה משמשת כמעסיק, חברת שליחויות מרכזית או צד לחוזה ההובלה בפועל.<br><br>
        2. <strong>העדר יחסי עובד-מעביד:</strong> מוסכם בזאת במפורש כי בין מפעיל המערכת לבין השליח ו/או הלקוח לא מתקיימים ולא יתקיימו כל יחסי עובד-מעביד מכל מין וסוג שהוא. השליח פועל כקבלן עצמאי לחלוטין.<br><br>
        3. <strong>אחריות בלעדית של השליח:</strong> השליח נושא באחריות המלאה, הבלעדית והאישית לכל נזק, אובדן, גניבה, קלקול או השחתה של הסחורה/המשלוח מרגע קבלתו ועד למסירתו ליעד. כמו כן, השליח אחראי בלעדית לציודו, לרכבו, ולעמידה בכל דיני התעבורה, הרישוי והביטוח כחוק.<br><br>
        4. <strong>פטור מלא מאחריות למפעיל המערכת:</strong> מפעיל המערכת לא יישא בשום אחריות ישירה או עקיפה לכל נזק גוף, נזק רכוש, תאונת דרכים, איחור במסירה, קנסות, תביעות צד ג' או הוצאות מכל סוג שנגרמו עקב או בקשר עם ביצוע המשלוחים בפועל.<br><br>
        5. <strong>שיפוי:</strong> השליח מתחייב לשפות ולפצות את מפעיל המערכת בגין כל דרישה, תביעה, הוצאה או נזק שיופנו כלפיו עקב פעילות השליח או הפרת תנאים אלו.
    </div>

    <form action="#" method="POST" onsubmit="event.preventDefault(); alert('הטופס נשמר בהצלחה!');">
        <div class="form-group"><label>שם מלא:</label><input type="text" required></div>
        <div class="form-group"><label>תעודת זהות:</label><input type="text" required></div>
        <div class="form-group"><label>כתובת מלאה:</label><input type="text" required></div>
        <div class="form-group"><label>כתובת אימייל:</label><input type="email" required></div>
        <div class="form-group"><label>מספר טלפון נייד:</label><input type="tel" required></div>
        <div class="form-group"><label>ח.פ / עוסק פטור (אופציונלי):</label><input type="text"></div>
        
        <div class="checkbox-group">
            <input type="checkbox" id="agree" required>
            <label for="agree" style="display:inline; margin:0;">קראתי בעיון, הבנתי ואני מאשר/ת ללא הסתייגות את תנאי החוזה, ההצהרה ופטור האחריות.</label>
        </div>
        
        <button type="submit">שמור ושלח חוזה התרשמות 🚀</button>
    </form>
</div>
</body>
</html>"""
    file_stream = BytesIO(html_content.encode("utf-8"))
    file_stream.seek(0)
    return file_stream

st.set_page_config(page_title="Speedy Delivery - מערכת ניהול משלוחים", page_icon="🚚", layout="wide")

CONTRACTS_FILE = "delivery_drivers_contracts.csv"
USERS_FILE = "couriers_db.json"
LOCATIONS_FILE = "couriers_live_locations.json"

def load_users_db():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    default_users = {
        "Admin": {"password": "Sma.srablove2028", "role": "מנהל מערכת ראשי (Super Admin)", "phone": ADMIN_PHONE, "company": "System", "contract_signed": True},
        "mohammad": {"password": "123", "role": "שליח", "phone": "972502616375", "company": "Independent", "contract_signed": True}
    }
    save_users_db(default_users)
    return default_users

def save_users_db(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=4)

def load_locations_db():
    if os.path.exists(LOCATIONS_FILE):
        try:
            with open(LOCATIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_location_data(username, loc_text):
    locs = load_locations_db()
    locs[username] = {
        "location": loc_text,
        "updated_at": get_israel_time()
    }
    with open(LOCATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(locs, f, ensure_ascii=False, indent=4)

def load_contracts_data():
    if os.path.exists(CONTRACTS_FILE):
        return pd.read_csv(CONTRACTS_FILE)
    return pd.DataFrame(columns=["שם משתמש", "תפקיד", "חברה", "שם מלא", "ת.ז", "כתובת", "אימייל", "טלפון", "ח.פ / עוסק פטור", "תאריך רישום"])

def save_contract_data(new_data):
    df = load_contracts_data()
    new_row = pd.DataFrame([new_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CONTRACTS_FILE, index=False, encoding="utf-8-sig")

def delete_contract_by_index(idx):
    df = load_contracts_data()
    if 0 <= idx < len(df):
        df = df.drop(idx).reset_index(drop=True)
        df.to_csv(CONTRACTS_FILE, index=False, encoding="utf-8-sig")

TRANSLATIONS = {
    "العربية (Arabic)": {
        "title": "🚚 نظام إدارة وتوصيل الشحنات السريع",
        "login_title": "تسجيل دخول المستخدمين والمندوبين",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_btn": "تسجيل الدخول",
        "login_error": "خطأ في اسم المستخدم أو كلمة المرور.",
        "logout": "تسجيل الخروج",
        "admin_menu": "قائمة الإدارة",
        "main_sys": "نظام الشحنات الرئيسي",
        "add_courier": "إضافة مندوب جديد",
        "add_company_admin": "إضافة مدير شركة توصيل",
        "manage_users": "إدارة وتعديل المستخدمين",
        "monthly_report": "📊 تقرير الحسابات والعمولات",
        "contract_menu": "📝 سجل العقود والبيانات المسجلة",
        "live_tracking": "📍 متابعة مواقع الشליחים (GPS)",
        "current_loc": "📍 موقعك الحالي / نقطة الانطلاق",
        "loc_placeholder": "أدخل موقعك الحالي (بلدة / مدينة):",
        "list_title": "📋 قائمة الشحنات",
        "whatsapp_btn": "📲 إرسال واتساب",
        "mark_delivered": "تحديد كـ تم التسليم",
        "delivered_success": "تم تحديث الشحنة!"
    },
    "עברית (Hebrew)": {
        "title": "🚚 מערכת ניהול וסידור משלוחים מהירה",
        "login_title": "כניסת משתמשים ושליחים",
        "username": "שם משתמש",
        "password": "סיסמה",
        "login_btn": "התחבר",
        "login_error": "שם משתמש או סיסמה שגויים.",
        "logout": "התנתק (Logout)",
        "admin_menu": "תפריט ניהול",
        "main_sys": "מערכת משלוחים ראשית",
        "add_courier": "הוספת שליח חדש",
        "add_company_admin": "הוספת מנהל חברת משלוחים",
        "manage_users": "ניהול ועריכת משתמשים",
        "monthly_report": "📊 סיכום חודשי ודוחות",
        "contract_menu": "📝 פנקס נרשמים וחוזים שמורים",
        "live_tracking": "📍 מעקב מיקום שליחים בזמן אמת",
        "current_loc": "📍 מיקום נוכחי ונקודת מוצא",
        "loc_placeholder": "הכנס את המיקום הנוכחי שלך (עיר / כפר):",
        "list_title": "📋 רשימת המשלוחים להיום",
        "whatsapp_btn": "📲 שלח וואטסאפ ללקוח",
        "mark_delivered": "סמן כנמסר",
        "delivered_success": "המשלוח עודכן כנמסר!"
    },
    "English": {
        "title": "🚚 Fast Delivery Management System",
        "login_title": "Courier & User Login",
        "username": "Username",
        "password": "Password",
        "login_btn": "Login",
        "login_error": "Invalid username or password.",
        "logout": "Logout",
        "admin_menu": "Management Menu",
        "main_sys": "Main Deliveries System",
        "add_courier": "Add New Courier",
        "add_company_admin": "Add Delivery Company Admin",
        "manage_users": "Manage Users",
        "monthly_report": "📊 Monthly Reports",
        "contract_menu": "📝 Registered Contracts",
        "live_tracking": "📍 Live Courier Tracking",
        "current_loc": "📍 Current Location",
        "loc_placeholder": "Enter current location:",
        "list_title": "📋 Deliveries List",
        "whatsapp_btn": "📲 WhatsApp Customer",
        "mark_delivered": "Mark Delivered",
        "delivered_success": "Updated successfully!"
    }
}

st.sidebar.markdown("---")
lang_choice = st.sidebar.selectbox("🌐 Language / لغة / שפה", ["العربية (Arabic)", "עברית (Hebrew)", "English"], index=1)
t = TRANSLATIONS[lang_choice]
is_rtl = lang_choice in ["العربية (Arabic)", "עברית (Hebrew)"]
dir_style = "rtl" if is_rtl else "ltr"
st.markdown(f"""<style>div.block-container {{ direction: {dir_style}; }}</style>""", unsafe_allow_html=True)

# כפתור הורדת טופס ההתרשמות והחוזה ב-HTML בסיידבר
st.sidebar.markdown("---")
st.sidebar.subheader("📄 טופס התרשמות וחוזה")
html_contract_file = generate_html_contract_form()
st.sidebar.download_button(
    label="📥 הורד טופס התרשמות וחוזה (.html)",
    data=html_contract_file,
    file_name="delivery_contract_form.html",
    mime="text/html"
)

if "couriers_db" not in st.session_state:
    st.session_state.couriers_db = load_users_db()

query_params = st.query_params

if "logged_in" not in st.session_state:
    if query_params.get("logged_in") == "true" and "username" in query_params:
        st.session_state.logged_in = True
        st.session_state.username = query_params["username"]
        st.session_state.role = query_params.get("role", "שליח")
        st.session_state.company = query_params.get("company", "Independent")
    else:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.company = ""

if "deliveries" not in st.session_state:
    current_time_il = get_israel_time()
    st.session_state.deliveries = [{
        "ברקוד": "TEST-001", "שם לקוח": "סמר שומרי", "שם חברה": "SHEIN", "טלפון": "972502616375",
        "כתובת מלאה": "כסרא-סמיע", "עיר": "כסרא-סמיע", "הערות": "משלוח בדיקה", "status": "ממתין",
        "courier": "mohammad", "company": "Independent", "date": current_time_il
    }]

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.company = ""
    st.query_params.clear()
    st.rerun()

if not st.session_state.logged_in:
    st.title(t["title"])
    st.subheader(t["login_title"])
    with st.form("login_form"):
        username_input = st.text_input(t["username"])
        password_input = st.text_input(t["password"], type="password")
        submit_btn = st.form_submit_button(t["login_btn"])
        if submit_btn:
            db = st.session_state.couriers_db
            if username_input in db and db[username_input]["password"] == password_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.session_state.role = db[username_input]["role"]
                st.session_state.company = db[username_input].get("company", "Independent")
                st.query_params["logged_in"] = "true"
                st.query_params["username"] = username_input
                st.query_params["role"] = db[username_input]["role"]
                st.query_params["company"] = st.session_state.company
                st.rerun()
            else:
                st.error(t["login_error"])

elif st.session_state.role != "מנהל מערכת ראשי (Super Admin)" and not st.session_state.couriers_db.get(st.session_state.username, {}).get("contract_signed", False):
    st.title("📝 טופס התרשמות, רישום פרטים ותנאי שימוש במערכת")
    
    # הצגת חוזה מורחב ומוגן משפטית במסך השליח
    st.markdown("""
    <div style="background-color: #f9fafb; border: 1px solid #d1d5db; padding: 20px; border-radius: 8px; max-height: 250px; overflow-y: scroll; margin-bottom: 20px; line-height: 1.6; font-size: 14px;">
        <strong>חוזה התקשרות, הצהרה ופטור מלא מאחריות - Speedy Delivery:</strong><br><br>
        1. <strong>מהות הפלטפורמה:</strong> מערכת זו מהווה פלטפורמה טכנולוגית בלבד לניהול וסידור משלוחים, ואינה צד לחוזה ההובלה או מעסיקה של השליחים.<br><br>
        2. <strong>העדר יחסי עובד-מעביד:</strong> מוסכם ומובהר בזאת במפורש כי לא מתקיימים יחסי עובד-מעביד בין מפעיל המערכת לבין השליח. השליח פועל כגורם עצמאי לחלוטין (קבלן עצמאי) הנושא באחריות לכל תשלום מס, ביטוח לאומי ותנאים סוציאליים של עצמו.<br><br>
        3. <strong>אחריות בלעדית לסחורה ולפעילות:</strong> השליח אחראי באופן בלעדי וישיר לכל נזק, אובדן, חוסר או פגיעה במשלוח מרגע קבלתו ועד למסירתו המלאה ללקוח. מפעיל המערכת לא יישא בכל אחריות לנזקי סחורה.<br><br>
        4. <strong>פטור גורף מאחריות לנזקי גוף ורכוש:</strong> מפעיל המערכת פטור באופן מלא ומחלט מכל אחריות בגין תאונות דרכים, נזקי גוף, נזקי רכוש, קנסות תנועה, עיכובים, או כל נזק אחר שעלול להיגרם לשליח או לצד ג' כלשהו במהלך או עקב ביצוע המשלוחים.<br><br>
        5. <strong>שיפוי:</strong> השליח מתחייב לשפות את מפעיל המערכת מיד עם דרישה ראשונה בגין כל תביעה, דרישה, הוצאה או נזק שייגרמו למפעיל המערכת עקב פעילותו של השליח.
    </div>
    """, unsafe_allow_html=True)

    with st.form("first_login_contract_form"):
        f_full_name = st.text_input("שם מלא (חובה):")
        f_id_num = st.text_input("תעודת זהות (חובה):")
        f_address = st.text_input("כתובת מלאה (חובה):")
        f_email = st.text_input("כתובת אימייל (חובה):")
        f_phone = st.text_input("מספר טלפון נייד (חובה):", value=st.session_state.couriers_db.get(st.session_state.username, {}).get("phone", ""))
        f_hp_or_exempt = st.text_input("מספר ח.פ / עוסק פטור (אופציונלי):")
        agree_terms = st.checkbox("קראתי את החוזה בעיון רב, הבנתי ואני מאשר/ת ללא הסתייגות את תנאי השימוש, ההצהרה ופטור האחריות.")
        submit_contract = st.form_submit_button("אישור החוזה וסיום הרישום 🚀")
        if submit_contract:
            if agree_terms and f_full_name and f_id_num and f_address and f_email and f_phone:
                reg_date = get_israel_time()
                st.session_state.couriers_db[st.session_state.username]["contract_signed"] = True
                st.session_state.couriers_db[st.session_state.username]["full_name"] = f_full_name
                st.session_state.couriers_db[st.session_state.username]["id_number"] = f_id_num
                st.session_state.couriers_db[st.session_state.username]["address"] = f_address
                st.session_state.couriers_db[st.session_state.username]["email"] = f_email
                st.session_state.couriers_db[st.session_state.username]["phone"] = format_whatsapp_phone(f_phone)
                st.session_state.couriers_db[st.session_state.username]["hp_exempt"] = f_hp_or_exempt if f_hp_or_exempt else "אין"
                st.session_state.couriers_db[st.session_state.username]["registration_date"] = reg_date
                save_users_db(st.session_state.couriers_db)
                
                save_contract_data({
                    "שם משתמש": st.session_state.username, "תפקיד": st.session_state.role, "חברה": st.session_state.company,
                    "שם מלא": f_full_name, "ת.ז": f_id_num, "כתובת": f_address, "אימייל": f_email,
                    "טלפון": format_whatsapp_phone(f_phone), "ח.פ / עוסק פטור": f_hp_or_exempt if f_hp_or_exempt else "אין", "תאריך רישום": reg_date
                })
                st.success("הפרטים והחוזה נשמרו בהצלחה!")
                st.rerun()
            else:
                st.error("נא למלא את כל שדות החובה ולסמן וי על אישור החוזה.")
    if st.sidebar.button(t["logout"]):
        logout_user()

elif st.session_state.role == "מנהל מערכת ראשי (Super Admin)":
    st.sidebar.title("מנהל ראשי")
    admin_menu = st.sidebar.radio(
        t["admin_menu"], 
        [
            t["main_sys"], 
            t["add_company_admin"],
            t["add_courier"], 
            t["manage_users"],
            t["monthly_report"],
            t["contract_menu"],
            t["live_tracking"]
        ]
    )
    if st.sidebar.button(t["logout"]):
        logout_user()

    if admin_menu == t["main_sys"]:
        st.title(t["main_sys"])
        admin_deliveries = st.session_state.deliveries
        col1, col2, col3 = st.columns(3)
        col1.metric("סך הכל משלוחים", len(admin_deliveries))
        col2.metric("ממתינים", len([d for d in admin_deliveries if d["status"] == "ממתין"]))
        col3.metric("נמסרו", len([d for d in admin_deliveries if d["status"] == "נמסר"]))
        st.divider()
        for idx, item in enumerate(admin_deliveries):
            status_color = "🟢" if item["status"] == "נמסר" else "🟠"
            with st.expander(f"{status_color} 📦 {item['שם לקוח']} | {item['עיר']} | סטטוס: {item['status']}"):
                st.write(f"**ברקוד:** {item['ברקוד']} | **טלפון:** {item['טלפון']}")
                if item["status"] == "ממתין" and st.button(t["mark_delivered"], key=f"adm_m_{idx}"):
                    item["status"] = "נמסר"
                    st.success(t["delivered_success"])
                    st.rerun()

    elif admin_menu == t["add_company_admin"]:
        st.title(t["add_company_admin"])
        with st.form("add_comp_form"):
            cu = st.text_input("שם משתמש מנהל:")
            cp = st.text_input("סיסמה:", type="password")
            cn = st.text_input("שם חברה:")
            cph = st.text_input("טלפון:")
            if st.form_submit_button("הוסף מנהל חברה") and cu and cp and cn and cph:
                st.session_state.couriers_db[cu] = {"password": cp, "role": "מנהל חברה (Company Admin)", "phone": format_whatsapp_phone(cph), "company": cn, "contract_signed": False}
                save_users_db(st.session_state.couriers_db)
                st.success("נוסף בהצלחה!")

    elif admin_menu == t["add_courier"]:
        st.title(t["add_courier"])
        with st.form("add_cour_form"):
            cu = st.text_input("שם משתמש שליח:")
            cp = st.text_input("סיסמה:", type="password")
            cph = st.text_input("טלפון:")
            comp_list = ["Independent"] + list(set([i.get("company") for u, i in st.session_state.couriers_db.items() if i.get("company") not in ["Independent", "System"]]))
            ccomp = st.selectbox("שיוך חברה:", comp_list)
            if st.form_submit_button("הוסף שליח") and cu and cp and cph:
                st.session_state.couriers_db[cu] = {"password": cp, "role": "שליח", "phone": format_whatsapp_phone(cph), "company": ccomp, "contract_signed": False}
                save_users_db(st.session_state.couriers_db)
                st.success("השליח נוסף בהצלחה!")

    elif admin_menu == t["manage_users"]:
        st.title(t["manage_users"])
        for usr, info in list(st.session_state.couriers_db.items()):
            if usr == "Admin": continue
            with st.expander(f"👤 {usr} ({info.get('role')}) - חברה: {info.get('company')}"):
                if st.button("מחק משתמש ❌", key=f"del_user_{usr}"):
                    del st.session_state.couriers_db[usr]
                    save_users_db(st.session_state.couriers_db)
                    st.success("המשתמש נמחק.")
                    st.rerun()

    elif admin_menu == t["monthly_report"]:
        st.title(t["monthly_report"])
        st.dataframe(pd.DataFrame([{"משתמש": u, **i} for u, i in st.session_state.couriers_db.items() if u != "Admin"]), use_container_width=True)

    elif admin_menu == t["contract_menu"]:
        st.title(t["contract_menu"])
        st.write("כאן תוכל לצפות בחוזים הרשומים ואף להסירם במידת הצורך:")
        contracts_df = load_contracts_data()
        if not contracts_df.empty:
            for c_idx, row in contracts_df.iterrows():
                st.markdown(f"**{row['שם מלא']}** | ת.ז: {row['ת.ז']} | טלפון: {row['טלפון']} | תאריך: {row['תאריך רישום']}")
                if st.button(f"🗑️ הסר חוזה זה מהרשימה", key=f"del_contract_{c_idx}"):
                    delete_contract_by_index(c_idx)
                    st.success("החוזה הוסר בהצלחה מהרשימה!")
                    st.rerun()
                st.divider()
        else:
            st.info("אין חוזים שמורים.")

    elif admin_menu == t["live_tracking"]:
        st.title(t["live_tracking"])
        locs = load_locations_db()
        if locs:
            for usr, data in locs.items():
                st.info(f"🛵 **שליח/משתמש:** {usr} | 📍 **מיקום אחרון:** {data['location']} | ⏰ **עודכן בתאריך ושעה:** {data['updated_at']}")
        else:
            st.info("עדיין לא דווחו מיקומים חיים על ידי השליחים.")

elif st.session_state.role == "מנהל חברה (Company Admin)":
    company_name = st.session_state.company
    st.title(f"🏢 מנהל חברה: {company_name}")
    if st.sidebar.button(t["logout"]):
        logout_user()
    comp_menu = st.sidebar.radio("תפריט", ["📦 משלוחי חברה", "📍 מעקב מיקום שליחי החברה"])
    if comp_menu == "📦 משלוחי חברה":
        st.subheader("משלוחים פעילים לחברה שלך:")
        comp_deliveries = [d for d in st.session_state.deliveries if d.get("company") == company_name]
        for idx, item in enumerate(comp_deliveries):
            st.write(f"📦 לקוח: {item['שם לקוח']} | עיר: {item['עיר']} | סטטוס: {item['status']}")
    elif comp_menu == "📍 מעקב מיקום שליחי החברה":
        st.subheader("📍 המיקום האחרון של שליחי החברה שלך:")
        locs = load_locations_db()
        comp_couriers = [u for u, i in st.session_state.couriers_db.items() if i.get("company") == company_name]
        found = False
        for usr in comp_couriers:
            if usr in locs:
                found = True
                st.success(f"🛵 **שליח:** {usr} | 📍 **מיקום:** {locs[usr]['location']} | ⏰ **עודכן:** {locs[usr]['updated_at']}")
        if not found:
            st.info("אין עדיין נתוני מיקום משליחי החברה.")

elif st.session_state.role == "שליח":
    st.title(f"🛵 שלום שליח: {st.session_state.username}")
    if st.sidebar.button(t["logout"]):
        logout_user()
        
    st.subheader("📍 עדכון המיקום הנוכחי שלך (GPS / נקודה אחרונה):")
    with st.form("update_my_location_form"):
        my_current_location_input = st.text_input("הכנס כתובת נוכחית, יישוב או קישור מיקום:", placeholder="לדוגמה: כסרא-סמיע, כביש ראשי")
        submit_loc = st.form_submit_button("עדכן מיקום אחרון במערכת 📍")
        if submit_loc and my_current_location_input:
            save_location_data(st.session_state.username, my_current_location_input)
            st.success("המיקום שלך עודכן בהצלחה למנהל ולחברה!")

    st.divider()
    st.subheader(t["list_title"])
    courier_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == st.session_state.username or d.get("company") == st.session_state.company]
    if not courier_deliveries:
        st.info("אין משלוחים ברשימה.")
    else:
        for idx, item in enumerate(courier_deliveries):
            status_color = "🟢" if item["status"] == "נמסר" else "🟠"
            with st.expander(f"{status_color} 📦 {item['שם לקוח']} | {item['עיר']} | סטטוס: {item['status']}"):
                st.write(f"**ברקוד:** {item['ברקוד']} | **טלפון:** {item['טלפון']}")
                if item["status"] == "ממתין" and st.button(t["mark_delivered"], key=f"c_m_{idx}"):
                    item["status"] = "נמסר"
                    st.success(t["delivered_success"])
                    st.rerun()
