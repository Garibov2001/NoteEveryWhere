from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *




# ===========================================
# ---------------Cofigurations ---------------
# ===========================================

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:admin@127.0.0.1:3306/todolist'
app.config['SECRET_KEY'] = "5791628bb0b13ce0c676dfde280ba245"
db = SQLAlchemy(app)


# ===========================================
# ----------------- Models ------------------:
# ===========================================

class users(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    name = db.Column(db.String(255), nullable= False)
    surname = db.Column(db.String(255), nullable= False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self): 
        return f"users('id: {self.id}', 'name: {self.name}' , 'surname: {self.surname}', 'email: {self.email}', 'password: {self.password}')" 



# ===========================================
# ----------------Routes --------------------
# ===========================================

@app.route('/login', methods = ['GET','POST'])
def login_page():
    if request.method == 'POST':
        return 'Welcome'
    else:
        return render_template('login.html')


@app.route('/register', methods = ['GET','POST'])
def register_page():
    if request.method == 'POST':
        print(request.form['name'])
        print(request.form['surname'])
        print(request.form['email'])
        print(request.form['password'])
        return 'Welcome'
    else:
        return render_template('register.html')
















# ===========================================
# ---------------Entry Point(Start) ---------------
# ===========================================


if __name__ == "__main__":
    app.run(debug = True)
