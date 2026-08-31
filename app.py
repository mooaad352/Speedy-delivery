import streamlit as st
import urllib.parse
from datetime import datetime, timezone, timedelta
import pandas as pd
import os
import json
from io import BytesIO

ISRAEL_OFFSET = timedelta(hours=2)
ADMIN_PHONE = "972502616375"
VAT_RATE = 0.18    # מע"מ 18%

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
        3. <strong>אחריות בלעדית של השליח:</strong> השליח נושא באחריות המלאה והבלעדית לכל נזק או אובדן במשלוח.<br><br>
        4. <strong>פטור מלא מאחריות למפעיל המערכת:</strong> מפעיל המערכת פטור מאחריות לנזקי גוף, רכוש ותאונות.<br><br>
        5. <strong>תשלומים והתחייבות פיננסית:</strong> השליח/מנהל מתחייב להסדיר את התשלומים בהתאם למשלוחים שבוצעו וטופלו במערכת.<br><br>
        6. <strong>הרשאה מלאה לבדיקת משלוחים שסורבו:</strong> ניתנת בזה הרשאה מלאה ובלעדית למפעיל המערכת לבדוק, ליצור קשר ולוודא באופן ישיר מול הלקוחות את כל המשלוחים שדווחו כסורבים או נדחו.<br><br>
        7. <strong>זכות תביעה אישית:</strong> מפעיל המערכת רשאי להגיש תביעה משפטית אישית בגין אי-הסדרת תשלום.<br><br>
        8. <strong>שיפוי:</strong> השליח מתחייב לשפות את מפעיל המערכת בגין כל נזק.
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
            <h2>מקארט (Speedy Delivery) - דוח וחשבון חודשי</h2>
            <p>סיכום פעילות עסקית</p>
        </div>
        <div class="invoice-details">
            <p><strong>חודש דיווח:</strong> {current_month_str}</p>
            <p><strong>תאריך הפקה:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
    </header>

    <section>
        <h3>פרטי נותן השירות / השליח:</h3>
        <p><strong>שם מלא / עסק:</strong> {user_name}</p>
        <p><strong>ח.פ / ת.ז / עוסק פטור:</strong> {user_hp}</p>
        <p><strong>סטטוס מס:</strong> {'עוסק פטור (ללא מע"מ)' if is_exempt else 'חייב במע"מ (כולל מע"מ 18%)'}</p>
    </section>

    <table>
        <thead>
            <tr>
                <th>תיאור הפעילות</th>
                <th>כמות משלוחים מזוכים</th>
                <th>תעריף ליחידה</th>
                <th>סה"כ לפני מע"מ</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>משלוחים שבוצעו וטופלו בהצלחה החודש</td>
                <td>{count_deliveries}</td>
                <td>₪{price_per_unit:.2f}</td>
                <td>₪{base_price:.2f}</td>
            </tr>
        </tbody>
    </table>

    <div class="totals">
        <div>סכום לפני מע"מ: <strong>₪{base_price:.2f}</strong></div>
        {"" if is_exempt else f'<div>מע"מ (18%): <strong>₪{vat_amount:.2f}</strong></div>'}
        <div class="final-amount">סכום סופי לתשלום: ₪{total_final:.2f}</div>
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

def load_users_db():
    default_users = {
        "Admin": {"password": "Sma.srablove2028", "role": "מנהל מערכת ראשי (Super Admin)", "phone": ADMIN_PHONE, "company": "System", "contract_signed": True},
        "mohammad": {"password": "123", "role": "שליח", "phone": "972502616375", "company": "Independent", "contract_signed": True}
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
        "login_title": "כניסת משתמשים ושליחים",
        "username": "שם משתמש",
        "password": "סיסמה",
        "login_btn": "התחבר",
        "login_error": "שם משתמש או סיסמה שגויים.",
        "logout": "התנתק (Logout)",
        "admin_menu": "תפריט ניהול ראשי",
        "courier_menu": "תפריט מנהל חברה",
        "main_sys": "מערכת משלוחים ראשית",
        "smart_route": "🗺️ סידור מסלול משלוחים אוטומטי (מרחקי GPS)",
        "add_delivery": "➕ הוספת משלוח חדש",
        "add_courier": "הוספת שליח חדש",
        "add_company_admin": "הוספת מנהל חברת משלוחים",
        "manage_users": "ניהול סיסמאות ומשתמשים",
        "monthly_report": "📊 סיכום חודשי ודוחות",
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
        "login_title": "تسجيل دخول المستخدمين والمندوبين",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_btn": "تسجيل الدخول",
        "login_error": "خطأ في اسم المستخدم أو كلمة المرور.",
        "logout": "تسجيل الخروج",
        "admin_menu": "قائمة الإدارة الرئيسية",
        "courier_menu": "قائمة مدير الشركة",
        "main_sys": "نظام الشحنات الرئيسي",
        "smart_route": "🗺️ ترتيب مسار الشحنات تلقائياً",
        "add_delivery": "➕ إضافة شحنة جديدة",
        "add_courier": "إضافة مندوب جديد",
        "add_company_admin": "إضافة مدير شركة توصيل",
        "manage_users": "إدارة كلمات المرور والمستخدمين",
        "monthly_report": "📊 تقرير الحسابات والعمولات",
        "contract_menu": "📝 سجل العقود والبيانات المسجلة",
        "live_tracking": "📍 متابعة مواقع الشليחים (GPS)",
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

if "saved_routes" not in st.session_state:
    st.session_state.saved_routes = {}

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
        f_hp_or_exempt = st.text_input("מספר ח.פ / עוסק פטור (אם עוסק פטור - כתוב 'פטור' או מספר עוסק פטור):")
        new_password_input = st.text_input("בחר סיסמה חדשה לחשבון שלך:", type="password")
        agree_terms = st.checkbox("קראתי את החוזה בעיון רב, הבנתי ואני מאשר/ת ללא הסתייגות את תנאי השימוש, ההצהרה, הרשאת הבדיקה למפעיל ופטור האחריות.")
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
            status_color = "🟢" if item.get("status") == "נמסר" else ("🔴" if "סורב" in item.get("status", "") else "🟠")
            full_address_str = f"כביש/רחוב: {item.get('כביש', '-')}, בית: {item.get('מספר בית', '-')}, קומה: {item.get('קומה', '-')}, יישוב: {item.get('עיר', '-')}"
            
            with st.expander(f"{status_color} 📦 {item.get('שם לקוח', '')} | {item.get('עיר', '')} | סטטוס: {item.get('status', '')}"):
                st.write(f"**ברקוד:** {item.get('ברקוד', '')} | **טלפון:** {item.get('טלפון', '')} | **כתובת:** {full_address_str}")
                
                c_phone = format_whatsapp_phone(item.get('טלפון', ''))
                company_name = item.get('שם חברה', 'General')
                wa_msg = urllib.parse.quote(f"שלום לך, השליח של {company_name} בדרך אליך! אנא הישאר זמין לקבל את המשלוח.")
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
        courier_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == selected_courier_route and d.get("status"] not in ["נמסר", "סורב על ידי הלקוח"]] # תוקן בצורה בטוחה
        
        if not courier_deliveries:
            st.info("אין משלוחים פעילים לשליח זה.")
        else:
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
                
                for s_idx, s_item in enumerate(sorted_route, 1):
                    st.markdown(f"**{s_idx}. 📦 לקוח: {s_item.get('שם לקוח', '')} | יישוב: {s_item.get('עיר', '')}**")
                    waze_query = urllib.parse.quote(f"{s_item.get('כביש', '')} {s_item.get('מספר בית', '')}, {s_item.get('עיר', '')}")
                    waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                    st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer;">🧭 נווט לתחנה ב-Waze</button></a>', unsafe_allow_html=True)
                    st.divider()

    elif admin_menu == t["add_delivery"]:
        st.title(t["add_delivery"])
        with st.form("add_delivery_form"):
            d_barcode = st.text_input("ברקוד משלוח:", value=f"DEL-{int(datetime.now().timestamp())}")
            d_client = st.text_input("שם הלקוח:")
            d_company = st.text_input("שם חברה / מותג (לדוגמה: SHEIN, Amazon, AliExpress):")
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
                st.session_state.couriers_db[cu] = {"password": cp, "role": "מנהל חברה (Company Admin)", "phone": format_whatsapp_phone(cph), "company": cn, "contract_signed": False}
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
                st.session_state.couriers_db[cu] = {"password": cp, "role": "שליח", "phone": format_whatsapp_phone(cph), "company": ccomp, "contract_signed": False}
                save_users_db(st.session_state.couriers_db)
                st.success("השליח נוסף בהצלחה!")

    elif admin_menu == t["manage_users"]:
        st.title("🔑 ניהול וצפייה בסיסמאות כל המשתמשים במערכת")
        st.info("כאן תוכל לראות את כל המשתמשים הרשומים (מנהלים ושליחים), כולל הסיסמה הנוכחית של כל אחד מהם, לעדכן אותה או למחוק משתמשים לפי הצורך.")
        
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

    elif admin_menu == t["monthly_report"]:
        st.title(t["monthly_report"])
        st.write("הפקת דוח חודשי וחישוב עמלות:")
        all_couriers = [u for u, i in st.session_state.couriers_db.items() if i.get("role") == "שליח"]
        selected_c_rep = st.selectbox("בחר שליח לדוח:", all_couriers if all_couriers else ["אין שליחים"])
        if selected_c_rep:
            delivered_count = len([d for d in st.session_state.deliveries if d.get("courier") == selected_c_rep and d.get("status") == "נמסר"])
            c_info = st.session_state.couriers_db.get(selected_c_rep, {})
            is_exempt = "פטור" in str(c_info.get("hp_exempt", ""))
            invoice_stream = generate_monthly_invoice_html(selected_c_rep, c_info.get("hp_exempt", "אין"), is_exempt, delivered_count, price_per_unit=10.0)
            st.download_button(
                label=f"📥 הורד חשבונית / סיכום חודשי עבור {selected_c_rep} (.html)",
                data=invoice_stream,
                file_name=f"invoice_{selected_c_rep}.html",
                mime="text/html"
            )

    elif admin_menu == t["contract_menu"]:
        st.title(t["contract_menu"])
        contracts_df = load_contracts_data()
        st.dataframe(contracts_df)

    elif admin_menu == t["change_password"]:
        st.title(t["change_password"])
        with st.form("admin_change_pwd"):
            old_p = st.text_input("סיסמה נוכחית:", type="password")
            new_p = st.text_input("סיסמה חדשה:", type="password")
            if st.form_submit_button("עדכן סיסמה") and old_p == st.session_state.couriers_db["Admin"]["password"]:
                st.session_state.couriers_db["Admin"]["password"] = new_p
                save_users_db(st.session_state.couriers_db)
                st.success("הסיסמה עודכנה בהצלחה!")

elif st.session_state.role == "מנהל חברה (Company Admin)":
    st.sidebar.title(f"מנהל חברה: {st.session_state.company}")
    comp_menu = st.sidebar.radio(
        t["courier_menu"],
        [
            t["main_sys"],
            t["smart_route"],
            t["add_delivery"],
            t["add_courier"],
            t["manage_users"],
            t["change_password"]
        ]
    )
    if st.sidebar.button(t["logout"]):
        logout_user()

    current_company = st.session_state.company
    company_couriers = [u for u, i in st.session_state.couriers_db.items() if i.get("company") == current_company and i.get("role") == "שליח"]

    if comp_menu == t["main_sys"]:
        st.title(f"📦 ניהול משלוחי חברה: {current_company}")
        comp_deliveries = [d for d in st.session_state.deliveries if d.get("company") == current_company or d.get("courier") in company_couriers]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("סך משלוחי חברה", len(comp_deliveries))
        col2.metric("פעילים / ממתינים", len([d for d in comp_deliveries if d.get("status") not in ["נמסר", "סורב על ידי הלקוח"]]))
        col3.metric("נמסרו בהצלחה", len([d for d in comp_deliveries if d.get("status") == "נמסר"]))
        st.divider()

        for idx, item in enumerate(comp_deliveries):
            status_color = "🟢" if item.get("status") == "נמסר" else ("🔴" if "סורב" in item.get("status", "") else "🟠")
            full_address_str = f"כביש/רחוב: {item.get('כביש', '-')}, בית: {item.get('מספר בית', '-')}, קומה: {item.get('קומה', '-')}, יישוב: {item.get('עיר', '-')}"
            
            with st.expander(f"{status_color} 📦 לקוח: {item.get('שם לקוח', '')} | עיר: {item.get('עיר', '')} | שליח: {item.get('courier', '')}"):
                st.write(f"**ברקוד:** {item.get('ברקוד', '')} | **טלפון:** {item.get('טלפון', '')} | **כתובת:** {full_address_str}")
                
                c_phone = format_whatsapp_phone(item.get('טלפון', ''))
                company_name = item.get('שם חברה', current_company)
                wa_msg = urllib.parse.quote(f"שלום לך, השליח של {company_name} בדרך אליך! אנא הישאר זמין לקבל את המשלוח.")
                wa_link = f"https://wa.me/{c_phone}?text={wa_msg}"
                waze_query = urllib.parse.quote(f"{item.get('כביש', '')} {item.get('מספר בית', '')}, {item.get('עיר', '')}")
                waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                
                b1, b2, b3 = st.columns(3)
                with b1:
                    st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["whatsapp_btn"]}</button></a>', unsafe_allow_html=True)
                with b2:
                    st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["waze_btn"]}</button></a>', unsafe_allow_html=True)
                with b3:
                    if st.button(t["mark_delivered"], key=f"comp_m_{idx}"):
                        item["status"] = "נמסר"
                        st.success(t["delivered_success"])
                        st.rerun()

    elif comp_menu == t["smart_route"]:
        st.title(t["smart_route"])
        selected_courier_route = st.selectbox("בחר שליח לסידור מסלול:", company_couriers if company_couriers else ["אין שליחים"])
        courier_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == selected_courier_route and d.get("status") not in ["נמסר", "סורב על ידי הלקוח"]]
        
        if not courier_deliveries:
            st.info("אין משלוחים פעילים לשליח זה.")
        else:
            all_cities = list(set([d.get("עיר", "אחר") for d in courier_deliveries]))
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                start_location = st.selectbox("📍 בחר נקודת התחלה (מוצא):", all_cities, key="comp_start_loc")
            with col_s2:
                end_location = st.selectbox("🏁 בחר נקודת סיום (יעד סופי):", all_cities, key="comp_end_loc")
            
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
                
                for s_idx, s_item in enumerate(sorted_route, 1):
                    st.markdown(f"**{s_idx}. 📦 לקוח: {s_item.get('שם לקוח', '')} | יישוב: {s_item.get('עיר', '')}**")
                    waze_query = urllib.parse.quote(f"{s_item.get('כביש', '')} {s_item.get('מספר בית', '')}, {s_item.get('עיר', '')}")
                    waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                    st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer;">🧭 נווט לתחנה ב-Waze</button></a>', unsafe_allow_html=True)
                    st.divider()

    elif comp_menu == t["add_delivery"]:
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
            assigned_courier = st.selectbox("שיוך שליח:", company_couriers if company_couriers else ["אין שליחים"])
            
            if st.form_submit_button("הוסף משלוח למערכת 🚀") and d_client and d_phone and d_city:
                new_item = {
                    "ברקוד": d_barcode, "שם לקוח": d_client, "שם חברה": current_company,
                    "טלפון": format_whatsapp_phone(d_phone), "כביש": d_street, "מספר בית": d_house, "קומה": d_floor, "עיר": d_city,
                    "הערות": d_notes, "status": "ממתין", "courier": assigned_courier, "company": current_company, "date": get_israel_time()
                }
                st.session_state.deliveries.append(new_item)
                st.success("המשלוח נוסף בהצלחה!")

    elif comp_menu == t["add_courier"]:
        st.title("➕ הוספת שליח לחברה")
        with st.form("comp_add_cour_form"):
            cu = st.text_input("שם משתמש שליח:")
            cp = st.text_input("סיסמה:", type="password")
            cph = st.text_input("טלפון:")
            if st.form_submit_button("הוסף שליח") and cu and cp and cph:
                st.session_state.couriers_db[cu] = {"password": cp, "role": "שליח", "phone": format_whatsapp_phone(cph), "company": current_company, "contract_signed": False}
                save_users_db(st.session_state.couriers_db)
                st.success("השליח נוסף בהצלחה לחברה שלך!")

    elif comp_menu == t["manage_users"]:
        st.title("🔑 ניהול שליחי החברה וסיסמאות")
        for usr, info in list(st.session_state.couriers_db.items()):
            if info.get("company") == current_company and info.get("role") == "שליח":
                with st.expander(f"👤 {usr}"):
                    st.markdown(f"**סיסמה נוכחית:** `{info.get('password', '')}`")
                    st.markdown(f"**טלפון:** `{info.get('phone', '-')}`")
                    with st.form(f"comp_change_pwd_{usr}"):
                        new_c_pwd = st.text_input("סיסמה חדשה לשליח:", type="password")
                        if st.form_submit_button("עדכן סיסמה"):
                            if new_c_pwd.strip():
                                st.session_state.couriers_db[usr]["password"] = new_c_pwd.strip()
                                save_users_db(st.session_state.couriers_db)
                                st.success("הסיסמה עודכנה בהצלחה!")
                                st.rerun()

    elif comp_menu == t["change_password"]:
        st.title(t["change_password"])
        with st.form("comp_admin_change_pwd"):
            old_p = st.text_input("סיסמה נוכחית:", type="password")
            new_p = st.text_input("סיסמה חדשה:", type="password")
            if st.form_submit_button("עדכן סיסמה") and old_p == st.session_state.couriers_db[st.session_state.username]["password"]:
                st.session_state.couriers_db[st.session_state.username]["password"] = new_p
                save_users_db(st.session_state.couriers_db)
                st.success("הסיסמה עודכנה בהצלחה!")

elif st.session_state.role == "שליח":
    st.sidebar.title(f"שליח: {st.session_state.username}")
    courier_menu = st.sidebar.radio(
        "תפריט שליח",
        [
            "📦 המשלוחים שלי",
            "➕ הוספת משלוח",
            "🗺️ מסלול מומלץ",
            "🔐 החלפת סיסמה"
        ]
    )
    if st.sidebar.button(t["logout"]):
        logout_user()

    my_username = st.session_state.username
    my_company = st.session_state.couriers_db.get(my_username, {}).get("company", "Independent")
    my_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == my_username]

    if courier_menu == "📦 המשלוחים שלי":
        st.title("📦 המשלוחים המוקצים אליך")
        col1, col2, col3 = st.columns(3)
        col1.metric("סך הכל משלוחים", len(my_deliveries))
        col2.metric("ממתינים לביצוע", len([d for d in my_deliveries if d.get("status") not in ["נמסר", "סורב על ידי הלקוח"]]))
        col3.metric("נמסרו בהצלחה", len([d for d in my_deliveries if d.get("status"] == "נמסר"]))
        st.divider()

        for idx, item in enumerate(my_deliveries):
            status_color = "🟢" if item.get("status") == "נמסר" else ("🔴" if "סורב" in item.get("status", "") else "🟠")
            full_address_str = f"כביש/רחוב: {item.get('כביש', '-')}, בית: {item.get('מספר בית', '-')}, קומה: {item.get('קומה', '-')}, יישוב: {item.get('עיר', '-')}"
            
            with st.expander(f"{status_color} 📦 לקוח: {item.get('שם לקוח', '')} | עיר: {item.get('עיר', '')} | סטטוס: {item.get('status', '')}"):
                st.write(f"**ברקוד:** {item.get('ברקוד', '')} | **טלפון:** {item.get('טלפון', '')} | **כתובת:** {full_address_str}")
                if item.get('הערות'):
                    st.info(f"הערות משלוח: {item.get('הערות')}")
                
                c_phone = format_whatsapp_phone(item.get('טלפון', ''))
                company_name = item.get('שם חברה', 'General')
                wa_msg = urllib.parse.quote(f"שלום לך, השליח של {company_name} בדרך אליך! אנא הישאר זמין לקבל את המשלוח.")
                wa_link = f"https://wa.me/{c_phone}?text={wa_msg}"
                waze_query = urllib.parse.quote(f"{item.get('כביש', '')} {item.get('מספר בית', '')}, {item.get('עיר', '')}")
                waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                
                b1, b2, b3, b4 = st.columns(4)
                with b1:
                    st.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["whatsapp_btn"]}</button></a>', unsafe_allow_html=True)
                with b2:
                    st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["waze_btn"]}</button></a>', unsafe_allow_html=True)
                with b3:
                    if st.button("סמן כנמסר ✅", key=f"cour_m_{idx}"):
                        item["status"] = "נמסר"
                        st.success("הסטטוס עודכן בהצלחה!")
                        st.rerun()
                with b4:
                    if st.button("סורב ❌", key=f"cour_r_{idx}"):
                        item["status"] = "סורב על ידי הלקוח"
                        st.warning("המשלוח עודכן כסורב.")
                        st.rerun()

    elif courier_menu == "➕ הוספת משלוח":
        st.title("➕ הוספת משלוח חדש (שליח)")
        with st.form("courier_add_delivery_form"):
            d_barcode = st.text_input("ברקוד משלוח:", value=f"DEL-{int(datetime.now().timestamp())}")
            d_client = st.text_input("שם הלקוח:")
            d_company = st.text_input("שם חברה / מותג:", value=my_company)
            d_phone = st.text_input("טלפון הלקוח:")
            d_street = st.text_input("כביש / רחוב:")
            d_house = st.text_input("מספר בית:")
            d_floor = st.text_input("קומה:")
            d_city = st.text_input("עיר / יישוב:")
            d_notes = st.text_area("הערות:")
            
            if st.form_submit_button("הוסף משלוח אליי 🚀") and d_client and d_phone and d_city:
                new_item = {
                    "ברקוד": d_barcode, "שם לקוח": d_client, "שם חברה": d_company if d_company else "General",
                    "טלפון": format_whatsapp_phone(d_phone), "כביש": d_street, "מספר בית": d_house, "קומה": d_floor, "עיר": d_city,
                    "הערות": d_notes, "status": "ממתין", "courier": my_username, "company": my_company, "date": get_israel_time()
                }
                st.session_state.deliveries.append(new_item)
                st.success("המשלוח נוסף בהצלחה לרשימת המשלוחים שלך!")

    elif courier_menu == "🗺️ מסלול מומלץ":
        st.title("🗺️ המסלול המומלץ עבורך")
        if my_username in st.session_state.saved_routes:
            saved_route = st.session_state.saved_routes[my_username]
            st.success("נמצא מסלול מוסדר עבורך על ידי המנהל:")
            for s_idx, s_item in enumerate(saved_route, 1):
                st.markdown(f"**{s_idx}. 📦 לקוח: {s_item.get('שם לקוח', '')} | יישוב: {s_item.get('עיר', '')}**")
                waze_query = urllib.parse.quote(f"{s_item.get('כביש', '')} {s_item.get('מספר בית', '')}, {s_item.get('עיר', '')}")
                waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                st.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer;">🧭 נווט לתחנה ב-Waze</button></a>', unsafe_allow_html=True)
                st.divider()
        else:
            st.info("המנהל טרם סידר עבורך מסלול אוטומטי. תוכל לצפות בכל המשלוחים תחת לשונית 'המשלוחים שלי'.")

    elif courier_menu == "🔐 החלפת סיסמה":
        st.title("🔐 החלפת סיסמה אישית")
        with st.form("courier_change_pwd"):
            old_p = st.text_input("סיסמה נוכחית:", type="password")
            new_p = st.text_input("סיסמה חדשה:", type="password")
            if st.form_submit_button("עדכן סיסמה") and old_p == st.session_state.couriers_db[my_username]["password"]:
                st.session_state.couriers_db[my_username]["password"] = new_p
                save_users_db(st.session_state.couriers_db)
                st.success("הסיסמה עודכנה בהצלחה!")
