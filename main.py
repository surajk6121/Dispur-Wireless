# main.py

from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from .models import User,Data,Subscribers
from . import db
import datetime
import time

today=datetime.date.today()

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/viewemps')
def viewemp():
    user = User.query.filter_by(role_id='CUST1').all()
    return render_template('viewemployees.html',employees=user)

@main.route('/subedit', methods=['POST'])
def subedit():
    if not "plan" in request.form:
        return redirect(url_for('subscriptions'))
    else:
        val=str(request.form['plan'])
        all_data2=Subscribers.query.all()
        print(all_data2)
        print("DEBUG START")
        print(val[0],current_user.id) 
        for i in all_data2:
            print("DEBUG START")
            print(i.Plan_ID,i.U_ID)
            print("END DEBUG")
            # if i.Plan_ID==int(val[0]) and i.U_ID==current_user.id:
            #     date_time_obj = datetime.datetime.strptime(i.Subscription_date, '%Y-%m-%d')
            #     delta=(today-date_time_obj).days
            #     if(delta>90):
            #         break
            #     else:
            #         flash("Cancellation of subscription is possible only after 3 months of cancellation.")
            #         return redirect(url_for('subscriptions'))
        sub = Subscribers.query.filter_by(Plan_ID=val).first()
        db.session.delete(sub)
        db.session.commit()
        return redirect(url_for('main.subscriptions'))



@main.route('/subscriptions')
def subscriptions():
    all_data = Subscribers.query.all()

    li=[]
    for i in all_data:
        all_data1 = Data.query.all()
        for j in all_data1:
            if i.U_ID==current_user.id:
                if i.Plan_ID==j.id:
                    li=li+[[i.Plan_ID,j.name,j.type,j.tariff,j.rental]]
    print(li)
    return render_template("subscription.html", employees = li)

@main.route('/edit')
@login_required
def edit():
    return render_template('edit.html',user=current_user)

@main.route('/edit',methods=['POST'])
@login_required
def edit_profile():
    email = request.form.get('editemail')
    address = request.form.get('editaddress')
    contact = request.form.get('editcontact')
    user = User.query.filter_by(id=current_user.id).first()
    user.email=email
    user.address=address
    user.contact=contact
    db.session.commit()
    return render_template('profile.html', user=current_user)

@main.route('/utariff')
def utariff():
    all_data = Data.query.all()
    return render_template('cust_index.html',employees=all_data)

@main.route('/atariff')
def atariff():
    all_data = Data.query.all()
    return render_template('admin_index.html',employees=all_data)

@main.route('/viewplanuser')
def viewplanuser():
    all_data = Subscribers.query.all()
    li=[]
    for i in all_data:
        all_data1 = Data.query.all()
        for j in all_data1:
            if i.Plan_ID==j.id:
                li=li+[[i.U_ID,i.Plan_ID,j.name,j.type,j.tariff,j.rental]]
    print(li)
    return render_template("subscriptionuser.html", employees = li)

@main.route('/planupdate', methods = ['GET', 'POST'])
def plan_update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.type = request.form['type']
        my_data.tariff = request.form['tariff']
        my_data.validity = request.form['validity']
        my_data.rental = request.form['rental']
        db.session.commit()
        flash("Tariff Plan Updated Successfully")
        return render_template('index.html')

@main.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Tariff Plan Deleted Successfully")
    return render_template('index.html')

@main.route('/post_insert', methods = ['POST'])
def post_insert():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        tariff = request.form['tariff']
        validity = request.form['validity']
        rental = request.form['rental']
        my_data = Data(name=name, type=type, tariff=tariff,validity=validity,rental=rental)
        db.session.add(my_data)
        db.session.commit()
        flash("Tariff Plan Inserted Successfully")
        return render_template('index.html')

@main.route('/add', methods=['POST'])
def add():
    if not "plan" in request.form:
        return redirect(url_for('cust_Index'))
    else:
        val=str(request.form['plan'])
        from ast import literal_eval
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        val = val[1:-1].split(',')
        print(val)
        #val=literal_eval(val)
        print('hello')
        print(val[0])
        subs=Subscribers(Plan_ID=int(val[0]),U_ID=current_user.id,Amount_Payable=int(val[5]),Date_Of_Call=0,Call_Duration=0,Subscription_date=today)
        db.session.add(subs)
        db.session.commit()
        return render_template('cust_index.html')


# ------------------>>>>access management<<<<<-----------------------------
@main.route('/accessPortal',methods=['GET','POST'])
def accessPortal():
    user = User.query.all()
    return render_template('AccessMP.html',employees=user)
    
@main.route('/accessupdate', methods = ['GET', 'POST'])
def accessupdate():
    if request.method == 'POST':
        level=['CUST1','EMP1','HR1','ISM1','ADM1']
        
        
        my_data = User.query.filter_by(id=request.form['user_id']).first()
        my_data.role_id = request.form['Access_Level']
        if my_data.role_id in level:
            if(level.index(current_user.role_id)>=level.index(my_data.role_id)):
                db.session.commit()
                flash("Updated successful")
                return redirect(url_for('main.accessPortal'))
            else:
                flash("Access Denied")
                return redirect(url_for('main.accessPortal'))
        else:
            flash("Invalid Role")
            return redirect(url_for('main.accessPortal'))