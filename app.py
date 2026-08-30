import streamlit as st
import urllib.parse
from datetime import datetime
import pytz

# הגדרת אזור זמן ישראל
ISRAEL_TZ = pytz.timezone('Asia/Jerusalem')

# הגדרת עיצוב הדף
st.set_page_config(page_title="מערכת ניהול משלוחים מהירה", page_icon="🚚", layout="wide")

# ניהול מצב התחברות (Session State)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# מאגר שליחים ומנהלים
if "couriers_db" not in st.session_state:
    st.session_state.couriers_db = {
        "Admin": {"password": "Sma.srablove2028", "role": "מנהל מערכת (Admin)", "phone": "+972500000000"},
        "mohammad": {"password": "123", "role": "שליח", "phone": "+972502616375"}
    }

# מאגר משלוחים במערכת (כולל משלוחי הבדיקה)
if "deliveries" not in st.session_state:
    current_time_il = datetime.now(ISRAEL_TZ).strftime("%Y-%m-%d %H:%M")
    st.session_state.deliveries = [
        {
            "ברקוד": "TEST-001",
            "שם לקוח": "סמר שומרי",
            "שם חברה": "SHEIN",
            "טלפון": "+972502616375",
            "כתובת מלאה": "רחוב 701 0, כסרא-סמיע (קומה 1)",
            "רחוב": "701",
            "בית": "0",
            "קומה": "1",
            "עיר": "כסרא-סמיע",
            "הערות": "משלוח בדיקה",
            "status": "ממתין",
            "courier": "mohammad",
            "date": current_time_il
        },
        {
            "ברקוד": "TEST-002",
            "שם לקוח": "סראב",
            "שם חברה": "ניודי",
            "טלפון": "+972503688324",
            "כתובת מלאה": "אלתותה 10, יאנוח",
            "רחוב": "אלתותה",
            "בית": "10",
            "קומה": "0",
            "עיר": "יאנוח",
            "הערות": "משלוח בדיקה",
            "status": "ממתין",
            "courier": "mohammad",
            "date": current_time_il
        }
    ]

# --- מסך התחברות ---
if not st.session_state.logged_in:
    st.title("🚚 מערכת ניהול משלוחים מהירה")
    st.subheader("כניסת משתמשים ושליחים")
    
    with st.form("login_form"):
        username_input = st.text_input("שם משתמש")
        password_input = st.text_input("סיסמה", type="password")
        submit_btn = st.form_submit_button("התחבר")
        
        if submit_btn:
            db = st.session_state.couriers_db
            if username_input in db and db[username_input]["password"] == password_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.session_state.role = db[username_input]["role"]
                st.rerun()
            else:
                st.error("שם משתמש או סיסמה שגויים. נסה שוב.")

# --- אזור הניהול למנהל (Admin) בלבד ---
elif st.session_state.role == "מנהל מערכת (Admin)":
    st.sidebar.title("مرحباً, מנהל ראשי")
    admin_menu = st.sidebar.radio(
        "תפריט ניהול", 
        [
            "מערכת משלוחים ראשית", 
            "הוספת שליח חדש", 
            "ניהול ועריכת משתמשים (סיסמאות וטלפונים)",
            "📊 סיכום חודשי והתחשבנות שליחים"
        ]
    )
    
    if st.sidebar.button("התנתק (Logout)"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    if admin_menu == "הוספת שליח חדש":
        st.title("➕ הוספת שליח או משתמש חדש")
        with st.form("add_courier_form"):
            new_user = st.text_input("שם משתמש חדש לשליח")
            new_pass = st.text_input("סיסמה לשליח", type="password")
            new_phone_input = st.text_input("מספר טלפון (לדוגמה: 0502616375):")
            new_role = st.selectbox("תפקיד במערכת", ["שליח", "מנהל מערכת (Admin)"])
            add_btn = st.form_submit_button("שמור שליח חדש")
            
            if add_btn:
                if new_user and new_pass:
                    formatted_phone = f"+972{new_phone_input[1:]}" if new_phone_input.startswith("0") else new_phone_input
                    st.session_state.couriers_db[new_user] = {
                        "password": new_pass, 
                        "role": new_role,
                        "phone": formatted_phone
                    }
                    st.success(f"השליח '{new_user}' נוסף בהצלחה!")

    elif admin_menu == "ניהול ועריכת משתמשים (סיסמאות וטלפונים)":
        st.title("👥 ניהול, החלפת סיסמאות ועדכון טלפונים לשליחים")
        for usr, info in st.session_state.couriers_db.items():
            with st.expander(f"עריכת משתמש: {usr} ({info.get('role', '')})"):
                with st.form(f"edit_user_{usr}"):
                    updated_pass = st.text_input("סיסמה חדשה", value=info["password"], type="password")
                    updated_phone = st.text_input("מספר טלפון מעודכן", value=info.get("phone", ""))
                    update_btn = st.form_submit_button(f"שמור שינויים עבור {usr}")
                    
                    if update_btn:
                        st.session_state.couriers_db[usr]["password"] = updated_pass
                        st.session_state.couriers_db[usr]["phone"] = updated_phone
                        st.success(f"הפרטים עבור {usr} עודכנו בהצלחה!")
        st.stop()

    elif admin_menu == "📊 סיכום חודשי והתחשבנות שליחים":
        st.title("📊 דוח סיכום משלוחים חודשי להתחשבנות")
        couriers_list = [usr for usr, info in st.session_state.couriers_db.items() if info.get("role") == "שליח"]
        
        summary_data = []
        for courier in couriers_list:
            completed_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == courier and d.get("status") == "נמסר"]
            total_count = len(completed_deliveries)
            summary_data.append({
                "שם השליח": courier,
                "טלפון": st.session_state.couriers_db[courier].get("phone", "לא הוזן"),
                "סך משלוחים שבוצעו (נמסר)": total_count
            })
            
        if summary_data:
            st.table(summary_data)
        else:
            st.info("אין עדיין נתונים על שליחים רשומים.")
        st.stop()

# --- מסך המערכת המרכזי (שליחים ומנהל) ---
if st.session_state.logged_in:
    # תפריט צד לשליחים כולל כפתור התנתק
    if st.session_state.role != "מנהל מערכת (Admin)":
        st.sidebar.title(f"مرحباً, {st.session_state.username}")
        st.sidebar.markdown("---")
        if st.sidebar.button("התנתק (Logout)"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("הגדרות ניווט ויציאה")
    start_point = st.sidebar.text_input("כתובת נקודת מוצא (מאיפה אתה יוצא)", "כסרא-סמיע")

    st.title("🚚 מערכת ניהול וסידור משלוחים מהירה")

    if st.session_state.role != "מנהל מערכת (Admin)":
        my_deliveries_count = len([d for d in st.session_state.deliveries if d.get("courier") == st.session_state.username and d.get("status") != "נמסר"])
        st.info(f"📦 יש לך כרגע **{my_deliveries_count}** משלוחים פעילים לביצוע להיום.")

    # הצגת השעה הנוכחית בישראל
    current_time_il_str = datetime.now(ISRAEL_TZ).strftime("%H:%M - %d/%m/%Y")
    st.caption(f"🕒 שעון ישראל נוכחי במערכת: **{current_time_il_str}**")

    # הוספת משלוח מהירה וישירה
    st.subheader("➕ הוספת משלוח חדש (מהיר לשטח)")
    
    with st.form("delivery_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            barcode_num = st.text_input("מספר מעקב / ברקוד:")
            cust_name = st.text_input("שם הלקוח:")
            company_name = st.text_input("שם החברה (החנות/העסק):", "SHEIN")
        with col2:
            raw_cust_phone = st.text_input("מספר טלפון של הלקוח (לדוגמה: 050...):")
            city_name = st.text_input("ישוב / עיר:", "כסרא-סמיע")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            street_name = st.text_input("שם רחוב:")
        with col_s2:
            house_num = st.text_input("מספר בית:")
        with col_s3:
            floor_num = st.text_input("קומה (אופציונלי):")
            
        cust_notes = st.text_input("הערות מיוחדות למשלוח (אופציונלי):")
        
        submit_del = st.form_submit_button("שמור משלוח במערכת")
        if submit_del:
            if cust_name and street_name and house_num:
                formatted_cust_phone = f"+972{raw_cust_phone[1:]}" if raw_cust_phone.startswith("0") else raw_cust_phone
                
                full_address = f"{street_name} {house_num}, {city_name}" + (f" (קומה {floor_num})" if floor_num else "")
                added_time = datetime.now(ISRAEL_TZ).strftime("%Y-%m-%d %H:%M")
                
                st.session_state.deliveries.append({
                    "ברקוד": barcode_num if barcode_num else "ללא ברקוד",
                    "שם לקוח": cust_name,
                    "שם חברה": company_name if company_name else "החברה",
                    "טלפון": formatted_cust_phone,
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
                st.success("המשלוח נוסף בהצלחה!")
            else:
                st.warning("נא למלא לפחות שם לקוח, שם רחוב ומספר בית.")

    # רשימת המשלוחים להיום ועדכון סטטוס
    st.subheader("📋 רשימת המשלוחים להיום וניהול מהיר")
    
    if st.session_state.role == "מנהל מערכת (Admin)":
        current_deliveries = st.session_state.deliveries
    else:
        current_deliveries = [d for d in st.session_state.deliveries if d.get("courier") == st.session_state.username]

    if len(current_deliveries) == 0:
        st.info("אין עדיין משלוחים לרשימה.")
    else:
        for index, item in enumerate(current_deliveries, start=1):
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    status_emoji = "✅ נמסר" if item.get("status") == "נמסר" else "⏳ ממתין"
                    st.markdown(f"**#{index} | {status_emoji} | ברקוד:** {item.get('ברקוד')} | **לקוח:** {item.get('שם לקוח')} | **חברה:** {item.get('שם חברה')}")
                    st.write(f"📍 **כתובת:** {item.get('כתובת מלאה')}")
                    st.caption(זמן_הוספה := f"נוסף בתאריך ושעה: {item.get('date', 'היום')}")
                    if item.get('הערות'):
                        st.caption(f"הערות: {item.get('הערות')}")
                with col2:
                    # חישוב ניווט שמתחשב בנקודת המוצא שהשליח הגדיר בצד ימין
                    dest_address = item.get('כתובת מלאה', '')
                    waze_url = f"https://www.waze.com/ul?from={urllib.parse.quote(start_point)}&q={urllib.parse.quote(dest_address)}&navigate=yes"
                    st.markdown(f"[🚗 נווט מ-{start_point} ב-Waze]({waze_url})", unsafe_allow_html=True)
                with col3:
                    if item.get("status") != "נמסר":
                        if st.button(f"סמן כנמסר #{index}", key=f"deliver_{index}"):
                            item["status"] = "נמסר"
                            st.success("המשלוח עודכן כנמסר!")
                            
                            cust_tel = item.get("טלפון", "").replace("+", "")
                            comp_name = item.get("שם חברה", "החברה")
                            customer_name = item.get("שם לקוח", "לקוח")
                            
                            if cust_tel:
                                customer_msg = f"שלום {customer_name}, אני השליח. יש לך משלוח מ{comp_name}, אני בדרך אליך אגיע בקרוב מאוד! 🚚"
                                encoded_customer_msg = urllib.parse.quote(customer_msg)
                                wa_customer_url = f"https://wa.me/{cust_tel}?text={encoded_customer_msg}"
                                
                                st.markdown(f"""
                                    <div style="background-color: #d4edda; padding: 10px; border-radius: 5px; text-align: center; margin-top: 5px;">
                                        <a href="{wa_customer_url}" target="_blank" style="color: #155724; font-weight: bold; font-size: 16px; text-decoration: none;">
                                            📲 לחץ כאן לשליחת הודעת וואטסאפ ללקוח
                                        </a>
                                    </div>
                                """, unsafe_allow_html=True)
                            
                            st.rerun()
                st.markdown("---")
