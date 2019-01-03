from flask import  flash,Blueprint,render_template,session,redirect,url_for,request,current_app,g
from .stockforms import LoginForm
from flask_login import login_required
from flask_login import login_user,logout_user
from .models import User,StockState
from . import db
view=Blueprint('view',__name__)
import sqlite3
import pickle

import plotly.offline as offline
import plotly.graph_objs as go
from datetime import datetime
import tushare as ts
import pandas as pd
import os

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
    return render_template('detail.html',name=session.get('uname'))

@view.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            session['uname']=form.name.data
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

@view.route('/stockplot')
@login_required
def stockplot():
    reqval=request.values.to_dict()
    if 'stockcode' in reqval:
        filename='../stock/savedata/'+reqval['stockcode']+'.pkl'
        if not os.path.exists(filename):
            return render_template('stockplotfig.html')

        with open(filename, 'rb') as f:
            stockinfo = pickle.load(f)
        dayK=stockinfo['data']

        displaylen=min(120,len(dayK.open))
        trace=go.Candlestick(x=dayK.date[0:displaylen],open=dayK.open[0:displaylen],high=dayK.high[0:displaylen],low=dayK.low[0:displaylen],close=dayK.close[0:displaylen],name='日均线')
        trace2=go.Scatter(x=dayK.date,y=stockinfo['zhicheng'][0:displaylen],mode='lines',name='支撑线')
        trace3=go.Scatter(x=dayK.date,y=stockinfo['zuli'][0:displaylen],mode='lines',name='阻力线')
        layout = go.Layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                )
            )
        )

        data = [trace,trace2,trace3]

        fig = go.Figure(data=data, layout=layout)



        trace4=go.Scatter(x=dayK.date,y=stockinfo['x1'][0:displaylen],mode='lines',name='x1')
        trace5 = go.Scatter(x=dayK.date, y=stockinfo['x2'][0:displaylen], mode='lines', name='x2')
        data2=[trace4,trace5]



        figurl = offline.plot(fig, include_plotlyjs=False, output_type='div')
        figurl2 = offline.plot(data2, include_plotlyjs=False, output_type='div')
        resdata={}
        resdata['figstr']=figurl+figurl2
        return render_template('stockplotfig.html',data=resdata)
