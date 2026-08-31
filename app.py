import streamlit as str_lit
import urllib.parse
from datetime import datetime, timezone, timedelta
import pandas as pd
import os
import json
from io import BytesIO

ISRAEL_OFFSET = timedelta(hours=2)
ADMIN_PHONE = "972502616375"
VAT_RATE = 0.18  # מע"מ 18%

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

def generate_personal_html_contract(data_dict):
    html_content = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>חוזה חתום - {data_dict.get('שם מלא', '')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 25px; direction: rtl; text-align: right; color: #333; }}
        .container {{ max-width: 750px; margin: auto; background: #ffffff; padding: 35px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); }}
        h2 {{ color: #1f2937; text-align: center; border-bottom: 2px solid #2563eb; padding-bottom: 10px; }}
        .details-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .details-table th, .details-table td {{ border: 1px solid #d1d5db; padding: 10px 14px; text-align: right; font-size: 14px; }}
        .details-table th {{ background-color: #f3f4f6; color: #374151; }}
        .contract-box {{ background: #f9fafb; border: 1px solid #d1d5db; padding: 15px; border-radius: 6px; font-size: 13px; margin-top: 20px; line-height: 1.6; color: #111827; }}
        .signature {{ margin-top: 25px; font-weight: bold; color: #16a34a; text-align: center; font-size: 16px; }}
    </style>
</head>
<body>
<div class="container">
    <h2>📄 טופס התרשמות וחוזה חתום - Speedy Delivery</h2>
    <table class="details-table">
        <tr><th>שם משתמש</th><td>{data_dict.get('שם משתמש', '')}</td></tr>
        <tr><th>תפקיד</th><td>{data_dict.get('תפקיד', '')}</td></tr>
        <tr><th>חברה משוייכת</th><td>{data_dict.get('חברה', '')}</td></tr>
        <tr><th>שם מלא</th><td>{data_dict.get('שם מלא', '')}</td></tr>
        <tr><th>תעודת זהות</th><td>{data_dict.get('ת.ז', '')}</td></tr>
        <tr><th>כתובת מלאה</th><td>{data_dict.get('כתובת', '')}</td></tr>
        <tr><th>אימייל</th><td>{data_dict.get('אימייל', '')}</td></tr>
        <tr><th>טלפון נייד</th><td>{data_dict.get('טלפון', '')}</td></tr>
        <tr><th>ח.פ / עוסק פטור</th><td>{data_dict.get('ח.פ / עוסק פטור', '')}</td></tr>
        <tr><th>תאריך ושעת אישור החוזה</th><td>{data_dict.get('תאריך רישום', '')}</td></tr>
    </table>
    <div class="contract-box">
        <strong>תנאי שימוש, הצהרה ופטור מלא מאחריות משפטית:</strong><br><br>
        1. מערכת "Speedy Delivery" מהווה פלטפורמה טכנולוגית עצמאית.<br>
        2. לא מתקיימים יחסי עובד-מעביד.<br>
        3. השליח אחראי באופן מלא על ניהול המשלוחים במערכת.<br>
        4. פטור מלא מאחריות למפעיל המערכת.<br>
        5. התחייבות לתשלום על המשלוחים שבוצעו וטופלו בתחילת חודש.<br>
        6. <strong>הרשאה מלאה לבדיקת משלוחים שסורבו:</strong> ניתנת בזה הרשאה מלאה ובלעדית למפעיל המערכת לבדוק, ליצור קשר ולוודא באופן ישיר מול הלקוחות את כל המשלוחים שדווחו כסורבים או נדחו.<br>
    </div>
    <div class="signature">✅ החוזה אושר ונחתם דיגיטלית בהצלחה</div>
</div>
</body>
</html>"""
    file_stream = BytesIO(html_content.encode("utf-8"))
    file_stream.seek(0)
    return file_stream

str_lit.set_page_config(page_title="Speedy Delivery - מערכת ניהול משלוחים", page_icon="🚚", layout="wide")

CONTRACTS_FILE = "delivery_drivers_contracts.csv"
USERS_FILE = "couriers_db.json"
LOCATIONS_FILE = "couriers_live_locations.json"

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

def delete_contract_by_index(idx):
    df = load_contracts_data()
    if 0 <= idx < len(df):
        df = df.drop(idx).reset_index(drop=True)
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
        "admin_menu": "תפריט ניהול",
        "main_sys": "מערכת משלוחים ראשית",
        "add_delivery": "➕ הוספת משלוח חדש",
        "add_courier": "הוספת שליח חדש",
        "add_company_admin": "הוספת מנהל חברת משלוחים",
        "manage_users": "ניהול ועריכת משתמשים",
        "monthly_report": "📊 סיכום חודשי ודוחות",
        "contract_menu": "📝 פנקס נרשמים וחוזים שמורים",
        "live_tracking": "📍 מעקב מיקום שליחים בזמן אמת",
        "verify_rejected": "🔍 אימות משלוחים שסורבו מול לקוחות",
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
        "admin_menu": "قائمة الإدارة",
        "main_sys": "نظام الشحنات الرئيسي",
        "add_delivery": "➕ إضافة شحنة جديدة",
        "add_courier": "إضافة مندوب جديد",
        "add_company_admin": "إضافة مدير شركة توصيل",
        "manage_users": "إدارة وتعديل المستخدمين",
        "monthly_report": "📊 تقرير الحسابات والعمولات",
        "contract_menu": "📝 سجل العقود والبيانات المسجلة",
        "live_tracking": "📍 متابعة مواقع الشليחים (GPS)",
        "verify_rejected": "🔍 التحقق من الشحنات المرفوضة مع العملاء",
        "whatsapp_btn": "📲 إرسال واتساب",
        "waze_btn": "🧭 التنقل عبر Waze",
        "mark_delivered": "تحديد كـ تم التسليم",
        "delivered_success": "تم تحديث الحالة بنجاح!"
    }
}

str_lit.sidebar.markdown("---")
lang_choice = str_lit.sidebar.selectbox("🌐 Language / שפה", ["עברית (Hebrew)", "العربية (Arabic)"], index=0)
t = TRANSLATIONS[lang_choice]

str_lit.sidebar.markdown("---")
str_lit.sidebar.subheader("📄 טופס התרשמות וחוזה")
html_contract_file = generate_html_contract_form()
str_lit.sidebar.download_button(
    label="📥 הורד טופס התרשמות וחוזה כללי (.html)",
    data=html_contract_file,
    file_name="delivery_contract_form.html",
    mime="text/html"
)

if "couriers_db" not in str_lit.session_state:
    str_lit.session_state.couriers_db = load_users_db()

query_params = str_lit.query_params

if "logged_in" not in str_lit.session_state:
    if query_params.get("logged_in") == "true" and "username" in query_params:
        str_lit.session_state.logged_in = True
        str_lit.session_state.username = query_params["username"]
        str_lit.session_state.role = query_params.get("role", "שליח")
        str_lit.session_state.company = query_params.get("company", "Independent")
    else:
        str_lit.session_state.logged_in = False
        str_lit.session_state.username = ""
        str_lit.session_state.role = ""
        str_lit.session_state.company = ""

if "deliveries" not in str_lit.session_state:
    current_time_il = get_israel_time()
    str_lit.session_state.deliveries = [{
        "ברקוד": "TEST-001", "שם לקוח": "סמר שומרי", "שם חברה": "SHEIN", "טלפון": "972502616375",
        "כתובת מלאה": "כסרא-סמיע", "עיר": "כסרא-סמיע", "הערות": "משלוח בדיקה", "status": "ממתין",
        "courier": "mohammad", "company": "Independent", "date": current_time_il,
        "rating": 0, "feedback": ""
    }]

def logout_user():
    str_lit.session_state.logged_in = False
    str_lit.session_state.username = ""
    str_lit.session_state.role = ""
    str_lit.session_state.company = ""
    str_lit.query_params.clear()
    str_lit.rerun()

if not str_lit.session_state.logged_in:
    str_lit.title(t["title"])
    str_lit.subheader(t["login_title"])
    with str_lit.form("login_form"):
        username_input = str_lit.text_input(t["username"])
        password_input = str_lit.text_input(t["password"], type="password")
        submit_btn = str_lit.form_submit_button(t["login_btn"])
        if submit_btn:
            db = str_lit.session_state.couriers_db
            if username_input in db and db[username_input]["password"] == password_input:
                str_lit.session_state.logged_in = True
                str_lit.session_state.username = username_input
                str_lit.session_state.role = db[username_input]["role"]
                str_lit.session_state.company = db[username_input].get("company", "Independent")
                str_lit.query_params["logged_in"] = "true"
                str_lit.query_params["username"] = username_input
                str_lit.query_params["role"] = db[username_input]["role"]
                str_lit.query_params["company"] = str_lit.session_state.company
                str_lit.rerun()
            else:
                str_lit.error(t["login_error"])

elif str_lit.session_state.role != "מנהל מערכת ראשי (Super Admin)" and not str_lit.session_state.couriers_db.get(str_lit.session_state.username, {}).get("contract_signed", False):
    str_lit.title("📝 טופס התרשמות, רישום פרטים ותנאי שימוש במערכת")
    with str_lit.form("first_login_contract_form"):
        f_full_name = str_lit.text_input("שם מלא (חובה):")
        f_id_num = str_lit.text_input("תעודת זהות (חובה):")
        f_address = str_lit.text_input("כתובת מלאה (חובה):")
        f_email = str_lit.text_input("כתובת אימייל (חובה):")
        f_phone = str_lit.text_input("מספר טלפון נייד (חובה):", value=str_lit.session_state.couriers_db.get(str_lit.session_state.username, {}).get("phone", ""))
        f_hp_or_exempt = str_lit.text_input("מספר ח.פ / עוסק פטור (אם עוסק פטור - כתוב 'פטור' או מספר עוסק פטור):")
        new_password_input = str_lit.text_input("בחר סיסמה חדשה לחשבון שלך:", type="password")
        agree_terms = str_lit.checkbox("קראתי את החוזה בעיון רב, הבנתי ואני מאשר/ת ללא הסתייגות את תנאי השימוש, ההצהרה, הרשאת הבדיקה למפעיל ופטור האחריות.")
        submit_contract = str_lit.form_submit_button("אישור החוזה, עדכון סיסמה וסיום הרישום 🚀")
        if submit_contract:
            if agree_terms and f_full_name and f_id_num and f_address and f_email and f_phone:
                reg_date = get_israel_time()
                str_lit.session_state.couriers_db[str_lit.session_state.username]["contract_signed"] = True
                str_lit.session_state.couriers_db[str_lit.session_state.username]["full_name"] = f_full_name
                str_lit.session_state.couriers_db[str_lit.session_state.username]["id_number"] = f_id_num
                str_lit.session_state.couriers_db[str_lit.session_state.username]["address"] = f_address
                str_lit.session_state.couriers_db[str_lit.session_state.username]["email"] = f_email
                str_lit.session_state.couriers_db[str_lit.session_state.username]["phone"] = format_whatsapp_phone(f_phone)
                str_lit.session_state.couriers_db[str_lit.session_state.username]["hp_exempt"] = f_hp_or_exempt if f_hp_or_exempt else "אין"
                str_lit.session_state.couriers_db[str_lit.session_state.username]["registration_date"] = reg_date
                if new_password_input.strip():
                    str_lit.session_state.couriers_db[str_lit.session_state.username]["password"] = new_password_input.strip()
                save_users_db(str_lit.session_state.couriers_db)
                
                save_contract_data({
                    "שם משתמש": str_lit.session_state.username, "תפקיד": str_lit.session_state.role, "חברה": str_lit.session_state.company,
                    "שם מלא": f_full_name, "ת.ז": f_id_num, "כתובת": f_address, "אימייל": f_email,
                    "טלפון": format_whatsapp_phone(f_phone), "ח.פ / עוסק פטור": f_hp_or_exempt if f_hp_or_exempt else "אין", "תאריך רישום": reg_date
                })
                str_lit.success("הפרטים, החוזה והסיסמה החדשה נשמרו בהצלחה!")
                str_lit.rerun()
            else:
                str_lit.error("נא למלא את כל שדות החובה ולסמן וי על אישור החוזה.")
    if str_lit.sidebar.button(t["logout"]):
        logout_user()

elif str_lit.session_state.role == "מנהל מערכת ראשי (Super Admin)":
    str_lit.sidebar.title("מנהל ראשי")
    admin_menu = str_lit.sidebar.radio(
        t["admin_menu"], 
        [
            t["main_sys"], 
            t["add_delivery"],
            t["add_company_admin"],
            t["add_courier"], 
            t["manage_users"],
            t["monthly_report"],
            t["contract_menu"],
            t["live_tracking"],
            t["verify_rejected"]
        ]
    )
    if str_lit.sidebar.button(t["logout"]):
        logout_user()

    if admin_menu == t["main_sys"]:
        str_lit.title(t["main_sys"])
        admin_deliveries = str_lit.session_state.deliveries
        col1, col2, col3 = str_lit.columns(3)
        col1.metric("סך הכל משלוחים במערכת", len(admin_deliveries))
        col2.metric("פעילים / ממתינים / נדחו", len([d for d in admin_deliveries if d["status"] not in ["נמסר", "סורב על ידי הלקוח"]]))
        col3.metric("נמסרו בהצלחה", len([d for d in admin_deliveries if d["status"] == "נמסר"]))
        str_lit.divider()
        for idx, item in enumerate(admin_deliveries):
            status_color = "🟢" if item["status"] == "נמסר" else ("🔴" if "סורב" in item["status"] else ("🔵" if "נדחה" in item["status"] else "🟠"))
            rating_stars = "⭐️" * int(item.get("rating", 0)) if item.get("rating", 0) > 0 else "טרם דורג"
            with str_lit.expander(f"{status_color} 📦 {item['שם לקוח']} | {item['עיר']} | סטטוס: {item['status']} | דירוג: {rating_stars}"):
                str_lit.write(f"**ברקוד:** {item['ברקוד']} | **טלפון:** {item['טלפון']} | **כתובת:** {item['כתובת מלאה']} | **הערות:** {item.get('הערות', 'אין')}")
                if item.get("rating", 0) > 0:
                    str_lit.info(f"⭐️ **דירוג הלקוח:** {item['rating']} מתוך 5 כוכבים | **משוב:** {item.get('feedback', 'אין הערות')}")
                
                c_phone = format_whatsapp_phone(item['טלפון'])
                wa_msg = urllib.parse.quote(f"שלום {item['שם לקוח']}, אני השליח בדרך אליך! יש לי משלוח מ{item['שם חברה']}.")
                wa_link = f"https://wa.me/{c_phone}?text={wa_msg}"
                waze_query = urllib.parse.quote(f"{item['כתובת מלאה']}, {item['עיר']}")
                waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                
                b1, b2, b3, b4, b5 = str_lit.columns(5)
                with b1:
                    str_lit.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["whatsapp_btn"]}</button></a>', unsafe_allow_html=True)
                with b2:
                    str_lit.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["waze_btn"]}</button></a>', unsafe_allow_html=True)
                with b3:
                    if str_lit.button(t["mark_delivered"], key=f"adm_m_{idx}"):
                        item["status"] = "נמסר"
                        str_lit.success(t["delivered_success"])
                        str_lit.rerun()
                with b4:
                    if str_lit.button("🔄 דחה למחר", key=f"adm_p_{idx}"):
                        item["status"] = "נדחה למחר על ידי הלקוח"
                        str_lit.success("עודכן כנדחה למחר!")
                        str_lit.rerun()
                with b5:
                    if str_lit.button("❌ סורב", key=f"adm_r_{idx}"):
                        item["status"] = "סורב על ידי הלקוח"
                        str_lit.warning("עודכן כסורב ולא ייחשב בתשלום.")
                        str_lit.rerun()

    elif admin_menu == t["add_delivery"]:
        str_lit.title(t["add_delivery"])
        with str_lit.form("add_delivery_form"):
            d_barcode = str_lit.text_input("ברקוד משלוח / מספר מעקב (QR):", value=f"DEL-{int(datetime.now().timestamp())}")
            d_client = str_lit.text_input("שם הלקוח:")
            d_company = str_lit.text_input("שם חברה / מותג ששולח (למשל: SHEIN):")
            d_phone = str_lit.text_input("טלפון הלקוח:")
            d_address = str_lit.text_input("כתובת מלאה:")
            d_city = str_lit.text_input("עיר / יישוב:")
            d_notes = str_lit.text_area("הערות למשלוח:")
            
            couriers_list = [u for u, i in str_lit.session_state.couriers_db.items() if i.get("role") == "שליח"]
            assigned_courier = str_lit.selectbox("שיוך שליח:", couriers_list if couriers_list else ["אין שליחים"])
            
            submit_new_del = str_lit.form_submit_button("הוסף משלוח למערכת 🚀")
            if submit_new_del and d_client and d_phone and d_city:
                new_item = {
                    "ברקוד": d_barcode, "שם לקוח": d_client, "שם חברה": d_company if d_company else "General",
                    "טלפון": format_whatsapp_phone(d_phone), "כתובת מלאה": d_address, "עיר": d_city,
                    "הערות": d_notes, "status": "ממתין", "courier": assigned_courier, "company": "System",
                    "date": get_israel_time(), "rating": 0, "feedback": ""
                }
                str_lit.session_state.deliveries.append(new_item)
                str_lit.success("המשלוח נוסף בהצלחה למערכת!")

    elif admin_menu == t["add_company_admin"]:
        str_lit.title(t["add_company_admin"])
        with str_lit.form("add_comp_form"):
            cu = str_lit.text_input("שם משתמש מנהל:")
            cp = str_lit.text_input("סיסמה ראשונית:", type="password")
            cn = str_lit.text_input("שם חברה:")
            cph = str_lit.text_input("טלפון:")
            if str_lit.form_submit_button("הוסף מנהל חברה") and cu and cp and cn and cph:
                str_lit.session_state.couriers_db[cu] = {"password": cp, "role": "מנהל חברה (Company Admin)", "phone": format_whatsapp_phone(cph), "company": cn, "contract_signed": False}
                save_users_db(str_lit.session_state.couriers_db)
                str_lit.success("מנהל החברה נוסף בהצלחה!")

    elif admin_menu == t["add_courier"]:
        str_lit.title(t["add_courier"])
        with str_lit.form("add_cour_form"):
            cu = str_lit.text_input("שם משתמש שליח / עובד:")
            cp = str_lit.text_input("סיסמה ראשונית:", type="password")
            cph = str_lit.text_input("טלפון:")
            comp_list = ["Independent"] + list(set([i.get("company") for u, i in str_lit.session_state.couriers_db.items() if i.get("company") not in ["Independent", "System"]]))
            ccomp = str_lit.selectbox("שיוך חברה:", comp_list)
            if str_lit.form_submit_button("הוסף שליח / עובד") and cu and cp and cph:
                str_lit.session_state.couriers_db[cu] = {"password": cp, "role": "שליח", "phone": format_whatsapp_phone(cph), "company": ccomp, "contract_signed": False}
                save_users_db(str_lit.session_state.couriers_db)
                str_lit.success("השליח/העובד נוסף בהצלחה!")

    elif admin_menu == t["manage_users"]:
        str_lit.title(t["manage_users"])
        str_lit.write("כאן תוכל לנהל את המשתמשים, לאפס או לשנות סיסמאות ישירות, או למחוק משתמשים שלא צריכים גישה.")
        for usr, info in list(str_lit.session_state.couriers_db.items()):
            if usr == "Admin": continue
            with str_lit.expander(f"👤 משתמש: {usr} ({info.get('role')}) - חברה: {info.get('company')}"):
                str_lit.write(f"**שם מלא:** {info.get('full_name', 'לא צוין')} | **טלפון:** {info.get('phone', '-')} | **ח.פ / עוסק פטור:** {info.get('hp_exempt', 'לא צוין')}")
                
                with str_lit.form(f"change_pwd_form_{usr}"):
                    new_admin_pwd = str_lit.text_input("שנה סיסמה למשתמש זה:", type="password", key=f"npwd_{usr}")
                    if str_lit.form_submit_button("עדכן סיסמה חדשה למשתמש") and new_admin_pwd.strip():
                        str_lit.session_state.couriers_db[usr]["password"] = new_admin_pwd.strip()
                        save_users_db(str_lit.session_state.couriers_db)
                        str_lit.success(f"הסיסמה עבור {usr} עודכנה בהצלחה!")
                
                if str_lit.button("מחק משתמש ❌", key=f"del_user_{usr}"):
                    del str_lit.session_state.couriers_db[usr]
                    save_users_db(str_lit.session_state.couriers_db)
                    str_lit.success("המשתמש נמחק בהצלחה.")
                    str_lit.rerun()

    elif admin_menu == t["monthly_report"]:
        str_lit.title("📊 סיכום חודשי ודוחות כספיים (1 ש\"ח לכל משלוח שנוסף, למעט משלוחים שסורבו)")
        str_lit.write("החישוב כולל את כל המשלוחים שנוספו והגיעו למצב 'נמסר' (כולל אלו שעוכבו או נדחה למחר ובסוף נמסרו). משלוחים שסורבו על ידי הלקוח **אינם** מחושבים.")
        
        report_data = []
        for usr, info in str_lit.session_state.couriers_db.items():
            if usr == "Admin": continue
            
            user_company = info.get("company", "Independent")
            valid_user_items = [
                d for d in str_lit.session_state.deliveries 
                if (d.get("courier") == usr or d.get("company") == user_company) and d.get("status"] != "סורב על ידי הלקוח"
            ]
            
            count_valid_deliveries = len(valid_user_items)
            base_price = count_valid_deliveries * 1.0
            
            hp_exempt_str = str(info.get("hp_exempt", "")).lower()
            is_exempt = "פטור" in hp_exempt_str or hp_exempt_str == "אין" or hp_exempt_str == ""
            
            if is_exempt:
                vat_amount = 0.0
                total_price = base_price
                tax_status = "עוסק פטור (ללא מע\"מ)"
            else:
                vat_amount = base_price * VAT_RATE
                total_price = base_price + vat_amount
                tax_status = "עוסק מורשה / חברה (כולל מע\"מ 18%)"
                
            report_data.append({
                "שם משתמש": usr,
                "שם מלא": info.get("full_name", "-"),
                "תפקיד": info.get("role", "-"),
                "חברה / שייכות": user_company,
                "סטטוס מע\"מ": tax_status,
                "סך משלוחים מזוכה": count_valid_deliveries,
                "סכום בסיס (ש\"ח)": f"{base_price:.2f} ₪",
                "מע\"מ (ש\"ח)": f"{vat_amount:.2f} ₪",
                "סכום סופי לתשלום (ש\"ח)": f"{total_price:.2f} ₪"
            })
            
        if report_data:
            df_report = pd.DataFrame(report_data)
            str_lit.dataframe(df_report, use_container_width=True)
            
            total_all_deliveries = sum([d["סך משלוחים מזוכה"] for d in report_data])
            total_all_revenue = sum([float(d["סכום סופי לתשלום (ש\"ח)"].replace(" ₪", "")) for d in report_data])
            
            str_lit.metric("📦 סך הכל משלוחים מזוכים במערכת החודש", total_all_deliveries)
            str_lit.metric("💰 סך כל ההכנסות הכלליות", f"{total_all_revenue:.2f} ₪")
        else:
            str_lit.info("אין נתונים להצגה בדוח החודשי.")

    elif admin_menu == t["contract_menu"]:
        str_lit.title(t["contract_menu"])
        contracts_df = load_contracts_data()
        if not contracts_df.empty:
            for c_idx, row in contracts_df.iterrows():
                str_lit.markdown(f"**{row['שם מלא']}** | ת.ז: {row['ת.ז']} | טלפון: {row['טלפון']} | תאריך: {row['תאריך רישום']}")
                personal_stream = generate_personal_html_contract(row.to_dict())
                str_lit.download_button(
                    label=f"📥 הורד חוזה HTML אישי עבור {row['שם מלא']}",
                    data=personal_stream,
                    file_name=f"contract_{row['שם משתמש']}.html",
                    mime="text/html",
                    key=f"dl_html_{c_idx}"
                )
                if str_lit.button(f"🗑️ הסר חוזה זה מהרשימה", key=f"del_contract_{c_idx}"):
                    delete_contract_by_index(c_idx)
                    str_lit.success("החוזה הוסר בהצלחה!")
                    str_lit.rerun()
                str_lit.divider()
        else:
            str_lit.info("אין חוזים שמורים.")

    elif admin_menu == t["live_tracking"]:
        str_lit.title(t["live_tracking"])
        locs = load_locations_db()
        if locs:
            for usr, data in locs.items():
                str_lit.info(f"🛵 **שליח/משתמש:** {usr} | 📍 **מיקום אחרון:** {data['location']} | ⏰ **עודכן:** {data['updated_at']}")
        else:
            str_lit.info("עדיין לא דווחו מיקומים חיים.")

    elif admin_menu == t["verify_rejected"]:
        str_lit.title("🔍 אימות משלוחים שסורבו מול לקוחות (בקרת מנהל ראשי)")
        str_lit.write("כאן תוכל לצפות בכל המשלוחים שדווחו כ'סורב על ידי הלקוח' על ידי השליחים או מנהלי החברות, ולבדוק ישירות מול הלקוח בטלפון או בוואטסאפ.")
        
        rejected_deliveries = [d for d in str_lit.session_state.deliveries if d.get("status") == "סורב על ידי הלקוח"]
        
        if not rejected_deliveries:
            str_lit.info("אין כרגע משלוחים שסומנו כסורבו על ידי הלקוחות.")
        else:
            for r_idx, r_item in enumerate(rejected_deliveries):
                with str_lit.expander(f"❌ לקוח: {r_item['שם לקוח']} | עיר: {r_item['עיר']} | ברקוד: {r_item['ברקוד']}"):
                    str_lit.write(f"**טלפון הלקוח:** {r_item['טלפון']} | **כתובת:** {r_item['כתובת מלאה']} | **שליח מטפל:** {r_item.get('courier', 'לא צוין')}")
                    str_lit.write(f"**הערות משלוח:** {r_item.get('הערות', 'אין')}")
                    
                    c_phone = format_whatsapp_phone(r_item['טלפון'])
                    verify_msg = urllib.parse.quote(f"שלום {r_item['שם לקוח']}, מעוניינים לוודא מולך האם אכן סירבת לקבל את המשלוח שלך מ-{r_item['שם חברה']}? (מערכת Speedy Delivery)")
                    wa_verify_link = f"https://wa.me/{c_phone}?text={verify_msg}"
                    phone_call_link = f"tel:{c_phone}"
                    
                    vb1, vb2, vb3 = str_lit.columns(3)
                    with vb1:
                        str_lit.markdown(f'<a href="{wa_verify_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">📲 בדוק בוואטסאפ מול הלקוח</button></a>', unsafe_allow_html=True)
                    with vb2:
                        str_lit.markdown(f'<a href="{phone_call_link}"><button style="background-color:#0284c7; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">📞 התקשר ללקוח</button></a>', unsafe_allow_html=True)
                    with vb3:
                        if str_lit.button("🔄 שנה סטטוס חזרה לממתין/נמסר", key=f"revert_rej_{r_idx}"):
                            r_item["status"] = "ממתין"
                            str_lit.success("הסטטוס שונה חזרה לממתין לצורך מסירה מחדש!")
                            str_lit.rerun()

elif str_lit.session_state.role == "שליח":
    courier_username = str_lit.session_state.username
    str_lit.sidebar.title(f"🛵 שליח: {courier_username}")
    
    courier_menu = str_lit.sidebar.radio(
        "תפריט שליח",
        [
            "📦 המשלוחים שלי",
            "➕ הוספת משלוח חדש",
            "📍 עדכון מיקום חי (GPS)"
        ]
    )
    
    if str_lit.sidebar.button(t["logout"]):
        logout_user()

    if courier_menu == "📦 המשלוחים שלי":
        str_lit.title("📦 המשלוחים שלי לביצוע")
        my_deliveries = [d for d in str_lit.session_state.deliveries if d.get("courier"] == courier_username]
        
        if not my_deliveries:
            str_lit.info("אין לך כרגע משלוחים משויכים. באפשרותך להוסיף משלוח חדש דרך התפריט בצד.")
        else:
            for idx, item in enumerate(my_deliveries):
                status_color = "🟢" if item["status"] == "נמסר" else ("🔴" if "סורב" in item["status"] else ("🔵" if "נדחה" in item["status"] else "🟠"))
                rating_stars = "⭐️" * int(item.get("rating", 0)) if item.get("rating", 0) > 0 else "טרם דורג"
                with str_lit.expander(f"{status_color} 📦 {item['שם לקוח']} | {item['עיר']} | סטטוס: {item['status']} | דירוג: {rating_stars}"):
                    str_lit.write(f"**ברקוד:** {item['ברקוד']} | **טלפון:** {item['טלפון']} | **כתובת:** {item['כתובת מלאה']} | **חברה שולחת:** {item['שם חברה']} | **הערות:** {item.get('הערות', 'אין')}")
                    
                    c_phone = format_whatsapp_phone(item['טלפון'])
                    wa_msg = urllib.parse.quote(f"שלום {item['שם לקוח']}, אני השליח בדרך אליך! יש לי משלוח מ-{item['שם חברה']}. נא להיות זמין.")
                    wa_link = f"https://wa.me/{c_phone}?text={wa_msg}"
                    
                    # וואטסאפ לבקשת הערכת משלוח
                    wa_rating_msg = urllib.parse.quote(f"תודה רבה שבחרת בנו! נשמח מאוד אם תוכל/י לדרג את שירות המשלוח מ-{item['שם חברה']} מ-1 עד 5 כוכבים, ולשלוח לנו את דעתך. (Speedy Delivery)")
                    wa_rating_link = f"https://wa.me/{c_phone}?text={wa_rating_msg}"
                    
                    waze_query = urllib.parse.quote(f"{item['כתובת מלאה']}, {item['עיר']}")
                    waze_link = f"https://waze.com/ul?q={waze_query}&navigate=yes"
                    
                    b1, b2, b3, b4, b5 = str_lit.columns(5)
                    with b1:
                        str_lit.markdown(f'<a href="{wa_link}" target="_blank"><button style="background-color:#25d366; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["whatsapp_btn"]}</button></a>', unsafe_allow_html=True)
                    with b2:
                        str_lit.markdown(f'<a href="{waze_link}" target="_blank"><button style="background-color:#33ccff; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer;">{t["waze_btn"]}</button></a>', unsafe_allow_html=True)
                    with b3:
                        if str_lit.button("סמן כנמסר ✅", key=f"cour_m_{idx}"):
                            item["status"] = "נמסר"
                            str_lit.success("המשלוח עודכן בהצלחה כ'נמסר'!")
                            str_lit.rerun()
                    with b4:
                        if str_lit.button("🔄 דחה למחר", key=f"cour_p_{idx}"):
                            item["status"] = "נדחה למחר על ידי הלקוח"
                            str_lit.success("עודכן כנדחה למחר!")
                            str_lit.rerun()
                    with b5:
                        if str_lit.button("❌ סורב", key=f"cour_r_{idx}"):
                            item["status"] = "סורב על ידי הלקוח"
                            str_lit.warning("עודכן כסורב.")
                            str_lit.rerun()
                    
                    str_lit.markdown("---")
                    str_lit.subheader("⭐ הערכת משלוח ומשוב לקוח")
                    with str_lit.form(f"rating_form_{idx}"):
                        current_r = int(item.get("rating", 5))
                        if current_r < 1 or current_r > 5:
                            current_r = 5
                        assigned_rating = str_lit.slider("בחר דירוג כוכבים (1 עד 5):", 1, 5, value=current_r, key=f"slider_rat_{idx}")
                        assigned_feedback = str_lit.text_input("הערת לקוח / משוב על המשלוח:", value=item.get("feedback", ""), key=f"feed_txt_{idx}")
                        
                        col_r1, col_r2 = str_lit.columns(2)
                        with col_r1:
                            submit_rating = str_lit.form_submit_button("שמור הערכת משלוח ⭐")
                        with col_r2:
                            str_lit.markdown(f'<a href="{wa_rating_link}" target="_blank"><button style="background-color:#128c7e; color:white; border:none; padding:8px 12px; border-radius:5px; width:100%; cursor:pointer; margin-top:2px;">📲 שלח בקשת דירוג בוואטסאפ</button></a>', unsafe_allow_html=True)
                        
                        if submit_rating:
                            item["rating"] = assigned_rating
                            item["feedback"] = assigned_feedback
                            str_lit.success("הערכת המשלוח והמשוב נשמרו בהצלחה!")
                            str_lit.rerun()

    elif courier_menu == "➕ הוספת משלוח חדש":
        str_lit.title("➕ הוספת משלוח חדש על ידי שליח")
        with str_lit.form("courier_add_del_form"):
            d_barcode = str_lit.text_input("ברקוד משלוח / מספר מעקב:", value=f"DEL-{int(datetime.now().timestamp())}")
            d_client = str_lit.text_input("שם הלקוח:")
            d_company = str_lit.text_input("שם חברה / מותג ששולח (למשל: SHEIN):")
            d_phone = str_lit.text_input("טלפון הלקוח:")
            d_address = str_lit.text_input("כתובת מלאה:")
            d_city = str_lit.text_input("עיר / יישוב:")
            d_notes = str_lit.text_area("הערות למשלוח:")
            
            submit_courier_del = str_lit.form_submit_button("הוסף משלוח אל הרשימה שלי 🚀")
            if submit_courier_del and d_client and d_phone and d_city:
                new_item = {
                    "ברקוד": d_barcode, "שם לקוח": d_client, "שם חברה": d_company if d_company else "General",
                    "טלפון": format_whatsapp_phone(d_phone), "כתובת מלאה": d_address, "עיר": d_city,
                    "הערות": d_notes, "status": "ממתין", "courier": courier_username, "company": str_lit.session_state.company,
                    "date": get_israel_time(), "rating": 0, "feedback": ""
                }
                str_lit.session_state.deliveries.append(new_item)
                str_lit.success("המשלוח נוסף בהצלחה למערכת ושויך אליך!")

    elif courier_menu == "📍 עדכון מיקום חי (GPS)":
        str_lit.title("📍 עדכון מיקום חי למנהל")
        with str_lit.form("loc_form"):
            loc_input = str_lit.text_input("הכנס כתובת נוכחית / עיר / אזור חלוקה:")
            submit_loc = str_lit.form_submit_button("עדכן מיקום למערכת 📍")
            if submit_loc and loc_input.strip():
                save_location_data(courier_username, loc_input.strip())
                str_lit.success("המיקום עודכן בהצלחה למנהל המערכת!")

elif str_lit.session_state.role == "מנהל חברה (Company Admin)":
    company_name = str_lit.session_state.company
    str_lit.title(f"🏢 מנהל חברה: {company_name}")
    if str_lit.sidebar.button(t["logout"]):
        logout_user()
    comp_menu = str_lit.sidebar.radio("תפריט", ["📦 משלוחי חברה", "➕ הוספת משלוח לחברה", "📍 עדכון ומעקב מיקום שליחי החברה"])
    
    if comp_menu == "📦 משלוחי חברה":
        str_lit.subheader("משלוחי פעילים לחברה שלך:")
        comp_deliveries = [d for d in str_lit.session_state.deliveries if d.get("company") == company_name or d.get("שם חברה") == company_name]
        for idx, item in enumerate(comp_deliveries):
            status_color = "🟢" if item["status"] == "נמסר" else "🟠"
