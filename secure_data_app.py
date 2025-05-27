import streamlit as st
import hashlib
import json
import time
from cryptography.fernet import Fernet
import base64

# Initialize session state variables if they don't exist
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'last_attempt_time' not in st.session_state:
    st.session_state.last_attempt_time = 0

# Function to hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to generate a key from passkey (for encryption)
def generate_key_from_passkey(passkey):
    # Use the passkey to create a consistent key
    hashed = hashlib.sha256(passkey.encode()).digest()
    # Ensure it's valid for Fernet (32 url-safe base64-encoded bytes)
    return base64.urlsafe_b64encode(hashed[:32])

# Function to encrypt data
def encrypt_data(text, passkey):
    key = generate_key_from_passkey(passkey)
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text, passkey, data_id):
    try:
        # Check if the passkey matches
        hashed_passkey = hash_passkey(passkey)
        if data_id in st.session_state.stored_data and st.session_state.stored_data[data_id]["passkey"] == hashed_passkey:
            # If passkey matches, decrypt the data
            key = generate_key_from_passkey(passkey)
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_text.encode()).decode()
            st.session_state.failed_attempts = 0
            return decrypted
        else:
            # Increment failed attempts
            st.session_state.failed_attempts += 1
            st.session_state.last_attempt_time = time.time()
            return None
    except Exception as e:
        # If decryption fails, increment failed attempts
        st.session_state.failed_attempts += 1
        st.session_state.last_attempt_time = time.time()
        return None

# Function to generate a unique ID for data
def generate_data_id():
    import uuid
    return str(uuid.uuid4())

# Function to reset failed attempts
def reset_failed_attempts():
    st.session_state.failed_attempts = 0

# Function to change page
def change_page(page):
    st.session_state.current_page = page

# Streamlit UI
st.title("🔒 Secure Data Encryption System")

# Navigation
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu, index=menu.index(st.session_state.current_page))

# Update current page based on selection
st.session_state.current_page = choice

# Check if too many failed attempts
if st.session_state.failed_attempts >= 3:
    # Force redirect to login page
    st.session_state.current_page = "Login"
    st.warning("🔒 Too many failed attempts! Reauthorization required.")

# Display current page
if st.session_state.current_page == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Store New Data", use_container_width=True):
            change_page("Store Data")
    with col2:
        if st.button("Retrieve Data", use_container_width=True):
            change_page("Retrieve Data")
    
    # Display stored data count
    st.info(f"Currently storing {len(st.session_state.stored_data)} encrypted data entries.")

elif st.session_state.current_page == "Store Data":
    st.subheader("📂 Store Data Securely")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")
    confirm_passkey = st.text_input("Confirm Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey and confirm_passkey:
            if passkey != confirm_passkey:
                st.error("⚠️ Passkeys do not match!")
            else:
                # Generate a unique ID for this data
                data_id = generate_data_id()
                
                # Hash the passkey
                hashed_passkey = hash_passkey(passkey)
                
                # Encrypt the data
                encrypted_text = encrypt_data(user_data, passkey)
                
                # Store in the required format
                st.session_state.stored_data[data_id] = {
                    "encrypted_text": encrypted_text,
                    "passkey": hashed_passkey
                }
                
                st.success("✅ Data stored securely!")
                
                # Display the data ID for retrieval
                st.code(data_id, language="text")
                st.info("⚠️ Save this Data ID! You'll need it to retrieve your data.")
        else:
            st.error("⚠️ All fields are required!")

elif st.session_state.current_page == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    
    # Show attempts remaining
    attempts_remaining = 3 - st.session_state.failed_attempts
    st.info(f"Attempts remaining: {attempts_remaining}")
    
    data_id = st.text_input("Enter Data ID:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Decrypt"):
        if data_id and passkey:
            if data_id in st.session_state.stored_data:
                encrypted_text = st.session_state.stored_data[data_id]["encrypted_text"]
                decrypted_text = decrypt_data(encrypted_text, passkey, data_id)

                if decrypted_text:
                    st.success("✅ Decryption successful!")
                    st.markdown("### Your Decrypted Data:")
                    st.code(decrypted_text, language="text")
                else:
                    st.error(f"❌ Incorrect passkey! Attempts remaining: {3 - st.session_state.failed_attempts}")
            else:
                st.error("❌ Data ID not found!")
                
            # Check if too many failed attempts after this attempt
            if st.session_state.failed_attempts >= 3:
                st.warning("🔒 Too many failed attempts! Redirecting to Login Page.")
                st.session_state.current_page = "Login"
                st.rerun()  # Updated from experimental_rerun()
        else:
            st.error("⚠️ Both fields are required!")

elif st.session_state.current_page == "Login":
    st.subheader("🔑 Reauthorization Required")
    
    # Add a simple timeout mechanism
    if time.time() - st.session_state.last_attempt_time < 10 and st.session_state.failed_attempts >= 3:
        remaining_time = int(10 - (time.time() - st.session_state.last_attempt_time))
        st.warning(f"🕒 Please wait {remaining_time} seconds before trying again.")
    else:
        login_pass = st.text_input("Enter Master Password:", type="password")

        if st.button("Login"):
            if login_pass == "admin123":  # Hardcoded for demo, replace with proper auth
                reset_failed_attempts()
                st.success("✅ Reauthorized successfully!")
                st.session_state.current_page = "Home"
                st.rerun()  # Updated from experimental_rerun()
            else:
                st.error("❌ Incorrect password!")

# Add a footer
st.markdown("---")
st.markdown("🔐 Secure Data Encryption System | Educational Project")