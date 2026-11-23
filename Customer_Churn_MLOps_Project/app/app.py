import streamlit as st
import requests
import sqlite3
import hashlib
import secrets
import hmac
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "users.db"
API_URL = st.sidebar.text_input("Prediction API URL", os.getenv("API_URL", "http://localhost:8000"))

st.set_page_config(page_title="Customer Churn Prediction", page_icon="📊", layout="wide")

def db():
    return sqlite3.connect(DB_PATH)

def init_db():
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )""")

def make_hash(password, salt=None):
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 310000)
    return salt.hex(), digest.hex()

def register(username, password):
    salt, digest = make_hash(password)
    try:
        with db() as conn:
            conn.execute("INSERT INTO users(username,salt,password_hash) VALUES(?,?,?)",
                         (username, salt, digest))
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate(username, password):
    with db() as conn:
        row = conn.execute("SELECT salt,password_hash FROM users WHERE username=?",
                           (username,)).fetchone()
    if not row:
        return False
    _, digest = make_hash(password, bytes.fromhex(row[0]))
    return hmac.compare_digest(digest, row[1])

init_db()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("📊 Customer Churn Prediction System")
    st.write("Login or register to access the prediction dashboard.")
    login_tab, register_tab = st.tabs(["Login", "Register"])
    with login_tab:
        with st.form("login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)
        if submitted:
            if authenticate(username.strip(), password):
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.rerun()
            else:
                st.error("Invalid username or password.")
    with register_tab:
        with st.form("register"):
            new_user = st.text_input("Choose username")
            new_pass = st.text_input("Choose password (at least 8 characters)", type="password")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account", use_container_width=True)
        if submitted:
            if not new_user.strip() or not new_pass:
                st.warning("Enter a username and password.")
            elif len(new_pass) < 8:
                st.warning("Password must be at least 8 characters.")
            elif new_pass != confirm:
                st.error("Passwords do not match.")
            elif register(new_user.strip(), new_pass):
                st.success("Account created. Please log in.")
            else:
                st.error("That username already exists.")
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.title("📊 Customer Churn Prediction Dashboard")
    st.write("Enter customer information and submit it to the FastAPI prediction service.")
    st.subheader("Customer Information")
    c1, c2, c3 = st.columns(3)
    with c1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.number_input("Tenure (months)", 0, 100, 12)
        phone = st.selectbox("Phone Service", ["Yes", "No"])
        multiple = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
    with c2:
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
    with c3:
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)"
        ])
        monthly = st.number_input("Monthly Charges", min_value=0.0, value=70.0, step=1.0)
        total = st.number_input("Total Charges", min_value=0.0, value=500.0, step=10.0)

    if st.button("🔮 Predict Customer Churn", use_container_width=True):
        customer = {
            "gender": gender, "SeniorCitizen": senior, "Partner": partner,
            "Dependents": dependents, "tenure": tenure, "PhoneService": phone,
            "MultipleLines": multiple, "InternetService": internet,
            "OnlineSecurity": security, "OnlineBackup": backup,
            "DeviceProtection": protection, "TechSupport": support,
            "StreamingTV": tv, "StreamingMovies": movies, "Contract": contract,
            "PaperlessBilling": paperless, "PaymentMethod": payment,
            "MonthlyCharges": monthly, "TotalCharges": total
        }
        try:
            response = requests.post(f"{API_URL.rstrip('/')}/predict", json=customer, timeout=30)
            response.raise_for_status()
            result = response.json()
            st.subheader("Prediction Result")
            st.metric("Churn probability", f"{result['churn_probability'] * 100:.2f}%")
            if result["prediction"] == 1:
                st.error("⚠️ Customer is likely to CHURN.")
            else:
                st.success("✅ Customer is likely to STAY.")
            st.progress(float(result["churn_probability"]))
        except requests.RequestException as exc:
            st.error(f"Could not reach the prediction API: {exc}")
    st.divider()
    st.caption("Streamlit UI | FastAPI | Scikit-learn | MLflow | DVC | Evidently AI")
