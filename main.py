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

@app.route('/', methods = ['GET','POST'])
@app.route('/login', methods = ['GET','POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if(email and password):
            record = users.query.filter(users.email == email, users.password == password).first()
            if(record):
                session['user_id'] = record.id
                return redirect(url_for('account_page', user_id = record.id))
            else:
                flash('Email or password is not true!', 'danger')
                return render_template('login.html', invalidField = request.form)
        else:
            flash('Email or password field is empty!', 'danger')
            return render_template('login.html', invalidField = request.form)
    else:
        # Eger login olubsa birde logine getmeyecek
        if('user_id' in session):
            record_id = session['user_id']
            return redirect(url_for('account_page', user_id = record_id))
        else:
            return render_template('login.html', invalidField = request.form)


@app.route('/register', methods = ['GET','POST'])
def register_page():
    if (request.method == 'POST'):        
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        if (name and surname and email and password):
            if(users.query.filter(users.email == email).first()):
                flash('This email is already exist!', 'danger')
                return render_template('register.html')                
            user = users(name = name, surname = surname, email = email, password = password)
            db.session.add(user)
            db.session.commit()
            flash(f'{name} {surname} registered. ', 'success')
            return redirect(url_for('login_page'))
        else:
            flash('Something is wrong!', 'danger')
            return render_template('register.html')
    else:
        if('user_id' in session):
            record_id = session['user_id']
            return redirect(url_for('account_page', user_id = record_id))
        else:
            return render_template('register.html')


@app.route('/account', methods = ['GET','POST'])
def account_page():
    record = users.query.filter(users.id == user_id).first()
    if(record == None):
        abort(404)
    else:
        if (request.method == 'POST'):        
            pass
        else:
            if('user_id' in session):
                record = users.query.filter(users.id == user_id).first()            
                return render_template('account.html', user = record)
            else:
                return redirect(url_for('login_page'))












# ===========================================
# ---------------Entry Point(Start) ---------------
# ===========================================


if __name__ == "__main__":
    app.run(debug = True)
