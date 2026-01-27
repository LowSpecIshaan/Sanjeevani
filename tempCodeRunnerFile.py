from flask import Flask, render_template, request, session, redirect, flash, jsonify, send_file, url_for, abort
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import timedelta
import base64
import datetime
import requests
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)
app.secret_key = "@0A7F221S"
app.permanent_session_lifetime = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ishaan_31@localhost/keralahealth'
db = SQLAlchemy(app)

client = InferenceClient(
    provider="featherless-ai",
    api_key=os.environ.get("HF_TOKEN")
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    aadhaar = db.Column(db.String(12), unique = True, nullable = False)
    email = db.Column(db.String(254), unique = True, nullable = False)
    password = db.Column(db.String(100))
    name = db.Column(db.String(30), nullable = False)
    profile_pic = db.Column(db.LargeBinary, nullable=True)
    city = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(40), nullable=True)

    def __init__(self, password, aadhaar, email, name, address, city):
        self.aadhaar = aadhaar
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.name = name
        self.address = address
        self.city = city

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class HealthHistory(db.Model):
    __tablename__ = 'health_history'
    id = db.Column(db.Integer, primary_key = True)
    aadhaar = db.Column(db.String(12), db.ForeignKey('user.aadhaar'), nullable = True)
    condition = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=True)
    date_diagnosed = db.Column(db.Date, nullable=True)
    last_updated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship("User", backref="health_history")

with app.app_context():
    db.create_all()

@app.route('/')
def red():
    return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def loginorsignup():
    if request.method == 'POST':
        if(request.form.get("form_type") == "login"):
            login_method = request.form.get('loginMethod')
            password = request.form.get('password')
            if(login_method == 'email'):
                email = request.form.get('email').strip().lower()
                user = User.query.filter_by(email = email).first()

                if user and user.check_password(password):
                    session.permanent = True
                    session['email'] = user.email
                    session['aadhaar'] = user.aadhaar
                    session['name'] = user.name
                    return redirect('/dashboard')
                else:
                    flash("Invalid Email or Password.", "error")
                    return render_template('login.html')

            if(login_method == 'aadhaar'):
                aadhaar = request.form.get('aadhaar')
                user = User.query.filter_by(aadhaar = aadhaar).first()

                if user and user.check_password(password):
                    session.permanent = True
                    session['email'] = user.email
                    session['aadhaar'] = user.aadhaar
                    session['name'] = user.name
                    return redirect('/dashboard')
                else:
                    flash("Invalid Aadhaar or Password.", "error")
                    return render_template('login.html')

        if(request.form.get("form_type") == "signup"):
            name = request.form.get('fullname')
            aadhaar = request.form.get('aadhaar')
            email = request.form.get('email').strip().lower()
            password = request.form.get('password')
            address = request.form.get('address')
            city = request.form.get('city')

            existing_email = User.query.filter_by(email=email).first()
            existing_aadhaar = User.query.filter_by(aadhaar=aadhaar).first()

            if existing_email:
                flash("Email already registered. Please login instead.", "error")
                return redirect('/login')
            elif existing_aadhaar:
                flash("Aadhaar already registered. Please login instead.", "error")
                return redirect("/login")
            else:
                new_user = User(password = password, aadhaar = aadhaar, email = email, name = name, address=address, city=city )
                db.session.add(new_user)
                db.session.commit()
                flash("Signup successful! Please login.", "success")
                return redirect('/login')
    return render_template("login.html")

@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    if(lang == 'hn'):
        flash("Language changed to Hindi", "info")
    elif(lang == 'ml'):
        flash("Language changed to Malayalam", "info")
    else:
        flash("Language changed to English", "info")

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if ('email' not in session) or ('aadhaar' not in session):
        flash("Please login", 'error')
        return redirect('/login')

    email = session.get("email")
    aadhaar = session.get("aadhaar")
    name = session.get('name')
    user = User.query.filter_by(aadhaar = session.get("aadhaar")).first()
    profile_pic = None
    if user.profile_pic:
        profile_pic = base64.b64encode(user.profile_pic).decode('utf-8')
    return render_template('dashboard.html', name = name, aadhaar = aadhaar[8:], profile_pic = profile_pic)

@app.route("/api/medical-history", methods=["GET"])
def get_medical_history():
    records = HealthHistory.query.filter_by(aadhaar = session.get("aadhaar"))
    return jsonify([
        {
            "id": r.id,
            "date_diagnosed": r.date_diagnosed.isoformat() if r.date_diagnosed else None,
            "condition": r.condition,
            "details": r.details
        }
        for r in records
    ])

@app.route("/api/medical-history", methods=["POST"])
def add_history():
    data = request.get_json()
    record = HealthHistory(
        aadhaar=session.get("aadhaar"),  # logged-in user’s aadhaar
        condition=data["condition"],
        details=data.get("details"),
        date_diagnosed=data.get("date_diagnosed")
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({
        "id": record.id,
        "date_diagnosed": str(record.date_diagnosed),
        "condition": record.condition,
        "details": record.details
    })

@app.route("/api/medical-history/<int:id>", methods=["PUT"])
def update_history(id):
    record = HealthHistory.query.get_or_404(id)
    data = request.get_json()

    record.condition = data.get("condition", record.condition)
    record.details = data.get("details", record.details)
    record.date_diagnosed = data.get("date_diagnosed", record.date_diagnosed)

    db.session.commit()
    return jsonify({
        "id": record.id,
        "date_diagnosed": str(record.date_diagnosed),
        "condition": record.condition,
        "details": record.details
    })

@app.route("/api/medical-history/<int:id>", methods=["DELETE"])
def delete_history(id):
    record = HealthHistory.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"})

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    try:
        completion = client.chat.completions.create(
            model="m42-health/Llama3-Med42-70B",
            messages=[{"role": "user", "content": user_message}],
            timeout=30
        )
        reply = completion.choices[0].message["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        app.logger.error(f"Med42 API error: {e}")
        return jsonify({"reply": "Sorry, I’m not able to reply right now."}), 500

# @app.route("/api/chat", methods=["POST"])
# def chat():
#     user_msg = request.json.get("message", "")
    
#     # For now: dummy reply
#     reply = "I am your AI healthcare assistant. You asked: " + user_msg
    
#     # Later: call HuggingFace/OpenAI API here
#     return jsonify({"reply": reply})


@app.route('/econtent')
def econtent():
    if ('email' not in session) or ('aadhaar' not in session):
        flash("Please login", 'error')
        return redirect('/login')
    return render_template('econtent.html')

@app.route('/profile', methods=["GET", "POST"])
def profile():
    if ('email' not in session) or ('aadhaar' not in session):
        flash("Please login", 'error')
        return redirect('/login')

    user = User.query.filter_by(email=session['email']).first()
    email = session.get("email")
    aadhaar = session.get("aadhaar")
    name = session.get('name')
    if request.method == 'POST':
        file = request.files.get('profile_pic')
        if file:
            user.profile_pic = file.read()

        city = request.form.get('city')
        if city:
            user.city = city

        address = request.form.get('address')
        if address:
            user.address = address

        db.session.commit()

    profile_pic = None
    if user.profile_pic:
        profile_pic = base64.b64encode(user.profile_pic).decode('utf-8')
    return render_template('/profile.html', name = name, email = email, aadhaar = aadhaar[8:], profile_pic = profile_pic, city = user.city, address = user.address, id = user.id)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect('/') 

@app.route('/generate_qr/<int:user_id>')
def generate_qr(user_id):
    # Dynamically get the host (e.g., http://localhost:5000/)
    base_url = request.host_url  # includes http:// and port
    link = f'{base_url}admin/dashboard/{user_id}'

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(link)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Send image as response
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    
    return send_file(buf, mimetype='image/png')

@app.route("/admin/dashboard/<int:id>")
def admin(id):
    worker = User.query.filter_by(id=id).first()
    if not worker:
        return "Worker not found", 404
    
    worker_history = HealthHistory.query.filter_by(aadhaar=worker.aadhaar).all()
    
    return render_template(
        'admindashboard.html',
        worker=worker,
        worker_history=worker_history
    )


if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True)