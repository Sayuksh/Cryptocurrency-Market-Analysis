from flask import Flask,jsonify,render_template,request,session,redirect,url_for,flash
from datetime import datetime,timedelta
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app=Flask(__name__)
COINGECKO_API_URL = 'https://api.coingecko.com/api/v3/coins'
app.permanent_session_lifetime = timedelta(minutes=5)
app.secret_key = "hello"

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)


class users(db.Model):
    email=db.Column("email",db.String(20),primary_key=True)
    password=db.Column("password",db.String(16))
    name =db.Column("name",db.String(20))
    username=db.Column("username",db.String(20),unique=True)
    def __init__(self,name,email,password,username):
        self.name=name
        self.email=email
        self.password=password
        self.username=username


@app.route('/')

def welcome():
    if "username" in session:
        return render_template("head.html")
    else:
        return redirect(url_for('login'))

def fetch_data(coin):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']['usd']

# def predictive_model():
    

@app.route('/bitcoin')
def bitcoin_data():
    if "username" in session:
        now = datetime.now()

        timestamp = datetime.timestamp(now)
        response = requests.get(f"{COINGECKO_API_URL}/bitcoin")
        bitcoin_data = response.json()
        

    # Extract relevant information
        name = bitcoin_data['name']
        symbol = bitcoin_data['symbol']
        current_price = bitcoin_data['market_data']['current_price']['usd']
        market_cap = bitcoin_data['market_data']['market_cap']['usd']
        high_24h = bitcoin_data['market_data']['high_24h']['usd']
        low_24h = bitcoin_data['market_data']['low_24h']['usd']
        return render_template('index.html', name=name, symbol=symbol,date_and_time=str(now) ,current_price=current_price,
                           market_cap=market_cap, high_24h=high_24h, low_24h=low_24h)
    else:
        return redirect(url_for('login'))

@app.route('/ethereum')
def ethereum_data():
    if 'username' in session:
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        response = requests.get(f"{COINGECKO_API_URL}/ethereum")
        ethereum_data = response.json()

    # Extract relevant information
        name = ethereum_data['name']
        symbol = ethereum_data['symbol']
        current_price = ethereum_data['market_data']['current_price']['usd']
        market_cap = ethereum_data['market_data']['market_cap']['usd']
        high_24h = ethereum_data['market_data']['high_24h']['usd']
        low_24h = ethereum_data['market_data']['low_24h']['usd']
        return render_template('index.html', name=name, symbol=symbol,date_and_time=str(now) ,current_price=current_price,
                           market_cap=market_cap, high_24h=high_24h, low_24h=low_24h)
        
        
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password=request.form["password"]
        user = users.query.filter_by(email=email).first()
        if user:
            if password == user.password:
                session["username"] = user.username
                return redirect(url_for("welcome"))
            
            else:
                flash("incorrect password")
                return redirect(url_for("login"))
        else:
            flash("user not found")
            return redirect(url_for("register"))
        
        
    else:
        if "username" in session:
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])

def register():
    if request.method=="POST":
        email = request.form["email"]
        password=request.form["password"]
        username=request.form["username"]
        name=request.form["name"]
        rpassword=request.form["rpassword"]
        if rpassword != password:
            flash("password and repeat password must be same")
            return redirect(url_for("register"))
        new_user = users(name=name, email=email, password=password, username=username)

        # Add the new user to the database session
        db.session.add(new_user)
        try:
            # Commit the changes to the database
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))
        except IntegrityError as e:
            # Handle the unique constraint violation (e.g., username already exists)
            db.session.rollback()
            flash("Registration failed. Choose a new username.", "error")
            return redirect(url_for("register"))
        except Exception as e:

            # Handle any exceptions (e.g., unique constraint violation)
            db.session.rollback()
            flash(f"Registration failed: {str(e)}", "error")
            return redirect(url_for("register"))
    else:
        if "username" in session:
            return redirect(url_for("username"))

        return render_template("signup.html")
@app.route("/user")
def user():
    if "username" in session:
        username = session["username"]
        return redirect(url_for("welcome"))
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    if "username" in session:
        flash("You are successfully logged out","info")
    session.pop("username", None)
    return redirect(url_for("login"))
if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)