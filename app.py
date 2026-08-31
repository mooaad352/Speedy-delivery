import streamlit as st
import urllib.parse
from datetime import datetime, timezone, timedelta
import pandas as pd
import os

# הגדרת שעון ישראל (UTC+2 / UTC+3)
ISRAEL_OFFSET = timedelta(hours=2)
ADMIN_PHONE = "972502616375"  # מספר הטלפון שלך כמנהל המערכת

def get_israel_time():
    return datetime.now(timezone(ISRAEL_OFFSET)).strftime("%Y-%m-%d %H:%M")

def get_current_date():
    return datetime.now(timezone(ISRAEL_OFFSET))

# הגדרת עיצוב הדף (כיוון מימין לשמאל כברירת מחדל)
st.set_page_config(page_title="Speedy Delivery - מערכת ניהול משלוחים", page_icon="🚚", layout="wide")

# --- קובץ שמירת חוזי שימוש ופרטי שליחים ---
CONTRACTS_FILE = "delivery_drivers_contracts.csv"
UPLOAD_DIR = "uploaded_documents"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

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
        "welcome_admin": "Admin Manager",
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

# --- מנגנון שמירת חיבור גם אחרי רענון ---
query_params = st.query_params

if "logged_in" not in st.session_state:
    if query_params.get("logged_in") == "true" and "username" in query_params:
        st.session_state.logged_in = True
        st.session_state.username = query_params["username"]
        st.session_state.role = query_params.get("role", "שליח")
    else:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

# מאגר שליחים ומנהלים
if "couriers_db" not in st.session_state:
    st.session_state.couriers_db = {
        "Admin": {"password": "Sma.srablove2028", "role": "מנהל מערכת (Admin)", "phone": ADMIN_PHONE},
        "mohammad": {"password": "123", "role": "שליח", "phone": "+972502616375"}
    }

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
            "date": current_time_il
        }
    ]

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
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
                
                st.query_params["logged_in"] = "true"
                st.query_params["username"] = username_input
                st.query_params["role"] = db[username_input]["role"]
                
                st.rerun()
            else:
                st.error(t["login_error"])

# --- אזור הניהול למנהל (Admin) בלבד ---
elif st.session_state.role == "מנהל מערכת (Admin)":
    st.sidebar.title(t["welcome_admin"])
    admin_menu = st.sidebar.radio(
        t["admin_menu"], 
        [
            t["main_sys"], 
            t["add_courier"], 
            t["manage_users"],
            t["monthly_report"],
            t["contract_menu"]
        ]
    )
    
    if st.sidebar.button(t["logout"]):
        logout_user()

    if admin_menu == t["add_courier"]:
        st.title(t["add_courier"])
        with st.form("add_courier_form"):
            new_user = st.text_input(t["username"])
            new_pass = st.text_input(t["password"], type="password")
            new_phone_input = st.text_input(t["phone"])
            new_role = st.selectbox("Role", ["שליח", "מנהל מערכת (Admin)"])
            add_btn = st.form_submit_button(t["login_btn"])
            
            if add_btn:
                if new_user and new_pass:
                    clean_phone = new_phone_input.replace("+", "").strip()
                    if clean_phone.startswith("0"):
                        clean_phone = "972" + clean_phone[1:]
                    st.session_state.couriers_db[new_user] = {
                        "password": new_pass, 
                        "role": new_role,
                        "phone": clean_phone
                    }
                    st.success("Added successfully!")
                    
                    # שימוש בכתובת המדויקת של האפליקציה שלך
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
        for usr, info in st.session_state.couriers_db.items():
            with st.expander(f"User: {usr} ({info.get('role', '')})"):
                with st.form(f"edit_user_{usr}"):
                    updated_pass = st.text_input(t["password"], value=info["password"], type="password")
                    updated_phone = st.text_input(t["phone"], value=info.get("phone", ""))
                    update_btn = st.form_submit_button(t["save_changes"])
                    
                    if update_btn:
                        st.session_state.couriers_db[usr]["password"] = updated_pass
                        st.session_state.couriers_db[usr]["phone"] = updated_phone
                        st.success(t["edit_success"])
        st.stop()

    elif admin_menu == t["monthly_report"]:
        st.title(t["monthly_report"])
        st.info("💡 החיוב למערכת מבוסס על 1 ₪ לכל משלוח שנקלט במערכת עבור כל שליח (לפני מע״מ לעוסק מורשה / פטור למע״מ לעוסק פטור).")
        
        couriers_list = [usr for usr, info in st.session_state.couriers_db.items() if info.get("role") == "שליח"]
        current_month_str = get_current_date().strftime("%Y-%m")
        st.subheader(f"📅 סיכום חודש נוכחי: {current_month_str}")

        for courier in couriers_list:
            courier_deliveries = [
                d for d in st.session_state.deliveries 
                if d.get("courier") == courier and d.get("date", "").startswith(current_month_str)
            ]
            total_count = len(courier_deliveries)
            
            amount_base = total_count * 1.0
            
            courier_phone = st.session_state.couriers_db[courier].get("phone", "")
            
            with st.expander(f"👤 שליח: {courier} | משלוחים שנקלטו: {total_count} | סכום בסיס: ₪{amount_base:.2f}"):
                st.write(f"📞 טלפון השליח: {courier_phone}")
                st.write(f"📊 פירוט חישוב:")
                st.write(f"- סך משלוחים שנקלטו במערכת: {total_count}")
                st.write(f"- סכום לתשלום (1 ש״ח למשלוח): ₪{amount_base:.2f}")
                
                st.write(f"📦 רשימת המשלוחים שנקלטו החודש:")
                for d in courier_deliveries:
                    st.caption(f"- ברקוד: {d.get('ברקוד')} | ללקוח: {d.get('שם לקוח')} | סטטוס: {d.get('status')} | תאריך: {d.get('date')}")
                
                if courier_phone:
                    fee_msg = f"שלום {courier}, סיכום השימוש שלך במערכת לחודש {current_month_str}:\n- סך משלוחים שנקלטו: {total_count}\n- סכום לתשלום: ₪{amount_base:.2f}\n\nתודה רבה!"
                    encoded_fee_msg = urllib.parse.quote(fee_msg)
                    wa_fee_url = f"https://wa.me/{courier_phone}?text={encoded_fee_msg}"
                    st.markdown(f"[📲 שליחת הודעת חיוב עמלות לשליח בוואטסאפ]({wa_fee_url})", unsafe_allow_html=True)
        
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

# --- מסך המערכת המרכזי (שליחים ומנהל) ---
if st.session_state.logged_in:
    if st.session_state.role != "מנהל מערכת (Admin)":
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
    if st.session_state.get("show_contract_screen", False) and st.session_state.role != "מנהל מערכת (Admin)":
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
        uploaded_file = st.file_uploader("העלה צילום / מסמך (PDF או תמונה של תעודת עוסק / ח.פ)", type=["pdf", "png", "jpg", "jpeg"])

        st.divider()

        st.subheader("3. תנאי השימוש במערכת ותשלום עמלות")
        contract_text = """
השימוש במערכת ניהול המשלוחים כפוף לתנאים הבאים:
1. מהות השירות: המערכת משמשת ככלי טכנולוגי מתקדם לניהול, סידור ורישום משלוחים עבור הפעילות העסקית העצמאית של השליח. הרישיון הינו אישי, בלתי ניתן להעברה ומוענק לשימוש בכפוף לעמידה בתנאים אלו.
2. תשלום עמלות ודמי שימוש: השליח מתחייב לשלם למנהל המערכת דמי שימוש ועמלה בסך 1 ₪ עבור כל משלוח שנקלט במערכת תחת חשבונו. הסכום האמור הוא לפני מע"מ עבור שליחים שהם עוסק מורשה, בעוד ששליחים שהם עוסק פטור פטורים מתשלום מע"מ בהתאם לחוק.
3. הסרת אחריות משפטית ותפעולית: האחריות הבלעדית והמלאה על ביצוע המשלוחים בשטח, החבילות מול הלקוחות, כלי הרכב, רישיונות, ביטוחים וכל הוצאה נלווית – חלה על השליח בלבד. מנהל המערכת מספק תוכנה טכנולוגית בלבד ואינו צד לעסקאות שבין השליח ללקוחותיו, ולא יישא באחריות לכל נזק, אובדן, עיכוב או תקלות בשטח.
4. אמינות נתונים ושימוש במערכת: כל הפרטים, הכתובות והמשלוחים שהשליח מזין למערכת הינם באחריותו המלאה. השליח מתחייב שלא לעשות במערכת שימוש בלתי חוקי או פוגעני.
5. קניין רוחני: כל הזכויות במערכת, בקוד, בעיצוב ובשם הינן רכושו הבלעדי של מנהל המערכת. חל איסור מוחלט להעתיק, לשכפל או לבצע הנדסה לאחור לתוכנה.
6. הפסקת שימוש: מנהל המערכת שומר לעצמו את הזכות לחסום או להפסיק את גיסתו של כל שליח למערכת באופן מיידי במקרה של הפרת תנאי מתנאים אלו או אי-תשלום עמלות.
7. שיפוי: השליח מתחייב לשפות את מנהל המערכת בגין כל נזק, הפסד או הוצאה (לרבות שכר טרחת עורך דין) שייגרמו עקב הפרת תנאים אלו או פעילותו של השליח.
"""
        st.text_area("תנאי השימוש המחייבים:", contract_text, height=200, disabled=True)

        st.divider()

        st.subheader("4. אישור וחתימה דיגיטלית")
        agree = st.checkbox("אני מאשר/ת שקראתי את תנאי השימוש בעיון, כי אני מסכים לתשלום העמלה (1 ₪ לכל משלוח שנקלט) ושכל הפרטים שמסרתי נכונים ומדויקים.")
        signature_name = st.text_input("הקלד את שמך המלא כחתימה דיגיטלית (חובה)")

        if st.button("שמור אישור והשלם רישום"):
            if not first_name or not last_name or not id_number or not phone or not address or not signature_name or not agree:
                st.error("אנא מלא את כל שדות החובה (שם פרטי, שם משפחה, ת.ז, טלפון, כתובת), הקלד חתימה דיגיטלית וסמן את תיבת האישור.")
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
                    "סוג עוסק": business_type,
                    "מספר_חפ": business_id_number if business_id_number else "לא הוזן",
                    "קובץ_חפ": file_path_saved,
                    "טלפון": phone,
                    "כתובת": address,
                    "רכב": vehicle_type,
                    "רישיון": license_number if license_number else "אין",
                    "חתימה": signature_name,
                    "תאריך ושעה": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                save_contract_data(driver_record)
                st.success(f"תודה רבה {first_name} {last_name}! אישור תנאי השימוש והפרטים שלך נקלטו בהצלחה במערכת.")
                st.session_state.show_contract_screen = False
    
        st.stop()

    st.sidebar.markdown("---")
    st.sidebar.subheader(t["current_loc"])
    start_point = st.sidebar.text_input(t["loc_placeholder"], "כסרא-סמיע")

    st.title(t["title"])

    if st.session_state.role != "מנהל מערכת (Admin)":
        my_deliveries_count = len([d for d in st.session_state.deliveries if d.get("courier") == st.session_state.username and d.get("status") != "נמסר"])
        st.info(f"📦 {t['active_deliveries']} **{my_deliveries_count}** {t['active_deliveries_end']}")

    current_time_il_str = get_israel_time()
    st.caption(f"🕒 {t['current_time']} **{current_time_il_str}** | 🏁 {t['start_point_label']} **{start_point}**")

    st.subheader(t["add_new_del"])
    
    with st.form("delivery_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            barcode_num = st.text_input(t["barcode"])
            cust_name = st.text_input(t["cust_name"])
            company_name = st.text_input(t["company_name"], "SHEIN")
        with col2:
            raw_cust_phone = st.text_input(t["phone"])
            city_name = st.text_input(t["city"], "כסרא-סמיע")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            street_name = st.text_input(t["street"])
        with col_s2:
            house_num = st.text_input(t["house"])
        with col_s3:
            floor_num = st.text_input(t["floor"])
            
        cust_notes = st.text_input(t["notes"])
        
        submit_del = st.form_submit_button(t["save_del"])
        if submit_del:
            if cust_name and city_name:
                clean_cust_phone = raw_cust_phone.replace("+", "").strip()
                if clean_cust_phone.startswith("0"):
                    clean_cust_phone = "972" + clean_cust_phone[1:]
                elif not clean_cust_phone.startswith("972"):
                    clean_cust_phone = "972" + clean_cust_phone
                
                addr_parts = []
                if street_name:
                    addr_parts.append(street_name)
                if house_num:
                    addr_parts.append(house_num)
                
                street_house_str = " ".join(addr_parts)
                full_address = f"{street_house_str + ', ' if street_house_str else ''}{city_name}" + (f" (קומה {floor_num})" if floor_num else "")
                
                added_time = get_israel_time()
                
                st.session_state.deliveries.append({
                    "ברקוד": barcode_num if barcode_num else "ללא ברקוד",
                    "שם לקוח": cust_name,
                    "שם חברה": company_name if company_name else "SHEIN",
                    "טלפון": clean_cust_phone,
                    "כתובת מלאה": full_address,
                    "רחוב": street_name,
                    "בית": house_num,
                    "קומה": floor_num,
                    "עיר": city_name,
                    "הערות": cust_notes,
                    "status": "ממתין",
                    "courier": st.session_state.username if st.session_state.role != "מנהל מערכת (Admin)" else "mohammad",
                    "date": added_time
                })
                st.success(t["del_success"])
            else:
                st.warning(t["fill_required"])

    st.subheader(t["list_title"])
    
    if st.button(t["sort_btn"]):
        if st.session_state.role == "מנהל מערכת (Admin)":
            st.session_state.deliveries.sort(key=lambda x: (x.get("עיר", "") != start_point, x.get("עיר", ""), x.get("רחוב", ""), str(x.get("בית", "0"))))
        else:
            other_deliveries = [d for d in st.session_state.deliveries if d.get("courier") != st.session_state.username]
            my_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == st.session_state.username]
            
            my_deliveries.sort(key=lambda x: (x.get("עיר", "") != start_point, x.get("עיר", ""), x.get("רחוב", ""), str(x.get("בית", "0"))))
            st.session_state.deliveries = other_deliveries + my_deliveries
            
        st.success(t["sort_success"])
        st.rerun()

    if st.session_state.role == "מנהל מערכת (Admin)":
        current_deliveries = st.session_state.deliveries
    else:
        current_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == st.session_state.username]

    if len(current_deliveries) == 0:
        st.info(t["no_deliveries"])
    else:
        for index, item in enumerate(current_deliveries, start=1):
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    status_str = f"✅ {t['status_delivered']}" if item.get("status") == "נמסר" else f"⏳ {t['status_waiting']}"
                    st.markdown(f"**#{index} | {status_str} | {t['barcode']}** {item.get('ברקוד')} | **{t['cust_name']}** {item.get('שם לקוח')}")
                    st.write(f"📍 **{t['address']}** {item.get('כתובת מלאה')}")
                    st.caption(f"{t['added_at']} {item.get('date', 'Today')}")
                    if item.get('הערות'):
                        st.caption(f"{t['notes']} {item.get('הערות')}")
                    
                    cust_tel = item.get("טלפון", "").strip()
                    comp_name = item.get("שם חברה", "SHEIN")
                    customer_name = item.get("שם לקוח", "Customer")
                    if cust_tel:
                        customer_msg = f"שלום {customer_name}, אני השליח. יש לך משלוח מ{comp_name}, אני בדרך אליך אגיע בקרוב מאוד! 🚚"
                        encoded_customer_msg = urllib.parse.quote(customer_msg)
                        wa_customer_url = f"https://wa.me/{cust_tel}?text={encoded_customer_msg}"
                        st.markdown(f"[{t['whatsapp_btn']}]({wa_customer_url})", unsafe_allow_html=True)

                with col2:
                    dest_address = item.get('כתובת מלאה', '')
                    waze_url = f"https://www.waze.com/ul?from={urllib.parse.quote(start_point)}&q={urllib.parse.quote(dest_address)}&navigate=yes"
                    st.markdown(f"[{t['waze_btn']} {start_point} ב-Waze]({waze_url})", unsafe_allow_html=True)
                
                with col3:
                    if item.get("status") != "נמסר":
                        if st.button(f"{t['mark_delivered']} #{index}", key=f"deliver_{index}"):
                            item["status"] = "נמסר"
                            st.success(t["delivered_success"])
                            st.rerun()
                
                with st.expander(f"{t['edit_del']} #{index}"):
                    with st.form(f"edit_delivery_form_{index}"):
                        e_barcode = st.text_input(t["barcode"], value=item.get("ברקוד", ""))
                        e_cust_name = st.text_input(t["cust_name"], value=item.get("שם לקוח", ""))
                        e_company = st.text_input(t["company_name"], value=item.get("שם חברה", ""))
                        e_phone = st.text_input(t["phone"], value=item.get("טלפון", ""))
                        e_city = st.text_input(t["city"], value=item.get("עיר", ""))
                        e_street = st.text_input(t["street"], value=item.get("רחוב", ""))
                        e_house = st.text_input(t["house"], value=item.get("בית", ""))
                        e_floor = st.text_input(t["floor"], value=item.get("קומה", ""))
                        e_notes = st.text_input(t["notes"], value=item.get("הערות", ""))
                        
                        save_edit_btn = st.form_submit_button(t["save_changes"])
                        if save_edit_btn:
                            item["ברקוד"] = e_barcode
                            item["שם לקוח"] = e_cust_name
                            item["שם חברה"] = e_company
                            item["טלפון"] = e_phone
                            item["עיר"] = e_city
                            item["רחוב"] = e_street
                            item["בית"] = e_house
                            item["קומה"] = e_floor
                            item["הערות"] = e_notes
                            
                            addr_parts = []
                            if e_street:
                                addr_parts.append(e_street)
                            if e_house:
                                addr_parts.append(e_house)
                            street_house_str = " ".join(addr_parts)
                            item["כתובת מלאה"] = f"{street_house_str + ', ' if street_house_str else ''}{e_city}" + (f" (קומה {e_floor})" if e_floor else "")
                            
                            st.success(t["edit_success"])
                            st.rerun()

                st.markdown("---")
