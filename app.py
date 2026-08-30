import streamlit as st
import urllib.parse
from datetime import datetime

# הגדרת עיצוב הדף
st.set_page_config(page_title="מערכת ניהול משלוחים", page_icon="🚚", layout="wide")

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
        "mohammad": {"password": "123", "role": "שליח", "phone": "+972501111111"}
    }

# מאגר משלוחים במערכת
if "deliveries" not in st.session_state:
    st.session_state.deliveries = []

# --- מסך התחברות ---
if not st.session_state.logged_in:
    st.title("🚚 מערכת ניהול משלוחים חכמה")
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
            new_phone = st.text_input("מספר טלפון של השליח (לדוגמה: +97250...):")
            new_role = st.selectbox("תפקיד במערכת", ["שליח", "מנהל מערכת (Admin)"])
            add_btn = st.form_submit_button("שמור שליח חדש")
            
            if add_btn:
                if new_user and new_pass:
                    st.session_state.couriers_db[new_user] = {
                        "password": new_pass, 
                        "role": new_role,
                        "phone": new_phone
                    }
                    st.success(f"השליח '{new_user}' נוסף בהצלחה!")

    elif admin_menu == "ניהול ועריכת משתמשים (סיסמאות וטלפונים)":
        st.title("👥 ניהול, החלפת סיסמאות ועדכון טלפונים לשליחים")
        st.write("כאן תוכל לעדכן את הסיסמה או מספר הטלפון של כל משתמש במערכת:")
        
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
        st.write("כאן תוכל לראות כמה משלוחים שבוצעו בפועל (בסטטוס 'נמסר') לכל שליח לצורך חישוב תשלום:")
        
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
    if st.session_state.role != "מנהל מערכת (Admin)":
        st.sidebar.title(f"مرحباً, {st.session_state.username}")
        if st.sidebar.button("התנתק (Logout)"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("הגדרות מערכת")
    start_point = st.sidebar.text_input("כתובת נקודת מוצא (הקלדה חופשית)", "חיפה")

    st.title("🚚 מערכת ניהול וסידור משלוחים")

    if st.session_state.role != "מנהל מערכת (Admin)":
        my_deliveries_count = len([d for d in st.session_state.deliveries if d.get("courier") == st.session_state.username and d.get("status") != "נמסר"])
        st.info(f"📦 יש לך כרגע **{my_deliveries_count}** משלוחים פעילים לביצוע להיום.")

    # הוספת משלוח חדש עם תמיכה מהירה בסורקים חיצוניים / מקלדת חכמה
    st.subheader("➕ הוספת משלוח חדש (תומך סריקה מהירה)")
    st.info("💡 טיפ לחיסכון בזמן: פשוט לחץ על שדה הטקסט והשתמש בסורק הברקוד או במקלדת החכמה של הטלפון כדי לקלוט נתונים באופן מיידי.")
    
    with st.form("delivery_form", clear_on_submit=True):
        cust_name = st.text_input("שם הלקוח:")
        company_name = st.text_input("שם החברה (החנות/העסק שממנו המשלוח):")
        cust_phone = st.text_input("מספר טלפון של הלקוח (לשליחת הודעה):")
        cust_address = st.text_input("כתובת למשלוח (הקלדה חופשית):")
        cust_notes = st.text_input("הערות מיוחדות למשלוח (אופציונלי):")
        
        submit_del = st.form_submit_button("שמור משלוח")
        if submit_del:
            if cust_name and cust_address:
                st.session_state.deliveries.append({
                    "שם לקוח": cust_name,
                    "שם חברה": company_name if company_name else "החברה",
                    "טלפון": cust_phone,
                    "כתובת": cust_address,
                    "הערות": cust_notes,
                    "status": "ממתין",
                    "courier": st.session_state.username if st.session_state.role != "מנהל מערכת (Admin)" else "mohammad",
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                st.success("המשלוח נוסף בהצלחה למערכת!")
            else:
                st.warning("נא למלא לפחות שם לקוח וכתובת.")

    # רשימת המשלוחים להיום ועדכון סטטוס
    st.subheader("📋 רשימת המשלוחים להיום ועדכון סטטוס")
    
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
                    st.markdown(f"**#{index} | {status_emoji} | לקוח:** {item.get('שם לקוח')} | **חברה:** {item.get('שם חברה')} | **כתובת:** {item.get('כתובת')}")
                    if item.get('הערות'):
                        st.caption(f"הערות: {item.get('הערות')}")
                with col2:
                    encoded_address = urllib.parse.quote(item.get('כתובת', ''))
                    waze_url = f"https://www.waze.com/ul?q={encoded_address}&navigate=yes"
                    st.markdown(f"[🚗 נווט ב-Waze]({waze_url})", unsafe_allow_html=True)
                with col3:
                    if item.get("status") != "נמסר":
                        if st.button(f"סמן כנמסר #{index}", key=f"deliver_{index}"):
                            item["status"] = "נמסר"
                            st.success("המשלוח עודכן כנמסר!")
                            
                            # שליחת הודעה מותאמת אישית ללקוח עם שם החברה
                            cust_tel = item.get("טלפון", "")
                            comp_name = item.get("שם חברה", "החברה")
                            if cust_tel:
                                customer_msg = f"שלום לך אני השליח יש לך משלוח מ{comp_name} אני בדרך אליך אגיע בקרוב"
                                encoded_customer_msg = urllib.parse.quote(customer_msg)
                                wa_customer_url = f"https://wa.me/{cust_tel}?text={encoded_customer_msg}"
                                st.markdown(f"📲 **[לחץ כאן לשליחת הודעת וואטסאפ ללקוח]({wa_customer_url})**", unsafe_allow_html=True)
                            
                            st.rerun()
                st.markdown("---")
