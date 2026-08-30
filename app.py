import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner

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
    st.session_state.deliveries = [
        {"id": "DEL-101", "customer": "אחמד סלאמה", "address": "כפר סמיע", "phone": "0500000000", "status": "ממתין", "courier": "mohammad"}
    ]

# --- מסך התחברות ---
if not st.session_state.logged_in:
    st.title("🚚 מערכת ניהול משלוחים חכמה")
    st.subheader("כניסת משתמשים ומנהלים")
    
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

# --- אזור מנהל המערכת (Admin) ---
elif st.session_state.role == "מנהל מערכת (Admin)":
    st.sidebar.title("مرحباً, מנהל")
    menu = st.sidebar.radio("תפריט ניהול", ["לוח בקרה ראשי", "הוספת שליח חדש", "ניהול משתמשים קיימים", "צפייה בכל המשלוחים"])
    
    if st.sidebar.button("התנתק (Logout)"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    if menu == "לוח בקרה ראשי":
        st.title("📊 לוח בקרה למנהל (Admin Dashboard)")
        col1, col2, col3 = st.columns(3)
        col1.metric("סך הכל שליחים", len(st.session_state.couriers_db))
        col2.metric("סך הכל משלוחים", len(st.session_state.deliveries))
        col3.metric("סטטוס חיבור", "מחובר כעת 🟢")

    elif menu == "הוספת שליח חדש":
        st.title("➕ הוספת שליח או משתמש חדש")
        with st.form("add_courier_form"):
            new_user = st.text_input("שם משתמש חדש")
            new_pass = st.text_input("סיסמה לשליח", type="password")
            new_role = st.selectbox("תפקיד במערכת", ["שליח", "מנהל מערכת (Admin)"])
            add_btn = st.form_submit_button("שמור שליח חדש")
            
            if add_btn:
                if new_user and new_pass:
                    st.session_state.couriers_db[new_user] = {"password": new_pass, "role": new_role}
                    st.success(f"השליח '{new_user}' נוסף בהצלחה!")

    elif menu == "ניהול משתמשים קיימים":
        st.title("👥 רשימת כל המשתמשים והשליחים הרשומים")
        users_data = [{"שם משתמש": usr, "סיסמה": info["password"], "תפקיד": info["role"]} for usr, info in st.session_state.couriers_db.items()]
        st.table(users_data)

    elif menu == "צפייה בכל המשלוחים":
        st.title("📦 כל המשלוחים במערכת")
        st.table(st.session_state.deliveries)

# --- אזור השליחים ---
else:
    st.sidebar.title(f"مرحباً, {st.session_state.username}")
    courier_menu = st.sidebar.radio("תפריט שליח", ["המשלוחים שלי", "סריקת ברקוד / QR", "הוספת משלוחים"])
    
    if st.sidebar.button("התנתק (Logout)"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    if courier_menu == "המשלוחים שלי":
        st.title(f"📦 המשלוחים של השליח: {st.session_state.username}")
        my_deliveries = [d for d in st.session_state.deliveries if d["courier"] == st.session_state.username]
        if my_deliveries:
            st.table(my_deliveries)
        else:
            st.info("אין לך משלוחים מוקצים כרגע.")

    elif courier_menu == "סריקת ברקוד / QR":
        st.title("📷 סריקת ברקוד / קוד QR משלוח")
        st.write("השתמש במצלמת המכשיר כדי לסרוק ברקוד של חבילה:")
        
        scanned_code = qrcode_scanner(key='qrcode_scanner')
        
        if scanned_code:
            st.success(f"זוהה קוד בהצלחה: {scanned_code}")

    elif courier_menu == "הוספת משלוחים":
        st.title("➕ הוספת משלוח חדש לשטח")
        with st.form("add_del_form"):
            del_id = st.text_input("מספר חבילה / ברקוד")
            cust_name = st.text_input("שם הלקוח")
            cust_addr = st.text_input("כתובת למשלוח")
            cust_phone = st.text_input("מספר טלפון")
            submit_delivery = st.form_submit_button("שמור משלוח")
            
            if submit_delivery:
                if del_id and cust_name:
                    st.session_state.deliveries.append({
                        "id": del_id,
                        "customer": cust_name,
                        "address": cust_addr,
                        "phone": cust_phone,
                        "status": "ממתין",
                        "courier": st.session_state.username
                    })
                    st.success("המשלוח נוסף בהצלחה למערכת שלך!")
