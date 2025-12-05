from flask import *
from database import *

admin=Blueprint("admin",__name__)

@admin.route("/adm")
def adm():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    return render_template("admin.html")

@admin.route("/viewcompny")
def viewcompny():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    data={}
    s="SELECT * FROM company"
    res=select(s)
    data['view']=res

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
        
        if action=='delete':
            qry="DELETE FROM company WHERE login_id='%s'" % (id)
            delete(qry)
            qry2="DELETE FROM login WHERE login_id='%s'" % (id)
            delete(qry2)
            return redirect(url_for('admin.viewcompny'))
        
        elif action=='update':
            qry1="SELECT * FROM company WHERE login_id='%s'" % (id)
            res=select(qry1)
            data['up']=res
    
    if 'up' in request.form:
        id=request.args['id']
        name=request.form['name']
        pl=request.form['pl']
        ph=request.form['ph']
        em=request.form['em']
        est=request.form['est']

        qry2="UPDATE company SET company_name='%s', place='%s', phone='%s', email='%s', est_year='%s' WHERE login_id='%s'" % (name, pl, ph, em, est, id)
        update(qry2)
        return redirect(url_for('admin.viewcompny'))

    return render_template("viewcmp.html",data=data)

@admin.route("/viewjobs")
def viewjobs():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    id=request.args["id"]
    data={}
    s="SELECT * FROM jobs WHERE company_id='%s'" % (id)
    res=select(s)
    data['view']=res
    
    return render_template("viewjobs.html",data=data)

@admin.route("/viewappl")
def viewappl():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    data={}
    s="SELECT a.*, j.title, u.fname, u.lname, c.company_name FROM application a INNER JOIN jobs j ON a.job_id=j.job_id INNER JOIN user u ON a.user_id=u.user_id INNER JOIN company c ON j.company_id=c.company_id"
    res=select(s)
    data['view']=res
    return render_template("viewappl.html",data=data)

@admin.route("/viewcmpln")
def viewcmpln():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    data={}
    s="SELECT * FROM complaints"
    res=select(s)
    data['view']=res
    return render_template("viewcmpln.html",data=data)

@admin.route("/sndreply",methods=['get','post'])
def sndreply():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    id=request.args['id']
    
    if 'submit' in request.form:
        rep=request.form['rep'].replace("'", "''")
        a="UPDATE complaints SET reply='%s' WHERE complaint_id='%s'" % (rep, id)
        update(a)
        return '''<script>alert('Replied successfully');window.location="/viewcmpln"</script>'''
    
    return render_template("sndreply.html")