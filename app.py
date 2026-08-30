import streamlit as st

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
        "Admin": {"password": "Sma.srablove2028", "role": "מנהל מערכת (Admin)"},
        "mohammad": {"password": "123", "role": "שליח"}
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
    st.sidebar.title(f"مرحباً, מנהל ראשי")
    admin_menu = st.sidebar.radio("תפריט ניהול", ["מערכת משלוחים ראשית", "הוספת שליח חדש", "ניהול משתמשים קיימים"])
    
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
            new_role = st.selectbox("תפקיד במערכת", ["שליח", "מנהל מערכת (Admin)"])
            add_btn = st.form_submit_button("שמור שליח חדש")
            
            if add_btn:
                if new_user and new_pass:
                    st.session_state.couriers_db[new_user] = {"password": new_pass, "role": new_role}
                    st.success(f"השליח '{new_user}' נוסף בהצלחה!")

    elif admin_menu == "ניהול משתמשים קיימים":
        st.title("👥 רשימת כל המשתמשים והשליחים הרשומים")
        users_data = [{"שם משתמש": usr, "סיסמה": info["password"], "תפקיד": info["role"]} for usr, info in st.session_state.couriers_db.items()]
        st.table(users_data)
        st.stop() # עוצר כאן אם המנהל בחר רק לנהל משתמשים, אחרת ממשיך למערכת המשלוחים

# --- מסך המערכת המרכזי (מופיע לשליחים ולמנהל) ---
if st.session_state.logged_in:
    if st.session_state.role != "מנהל מערכת (Admin)":
        # תפריט צד לשליחים עם אפשרות התנתקות
        st.sidebar.title(f"مرحباً, {st.session_state.username}")
        if st.sidebar.button("התנתק (Logout)"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("הגדרות מערכת")
    start_point = st.sidebar.text_input("כתובת נקודת מוצא (עסק/מחסן)", "חיפה")
    st.sidebar.info("💡 טיפ: באייפון ניתן לשמור את האתר (PWA) כקיצור דרך במסך הבית.")

    # כותרת ראשית של האפליקציה כמו בתמונה
    st.title("🚚 מערכת ניהול וסידור משלוחים")

    # סעיף סריקת QR
    st.subheader("📷 סריקת מדבקת משלוח (QR)")
    scan_checkbox = st.checkbox("פתח מצלמה לסריקה")
    if scan_checkbox:
        st.info("המצלמה תופעל כאן לסריקת ברקוד/QR...")

    # סעיף הוספת משלוח חדש
    st.subheader("➕ הוספת משלוח חדש")
    with st.form("delivery_form", clear_on_submit=True):
        cust_name = st.text_input("שם הלקוח:")
        cust_phone = st.text_input("מספר טלפון של הלקוח (לדוגמה: +972501111111):")
        cust_address = st.text_input("כתובת למשלוח (או כתובת שנסרקה):")
        cust_notes = st.text_input("הערות מיוחדות למשלוח (אופציונלי):")
        
        submit_del = st.form_submit_button("שמור משלוח")
        if submit_del:
            if cust_name and cust_address:
                st.session_state.deliveries.append({
                    "שם לקוח": cust_name,
                    "טלפון": cust_phone,
                    "כתובת": cust_address,
                    "הערות": cust_notes,
                    "שליח": st.session_state.username
                })
                st.success("המשלוח נוסף בהצלחה למערכת!")
            else:
                st.warning("נא למלא לפחות שם לקוח וכתובת.")

    # בחירת נקודת מוצא למסלול
    st.subheader("🧭 בחירת נקודת מוצא למסלול")
    st.write("בחירה מאיפה להתחיל את המסלול המכוני:")
    selected_origin = st.selectbox("", [start_point, "תל אביב", "ירושלים", "באר שבע"], label_visibility="collapsed")
    
    # כפתור רענון קטן
    if st.button("🔄"):
        st.rerun()

    # רשימת המשלוחים להיום
    st.subheader("📋 רשימת המשלוחים להיום")
    if len(st.session_state.deliveries) == 0:
        st.info("עדיין לא נוספו משלוחים לרשימה.")
    else:
        st.table(st.session_state.deliveries)
