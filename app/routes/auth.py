from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from app import db
from app.models import User
auth_bp=Blueprint('auth',__name__)

USER_CREDENTIALS={
    'username':'admin',
    'password':'1234'
}
@auth_bp.route('/login',methods=["GET","POST"])
def login():
    if request.method =="POST":
        username= request.form.get('username')
        password=request.form.get('password')
        
        if username==USER_CREDENTIALS['username'] and password==USER_CREDENTIALS['password']:
            session['user']=username
            flash('Login Successful','success')
            return redirect(url_for('tasks.view_tasks'))
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = username
            flash('Login Successful', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash("Invalid Username or Password",'danger')
    return render_template("login.html")


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    from app.models import User
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Please fill out all fields', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user',None)
    flash("Logged out!!",'info')
    return redirect(url_for('auth.login'))