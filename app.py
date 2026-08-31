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

    # 1. מערכת משלוחים ראשית
    if admin_menu == t["main_sys"]:
        st.title(t["main_sys"])
        
        st.markdown(f"### {t['current_loc']}")
        start_location = st.text_input(t["loc_placeholder"], value="כסרא-סמיע")
        
        admin_deliveries = st.session_state.deliveries
        
        completed_count = len([d for d in admin_deliveries if d["status"] == "נמסר"])
        pending_count = len([d for d in admin_deliveries if d["status"] == "ממתין"])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("סך הכל משלוחים", len(admin_deliveries))
        col2.metric("ממתינים לביצוע", pending_count)
        col3.metric("נמסרו בהצלחה", completed_count)
        
        st.divider()

        with st.expander(t["add_new_del"], expanded=False):
            with st.form("admin_add_delivery_form"):
                col_a, col_b = st.columns(2)
                with col_a:
                    new_barcode = st.text_input(t["barcode"], value=f"DEL-{len(admin_deliveries)+101}")
                    new_cust_name = st.text_input(t["cust_name"])
                    new_company_name = st.text_input(t["company_name"], value="Shop")
                    new_phone = st.text_input(t["phone"], value="972")
                with col_b:
                    new_city = st.text_input(t["city"])
                    new_street = st.text_input(t["street"])
                    new_house = st.text_input(t["house"])
                    new_floor = st.text_input(t["floor"])
                
                new_notes = st.text_area(t["notes"])
                
                company_list = list(set([info.get("company", "Independent") for usr, info in st.session_state.couriers_db.items()]))
                assigned_company = st.selectbox("שייך לחברת משלוחים:", company_list)
                
                submit_new_del = st.form_submit_button(t["save_del"])
                if submit_new_del:
                    if new_cust_name and new_city:
                        current_time_il = get_israel_time()
                        new_item = {
                            "ברקוד": new_barcode,
                            "שם לקוח": new_cust_name,
                            "שם חברה": new_company_name,
                            "טלפון": new_phone,
                            "כתובת מלאה": f"{new_city}, {new_street} {new_house}".strip(),
                            "רחוב": new_street,
                            "בית": new_house,
                            "קומה": new_floor,
                            "עיר": new_city,
                            "הערות": new_notes,
                            "status": "ממתין",
                            "courier": "Admin",
                            "company": assigned_company,
                            "date": current_time_il
                        }
                        st.session_state.deliveries.append(new_item)
                        st.success(t["del_success"])
                        st.rerun()
                    else:
                        st.warning(t["fill_required"])

        st.divider()
        st.subheader(t["list_title"])

        if st.button(t["sort_btn"]):
            st.success(t["sort_success"])

        if not admin_deliveries:
            st.info(t["no_deliveries"])
        else:
            for idx, item in enumerate(admin_deliveries):
                status_color = "🟢" if item["status"] == "נמסר" else "🟠"
                with st.expander(f"{status_color} 📦 {item['שם לקוח']} | {item['עיר']} | חברה: {item.get('company', 'Independent')} | סטטוס: {item['status']}"):
                    st.write(f"**{t['barcode']}** {item['ברקוד']}")
                    st.write(f"**{t['company_name']}** {item['שם חברה']}")
                    st.write(f"**{t['phone']}** {item['טלפון']}")
                    st.write(f"**{t['address']}** {item['עיר']}, {item.get('רחוב', '')} {item.get('בית', '')}")
                    st.write(f"**הערות:** {item.get('הערות', 'אין')}")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if item["status"] == "ממתין":
                            if st.button(t["mark_delivered"], key=f"admin_mark_{idx}"):
                                item["status"] = "נמסר"
                                st.success(t["delivered_success"])
                                st.rerun()
                    with col_btn2:
                        phone_clean = item['טלפון'].strip().replace("+", "")
                        cust_n = item['שם לקוח']
                        comp_n = item['שם חברה']
                        wa_text = f"שלום {cust_n}, שליח בדרך אליך עם משלוח מ-{comp_n}."
                        whatsapp_link = f"https://wa.me/{phone_clean}?text={urllib.parse.quote(wa_text)}"
                        st.markdown(f"[{t['whatsapp_btn']}]({whatsapp_link})", unsafe_allow_html=True)

    # 2. הוספת מנהל חברת משלוחים
    elif admin_menu == t["add_company_admin"]:
        st.title(t["add_company_admin"])
        with st.form("add_comp_admin_form"):
            new_comp_username = st.text_input("שם משתמש למנהל החברה:")
            new_comp_password = st.text_input("סיסמה:", type="password")
            new_comp_name = st.text_input("שם חברת המשלוחים / עסק:")
            new_comp_phone = st.text_input("מספר טלפון ליצירת קשר:")
            
            submit_comp = st.form_submit_button("הוסף מנהל חברה חדש")
            if submit_comp:
                if new_comp_username and new_comp_password and new_comp_name:
                    if new_comp_username in st.session_state.couriers_db:
                        st.error("שם המשתמש כבר קיים במערכת!")
                    else:
                        st.session_state.couriers_db[new_comp_username] = {
                            "password": new_comp_password,
                            "role": "מנהל חברה (Company Admin)",
                            "phone": new_comp_phone,
                            "company": new_comp_name
                        }
                        save_users_db(st.session_state.couriers_db)
                        st.success(f"מנהל החברה '{new_comp_username}' נוסף בהצלחה!")
                else:
                    st.warning("נא למלא את כל השדות החובה.")

    # 3. הוספת שליח חדש
    elif admin_menu == t["add_courier"]:
        st.title(t["add_courier"])
        with st.form("add_courier_form"):
            c_username = st.text_input("שם משתמש לשליח:")
            c_password = st.text_input("סיסמה:", type="password")
            c_phone = st.text_input("מספר טלפון של השליח:")
            
            company_list = list(set([info.get("company", "Independent") for usr, info in st.session_state.couriers_db.items()]))
            c_company = st.selectbox("שייך לחברת משלוחים:", company_list)
            
            submit_courier = st.form_submit_button("הוסף שליח חדש")
            if submit_courier:
                if c_username and c_password:
                    if c_username in st.session_state.couriers_db:
                        st.error("שם המשתמש כבר קיים!")
                    else:
                        st.session_state.couriers_db[c_username] = {
                            "password": c_password,
                            "role": "שליח",
                            "phone": c_phone,
                            "company": c_company
                        }
                        save_users_db(st.session_state.couriers_db)
                        st.success(f"השליח '{c_username}' נוסף בהצלחה!")
                else:
                    st.warning("נא למלא שם משתמש וסיסמה.")

    # 4. ניהול ועריכת משתמשים קיימים
    elif admin_menu == t["manage_users"]:
        st.title(t["manage_users"])
        st.write("כאן ניתן לצפות בכל המשתמשים הרשומים במערכת, לעדכן סיסמאות או למחוק משתמשים.")
        
        users_db = st.session_state.couriers_db
        for usr, info in list(users_db.items()):
            if usr == "Admin":
                continue
            with st.expander(f"👤 משתמש: {usr} | תפקיד: {info.get('role')} | חברה: {info.get('company', 'N/A')}"):
                with st.form(f"edit_user_{usr}"):
                    new_pass = st.text_input("עדכן סיסמה חדשה:", value=info.get("password", ""))
                    new_ph = st.text_input("עדכן טלפון:", value=info.get("phone", ""))
                    
                    col_u1, col_u2 = st.columns(2)
                    with col_u1:
                        update_btn = st.form_submit_button("שמור שינויים")
                    with col_u2:
                        delete_btn = st.form_submit_button("מחק משתמש זה ❌")
                    
                    if update_btn:
                        users_db[usr]["password"] = new_pass
                        users_db[usr]["phone"] = new_ph
                        save_users_db(users_db)
                        st.success(f"הפרטים של {usr} עודכנו בהצלחה!")
                        st.rerun()
                    
                    if delete_btn:
                        del users_db[usr]
                        save_users_db(users_db)
                        st.success(f"המשתמש {usr} נמחק מהמערכת.")
                        st.rerun()

    # 5. דוח חודשי
    elif admin_menu == t["monthly_report"]:
        st.title(t["monthly_report"])
        st.info("💡 החיוב וההתחשבנות מתבצעים ישירות מול מנהלי החברות או השליחים העצמאיים עבור كل משלוח שנקלט.")
        
        current_month_str = get_current_date().strftime("%Y-%m")
        st.subheader(f"📅 סיכום חודש נוכחי: {current_month_str}")

        company_admins = [usr for usr, info in st.session_state.couriers_db.items() if info.get("role"] == "מנהל חברה (Company Admin)"]
        
        report_data = []
        total_system_deliveries = 0

        for c_usr in company_admins:
            c_info = st.session_state.couriers_db[c_usr]
            c_name = c_info.get("company", c_usr)
            
            comp_deliveries = [d for d in st.session_state.deliveries if d.get("company") == c_name]
            count_del = len(comp_deliveries)
            total_system_deliveries += count_del
            
            report_data.append({
                "שם מנהל": c_usr,
                "שם חברה": c_name,
                "טלפון": c_info.get("phone", ""),
                "כמות משלוחים החודש": count_del
            })

        if report_data:
            df_report = pd.DataFrame(report_data)
            st.dataframe(df_report, use_container_width=True)
            st.metric("סך הכל משלוחים במערכת החודש", total_system_deliveries)
        else:
            st.info("אין נתוני חברות זמינים להצגה בדוח החודשי.")

    # 6. תנאי שימוש
    elif admin_menu == t["contract_menu"]:
        st.title(t["contract_menu"])
        st.write("כאן ניתן לראות את תנאי השימוש ואישורי העמלות של המערכת.")
        contracts_df = load_contracts_data()
        if not contracts_df.empty:
            st.dataframe(contracts_df, use_container_width=True)
        else:
            st.info("אין עדיין חוזים או אישורי תנאים רשומים במערכת.")

# --- אזור מנהל חברה או שליח ---
else:
    st.title(f"{t['welcome_courier']} {st.session_state.username}")
    if st.sidebar.button(t["logout"]):
        logout_user()
    
    st.write(f"הנך מחובר כחלק מ-{st.session_state.company}")
    
    st.subheader(t["list_title"])
    filtered_deliveries = [d for d in st.session_state.deliveries if st.session_state.role == "מנהל מערכת ראשי (Super Admin)" or d.get("company") == st.session_state.company or d.get("courier") == st.session_state.username]
    
    if not filtered_deliveries:
        st.info(t["no_deliveries"])
    else:
        for idx, item in enumerate(filtered_deliveries):
            with st.expander(f"📦 {item['שם לקוח']} | {item['עיר']} | סטטוס: {item['status']}"):
                st.write(f"**{t['barcode']}** {item['ברקוד']}")
                st.write(f"**{t['company_name']}** {item['שם חברה']}")
                st.write(f"**{t['phone']}** {item['טלפון']}")
                st.write(f"**{t['address']}** {item['עיר']}, {item.get('רחוב', '')} {item.get('בית', '')}")
                
                if item["status"] == "ממתין":
                    if st.button(t["mark_delivered"], key=f"mark_{idx}"):
                        item["status"] = "נמסר"
                        st.success(t["delivered_success"])
                        st.rerun()
