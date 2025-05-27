# 🔐 Secure Data Encryption System

This is a **Streamlit-based web app** that allows users to securely **encrypt and store sensitive data** using a unique **passkey**, and later retrieve it with the same passkey. Built as an educational project to demonstrate secure data handling with hashing and encryption.

---

## 🧠 Features

- Encrypt and store any text securely
- Retrieve encrypted data using a unique ID and passkey
- Login mechanism after multiple failed attempts
- AES-level security using `cryptography.fernet`
- Smooth navigation between pages via sidebar
- Reauthorization lock after 3 wrong passkey attempts

---

## 📦 Technologies Used

- Python
- [Streamlit](https://streamlit.io/)
- Cryptography (Fernet)
- Hashlib
- UUID
- Base64

---

## 🚀 How to Run

### 🔧 Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/secure-data-encryption.git
cd secure-data-encryption
🧪 Step 2: Create a Virtual Environment (optional but recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
📥 Step 3: Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt is missing, install manually:

bash
Copy
Edit
pip install streamlit cryptography
▶️ Step 4: Run the App
bash
Copy
Edit
streamlit run secure_data_app.py
📁 File Structure
bash
Copy
Edit
📂 secure-data-encryption
├── secure_data_app.py      # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
🔐 How It Works
Store Data:

Enter the text you want to secure

Provide a passkey and confirm it

A unique ID is generated — keep it safe

Retrieve Data:

Enter the saved unique ID

Enter the same passkey used while storing

Get your original data back securely

Security Lock:

After 3 wrong attempts, the system locks

You must reauthorize via the "Login" page with the master password (admin123)

📸 Screenshots
Add screenshots here after deploying or running the app locally.

🙌 Acknowledgements
This project is inspired by encryption principles and educational demos using Streamlit and Python.

📜 License
This project is licensed for educational and demo purposes.

yaml
Copy
Edit

---

Let me know if you want me to:
- Add the `requirements.txt` file
- Help deploy this to **Streamlit Cloud**
- Add your GitHub username in the clone URL

Ready? 😊







