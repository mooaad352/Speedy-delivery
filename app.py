import streamlit as st

# הגדרת עיצוב הדף
st.set_page_config(page_title="מערכת ניהול משלוחים", page_icon="🚚", layout="wide")

# ניהול מצב התחברות (Session State) בסיסי
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
    st.sidebar.title(f"مرحباً, מנהל")
    menu = st.sidebar.radio("תפריט ניהול", ["לוח בקרה ראשי", "הוספת שליח חדש", "ניהול משתמשים קיימים"])
    
    if st.sidebar.button("התנתק (Logout)"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()

    if menu == "לוח בקרה ראשי":
        st.title("📊 لוח בקרה למנהל (Admin Dashboard)")
        st.write("כאן תוכל לצפות בנתוני הפעילות של המערכת:")
        
        st.markdown("### מעקב משתמשים ופעילות")
        col1, col2, col3 = st.columns(3)
        col1.metric("סך הכל שליחים/משתמשים", len(st.session_state.couriers_db))
        col2.metric("סטטוס חיבור", "מחובר כעת 🟢")
        col3.metric("סוג חשבון", "מנהל ראשי")
        
        st.info("💡 טיפ: דרך החשבון שלך אתה מנהל את כל השליחים ויכול להוסיף חדשים בקלות מהתפריט בצד.")

    elif menu == "הוספת שליח חדש":
        st.title("➕ הוספת שליח או משתמש חדש")
        st.write("הזן את הפרטים של השליח כדי שיוכל להתחבר למערכת עם שם משתמש וסיסמה משלו:")
        
        with st.form("add_courier_form"):
            new_user = st.text_input("שם משתמש חדש (באנגלית או מספרים)")
            new_pass = st.text_input("סיסמה לשליח", type="password")
            new_role = st.selectbox("תפקיד במערכת", ["שליח", "מנהל מערכת (Admin)"])
            add_btn = st.form_submit_button("שמור שליח חדש")
            
            if add_btn:
                if new_user.strip() == "" or new_pass.strip() == "":
                    st.error("נא למלא את כל השדות.")
                elif new_user in st.session_state.couriers_db:
                    st.warning("שם המשתמש כבר קיים במערכת.")
                else:
                    st.session_state.couriers_db[new_user] = {
                        "password": new_pass,
                        "role": new_role
                    }
                    st.success(f"השליח '{new_user}' נוסף בהצלחה!")

    elif menu == "ניהול משתמשים קיימים":
        st.title("👥 רשימת כל המשתמשים והשליחים הרשומים")
        st.write("להלן רשימת כל האנשים שיש גישה למערכת והסיסמאות שלהם:")
        
        users_data = []
        for usr, info in st.session_state.couriers_db.items():
            users_data.append({
                "שם משתמש": usr,
                "סיסמה": info["password"],
                "תפקיד": info["role"]
            })
        
        st.table(users_data)

# --- אזור השליחים הרגילים ---
else:
    st.sidebar.title(f"مرحباً, {st.session_state.username}")
    if st.sidebar.button("התנתק (Logout)"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()
        
    st.title("📦 אזור שליחים - ניהול משלוחים")
    st.write(f"ברוך הבא, **{st.session_state.username}**! אתה מחובר כשליח פעיל במערכת.")
    st.info("כאן יוצגו בהמשך המשלוחים המוקצים אליך, כפתורי הסריקה (QR) וקישורי הניווט ל-Waze.")
