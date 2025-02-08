from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'your_secret_key_here'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mainpage")
def mainpage():
    return render_template("main page.html") 

@app.route("/top_pics")
def top_pics():
    return render_template("top_pics.html")

@app.route("/actor")
def actor():
    return render_template("actors.html")

@app.route("/san")
def san():
    return render_template("san.html")

@app.route("/dhaku")
def dhaku():
    return render_template("dhaku.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form.get("uname")
        passw = request.form.get("passw")

       
        login_user = User.query.filter_by(username=uname).first()

        if login_user and check_password_hash(login_user.password, passw):
        
            session["user_id"] = login_user.id
            session["username"] = login_user.username
            flash("Login successful!", "success")
            return redirect(url_for("mainpage"))
        else:
            flash("Invalid username or password!", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form.get('uname')
        mail = request.form.get('mail')
        passw = request.form.get('passw')

       
        existing_user = User.query.filter((User.username == uname) | (User.email == mail)).first()
        if existing_user:
            flash("Username or email already exists!", "danger")
            return redirect(url_for("register"))

      
        hashed_password = generate_password_hash(passw, method="pbkdf2:sha256")
        new_user = User(username=uname, email=mail, password=hashed_password)

        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            flash(f"Error: {e}", "danger")
            db.session.rollback()
            return redirect(url_for("register"))

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")



@app.route("/logout")
def logout():
    
    session.clear()
    flash("Successfully logged out.", "success")
    return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
