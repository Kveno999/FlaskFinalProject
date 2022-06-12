from flask import Flask,request,render_template,url_for,redirect,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'Kveno'

class Database(db.Model):
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    password = db.Column(db.String(100))


def __ini__(self,name,lastname, password):
    self.name = name
    self.lastname = lastname
    self.password = password

db.create_all()


@app.route('/registration',methods = ['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if not any(char.isdigit() for char in request.form['psw']):
            return render_template("registration.html")
        else:
            name = request.form['name']
            lastname = request.form['lastname']
            password = generate_password_hash(request.form["psw"])
            user_info = Database(name=name,lastname=lastname, password=password)
            db.session.add(user_info)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('registration.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['psw']
        user = Database.query.filter_by(name=name).first()
        session['client'] = name

        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('login'))
        return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template("home.html", name = session['client'])
