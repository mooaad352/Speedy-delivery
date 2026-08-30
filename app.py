import streamlit as st
import urllib.parse
import json
import os
from streamlit_qrcode_scanner import qrcode_scanner

# הגדרת כותרת האפליקציה (חובה שתהיה ראשונה)
st.set_page_config(page_title="מערכת ניהול משלוחים מתקדמת", page_icon="🚚", layout="centered")

# --- הגדרת משתמשים במערכת (Admin והשליחים) ---
USERS = {
    "Admin": {"password": "Sma.srablove2028", "role": "admin"},
    # אפשר להוסיף שליחים נוספים כאן בהמשך, למשל:
    # "driver1": {"password": "123", "role": "driver"}
}

# ניהול מצב התחברות בזיכרון של הסשן
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# ==========================================
# 1. מסך התחברות (אם המשתמש לא מחובר)
# ==========================================
if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
        .stApp { background-color: #1e1e2f; color: #ffffff; }
        h1, h2, h3, h4, h5, h6, p, label { color: #ffffff !important; }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("🚚 מערכת ניהול משלוחים - כניסה")
    st.write("נא להזין את פרטי ההתחברות שלך:")
    
    with st.form("login_form"):
        username = st.text_input("שם משתמש (Username)")
        password = st.text_input("סיסמה (Password)", type="password")
        submit = st.form_submit_button("התחבר")
        
        if submit:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = USERS[username]["role"]
                st.rerun()
            else:
                st.error("שם משתמש או סיסמה שגויים. נא לנסות שוב.")

# ==========================================
# 2. אזור מנהל (Admin Dashboard)
# ==========================================
elif st.session_state.role == "admin":
    st.markdown(
        """
        <style>
        .stApp { background-color: #1e1e2f; color: #ffffff; }
        h1, h2, h3, h4, h5, h6, p, label { color: #ffffff !important; }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.title(f"مرحباً, מנהל ({st.session_state.username})")
    if st.sidebar.button("התנתק (Logout)"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.title("📊 לוח בקרה למנהל (Admin Dashboard)")
    st.write("כאן תוכל לצפות בנתוני הפעילות של המערכת:")
    
    # טבלת מעקב ניהולית
    st.subheader("מעקב משתמשים ופעילות")
    st.table({
        "משתמש": ["Admin"],
        "תפקיד": ["מנהל מערכת (Admin)"],
        "סטטוס חיבור": ["מחובר כעת 🟢"]
    })
    
    st.info("💡 טיפ: דרך החשבון שלך אתה מנהל את המערכת ורואה את כל בסיס הנתונים.")
    
    # אפשרות לצפות בנתוני המשלוחים גם מהאדמין אם תרצה
    DATA_FILE = "deliveries_data.json"
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            admin_deliveries = json.load(f)
        st.subheader("📦 סך כל המשלוחים במערכת")
        st.write(f"קיימים כרגע **{len(admin_deliveries)}** משלוחים שמורים במערכת.")
        if admin_deliveries:
            st.json(admin_deliveries)

# ==========================================
# 3. אזור העבודה המלא (שליח / הפעלת האפליקציה)
# ==========================================
else:
    # --- הוספת עיצוב ורקע למסך ---
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #1e1e2f;
            color: #ffffff;
        }
        h1, h2, h3, h4, h5, h6, p, label {
            color: #ffffff !important;
        }
        div.stContainer {
            background-color: #2b2b40;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # כפתור התנתקות בסיידבר
    st.sidebar.title(f"שליח: {st.session_state.username}")
    if st.sidebar.button("התנתק (Logout)"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🚚 מערכת ניהול וסידור משלוחים")

    # קובץ שמירה מקומי לשמירת הנתונים שלא ימחקו ברענון
    DATA_FILE = "deliveries_data.json"

    def load_deliveries():
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_deliveries(deliveries):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(deliveries, f, ensure_ascii=False, indent=4)

    # ניהול רשימת המשלוחים בזיכרון של הסשן עם טעינה מהקובץ
    if "deliveries" not in st.session_state:
        st.session_state.deliveries = load_deliveries()

    # סיידבר - הגדרות עסק ונקודת מוצא כללית
    st.sidebar.header("הגדרות מערכת")
    start_location = st.sidebar.text_input("כתובת נקודת מוצא ראשית (עסק/מחסן):", "חיפה")

    st.sidebar.markdown("---")
    st.sidebar.info("טיפ: באייפון ניתן לשמור את האתר כקיצור דרך במסך הבית (PWA).")

    # --- חלק סריקת QR ---
    st.subheader("📷 סריקת מדבקת משלוח (QR)")
    scan_toggle = st.checkbox("פתח מצלמה לסריקה")

    scanned_data = None
    if scan_toggle:
        scanned_data = qrcode_scanner(key="qrcode_scanner")
        if scanned_data:
            st.success(f"זוהה קוד בהצלחה: {scanned_data}")

    # טופס הוספת משלוח חדש
    st.subheader("➕ הוספת משלוח חדש")

    with st.form("delivery_form", clear_on_submit=True):
        customer_name = st.text_input("שם הלקוח:")
        customer_phone = st.text_input("מספר טלפון של הלקוח (לדוגמה: 972501111111+):")
        
        default_address = f"נתוני QR: {scanned_data}" if scanned_data else ""
        delivery_address = st.text_input("כתובת למשלוח (או כתובת שנסרקה):", value=default_address)
        
        delivery_notes = st.text_input("הערות מיוחדות למשלוח (אופציונלי):", "")
        
        submitted = st.form_submit_button("הוסף לרשימת המשלוחים")
        
        if submitted:
            if customer_name and customer_phone and delivery_address:
                new_item = {
                    "name": customer_name,
                    "phone": customer_phone,
                    "address": delivery_address,
                    "notes": delivery_notes,
                    "completed": False
                }
                st.session_state.deliveries.append(new_item)
                save_deliveries(st.session_state.deliveries)
                st.success(f"המשלוח עבור {customer_name} נוסף בהצלחה!")
                st.rerun()
            else:
                st.warning("נא למלא את כל השדות החובה (שם, טלפון וכתובת).")

    # --- בחירת נקודת התחלה למסלול ---
    st.subheader("🧭 בחירת נקודת מוצא למסלול")

    available_start_points = [start_location] + [d['address'] for d in st.session_state.deliveries]
    selected_start_point = st.selectbox("בחר מאיפה להתחיל את המסלול הנוכחי:", available_start_points)

    # כפתור לסידור אוטומטי
    if st.button("🔄 רענן וסדר רשימה"):
        st.session_state.deliveries.sort(key=lambda x: x["completed"])
        save_deliveries(st.session_state.deliveries)
        st.rerun()

    # הצגת רשימת המשלוחים
    st.subheader("📋 רשימת המשלוחים להיום")

    if not st.session_state.deliveries:
        st.info("עדיין לא נוספו משלוחים לרשימה.")
    else:
        st.info(f"המסלול מותאם כרגע ליציאה מתוך: **{selected_start_point}** 📍")
        
        sorted_indices = sorted(range(len(st.session_state.deliveries)), key=lambda i: st.session_state.deliveries[i]["completed"])
        
        for idx, index in enumerate(sorted_indices):
            delivery = st.session_state.deliveries[index]
            
            with st.container():
                status_prefix = "✅ ~~" if delivery["completed"] else f"**עצירה {idx + 1}: "
                status_suffix = " (בוצע)**" if delivery["completed"] else "**"
                
                st.markdown(f"{status_prefix}{delivery['name']}{status_suffix}")
                st.write(f"📍 כתובת: {delivery['address']}")
                
                if delivery["notes"]:
                    st.warning(f"📝 הערה לשליח: {delivery['notes']}")
                
                # יצירת קישור וואטסאפ ישיר ללקוח
                msg = f"היי {delivery['name']}, המשלוח שלך בדרך אליך!"
                encoded_msg = urllib.parse.quote(msg)
                wa_link = f"https://wa.me/{delivery['phone']}?text={encoded_msg}"
                
                st.markdown(f"📞 טלפון לקוח: {delivery['phone']}  [📱 שלח הודעה]({wa_link})", unsafe_allow_html=True)
                
                # כפתורי ניווט
                encoded_address = urllib.parse.quote(delivery['address'])
                waze_link = f"https://www.waze.com/ul?q={encoded_address}&navigate=yes"
                google_maps_link = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"🚗 [נווט עם Waze]({waze_link})", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"🗺️ [נווט עם Google Maps]({google_maps_link})", unsafe_allow_html=True)
                
                # תיבת סימון לסימון המשלוח כבוצע
                is_completed = st.checkbox("סמן כבוצע ✅", value=delivery["completed"], key=f"check_{index}")
                if is_completed != delivery["completed"]:
                    st.session_state.deliveries[index]["completed"] = is_completed
                    save_deliveries(st.session_state.deliveries)
                    st.rerun()
                
                st.markdown("---")

        if st.button("🗑️ נקה הכל"):
            st.session_state.deliveries = []
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            st.rerun()
