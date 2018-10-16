from flask import  flash,Blueprint,render_template,session,redirect,url_for
from .stockforms import LoginForm
from flask_login import login_required
from flask_login import login_user
from .models import User
view=Blueprint('view',__name__)



@view.route('/',methods=['GET','POST'])
def index():
    form=LoginForm()
    if form.validate_on_submit():
        session['name']=form.name.data
        return redirect(url_for('view.detail'))
    return render_template('index.html',form=form,name=session.get('name'))


@view.route('/detail')
@login_required
def detail():
    return render_template('detail.html')

@view.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('view.detail'))
        flash('Invalid username or password.')
    return render_template('index.html',form=form,name=session.get('name'))


@view.route('/navigator',methods=['GET','POST'])
@login_required
def navigator():
    return render_template('navigator.html')


@view.route('/stockdetail',methods=['GET','POST'])
@login_required
def stockdetail():
    return render_template('stockdetail.html')