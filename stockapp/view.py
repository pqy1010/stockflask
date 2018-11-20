from flask import  flash,Blueprint,render_template,session,redirect,url_for,request,current_app,g
from .stockforms import LoginForm
from flask_login import login_required
from flask_login import login_user,logout_user
from .models import User,StockState
from . import db
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
@view.route('/searchstock')
@login_required
def searchstock():
    reqval=request.values.to_dict()
    if 'page' not in reqval:
        reqval['page']=1
    if 'cmd' not in reqval:
        reqval['cmd']=1

    if int(reqval['cmd'])==1:
        pagination = StockState.query.filter_by().paginate(int(reqval['page']), per_page=8,error_out=False)
    elif int(reqval['cmd'])==2:
        pagination = StockState.query.filter_by(state='wait buy').paginate(int(reqval['page']), per_page=8, error_out=False)
    elif int(reqval['cmd'])==3:
        pagination = StockState.query.filter_by(state='own').paginate(int(reqval['page']), per_page=8, error_out=False)
    elif int(reqval['cmd']) == 4:
        pagination = StockState.query.filter_by(state='selling').paginate(int(reqval['page']), per_page=8, error_out=False)
    elif int(reqval['cmd']) == 5:
        pagination = StockState.query.filter_by(state='sold').paginate(int(reqval['page']), per_page=8, error_out=False)
    elif int(reqval['cmd']) == 6:
        pagination = StockState.query.filter_by(state='buying').paginate(int(reqval['page']), per_page=8, error_out=False)
    elif int(reqval['cmd']) == 7:
        pagination = StockState.query.filter_by(state='ignore').paginate(int(reqval['page']), per_page=8,error_out=False)

    stocklist=pagination.items
    data={}
    data['stocklist']=stocklist
    data['displaylist'] = ['name', 'code', 'ctime', 'b_time', 'b_price', 'b_money', 'b_count', 'owntime', 'state', 'earn','earnrate', 's_price','s_time']
    data['cmd']=reqval['cmd']
    data['page']=reqval['page']
    return render_template('stockdetail.html',data=data,pagination=pagination)

@view.route('/updatestockstate')
@login_required
def updatestockstate():
    reqval=request.values.to_dict()
    stock=StockState.query.filter_by(ID=int(reqval['stockID'])).first()




    upstate=int(reqval['upstate'])
    if upstate==11:# wait buy->buying
        stock.state='buying'
    elif upstate==12:# wait buy->ignore
        stock.state='ignore'
    elif upstate==13:# buying->wait buy
        stock.state='wait buy'
    elif upstate==14:# own->selling
        stock.state='selling'
    elif upstate==15:# selling->own
        stock.state='own'
    elif upstate==16:# ignore->wait buy
        stock.state='wait buy'
    db.session.commit()

    return redirect(url_for('view.searchstock',cmd=reqval['cmd'],page=reqval['page']))