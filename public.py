from flask import *
from database import *

public=Blueprint("public",__name__)


@public.route("/")
def home():
    return render_template("home.html")

@public.route("/company_reg",methods=['post','get'])
def comp_reg():
    if 'reg' in request.form:
        cmp=request.form['cmp']
        plc=request.form['place']
        phone=request.form['ph']
        email=request.form['mail']
        est_yr=request.form['year']
        username=request.form['uname']
        password=request.form['password']

        qry="insert into login values(null,'%s','%s','company')"%(username,password)
        res=insert(qry)

        qry1="insert into company values(null,'%s','%s','%s','%s','%s','%s')"%(res,cmp,plc,phone,email,est_yr)
        res1=insert(qry1)
 
    return render_template("comp_reg.html")


@public.route("/login",methods=['post','get'])
def login():
    if 'log' in request.form:
        uname=request.form['uname']
        psw=request.form['psw']

        a="select * from login where username='%s' and password='%s'"%(uname,psw)
        res=select(a)

        session['login_id']=res[0]['login_id']

        if res[0]['usertype']=='company':
            s="select * from company where login_id='%s'"%(session['login_id'])
            r=select(s)
            session['cid']=r[0]['company_id']
            return redirect(url_for("compny.cmp"))
        
        elif res[0]['usertype']=='admin':
            return redirect(url_for("admin.adm"))
    return render_template("login.html")

@public.route("/upjob",methods=['post','get'])
def upjob():
    if 'sub' in request.form:
        title=request.form['title']
        qual=request.form['quali']
        det=request.form['details']
        date=request.form['date']


        qry="insert into jobs values(null,'%s','%s','%s','%s','%s',curdate(),'pending')"%(session['cid'],title,qual,det,date)
        res=insert(qry)
 
    return render_template("job.html")

@public.route("/user_reg", methods=['GET', 'POST'])
def user_reg():
    if 'reg' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['mail']
        username = request.form['uname']
        password = request.form['password']
        
        # Insert into login table
        qry = "INSERT INTO login VALUES(null,'%s','%s','user')" % (username, password)
        res = insert(qry)
        
        # Insert into user table
        qry1 = "INSERT INTO user VALUES(null,'%s','%s','%s','%s','%s','%s',NULL,NULL)" % (res, fname, lname, place, email, phone)
        res1 = insert(qry1)
        
        flash('Registration successful! Please login.')
        return redirect(url_for('public.login'))
    
    return render_template("user_reg.html")
