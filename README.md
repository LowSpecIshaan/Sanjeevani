📌 Sanjeevani — AI-Powered Healthcare Assistant for Migrant Workers of Kerala (built for SIH'25)

Sanjeevani is a Flask-based web application designed to assist migrant workers in Kerala with healthcare support, medical history management, and AI-driven preliminary diagnoses.
The platform enables users to store health records, access e-content, update personal profiles, and receive quick AI-based medical guidance.

🚀 Features
👤 User Authentication

Login via Email or Aadhaar Number

Secure password hashing with bcrypt

Persistent user sessions

🧬 AI Healthcare Assistant

Integrated with HuggingFace / Ollama (Mistral) for short medical guidance

Generates a 1–2 line preliminary diagnosis based on user symptoms

🩺 Medical History Management

Add, update, and retrieve medical records

Auto-timestamped entries

Displays diagnosis history on dashboard

🏥 Admin Dashboard

Admin can scan QR code of a worker

View their full medical history

Useful for quick healthcare screening

🖼️ Profile Management

Upload profile picture

Update address and city

Aadhaar-masked display (XXXXXX1234)

🎓 E-Content

Health awareness materials based on government schemes

Multi-language support (English, Hindi, Malayalam)

📱 QR Code System

Worker-specific QR code generation

Opens worker’s admin dashboard via scanned link

Useful for health camps or field hospitals

🛠️ Tech Stack

Backend

Flask (Python)

SQLAlchemy ORM

PyMySQL (MySQL driver)

python-dotenv

bcrypt

Frontend

HTML, CSS, JavaScript

Jinja2 Templates

AI Services

HuggingFace Inference API

Or local Ollama/Mistral model via HTTP endpoint

Database

MySQL

🔐 Environment Variables (.env)

Create a .env file in the project root:

SECRET_KEY=your_secret_key
DB_URL=mysql+pymysql://root:yourpassword@localhost/keralahealth
HF_API_KEY=your_huggingface_api_key


Never commit this file — it’s already added to .gitignore.

▶️ Running the Project Locally
1. Create a virtual environment
python -m venv env
env\Scripts\activate    # Windows

2. Install dependencies
pip install -r requirements.txt

3. Set up .env file

Add your keys/passwords there.

4. Run the application
python app.py

