from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from datetime import timedelta, date




# ===========================================
# ---------------Cofigurations ---------------
# ===========================================

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:admin@127.0.0.1:3306/todolist'
app.config['SECRET_KEY'] = "5791628bb0b13ce0c676dfde280ba245"
app.permanent_session_lifetime = timedelta(days=5)
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

class lists(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False) # Foreign key to Candidates   
    status = db.Column(db.Integer, nullable= False, default = 0)  # 0 -Undone, 1- Done
    star = db.Column(db.Boolean(), nullable= False, default = False) # True - Starred, False - Unstarred
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date(), nullable= False, default = date.today )

    def __repr__(self): 
        return f"lists('id: {self.id}', 'user_id: {self.user_id}' , 'status: {self.status}', 'content: {self.content}', 'date: {self.date}')" 


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
                return redirect(url_for('account_page'))
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
            return redirect(url_for('account_page'))
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
            return redirect(url_for('account_page'))
        else:
            return render_template('register.html')

@app.route('/account', methods = ['GET'])
def account_page():
    title = 'Your List'
    if('user_id' in session):      
        record = users.query.filter(users.id == session['user_id']).first()            
        return render_template('account.html', user = record, title = title, settings = False)
    else:
        return redirect(url_for('login_page'))

@app.route('/account/settings', methods = ['GET','POST'])
def account_settings_page():
    title = 'Account Settings'
    if('user_id' in session):
        if (request.method == 'POST'): 
            argName = request.form['name']
            argSurname = request.form['surname']
            argPass = request.form['password']
            argConfirmPass = request.form['confirm_password']
            argCurrentPass = request.form['current_password']

            if ((argName and argSurname and (bool(argPass) == False) 
                and (bool(argConfirmPass) == False))):
                record = users.query.filter(users.id == session['user_id']).first()
                if (argCurrentPass == record.password):
                    record.name = argName
                    record.surname = argSurname
                    db.session.commit()
                    flash('Your account is updated!', 'success')
                    return redirect(url_for('account_page'))
                else:
                    flash('Your current password is not true!', 'danger')
                    record = users.query.filter(users.id == session['user_id']).first()            
                    return render_template('account_settings.html', user = record, title = title, settings = True)
            elif(argName and argSurname and argPass and argConfirmPass):
                if (argPass == argConfirmPass):
                    record = users.query.filter(users.id == session['user_id']).first()
                    if (argCurrentPass == record.password):
                        record.name = argName
                        record.surname = argSurname
                        record.password = argPass
                        db.session.commit()
                        flash('Your account is updated!', 'success')
                        return redirect(url_for('account_page'))
                    else:
                        flash('Your current password is not true!', 'danger')
                        record = users.query.filter(users.id == session['user_id']).first()            
                        return render_template('account_settings.html', user = record, title = title,  settings = True)
                else:
                    flash('Your passwords doesn\'t match!', 'danger')
                    record = users.query.filter(users.id == session['user_id']).first()            
                    return render_template('account_settings.html', user = record, title = title,  settings = True)
            else:
                flash('Name, surname or all fields can\'t be empty!', 'danger')
                record = users.query.filter(users.id == session['user_id']).first()            
                return render_template('account_settings.html', user = record, title = title,  settings = True)
        else:            
            record = users.query.filter(users.id == session['user_id']).first()            
            return render_template('account_settings.html', user = record, title = title, settings = True)
    else:
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout_page():
    session.pop('user_id', None)
    return redirect(url_for('login_page'))


@app.route('/account/note_add', methods = ['POST'])
def note_add():
    if('user_id' in session):   
        noteObj = lists(user_id = session['user_id'], content = request.form['content'])
        db.session.add(noteObj)
        db.session.commit()

        return 'Hello'  
        # record = users.query.filter(users.id == session['user_id']).first()            
        # return render_template('account.html', user = record, title = title, settings = False)
    else:
        return redirect(url_for('login_page'))












# ===========================================
# ---------------Entry Point(Start) ---------------
# ===========================================


if __name__ == "__main__":
    app.run(debug = True)
