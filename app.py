import streamlit as st
import urllib.parse
from datetime import datetime, timezone, timedelta
import pandas as pd
import os
import json

# הגדרת שעון ישראל (UTC+2 / UTC+3)
ISRAEL_OFFSET = timedelta(hours=2)
ADMIN_PHONE = "972502616375"  # מספר הטלפון שלך כמנהל המערכת הראשי

def get_israel_time():
    return datetime.now(timezone(ISRAEL_OFFSET)).strftime("%Y-%m-%d %H:%M")

def get_current_date():
    return datetime.now(timezone(ISRAEL_OFFSET))

# הגדרת עיצוב הדף (כיוון מימין לשמאל כברירת מחדל)
st.set_page_config(page_title="Speedy Delivery - מערכת ניהול משלוחים", page_icon="🚚", layout="wide")

# --- קבצי שמירה מקומיים למערכת ---
CONTRACTS_FILE = "delivery_drivers_contracts.csv"
USERS_FILE = "couriers_db.json"
UPLOAD_DIR = "uploaded_documents"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# טעינת משתמשים מקובץ
def load_users_db():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # ברירת מחדל ראשונית אם הקובץ לא קיים
    default_users = {
        "Admin": {"password": "Sma.srablove2028", "role": "מנהל מערכת ראשי (Super Admin)", "phone": ADMIN_PHONE, "company": "System"},
        "mohammad": {"password": "123", "role": "שליח", "phone": "+972502616375", "company": "Independent"}
    }
    save_users_db(default_users)
    return default_users

def save_users_db(users_dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users_dict, f, ensure_ascii=False, indent=4)

def load_contracts_data():
    if os.path.exists(CONTRACTS_FILE):
        return pd.read_csv(CONTRACTS_FILE)
    return pd.DataFrame(columns=["שם פרטי", "שם משפחה", "תז", "חפ_או_עוסק", "מספר_חפ", "קובץ_חפ", "טלפון", "כתובת", "סוג עוסק", "רכב", "רישיון", "חתימה", "תאריך ושעה"])

def save_contract_data(new_data):
    df = load_contracts_data()
    new_row = pd.DataFrame([new_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CONTRACTS_FILE, index=False)

# --- מילון תרגומים מלא למערכת (ערבית, עברית, אנגלית) ---
TRANSLATIONS = {
    "العربية (Arabic)": {
        "title": "🚚 نظام إدارة وتوصيل الشحنات السريع",
        "login_title": "تسجيل دخول المستخدمين والمندوبين",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_btn": "تسجيل الدخول",
        "login_error": "اسم المستخدم أو كلمة المرور غير صحيحة. حاول مرة أخرى.",
        "logout": "تسجيل الخروج (Logout)",
        "admin_menu": "قائمة الإدارة",
        "main_sys": "نظام الشحنات الرئيسي",
        "add_courier": "إضافة مندوب جديد",
        "add_company_admin": "إضافة مدير شركة توصيل",
        "manage_users": "إدارة وتعديل المستخدمين",
        "monthly_report": "📊 تقرير الحسابات الشهري والعمولات",
        "contract_menu": "📝 شروط وطريقة استخدام النظام",
        "current_loc": "📍 موقعك الحالي / نقطة الانطلاق",
        "loc_placeholder": "أدخل موقعك الحالي (بلدة / مدينة):",
        "active_deliveries": "لديك حالياً",
        "active_deliveries_end": "شحنات نشطة للتنفيذ اليوم.",
        "current_time": "وقت إسرائيل الحالي:",
        "start_point_label": "نقطة الانطلاق الحالية:",
        "add_new_del": "➕ إضافة شحنة جديدة (تناسب القرى بدون شوارع)",
        "barcode": "رقم التعقب / الباركود:",
        "cust_name": "اسم الزبون:",
        "company_name": "اسم الشركة (المتجر):",
        "phone": "رقم هاتف الزبون (مثال: 0502616375):",
        "city": "البلدة / المدينة:",
        "street": "الشارع (اختياري - اتركه فارغاً إذا لم يوجد):",
        "house": "رقم البيت (اختياري):",
        "floor": "الطابق (اختياري):",
        "notes": "ملاحظات خاصة بالشحنة:",
        "save_del": "حفظ الشحنة في النظام",
        "del_success": "تمت إضافة الشحنة بنجاح!",
        "fill_required": "الرجاء تعبئة اسم الزبون والبلدة على الأقل.",
        "list_title": "📋 قائمة شحنات اليوم والإدارة السريعة",
        "sort_btn": "🔄 ترتيب المسار تلقائياً حسب البلدة، الشارع ورقم البيت",
        "sort_success": "تم ترتيب المسار تلقائياً بدءاً من موقعك الحالي!",
        "no_deliveries": "لا توجد شحنات في القائمة حالياً.",
        "status_delivered": "تم التسليم",
        "status_waiting": "قيد الانتظار",
        "address": "العنوان:",
        "added_at": "تاريخ الإضافة:",
        "whatsapp_btn": "📲 إرسال رسالة واتساب للزبون",
        "waze_btn": "🚗 التنقل من",
        "mark_delivered": "تحديد كـ تم التسليم",
        "delivered_success": "تم تحديث الشحنة كـ تم التسليم!",
        "edit_del": "✏️ تعديل تفاصيل الشحنة",
        "save_changes": "حفظ التغييرات",
        "edit_success": "تم تحديث الشحنة بنجاح!",
        "welcome_admin": "مرحباً، المدير الرئيسي",
        "welcome_company_admin": "مرحباً، مدير شركة التوصيل",
        "welcome_courier": "مرحباً",
        "language": "🌐 لغة التطبيق / Language"
    },
    "עברית (Hebrew)": {
        "title": "🚚 מערכת ניהול וסידור משלוחים מהירה",
        "login_title": "כניסת משתמשים ושליחים",
        "username": "שם משתמש",
        "password": "סיסמה",
        "login_btn": "התחבר",
        "login_error": "שם משתמש או סיסמה שגויים. נסה שוב.",
        "logout": "התנתק (Logout)",
        "admin_menu": "תפריט ניהול",
        "main_sys": "מערכת משלוחים ראשית",
        "add_courier": "הוספת שליח חדש",
        "add_company_admin": "הוספת מנהל חברת משלוחים",
        "manage_users": "ניהול ועריכת משתמשים",
        "monthly_report": "📊 סיכום חודשי, חישוב עמלות ותשלומים למערכת",
        "contract_menu": "📝 תנאי שימוש במערכת ואישור עמלות",
        "current_loc": "📍 מיקום נוכחי ונקודת מוצא",
        "loc_placeholder": "הכנס את המיקום הנוכחי שלך (עיר / כפר):",
        "active_deliveries": "יש לך כרגע",
        "active_deliveries_end": "משלוחים פעילים לביצוע להיום.",
        "current_time": "שעון ישראל נוכחי במערכת:",
        "start_point_label": "נקודת המוצא הנוכחית שלך:",
        "add_new_del": "➕ הוספת משלוח חדש (מתאים גם לכפרים ללא רחובות)",
        "barcode": "מספר מעקב / ברקוד:",
        "cust_name": "שם הלקוח:",
        "company_name": "שם החברה (החנות/העסק):",
        "phone": "מספר טלפון של הלקוח (לדוגמה: 0502616375):",
        "city": "ישוב / כפר:",
        "street": "שם רחוב (אופציונלי - ניתן להשאיר ריק):",
        "house": "מספר בית (אופציונלי):",
        "floor": "קומה (אופציונלי):",
        "notes": "הערות מיוחדות למשלוח:",
        "save_del": "שמור משלוח במערכת",
        "del_success": "המשלוח נוסף בהצלחה!",
        "fill_required": "נא למלא לפחות שם לקוח וישוב / כפר.",
        "list_title": "📋 רשימת המשלוחים להיום וניהול מהיר",
        "sort_btn": "🔄 סדר מסלול אוטומטית לפי ישוב, רחוב ומספר בית",
        "sort_success": "המסלול סודר אוטומטית החל מהמיקום שלך!",
        "no_deliveries": "אין עדיין משלוחים לרשימה.",
        "status_delivered": "נמסר",
        "status_waiting": "ממתין",
        "address": "כתובת:",
        "added_at": "נוסף בתאריך ושעה:",
        "whatsapp_btn": "📲 שלח הודעת וואטסאפ ללקוח",
        "waze_btn": "🚗 נווט מ-",
        "mark_delivered": "סמן כנמסר",
        "delivered_success": "המשלוח עודכן כנמסר!",
        "edit_del": "✏️ ערוך פרטי משלוח",
        "save_changes": "שמור שינויים",
        "edit_success": "המשלוח עודכן בהצלחה!",
        "welcome_admin": "מנהל ראשי",
        "welcome_company_admin": "מנהל חברת משלוחים",
        "welcome_courier": "שלום",
        "language": "🌐 שפת אפליקציה / Language"
    },
    "English": {
        "title": "🚚 Fast Delivery Management System",
        "login_title": "Courier & User Login",
        "username": "Username",
        "password": "Password",
        "login_btn": "Login",
        "login_error": "Invalid username or password. Please try again.",
        "logout": "Logout",
        "admin_menu": "Management Menu",
        "main_sys": "Main Deliveries System",
        "add_courier": "Add New Courier",
        "add_company_admin": "Add Delivery Company Admin",
        "manage_users": "Manage & Edit Users",
        "monthly_report": "📊 Monthly System Fees & Reports",
        "contract_menu": "📝 System Usage Terms & Fees",
        "current_loc": "📍 Current Location & Origin",
        "loc_placeholder": "Enter your current location (City/Village):",
        "active_deliveries": "You currently have",
        "active_deliveries_end": "active deliveries for today.",
        "current_time": "Current Israel Time:",
        "start_point_label": "Your Current Starting Point:",
        "add_new_del": "➕ Add New Delivery (Works for villages without streets)",
        "barcode": "Tracking Number / Barcode:",
        "cust_name": "Customer Name:",
        "company_name": "Company Name (Store):",
        "phone": "Customer Phone Number (e.g., 0502616375):",
        "city": "City / Village:",
        "street": "Street Name (Optional - leave blank if none):",
        "house": "House Number (Optional):",
        "floor": "Floor (Optional):",
        "notes": "Special Delivery Notes:",
        "save_del": "Save Delivery to System",
        "del_success": "Delivery added successfully!",
        "fill_required": "Please fill in at least the customer name and city/village.",
        "list_title": "📋 Today's Deliveries & Quick Management",
        "sort_btn": "🔄 Auto-sort route by City, Street, and House Number",
        "sort_success": "Route sorted automatically starting from your current location!",
        "no_deliveries": "No deliveries in the list yet.",
        "status_delivered": "Delivered",
        "status_waiting": "Pending",
        "address": "Address:",
        "added_at": "Added at:",
        "whatsapp_btn": "📲 Send WhatsApp to Customer",
        "waze_btn": "🚗 Navigate from",
        "mark_delivered": "Mark as Delivered",
        "delivered_success": "Delivery updated as delivered!",
        "edit_del": "✏️ Edit Delivery Details",
        "save_changes": "Save Changes",
        "edit_success": "Delivery updated successfully!",
        "welcome_admin": "Super Admin",
        "welcome_company_admin": "Delivery Company Admin",
        "welcome_courier": "Hello",
        "language": "🌐 App Language"
    }
}

# --- בחירת שפה בסיידבר ---
st.sidebar.markdown("---")
lang_choice = st.sidebar.selectbox("🌐 Language / لغة / שפה", ["العربية (Arabic)", "עברית (Hebrew)", "English"], index=1)
t = TRANSLATIONS[lang_choice]

is_rtl = lang_choice in ["العربية (Arabic)", "עברית (Hebrew)"]
dir_style = "rtl" if is_rtl else "ltr"

st.markdown(f"""
<style>
    div.block-container {{
        direction: {dir_style};
    }}
</style>
""", unsafe_allow_html=True)

# --- טעינת מאגר משתמשים מתמיד ---
if "couriers_db" not in st.session_state:
    st.session_state.couriers_db = load_users_db()

# --- מנגנון שמירת חיבור גם אחרי רענון ---
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

# מאגר משלוחים במערכת
if "deliveries" not in st.session_state:
    current_time_il = get_israel_time()
    st.session_state.deliveries = [
        {
            "ברקוד": "TEST-001",
            "שם לקוח": "סמר שומרי",
            "שם חברה": "SHEIN",
            "טלפון": "972502616375",
            "כתובת מלאה": "כסרא-סמיע",
            "רחוב": "",
            "בית": "",
            "קומה": "",
            "עיר": "כסרא-סמיע",
            "הערות": "משלוח בדיקה",
            "status": "ממתין",
            "courier": "mohammad",
            "company": "Independent",
            "date": current_time_il
        }
    ]

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.company = ""
    st.query_params.clear()
    st.rerun()

# --- מסך התחברות ---
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
                st.session_state.company = db[username_input].get("company", username_input if db[username_input]["role"] == "מנהל חברה (Company Admin)" else "Independent")
                
                st.query_params["logged_in"] = "true"
                st.query_params["username"] = username_input
                st.query_params["role"] = db[username_input]["role"]
                st.query_params["company"] = st.session_state.company
                
                st.rerun()
            else:
                st.error(t["login_error"])

# --- אזור הניהול למנהל הראשי (Super Admin) ---
elif st.session_state.role == "מנהל מערכת ראשי (Super Admin)":
    st.sidebar.title(t["welcome_admin"])
    admin_menu = st.sidebar.radio(
        t["admin_menu"], 
        [
            t["main_sys"], 
            t["add_company_admin"],
            t["add_courier"], 
            t["manage_users"],
            t["monthly_report"],
            t["contract_menu"]
        ]
    )
    
    if st.sidebar.button(t["logout"]):
        logout_user()

    if admin_menu == t["add_company_admin"]:
        st.title(t["add_company_admin"])
        with st.form("add_company_admin_form"):
            c_username = st.text_input(t["username"])
            c_pass = st.text_input(t["password"], type="password")
            c_phone = st.text_input(t["phone"])
            c_name = st.text_input("שם חברת המשלוחים (Company Name)")
            add_c_btn = st.form_submit_button(t["login_btn"])
            
            if add_c_btn:
                if c_username and c_pass and c_name:
                    clean_phone = c_phone.replace("+", "").strip()
                    if clean_phone.startswith("0"):
                        clean_phone = "972" + clean_phone[1:]
                    
                    st.session_state.couriers_db[c_username] = {
                        "password": c_pass,
                        "role": "מנהל חברה (Company Admin)",
                        "phone": clean_phone,
                        "company": c_name
                    }
                    save_users_db(st.session_state.couriers_db)
                    st.success(f"נוסף בהצלחה מנהל חברה עבור '{c_name}' ונשמר במערכת!")
                    
                    base_url = "https://speedy-delivery-app.streamlit.app/"
                    login_link = f"{base_url}?username={urllib.parse.quote(c_username)}"
                    st.info(f"🔗 קישור התחברות ישיר למנהל החברה:\n`{login_link}`")

    elif admin_menu == t["add_courier"]:
        st.title(t["add_courier"])
        with st.form("add_courier_form"):
            new_user = st.text_input(t["username"])
            new_pass = st.text_input(t["password"], type="password")
            new_phone_input = st.text_input(t["phone"])
            
            company_options = [usr for usr, info in st.session_state.couriers_db.items() if info.get("role") == "מנהל חברה (Company Admin)"]
            company_options.insert(0, "עצמאי (Independent / מנהל ראשי)")
            assigned_company = st.selectbox("שייך לחברת משלוחים / מנהל", company_options)
            
            add_btn = st.form_submit_button(t["login_btn"])
            
            if add_btn:
                if new_user and new_pass:
                    clean_phone = new_phone_input.replace("+", "").strip()
                    if clean_phone.startswith("0"):
                        clean_phone = "972" + clean_phone[1:]
                    
                    comp_val = st.session_state.couriers_db[assigned_company].get("company", "Independent") if assigned_company != "עצמאי (Independent / מנהל ראשי)" else "Independent"
                    
                    st.session_state.couriers_db[new_user] = {
                        "password": new_pass, 
                        "role": "שליח",
                        "phone": clean_phone,
                        "company": comp_val
                    }
                    save_users_db(st.session_state.couriers_db)
                    
                    st.success("Added successfully and saved to database!")
                    
                    base_url = "https://speedy-delivery-app.streamlit.app/"
                    login_link = f"{base_url}?username={urllib.parse.quote(new_user)}"
                    
                    st.info(f"🔗 קישור התחברות ישיר לשליח החדש:\n`{login_link}`")
                    
                    courier_phone = clean_phone
                    if courier_phone:
                        wa_msg = f"مرحباً {new_user}, تم إضافتك كمندوب في نظام التوصيل. يمكنك الدخول عبر الرابط التالي:\n{login_link}\nكلمة المرور هي: {new_pass}"
                        encoded_wa = urllib.parse.quote(wa_msg)
                        wa_url = f"https://wa.me/{courier_phone}?text={encoded_wa}"
                        st.markdown(f"[📲 إرسال تفاصيل الدخول للشليح عبر الواتساب (Send Login via WhatsApp)]({wa_url})", unsafe_allow_html=True)

    elif admin_menu == t["manage_users"]:
        st.title(t["manage_users"])
        st.write("ניהול, עריכה או מחיקה של מנהלי חברות ושליחים פרטיים במערכת:")

        company_admins_list = {k: v for k, v in st.session_state.couriers_db.items() if v.get("role") == "מנהל חברה (Company Admin)"}
        couriers_list = {k: v for k, v in st.session_state.couriers_db.items() if v.get("role") == "שליח"}

        st.subheader("🏢 מנהלי חברות משלוחים רשומים")
        if not company_admins_list:
            st.info("אין מנהלי חברות רשומים כרגע.")
        else:
            for usr, info in company_admins_list.items():
                with st.expander(f"מנהל חברה: {usr} | חברה: {info.get('company', '')} | טלפון: {info.get('phone', '')}"):
                    with st.form(f"edit_c_admin_{usr}"):
                        updated_pass = st.text_input(t["password"], value=info["password"], type="password", key=f"pass_c_{usr}")
                        updated_phone = st.text_input(t["phone"], value=info.get("phone", ""), key=f"phone_c_{usr}")
                        updated_comp_name = st.text_input("שם החברה", value=info.get("company", ""), key=f"comp_name_{usr}")
                        update_c_btn = st.form_submit_button(t["save_changes"])
                        
                        if update_c_btn:
                            st.session_state.couriers_db[usr]["password"] = updated_pass
                            st.session_state.couriers_db[usr]["phone"] = updated_phone
                            st.session_state.couriers_db[usr]["company"] = updated_comp_name
                            save_users_db(st.session_state.couriers_db)
                            st.success(t["edit_success"])
                            st.rerun()
                    
                    if st.button(f"🗑️ מחק מנהל חברה {usr}", key=f"del_c_admin_{usr}"):
                        del st.session_state.couriers_db[usr]
                        save_users_db(st.session_state.couriers_db)
                        st.success(f"מנהל החברה {usr} נמחק בהצלחה!")
                        st.rerun()

        st.subheader("🛵 שליחים פרטיים רשומים במערכת")
        if not couriers_list:
            st.info("אין שליחים רשומים כרגע.")
        else:
            for usr, info in couriers_list.items():
                with st.expander(f"שליח פרטי: {usr} | חברה שייכות: {info.get('company', 'Independent')} | טלפון: {info.get('phone', '')}"):
                    with st.form(f"edit_courier_{usr}"):
                        updated_pass = st.text_input(t["password"], value=info["password"], type="password", key=f"pass_courier_{usr}")
                        updated_phone = st.text_input(t["phone"], value=info.get("phone", ""), key=f"phone_courier_{usr}")
                        
                        all_comps = [c_usr for c_usr, c_inf in st.session_state.couriers_db.items() if c_inf.get("role") == "מנהל חברה (Company Admin)"]
                        all_comps.insert(0, "Independent")
                        current_comp_idx = all_comps.index(info.get("company")) if info.get("company") in all_comps else 0
                        updated_company = st.selectbox("שייך לחברה מחדש", all_comps, index=current_comp_idx, key=f"select_comp_{usr}")
                        
                        update_cour_btn = st.form_submit_button(t["save_changes"])
                        
                        if update_cour_btn:
                            st.session_state.couriers_db[usr]["password"] = updated_pass
                            st.session_state.couriers_db[usr]["phone"] = updated_phone
                            st.session_state.couriers_db[usr]["company"] = updated_company
                            save_users_db(st.session_state.couriers_db)
                            st.success(t["edit_success"])
                            st.rerun()
                    
                    if st.button(f"🗑️ מחק שליח פרטי {usr}", key=f"del_cour_{usr}"):
                        del st.session_state.couriers_db[usr]
                        save_users_db(st.session_state.couriers_db)
                        st.success(f"השליח {usr} נמחק בהצלחה!")
                        st.rerun()

        st.stop()

    elif admin_menu == t["monthly_report"]:
        st.title(t["monthly_report"])
        st.info("💡 החיוב למערכת מבוסס על 1 ₪ לכל משלוח שנקלט במערכת עבור כל שליח / חברה.")
        
        current_month_str = get_current_date().strftime("%Y-%m")
        st.subheader(f"📅 סיכום חודש נוכחי: {current_month_str}")

        # התיקון המרכזי של השגיאה (SyntaxError) בשורה 482 (סגירת הסוגריים המרובעים ב-role)
        company_admins = [usr for usr, info in st.session_state.couriers_db.items() if info.get("role") == "מנהל חברה (Company Admin)"]
        
        for c_usr in company_admins:
            c_info = st.session_state.couriers_db[c_usr]
            c_name = c_info.get("company", c_usr)
            c_phone = c_info.get("phone", "")
            
            company_couriers = [usr for usr, info in st.session_state.couriers_db.items() if info.get("company") == c_name]
            
            company_deliveries = [
                d for d in st.session_state.deliveries 
                if (d.get("company") == c_name or d.get("courier") in company_couriers or d.get("courier") == c_usr) 
                and d.get("date", "").startswith(current_month_str)
            ]
            
            total_count = len(company_deliveries)
            amount_base = total_count * 1.0
            
            with st.expander(f"🏢 חברה / מנהל: {c_name} (משתמש: {c_usr}) | סך משלוחים: {total_count} | סכום לתשלום: ₪{amount_base:.2f}"):
                st.write(f"📞 טלפון מנהל החברה: {c_phone}")
                st.write(f"👥 שליחים רשומים תחת חברה זו: {', '.join(company_couriers) if company_couriers else 'אין שליחים נוספים'}")
                st.write(f"📦 פירוט כל המשלוחים של החברה החודש:")
                for d in company_deliveries:
                    st.caption(f"- שליח: {d.get('courier')} | ברקוד: {d.get('ברקוד')} | ללקוח: {d.get('שם לקוח')} | סטטוס: {d.get('status')} | תאריך: {d.get('date')}")
                
                if c_phone:
                    fee_msg = f"שלום {c_name}, סיכום השימוש של חברתך במערכת לחודש {current_month_str}:\n- סך משלוחים שנקלטו (כל השליחים): {total_count}\n- סכום לתשלום: ₪{amount_base:.2f}\n\nתודה רבה!"
                    encoded_fee_msg = urllib.parse.quote(fee_msg)
                    wa_fee_url = f"https://wa.me/{c_phone}?text={encoded_fee_msg}"
                    st.markdown(f"[📲 שליחת הודעת חיוב עמלות למנהל החברה בוואטסאפ]({wa_fee_url})", unsafe_allow_html=True)
        
        st.stop()

    elif admin_menu == t["contract_menu"]:
        st.title(t["contract_menu"])
        st.write("צפייה באישור תנאי השימוש ופרטי השליחים הרשומים במערכת:")
        
        contracts_df = load_contracts_data()
        if contracts_df.empty:
            st.info("עדיין לא נרשמו שליחים שאישרו את תנאי המערכת.")
        else:
            st.dataframe(contracts_df, use_container_width=True)
            csv_data = contracts_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="הורד רשימת אישורי שליחים (CSV)",
                data=csv_data,
                file_name="delivery_drivers_contracts.csv",
                mime="text/csv",
            )
        st.stop()

# --- אזור ניהול לחברת משלוחים (Company Admin) ---
elif st.session_state.role == "מנהל חברה (Company Admin)":
    st.sidebar.title(f"{t['welcome_company_admin']}: {st.session_state.company}")
    company_menu = st.sidebar.radio(
        t["admin_menu"], 
        [
            t["main_sys"], 
            t["add_courier"], 
            t["monthly_report"]
        ]
    )
    
    if st.sidebar.button(t["logout"]):
        logout_user()

    my_company_name = st.session_state.company

    if company_menu == t["add_courier"]:
        st.title(t["add_courier"])
        st.write(f"הוספת שליח חדש תחת החברה שלך: **{my_company_name}**")
        with st.form("add_company_courier_form"):
            new_user = st.text_input(t["username"])
            new_pass = st.text_input(t["password"], type="password")
            new_phone_input = st.text_input(t["phone"])
            add_btn = st.form_submit_button(t["login_btn"])
            
            if add_btn:
                if new_user and new_pass:
                    clean_phone = new_phone_input.replace("+", "").strip()
                    if clean_phone.startswith("0"):
                        clean_phone = "972" + clean_phone[1:]
                    
                    st.session_state.couriers_db[new_user] = {
                        "password": new_pass, 
                        "role": "שליח",
                        "phone": clean_phone,
                        "company": my_company_name
                    }
                    save_users_db(st.session_state.couriers_db)
                    st.success("השליח נוסף בהצלחה ושויך לחברה שלך!")
                    
                    base_url = "https://speedy-delivery-app.streamlit.app/"
                    login_link = f"{base_url}?username={urllib.parse.quote(new_user)}"
                    st.info(f"🔗 קישור התחברות ישיר לשליח:\n`{login_link}`")

    elif company_menu == t["monthly_report"]:
        st.title(t["monthly_report"])
        current_month_str = get_current_date().strftime("%Y-%m")
        st.subheader(f"📅 סיכום חודשי לחברת {my_company_name} (חודש: {current_month_str})")
        
        company_couriers = [usr for usr, info in st.session_state.couriers_db.items() if info.get("company") == my_company_name]
        company_deliveries = [
            d for d in st.session_state.deliveries 
            if (d.get("company") == my_company_name or d.get("courier") in company_couriers or d.get("courier") == st.session_state.username) 
            and d.get("date", "").startswith(current_month_str)
        ]
        
        total_count = len(company_deliveries)
        amount_base = total_count * 1.0
        
        st.metric(label="📦 סך כל המשלוחים של החברה החודש", value=total_count)
        st.metric(label="💰 סכום עמלות כולל לתשלום למערכת (1 ש״ח למשלוח)", value=f"₪{amount_base:.2f}")
        
        st.subheader("👥 פירוט פעילות לפי שליחי החברה:")
        for c in company_couriers:
            c_deliveries = [d for d in company_deliveries if d.get("courier") == c]
            st.write(f"- **שליח: {c}** | מספר משלוחים שביצע: {len(c_deliveries)}")
        
        st.subheader("📋 רשימת כל המשלוחים המלאה של החברה:")
        for d in company_deliveries:
            st.caption(f"- שליח: {d.get('courier')} | ברקוד: {d.get('ברקוד')} | ללקוח: {d.get('שם לקוח')} | סטטוס: {d.get('status')} | תאריך: {d.get('date')}")
        
        st.stop()

# --- מסך המערכת המרכזי (שליחים, מנהלי חברות ומנהל ראשי) ---
if st.session_state.logged_in:
    if st.session_state.role == "שליח":
        st.sidebar.title(f"{t['welcome_courier']}, {st.session_state.username}")
        st.sidebar.markdown("---")
        
        if st.sidebar.button("📝 אישור תנאי שימוש ופרטים אישיים"):
            st.session_state.show_contract_screen = True
        else:
            if "show_contract_screen" not in st.session_state:
                st.session_state.show_contract_screen = False

        if st.sidebar.button(t["logout"]):
            logout_user()

    # בדיקה האם השליח ביקש להציג את מסך אישור החוזה והפרטים
    if st.session_state.get("show_contract_screen", False) and st.session_state.role == "שליח":
        st.title("📝 תנאי שימוש במערכת ורישום פרטי השליח")
        st.write("אנא מלא את פרטיך האישיים והעסקיים במדויק וקרא את תנאי השימוש טרם האישור.")

        if st.button("⬅️ חזרה למערכת המשלוחים"):
            st.session_state.show_contract_screen = False
            st.rerun()

        st.subheader("1. פרטים אישיים ועסקיים")
        col1, col2 = st.columns(2)

        with col1:
            first_name = st.text_input("שם פרטי (חובה)")
            last_name = st.text_input("שם משפחה (חובה)")
            id_number = st.text_input("מספר תעודת זהות (חובה)")
            phone = st.text_input("מספר טלפון נייד (חובה)")

        with col2:
            address = st.text_input("כתובת מלאה (רחוב, בית, ישוב) (חובה)")
            business_type = st.selectbox("סוג מעמד עסקי", ["עוסק פטור", "עוסק מורשה"])
            business_id_number = st.text_input("מספר ח.פ / מספר עוסק מורשה / פטור")
            vehicle_type = st.selectbox("סוג כלי רכב", ["אופנוע", "רכב פרטי", "אופניים חשמליים", "ברגל"])
            license_number = st.text_input("מספר רישיון נהיגה")

        st.subheader("2. העלאת מסמך עסק / תעודת עוסק או ח.פ")
        uploaded_file = st.file_uploader("העלה צילום / מסמך (PDF أو תמונה של תעודת עוסק / ح.פ)", type=["pdf", "png", "jpg", "jpeg"])

        st.divider()

        st.subheader("3. תנאי השימוש במערכת ותשלום עמלות")
        contract_text = """
השימוש במערכת ניהול המשלוחים כפוף לתנאים הבאים:
1. מהות השירות: המערכת משמשת ככלי טכנולוגי מתקדם לניהול, סידור ורישום משלוחים עבור הפעילות העסקית העצמאית של השליח.
2. תשלום עמלות ודמי שימוש: השליח מתחייב לשלם למנהל המערכת דמי שימוש ועמלה בסך 1 ₪ עבור כל משלוח שנקלט במערכת תחת חשבונו.
3. הסרת אחריות משפטית ותפעולית: האחריות הבלעדית על ביצוע המשלוחים חלה על השליח בלבד.
4. קניין רוחני: כל הזכויות במערכת הינן רכושו של מנהל המערכת.
"""
        st.text_area("תנאי השימוש המחייבים:", contract_text, height=200, disabled=True)

        st.divider()

        st.subheader("4. אישור וחתימה דיגיטלית")
        agree = st.checkbox("אני מאשר/ת שקראתי את תנאי השימוש בעיון, כי אני מסכים לתשלום העמלה ושכל הפרטים נכונים.")
        signature_name = st.text_input("הקלד את שמך המלא כחתימה דיגיטלית (חובה)")

        if st.button("שמור אישור והשלם רישום"):
            if not first_name or not last_name or not id_number or not phone or not address or not signature_name or not agree:
                st.error("אנא מלא את כל שדות החובה.")
            else:
                file_path_saved = "ללא קובץ"
                if uploaded_file is not None:
                    file_path_saved = os.path.join(UPLOAD_DIR, f"{id_number}_{uploaded_file.name}")
                    with open(file_path_saved, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                driver_record = {
                    "שם פרטי": first_name,
                    "שם משפחה": last_name,
                    "תז": id_number,
                    "חפ_או_עוסק": business_type,
                    "מספר_חפ": business_id_number,
                    "קובץ_חפ": file_path_saved,
                    "טלפון": phone,
                    "כתובת": address,
                    "סוג עוסק": business_type,
                    "רכב": vehicle_type,
                    "רישיון": license_number,
                    "חתימה": signature_name,
                    "תאריך ושעה": get_israel_time()
                }
                save_contract_data(driver_record)
                st.success("הפרטים והאישור נשמרו בהצלחה במערכת!")
                st.session_state.show_contract_screen = False
                st.rerun()
        st.stop()

    # --- הצגת מסך ניהול המשלוחים הראשי ---
    st.title(t["title"])
    
    # סינון משלוחים לפי הרשאות משתמש
    role = st.session_state.role
    username = st.session_state.username
    company = st.session_state.company

    if role == "מנהל מערכת ראשי (Super Admin)":
        user_deliveries = st.session_state.deliveries
    elif role == "מנהל חברה (Company Admin)":
        company_couriers = [usr for usr, info in st.session_state.couriers_db.items() if info.get("company") == company]
        user_deliveries = [d for d in st.session_state.deliveries if d.get("company") == company or d.get("courier") in company_couriers or d.get("courier") == username]
    else:  # שליח רגיל
        user_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == username]

    st.sidebar.markdown("---")
    st.sidebar.subheader(t["current_loc"])
    start_location = st.sidebar.text_input(t["loc_placeholder"], value="כסרא-סמיע")

    st.info(f"{t['active_deliveries']} **{len(user_deliveries)}** {t['active_deliveries_end']}")
    st.caption(f"{t['current_time']} {get_israel_time()} | {t['start_point_label']} **{start_location}**")

    # טופס הוספת משלוח חדש
    with st.expander(t["add_new_del"], expanded=False):
        with st.form("add_delivery_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_barcode = st.text_input(t["barcode"], value=f"TRK-{int(datetime.now().timestamp())}")
                new_cust_name = st.text_input(t["cust_name"])
                new_comp_name = st.text_input(t["company_name"], value=company if role != "מנהל מערכת ראשי (Super Admin)" else "Independent")
                new_phone = st.text_input(t["phone"])
            with col2:
                new_city = st.text_input(t["city"])
                new_street = st.text_input(t["street"])
                new_house = st.text_input(t["house"])
                new_floor = st.text_input(t["floor"])
            
            new_notes = st.text_area(t["notes"])
            submit_delivery = st.form_submit_button(t["save_del"])

            if submit_delivery:
                if not new_cust_name or not new_city:
                    st.error(t["fill_required"])
                else:
                    full_addr = f"{new_city}"
                    if new_street:
                        full_addr += f", {new_street}"
                    if new_house:
                        full_addr += f" {new_house}"

                    delivery_item = {
                        "ברקוד": new_barcode,
                        "שם לקוח": new_cust_name,
                        "שם חברה": new_comp_name,
                        "טלפון": new_phone,
                        "כתובת מלאה": full_addr,
                        "רחוב": new_street,
                        "בית": new_house,
                        "קומה": new_floor,
                        "עיר": new_city,
                        "הערות": new_notes,
                        "status": "ממתין",
                        "courier": username,
                        "company": company if role != "מנהל מערכת ראשי (Super Admin)" else "Independent",
                        "date": get_israel_time()
                    }
                    st.session_state.deliveries.append(delivery_item)
                    st.success(t["del_success"])
                    st.rerun()

    st.divider()
    st.subheader(t["list_title"])

    if not user_deliveries:
        st.warning(t["no_deliveries"])
    else:
        if st.button(t["sort_btn"]):
            # סידור המסלול אלפabetית לפי עיר, רחוב ומספר בית
            st.session_state.deliveries = sorted(
                st.session_state.deliveries,
                key=lambda x: (x.get("עיר", ""), x.get("רחוב", ""), str(x.get("בית", "")))
            )
            st.success(t["sort_success"])
            st.rerun()

        for idx, d in enumerate(user_deliveries):
            status_color = "🟢" if d.get("status") == "נמסר" else "🟠"
            with st.expander(f"{status_color} {idx+1}. {d.get('שם לקוח')} | {d.get('עיר')} ({d.get('שם חברה')}) - [ברקוד: {d.get('ברקוד')}]"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**{t['cust_name']}** {d.get('שם לקוח')}")
                    st.write(f"**{t['company_name']}** {d.get('שם חברה')}")
                    st.write(f"**{t['phone']}** {d.get('טלפון')}")
                    st.write(f"**{t['address']}** {d.get('כתובת מלאה')}")
                    if d.get("הערות"):
                        st.info(f"**{t['notes']}** {d.get('הערות')}")
                with col_b:
                    st.write(f"**{t['added_at']}** {d.get('date')}")
                    st.write(f"**סטטוס:** {d.get('status')}")
                    st.write(f"**שליח מבצע:** {d.get('courier')}")

                # כפתורי פעולה מהירים (וואטסאפ, ניווט, סימון כנמסר)
                c_phone_clean = str(d.get("טלפון", "")).replace("+", "").strip()
                if c_phone_clean.startswith("0"):
                    c_phone_clean = "972" + c_phone_clean[1:]
                
                wa_text = f"مرحباً {d.يجري if 'שם לקוח' in d else d.get('שם לקוח')}, مندوب التوصيل في طريقه إليك بخصوص شحنة من {d.get('שם חברה')}. يرجى الجاهزية."
                encoded_wa = urllib.parse.quote(wa_text)
                wa_link = f"https://wa.me/{c_phone_clean}?text={encoded_wa}"

                waze_dest = urllib.parse.quote(f"{d.get('עיר')} {d.get('רחוב', '')} {d.get('בית', '')}")
                waze_origin = urllib.parse.quote(start_location)
                waze_link = f"https://www.waze.com/ul?q={waze_dest}&navigate=yes"

                b_col1, b_col2, b_col3 = st.columns(3)
                with b_col1:
                    if c_phone_clean:
                        st.markdown(f"[📲 וואטסאפ ללקוח]({wa_link})", unsafe_allow_html=True)
                with b_col2:
                    st.markdown(f"[🚗 נווט בוויז]({waze_link})", unsafe_allow_html=True)
                with b_col3:
                    if d.get("status") != "נמסר":
                        if st.button(t["mark_delivered"], key=f"deliv_btn_{idx}"):
                            # עדכון הסטטוס במסשיון
                            for real_idx, orig_d in enumerate(st.session_state.deliveries):
                                if orig_d.get("ברקוד") == d.get("ברקוד") and orig_d.get("שם לקוח") == d.get("שם לקוח"):
                                    st.session_state.deliveries[real_idx]["status"] = "נמסר"
                                    break
                            st.success(t["delivered_success"])
                            st.rerun()

                # עריכת פרטי משלוח
                with st.form(f"edit_delivery_form_{idx}"):
                    st.subheader(t["edit_del"])
                    e_cust = st.text_input(t["cust_name"], value=d.get("שם לקוח"), key=f"e_cust_{idx}")
                    e_phone = st.text_input(t["phone"], value=d.get("טלפון"), key=f"e_phone_{idx}")
                    e_city = st.text_input(t["city"], value=d.get("עיר"), key=f"e_city_{idx}")
                    e_street = st.text_input(t["street"], value=d.get("רחוב", ""), key=f"e_street_{idx}")
                    e_house = st.text_input(t["house"], value=d.get("בית", ""), key=f"e_house_{idx}")
                    e_notes = st.text_area(t["notes"], value=d.get("הערות", ""), key=f"e_notes_{idx}")
                    
                    save_edit = st.form_submit_button(t["save_changes"])
                    if save_edit:
                        for real_idx, orig_d in enumerate(st.session_state.deliveries):
                            if orig_d.get("ברקוד") == d.get("ברקוד"):
                                st.session_state.deliveries[real_idx]["שם לקוח"] = e_cust
                                st.session_state.deliveries[real_idx]["טלפון"] = e_phone
                                st.session_state.deliveries[real_idx]["עיר"] = e_city
                                st.session_state.deliveries[real_idx]["רחוב"] = e_street
                                st.session_state.deliveries[real_idx]["בית"] = e_house
                                st.session_state.deliveries[real_idx]["הערות"] = e_notes
                                full_addr = f"{e_city}"
                                if e_street:
                                    full_addr += f", {e_street}"
                                if e_house:
                                    full_addr += f" {e_house}"
                                st.session_state.deliveries[real_idx]["כתובת מלאה"] = full_addr
                                break
                        st.success(t["edit_success"])
                        st.rerun()
