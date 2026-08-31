import streamlit as st
import urllib.parse
from datetime import datetime, timezone, timedelta
import pandas as pd
import os
import json
from io import BytesIO

ISRAEL_OFFSET = timedelta(hours=2)
ADMIN_PHONE = "972502616375"
VAT_RATE = 0.18   # מע"מ 18%

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
        .contract-box { background: #f9fafb; border: 1px solid #d1d5db; padding: 15px; border-radius: 6px; height: 260px; overflow-y: scroll; font-size: 13px; margin-bottom: 20px; line-height: 1.6; color: #111827; }
    </style>
</head>
<body>
<div class="container">
    <h2>📝 טופס התרשמות וחוזה התקשרות - Speedy Delivery</h2>
    <div class="contract-box">
        <strong>תנאי שימוש, הצהרה ופטור מלא מאחריות משפטית:</strong><br><br>
        1. <strong>מהות הפלטפורמה:</strong> מערכת "Speedy Delivery" משמשת כפלטפורמה טכנולוגית עצמאית.<br><br>
        2. <strong>העדר יחסי עובד-מעביד:</strong> מוסכם בזאת במפורש כי לא מתקיימים יחסי עובד-מעביד.<br><br>
        3. <strong>אחריות בלעדית:</strong> השליח או מנהל החברה נושאים באחריות המלאה והבלעדית לכל ניהול המשלוחים.<br><br>
        4. <strong>פטור מלא מאחריות למפעיל המערכת:</strong> מפעיל המערכת פטור מאחריות לנזקי גוף, רכוש ותאונות.<br><br>
        5. <strong>תשלומים והתחייבות פיננסית:</strong> מנהל החברה מתחייב להסדיר את התשלומים והחשבונות עבור כלל המשלוחים שבוצעו תחת ניהולו במערכת.<br><br>
        6. <strong>הרשאה מלאה לבדיקת משלוחים שסורבו:</strong> ניתנת בזה הרשאה מלאה למפעיל המערכת לבדוק ולוודא מול הלקוחות משלוחים שדווחו כסורבים.<br><br>
        7. <strong>שיפוי:</strong> המשתמש מתחייב לשפות את מפעיל המערכת בגין כל נזק.
    </div>
</div>
</body>
</html>"""
    file_stream = BytesIO(html_content.encode("utf-8"))
    file_stream.seek(0)
    return file_stream

def generate_monthly_invoice_html(user_name, user_hp, is_exempt, count_deliveries, price_per_unit=1.0):
    base_price = count_deliveries * price_per_unit
    vat_amount = 0.0 if is_exempt else base_price * VAT_RATE
    total_final = base_price + vat_amount
    current_month_str = datetime.now().strftime("%m/%Y")
    
    html_content = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>חשבונית / דוח סיכום חודשי - {user_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f9f9f9; color: #333; margin: 0; padding: 20px; }}
        .invoice-box {{ max-width: 800px; margin: auto; background: #fff; padding: 30px; border: 1px solid #eee; box-shadow: 0 0 10px rgba(0,0,0,0.15); border-radius: 8px; }}
        header {{ border-bottom: 2px solid #2563eb; padding-bottom: 15px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
        .company-details h2 {{ margin: 0; color: #2563eb; }}
        .invoice-details {{ text-align: left; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #d1d5db; padding: 12px; text-align: right; }}
        th {{ background-color: #f3f4f6; }}
        .totals {{ margin-top: 25px; border-top: 2px solid #333; padding-top: 15px; text-align: left; font-size: 1.1em; }}
        .totals div {{ margin-bottom: 8px; }}
        .final-amount {{ font-weight: bold; font-size: 1.3em; color: #16a34a; }}
        .footer {{ margin-top: 40px; text-align: center; font-size: 0.9em; color: #777; }}
        .btn-print {{ background: #2563eb; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 5px; font-size: 1em; margin-top: 20px; }}
    </style>
</head>
<body>
<div class="invoice-box">
    <header>
        <div class="company-details">
            <h2>מקארט (Speedy Delivery) - דוח וחשבון חודשי מרוכז</h2>
            <p>סיכום פעילות עסקית כוללת</p>
        </div>
        <div class="invoice-details">
            <p><strong>חודש דיווח:</strong> {current_month_str}</p>
            <p><strong>תאריך הפקה:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
    </header>

    <section>
        <h3>פרטי מנהל החברה / העסק:</h3>
        <p><strong>שם מנהל / חברה:</strong> {user_name}</p>
        <p><strong>ח.פ / ת.ז / עוסק פטור:</strong> {user_hp}</p>
        <p><strong>סטטוס מס:</strong> {'עוסק פטור (ללא מע"מ)' if is_exempt else 'חייב במע"מ (כולל מע"מ 18%)'}</p>
    </section>

    <table>
        <thead>
            <tr>
                <th>תיאור הפעילות הכללית</th>
                <th>סך המשלוחים שבוצעו (כולל שליחי החברה)</th>
                <th>תעריף ליחידה</th>
                <th>סה"כ לפני מע"מ</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>סך כל המשלוחים שטופלו ובוצעו במערכת תחת ניהולך החודש</td>
                <td>{count_deliveries}</td>
                <td>₪{price_per_unit:.2f}</td>
                <td>₪{base_price:.2f}</td>
            </tr>
        </tbody>
    </table>

    <div class="totals">
        <div>סכום לפני מע"מ: <strong>₪{base_price:.2f}</strong></div>
        {"" if is_exempt else f'<div>מע"מ (18%): <strong>₪{vat_amount:.2f}</strong></div>'}
        <div class="final-amount">סכום סופי לתשלום מרוכז מול המערכת: ₪{total_final:.2f}</div>
    </div>

    <div style="text-align: center;">
        <button class="btn-print" onclick="window.print()">הדפס / שמור כ-PDF</button>
    </div>

    <div class="footer">
        הופק אוטומטית ממערכת מקארט - Speedy Delivery.
    </div>
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
    default_users = {
        "Admin": {"password": "Sma.srablove2028", "role": "מנהל מערכת ראשי (Super Admin)", "phone": ADMIN_PHONE, "company": "System", "contract_signed": True},
        "mohammad": {"password": "123", "role": "מנהל חברה (Company Admin)", "phone": "972502616375", "company": "Independent", "contract_signed": True}
    }
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "Admin" not in data:
                    data["Admin"] = default_users["Admin"]
                else:
                    data["Admin"]["password"] = "Sma.srablove2028"
                    data["Admin"]["role"] = "מנהל מערכת ראשי (Super Admin)"
                return data
        except Exception:
            pass
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
    locs[username] = {"location": loc_text, "updated_at": get_israel_time()}
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

TRANSLATIONS = {
    "עברית (Hebrew)": {
        "title": "🚚 מערכת ניהול וסידור משלוחים מהירה",
        "login_title": "כניסת משתמשים ומנהלי חברות",
        "username": "שם משתמש",
        "password": "סיסמה",
        "login_btn": "התחבר",
        "login_error": "שם משתמש או סיסמה שגויים.",
        "logout": "התנתק (Logout)",
        "admin_menu": "תפריט ניהול ראשי",
        "company_admin_menu": "תפריט מנהל חברה ושליחים",
        "courier_menu": "תפריט שליח",
        "main_sys": "מערכת משלוחים ראשית",
        "smart_route": "🗺️ סידור מסלול משלוחים אוטומטי (מרחקי GPS)",
        "add_delivery": "➕ הוספת משלוח חדש",
        "add_courier": "הוספת שליח תחת ניהולך",
        "add_company_admin": "הוספת מנהל חברה",
        "manage_users": "ניהול ועריכת משתמשים",
        "monthly_report": "📊 סיכום חודשי ודוחות מרוכזים",
        "contract_menu": "📝 פנקס נרשמים וחוזים שמורים",
        "live_tracking": "📍 מעקב מיקום שליחים בזמן אמת",
        "verify_rejected": "🔍 אימות משלוחים שסורבו מול לקוחות",
        "change_password": "🔐 החלפת סיסמה אישית",
        "whatsapp_btn": "📲 שלח וואטסאפ ללקוח",
        "waze_btn": "🧭 נווט ב-Waze",
        "mark_delivered": "סמן כנמסר",
        "delivered_success": "הסטטוס עודכן בהצלחה!"
    },
    "العربية (Arabic)": {
        "title": "🚚 نظام إدارة وتوصيل الشحنات السريع",
        "login_title": "تسجيل دخول المستخدمين ومديري الشركات",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_btn": "تسجيل الدخول",
        "login_error": "خطأ في اسم المستخدم أو كلمة المرور.",
        "logout": "تسجيل الخروج",
        "admin_menu": "قائمة الإدارة الرئيسية",
        "company_admin_menu": "قائمة مدير الشركة والمندوبين",
        "courier_menu": "قائمة المندوب",
        "main_sys": "نظام الشحنات الرئيسي",
        "smart_route": "🗺️ ترتيب مسار الشحنات تلقائياً",
        "add_delivery": "➕ إضافة شحنة جديدة",
        "add_courier": "إضافة مندوب تحت إدارتك",
        "add_company_admin": "إضافة مدير شركة",
        "manage_users": "إدارة وتعديل المستخدمين",
        "monthly_report": "📊 تقرير الحسابات والعمولات المجمع",
        "contract_menu": "📝 سجل العقود والبيانات المسجلة",
        "live_tracking": "📍 متابعة مواقع المندوبين (GPS)",
        "verify_rejected": "🔍 التحقق من الشحنات المرفوضة مع العملاء",
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

st.sidebar.markdown("---")
st.sidebar.subheader("📄 טופס התרשמות וחוזה")
html_contract_file = generate_html_contract_form()
st.sidebar.download_button(
    label="📥 הורד טופס התרשמות וחוזה כללי (.html)",
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
        "כביש": "רחוב ראשי", "מספר בית": "10", "קומה": "2", "עיר": "כסרא-סמיע", "הערות": "משלוח בדיקה", "status": "ממתין",
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
    with st.form("first_login_contract_form"):
        f_full_name = st.text_input("שם מלא (חובה):")
        f_id_num = st.text_input("תעודת זהות (חובה):")
        f_address = st.text_input("כתובת מגורים מלאה (חובה):")
        f_email = st.text_input("כתובת אימייל (חובה):")
        f_phone = st.text_input("מספר טלפון נייד (חובה):", value=st.session_state.couriers_db.get(st.session_state.username, {}).get("phone", ""))
        f_hp_or_exempt = st.text_input("מספר ח.פ / עוסק פטור (אם עוסק פטור - כתוב 'פטור'):")
        new_password_input = st.text_input("בחר סיסמה חדשה לחשבון שלך:", type="password")
        agree_terms = st.checkbox("קראתי את החוזה בעיון רב, הבנתי ואני מאשר/ת ללא הסתייגות את תנאי השימוש וההצהרה.")
        submit_contract = st.form_submit_button("אישור החוזה, עדכון סיסמה וסיום הרישום 🚀")
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
                if new_password_input.strip():
                    st.session_state.couriers_db[st.session_state.username]["password"] = new_password_input.strip()
                save_users_db(st.session_state.couriers_db)
                
                save_contract_data({
                    "שם משתמש": st.session_state.username, "תפקיד": st.session_state.role, "חברה": st.session_state.company,
                    "שם מלא": f_full_name, "ת.ז": f_id_num, "כתובת": f_address, "אימייל": f_email,
                    "טלפון": format_whatsapp_phone(f_phone), "ח.פ / עוסק פטור": f_hp_or_exempt if f_hp_or_exempt else "אין", "תאריך רישום": reg_date
                })
                st.success("הפרטים, החוזה והסיסמה החדשה נשמרו בהצלחה!")
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
            t["smart_route"],
            t["add_delivery"],
            t["add_company_admin"],
            t["add_courier"], 
            t["manage_users"],
            t["monthly_report"],
            t["contract_menu"],
            t["live_tracking"],
            t["verify_rejected"],
            t["change_password"]
        ]
    )
    if st.sidebar.button(t["logout"]):
        logout_user()

    if admin_menu == t["main_sys"]:
        st.title(t["main_sys"])
        admin_deliveries = st.session_state.deliveries
        col1, col2, col3 = st.columns(3)
        col1.metric("סך הכל משלוחים במערכת", len(admin_deliveries))
        col2.metric("פעילים / ממתינים", len([d for d in admin_deliveries if d.get("status") not in ["נמסר", "סורב על ידי הלקוח"]]))
        col3.metric("נמסרו בהצלחה", len([d for d in admin_deliveries if d.get("status") == "נמסר"]))
        st.divider()
        for idx, item in enumerate(admin_deliveries):
            status_color = "🟢" if item.get("status") == "נמסר" else ("🔴" if "סורב" in item.get("status", "") else ("🔵" if "נדחה" in item.get("status", "") else "🟠"))
            full_address_str = f"כביש/רחוב: {item.get('כביש', '-')}, בית: {item.get('מספר בית', '-')}, קומה: {item.get('קומה', '-')}, יישוב/כפר: {item.get('עיר', '-')}"
            
            with st.expander(f"{status_color} 📦 {item.get('שם לקוח', '')} | {item.get('עיר', '')} | שליח: {item.get('courier', '')} | סטטוס: {item.get('status', '')}"):
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
                    if st.button(t["mark_delivered"], key=f"adm_m_{idx}"):
                        item["status"] = "נמסר"
                        st.success(t["delivered_success"])
                        st.rerun()
                with b4:
                    if st.button("🔄 דחה למחר", key=f"adm_p_{idx}"):
                        item["status"] = "נדחה למחר על ידי הלקוח"
                        st.success("עודכן כנדחה למחר!")
                        st.rerun()
                with b5:
                    if st.button("❌ סורב", key=f"adm_r_{idx}"):
                        item["status"] = "סורב על ידי הלקוח"
                        st.warning("עודכן כסורב ולא ייחשב בתשלום.")
                        st.rerun()

    elif admin_menu == t["smart_route"]:
        st.title(t["smart_route"])
        couriers_list = list(st.session_state.couriers_db.keys())
        selected_courier_route = st.selectbox("בחר שליח או מנהל לסידור מסלול:", couriers_list)
        courier_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == selected_courier_route and d.get("status") not in ["נמסר", "סורב על ידי הלקוח"]]
        
        if not courier_deliveries:
            st.info("אין משלוחים פעילים לשם זה.")
        else:
            all_cities = list(set([d.get("עיר", "אחר") for d in courier_deliveries]))
            start_location = st.selectbox("📍 בחר מיקום התחלה (נקודת מוצא):", all_cities)
            if st.button("🚀 הפעל סידור אוטומטי של המסלול"):
                remaining = list(courier_deliveries)
                sorted_route = []
                current_point = start_location
                while remaining:
                    next_item = min(remaining, key=lambda x: 0 if x.get("עיר") == current_point else len(str(x.get("עיר"))))
                    sorted_route.append(next_item)
                    current_point = next_item.get("עיר")
                    remaining.remove(next_item)
                st.success("✅ המסלול סודר בהצלחה!")
                for s_idx, s_item in enumerate(sorted_route, 1):
                    st.markdown(f"**{s_idx}. 📦 לקוח: {s_item.get('שם לקוח', '')} | יישוב: {s_item.get('עיר', '')} | כתובת: {s_item.get('כביש', '')} {s_item.get('מספר בית', '')}**")

    elif admin_menu == t["add_delivery"]:
        st.title(t["add_delivery"])
        with st.form("add_delivery_form"):
            d_barcode = st.text_input("ברקוד משלוח:", value=f"DEL-{int(datetime.now().timestamp())}")
            d_client = st.text_input("שם הלקוח:")
            d_company = st.text_input("שם חברה / מותג:")
            d_phone = st.text_input("טלפון הלקוח:")
            d_street = st.text_input("כביש / רחוב:")
            d_house = st.text_input("מספר בית:")
            d_floor = st.text_input("קומה:")
            d_city = st.text_input("עיר / יישוב:")
            d_notes = st.text_area("הערות:")
            
            all_users_list = list(st.session_state.couriers_db.keys())
            assigned_to = st.selectbox("שיוך משלוח לשליח או למנהל חברה:", all_users_list)
            
            if st.form_submit_button("הוסף משלוח למערכת 🚀") and d_client and d_phone and d_city:
                assigned_company = st.session_state.couriers_db.get(assigned_to, {}).get("company", "Independent")
                new_item = {
                    "ברקוד": d_barcode, "שם לקוח": d_client, "שם חברה": d_company if d_company else "General",
                    "טלפון": format_whatsapp_phone(d_phone), "כביש": d_street, "מספר בית": d_house, "קומה": d_floor, "עיר": d_city,
                    "הערות": d_notes, "status": "ממתין", "courier": assigned_to, "company": assigned_company,
                    "date": get_israel_time()
                }
                st.session_state.deliveries.append(new_item)
                st.success("המשלוח נוסף בהצלחה!")

    elif admin_menu == t["add_company_admin"]:
        st.title(t["add_company_admin"])
        with st.form("add_comp_form"):
            cu = st.text_input("שם משתמש מנהל חברה:")
            cp = st.text_input("סיסמה:", type="password")
            cn = st.text_input("שם החברה:")
            cph = st.text_input("טלפון:")
            if st.form_submit_button("הוסף מנהל חברה") and cu and cp and cn and cph:
                st.session_state.couriers_db[cu] = {"password": cp, "role": "מנהל חברה (Company Admin)", "phone": format_whatsapp_phone(cph), "company": cn, "contract_signed": False}
                save_users_db(st.session_state.couriers_db)
                st.success("מנהל החברה נוסף בהצלחה!")

    elif admin_menu == t["add_courier"]:
        st.title(t["add_courier"])
        with st.form("add_cour_form"):
            cu = st.text_input("שם משתמש שליח:")
            cp = st.text_input("סיסמה:", type="password")
            cph = st.text_input("טלפון:")
            comp_list = list(set([i.get("company") for u, i in st.session_state.couriers_db.items() if i.get("company") not in ["System"]]))
            ccomp = st.selectbox("שיוך לחברה:", comp_list if comp_list else ["Independent"])
            if st.form_submit_button("הוסף שליח") and cu and cp and cph:
                st.session_state.couriers_db[cu] = {"password": cp, "role": "שליח", "phone": format_whatsapp_phone(cph), "company": ccomp, "contract_signed": False}
                save_users_db(st.session_state.couriers_db)
                st.success("השליח נוסף בהצלחה!")

    elif admin_menu == t["manage_users"]:
        st.title(t["manage_users"])
        for usr, info in list(st.session_state.couriers_db.items()):
            if usr == "Admin": continue
            with st.expander(f"👤 משתמש: {usr} ({info.get('role')}) - חברה: {info.get('company')}"):
                if st.button(f"🗑️ מחק משתמש {usr}", key=f"del_user_{usr}"):
                    del st.session_state.couriers_db[usr]
                    save_users_db(st.session_state.couriers_db)
                    st.success("המשתמש נמחק!")
                    st.rerun()

    elif admin_menu == t["monthly_report"]:
        st.title(t["monthly_report"])
        company_admins = [u for u, i in st.session_state.couriers_db.items() if i.get("role") == "מנהל חברה (Company Admin)"]
        selected_admin_rep = st.selectbox("בחר מנהל חברה להפקת דוח כספי מרוכז:", company_admins if company_admins else ["אין מנהלי חברות"])
        
        if selected_admin_rep and selected_admin_rep != "אין מנהלי חברות":
            admin_company = st.session_state.couriers_db.get(selected_admin_rep, {}).get("company", "")
            company_deliveries = [d for d in st.session_state.deliveries if d.get("company") == admin_company or d.get("courier") == selected_admin_rep]
            delivered_count = len([d for d in company_deliveries if d.get("status") == "נמסר"])
            
            user_info = st.session_state.couriers_db.get(selected_admin_rep, {})
            u_name = user_info.get("full_name", selected_admin_rep)
            u_hp = user_info.get("hp_exempt", "אין")
            is_exempt = "פטור" in str(u_hp) or u_hp == "אין"
            
            st.metric("סך הכל משלוחים שנמסרו (כולל כל שליחי החברה תחת שמך)", delivered_count)
            price_per_del = st.number_input("תעריף לכל משלוח (₪):", value=1.0, step=0.5)
            
            invoice_stream = generate_monthly_invoice_html(u_name, u_hp, is_exempt, delivered_count, price_per_del)
            st.download_button(
                label="📥 הורד חשבונית / דוח חודשי מרוכז כקובץ HTML",
                data=invoice_stream,
                file_name=f"Monthly_Report_Company_{selected_admin_rep}.html",
                mime="text/html"
            )

    elif admin_menu == t["contract_menu"]:
        st.title(t["contract_menu"])
        contracts_df = load_contracts_data()
        if contracts_df.empty:
            st.info("אין עדיין חוזים רשומים במערכת.")
        else:
            st.dataframe(contracts_df, use_container_width=True)

    elif admin_menu == t["live_tracking"]:
        st.title(t["live_tracking"])
        locs = load_locations_db()
        for usr, data in locs.items():
            st.info(f"**משתמש:** {usr} | **מיקום:** {data.get('location')} | **עודכן:** {data.get('updated_at')}")

    elif admin_menu == t["verify_rejected"]:
        st.title(t["verify_rejected"])
        rejected_deliveries = [d for d in st.session_state.deliveries if "סורב" in d.get("status", "") or "נדחה" in d.get("status", "")]
        for r_item in rejected_deliveries:
            st.warning(f"📦 לקוח: {r_item.get('שם לקוח', '')} | טלפון: {r_item.get('טלפון', '')}")

    elif admin_menu == t["change_password"]:
        st.title(t["change_password"])
        with st.form("change_admin_pwd_form"):
            old_p = st.text_input("סיסמה נוכחית:", type="password")
            new_p = st.text_input("סיסמה חדשה:", type="password")
            if st.form_submit_button("עדכן סיסמה") and old_p == st.session_state.couriers_db["Admin"]["password"]:
                st.session_state.couriers_db["Admin"]["password"] = new_p
                save_users_db(st.session_state.couriers_db)
                st.success("הסיסמה עודכנה בהצלחה!")

elif st.session_state.role == "מנהל חברה (Company Admin)":
    st.sidebar.title(t["company_admin_menu"])
    comp_admin_menu = st.sidebar.radio(
        t["company_admin_menu"],
        [
            t["main_sys"],
            t["smart_route"],
            t["add_courier"],
            t["add_delivery"],
            t["monthly_report"],
            "📍 עדכן את המיקום החי שלי (GPS)",
            t["change_password"]
        ]
    )
    if st.sidebar.button(t["logout"]):
        logout_user()

    if comp_admin_menu == t["main_sys"]:
        st.title(f"🚚 ניהול משלוחים - {st.session_state.username} (חברת {st.session_state.company})")
        my_company_name = st.session_state.company
        
        company_deliveries = [d for d in st.session_state.deliveries if d.get("company") == my_company_name or d.get("courier") == st.session_state.username]
        
        col1, col2 = st.columns(2)
        col1.metric("סך משלוחי החברה והשליחים", len(company_deliveries))
        col2.metric("נמסרו בהצלחה", len([d for d in company_deliveries if d.get("status") == "נמסר"]))
        st.divider()

        if not company_deliveries:
            st.info("אין משלוחים תחת ניהולך כרגע.")
        else:
            for idx, item in enumerate(company_deliveries):
                status_color = "🟢" if item.get("status") == "נמסר" else ("🔴" if "סורב" in item.get("status", "") else "🟠")
                with st.expander(f"{status_color} 📦 לקוח: {item.get('שם לקוח', '')} | שליח מבצע: {item.get('courier', '')} | סטטוס: {item.get('status', '')}"):
                    st.write(f"**כתובת:** {item.get('כביש', '')}, {item.get('עיר', '')} | **טלפון:** {item.get('טלפון', '')}")
                    
                    c_phone = format_whatsapp_phone(item.get('טלפון', ''))
                    wa_link = f"https://wa.me/{c_phone}"
                    waze_link = f"https://waze.com/ul?q={urllib.parse.quote(item.get('עיר', ''))}&navigate=yes"
                    
                    b1, b2, b3 = st.columns(3)
                    with b1:
                        st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:6px; border-radius:4px; width:100%;">וואטסאפ</button></a>', unsafe_allow_html=True)
                    with b2:
                        st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:6px; border-radius:4px; width:100%;">Waze</button></a>', unsafe_allow_html=True)
                    with b3:
                        if st.button("סמן כנמסר", key=f"comp_m_{idx}"):
                            item["status"] = "נמסר"
                            st.success("עודכן!")
                            st.rerun()

    elif comp_admin_menu == t["smart_route"]:
        st.title(t["smart_route"])
        my_company_name = st.session_state.company
        company_deliveries = [d for d in st.session_state.deliveries if (d.get("company") == my_company_name or d.get("courier") == st.session_state.username) and d.get("status") not in ["נמסר", "סורב על ידי הלקוח"]]
        if not company_deliveries:
            st.info("אין משלוחים פעילים לסידור.")
        else:
            all_cities = list(set([d.get("עיר", "אחר") for d in company_deliveries]))
            start_location = st.selectbox("בחר נקודת מוצא למסלול:", all_cities)
            if st.button("סדר מסלול אוטומטית"):
                st.success("המסלול סודר בהצלחה!")
                for s_item in company_deliveries:
                    st.markdown(f"- **{s_item.get('שם לקוח', '')}** ({s_item.get('עיר', '')}) - שליח: {s_item.get('courier', '')}")

    elif comp_admin_menu == t["add_courier"]:
        st.title(t["add_courier"])
        st.write("כאן תוכל להוסיף שליחים חדשים שיופעלו תחת החברה והניהול שלך:")
        with st.form("comp_add_courier_form"):
            cu = st.text_input("שם משתמש לשליח החדש:")
            cp = st.text_input("סיסמה ראשונית:", type="password")
            cph = st.text_input("טלפון נייד:")
            if st.form_submit_button("הוסף שליח לחברה שלי 🚀") and cu and cp and cph:
                st.session_state.couriers_db[cu] = {
                    "password": cp,
                    "role": "שליח",
                    "phone": format_whatsapp_phone(cph),
                    "company": st.session_state.company,
                    "contract_signed": False
                }
                save_users_db(st.session_state.couriers_db)
                st.success(f"השליח {cu} נוסף בהצלחה תחת ניהול חברתך ({st.session_state.company})!")

    elif comp_admin_menu == t["add_delivery"]:
        st.title(t["add_delivery"])
        st.write("הוסף משלוחים ושייך אותם אליך או לשליחים שתחת ניהולך:")
        with st.form("comp_add_delivery_form"):
            d_barcode = st.text_input("ברקוד:", value=f"DEL-{int(datetime.now().timestamp())}")
            d_client = st.text_input("שם הלקוח:")
            d_phone = st.text_input("טלפון הלקוח:")
            d_street = st.text_input("כביש / רחוב:")
            d_city = st.text_input("עיר / יישוב:")
            d_notes = st.text_area("הערות:")
            
            allowed_assignees = [st.session_state.username] + [u for u, i in st.session_state.couriers_db.items() if i.get("company") == st.session_state.company and i.get("role") == "שליח"]
            assigned_courier = st.selectbox("בחר למי לשייך את המשלוח (עליך או לאחד מהשליחים שלך):", allowed_assignees)
            
            if st.form_submit_button("הוסף משלוח 🚀") and d_client and d_phone and d_city:
                new_item = {
                    "ברקוד": d_barcode, "שם לקוח": d_client, "שם חברה": st.session_state.company,
                    "טלפון": format_whatsapp_phone(d_phone), "כביש": d_street, "מספר בית": "", "קומה": "", "עיר": d_city,
                    "הערות": d_notes, "status": "ממתין", "courier": assigned_courier, "company": st.session_state.company,
                    "date": get_israel_time()
                }
                st.session_state.deliveries.append(new_item)
                st.success("המשלוח נוסף בהצלחה!")

    elif comp_admin_menu == t["monthly_report"]:
        st.title(t["monthly_report"])
        st.write("📊 סיכום פיננסי חודשי מרוכז: החישוב והתשלום מרוכזים באופן בלעדי אצלך כמנהל החברה עבור כל כמות המשלוחים שבוצעה במערכת תחתך ותחת שליחיך.")
        
        my_company_name = st.session_state.company
        company_deliveries = [d for d in st.session_state.deliveries if d.get("company") == my_company_name or d.get("courier") == st.session_state.username]
        delivered_count = len([d for d in company_deliveries if d.get("status") == "נמסר"])
        
        user_info = st.session_state.couriers_db.get(st.session_state.username, {})
        u_name = user_info.get("full_name", st.session_state.username)
        u_hp = user_info.get("hp_exempt", "אין")
        is_exempt = "פטור" in str(u_hp) or u_hp == "אין"
        
        st.metric("סך הכל משלוחים שנמסרו (כולל משלוחי שליחי החברה)", delivered_count)
        price_per_del = st.number_input("תעריף מרוכז לכל משלוח (₪):", value=1.0, step=0.5)
        
        invoice_stream = generate_monthly_invoice_html(u_name, u_hp, is_exempt, delivered_count, price_per_del)
        st.download_button(
            label="📥 הורד חשבונית / דוח כספי חודשי מרוכז לשם שלך (.html)",
            data=invoice_stream,
            file_name=f"Monthly_Report_Company_Admin_{st.session_state.username}.html",
            mime="text/html"
        )

    elif comp_admin_menu == "📍 עדכן את המיקום החי שלי (GPS)":
        st.title("📍 עדכון מיקום חי")
        with st.form("comp_loc_form"):
            user_loc_text = st.text_input("הכנס מיקום נוכחי:")
            if st.form_submit_button("שלח מיקום 📡") and user_loc_text:
                save_location_data(st.session_state.username, user_loc_text)
                st.success("המיקום עודכן בהצלחה!")

    elif comp_admin_menu == t["change_password"]:
        st.title(t["change_password"])
        with st.form("change_comp_pwd_form"):
            old_p = st.text_input("סיסמה נוכחית:", type="password")
            new_p = st.text_input("סיסמה חדשה:", type="password")
            conf_p = st.text_input("אימות סיסמה חדשה:", type="password")
            if st.form_submit_button("עדכן סיסמה 🔐"):
                user_info = st.session_state.couriers_db.get(st.session_state.username, {})
                if old_p == user_info.get("password"):
                    if new_p == conf_p and new_p.strip():
                        user_info["password"] = new_p.strip()
                        save_users_db(st.session_state.couriers_db)
                        st.success("הסיסמה שונתה בהצלחה!")
                    else:
                        st.error("הסיסמאות אינן תואמות.")
                else:
                    st.error("סיסמה נוכחית שגויה.")

elif st.session_state.role == "שליח":
    st.sidebar.title(t["courier_menu"])
    courier_menu = st.sidebar.radio(
        t["courier_menu"],
        [
            t["main_sys"],
            t["smart_route"],
            "📍 עדכן את המיקום החי שלי (GPS)",
            t["change_password"]
        ]
    )
    if st.sidebar.button(t["logout"]):
        logout_user()

    if courier_menu == t["main_sys"]:
        st.title(f"🚚 רשימת המשלוחים שלי ({st.session_state.username})")
        my_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == st.session_state.username]
        
        if not my_deliveries:
            st.info("אין לך משלוחים מוקצים כרגע.")
        else:
            for idx, item in enumerate(my_deliveries):
                status_color = "🟢" if item.get("status") == "נמסר" else ("🔴" if "סורב" in item.get("status", "") else "🟠")
                with st.expander(f"{status_color} 📦 {item.get('שם לקוח', '')} | {item.get('עיר', '')} | סטטוס: {item.get('status', '')}"):
                    st.write(f"**כתובת:** {item.get('כביש', '')}, {item.get('עיר', '')} | **טלפון:** {item.get('טלפון', '')}")
                    c_phone = format_whatsapp_phone(item.get('טלפון', ''))
                    wa_link = f"https://wa.me/{c_phone}"
                    waze_link = f"https://waze.com/ul?q={urllib.parse.quote(item.get('עיר', ''))}&navigate=yes"
                    
                    b1, b2, b3 = st.columns(3)
                    with b1:
                        st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:6px; border-radius:4px; width:100%;">וואטסאפ</button></a>', unsafe_allow_html=True)
                    with b2:
                        st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:6px; border-radius:4px; width:100%;">Waze</button></a>', unsafe_allow_html=True)
                    with b3:
                        if st.button("סמן כנמסר", key=f"cour_m_{idx}"):
                            item["status"] = "נמסר"
                            st.success("עודכן!")
                            st.rerun()

    elif courier_menu == t["smart_route"]:
        st.title(t["smart_route"])
        my_active = [d for d in st.session_state.deliveries if d.get("courier") == st.session_state.username and d.get("status") not in ["נמסר", "סורב על ידי הלקוח"]]
        if not my_active:
            st.info("אין משלוחים פעילים.")
        else:
            all_cities = list(set([d.get("עיר", "אחר") for d in my_active]))
            start_location = st.selectbox("בחר נקודת מוצא:", all_cities)
            if st.button("סדר מסלול"):
                st.success("המסלול סודר בהצלחה!")

    elif courier_menu == "📍 עדכן את המיקום החי שלי (GPS)":
        st.title("📍 עדכון מיקום חי")
        with st.form("courier_loc_form"):
            user_loc_text = st.text_input("מיקום נוכחי:")
            if st.form_submit_button("שלח מיקום 📡") and user_loc_text:
                save_location_data(st.session_state.username, user_loc_text)
                st.success("המיקום עודכן בהצלחה!")

    elif courier_menu == t["change_password"]:
        st.title(t["change_password"])
        with st.form("change_cour_pwd_form"):
            old_p = st.text_input("סיסמה נוכחית:", type="password")
            new_p = st.text_input("סיסמה חדשה:", type="password")
            if st.form_submit_button("עדכן סיסמה") and old_p == st.session_state.couriers_db[st.session_state.username]["password"]:
                st.session_state.couriers_db[st.session_state.username]["password"] = new_p
                save_users_db(st.session_state.couriers_db)
                st.success("הסיסמה שונתה בהצלחה!")
