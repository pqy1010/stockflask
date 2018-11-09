from flask import  flash,Blueprint,render_template,session,redirect,url_for,request,current_app,g
from .stockforms import LoginForm
from flask_login import login_required
from flask_login import login_user,logout_user
from .models import User,StockState
view=Blueprint('view',__name__)
import sqlite3


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


# @view.route('/stockdetail',methods=['GET','POST'])
@login_required
def stockdetail():
    return render_template('stockdetail.html')

@view.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('view.index'))



@view.route('/stockdetail',methods=['GET','POST'])
@view.route('/searchstock/(status)')
@login_required
def searchstock(status='wait buy'):
    page = request.args.get('page', 1, type=int)
    pagination = StockState.query.filter_by(state=status).paginate(page, per_page=8,error_out=False)
    stocklist=pagination.items
    data={}
    data['stocklist']=stocklist
    return render_template('stockdetail.html',data=data,pagination=pagination)