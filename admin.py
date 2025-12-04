from flask import *
from database import *
admin=Blueprint("admin",__name__)
@admin.route("/adm")
def adm():
    return render_template("admin.html")

@admin.route("/viewcompny")
def viewcompny():
    data={}
    s="select * from company"
    res=select(s)
    data['view']=res

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='delete':
        qry="delete from company where login_id='%s'"%(id)
        delete(qry)
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
    else:
        action=None
    if action=='update':
        qry1="select * from company where login_id='%s'"%(id)
        res=select(qry1)
        data['up']=res
    if 'up' in request.form:
        name=request.form['name']
        pl=request.form['pl']
        ph=request.form['ph']
        em=request.form['em']
        est=request.form['est']

        qry2="update company set company name='%s',place='%s', Phone='%s',email='%s', est='%s' where login_id='%s'"%(name,pl,ph,em,est,id)
        update(qry2)

    return render_template("viewcmp.html",data=data)

@admin.route("/viewjobs")
def viewjobs():
    id=request.args["id"]

    data={}
    s="select * from jobs where company_id='%s'"%(id)
    res=select(s)
    data['view']=res
    if 'view' in request.form:
        title=request.form['title']
        quali=request.form['quali']
        details=request.form['details']
        date=request.form['date']
        up=request.form['up']

        qry2="update job set company title='%s',quali='%s', details='%s',ldate='%s', up='%s' where company_id='%s'"%(title,quali,details,date,up,id)
        update(qry2)

    return render_template("viewjobs.html",data=data)

@admin.route("/viewappl")
def viewappl():
    data={}
    s="select * from application_request"
    res=select(s)
    data['view']=res
    return render_template("viewappl.html",data=data)


@admin.route("/viewcmpln")
def viewcmpln():
    data={}
    s="select * from complaints"
    res=select(s)
    data['view']=res
    return render_template("viewcmpln.html",data=data)

@admin.route("/sndreply",methods=['get','post'])
def sndreply():
    id=request.args['id']
    
    if 'submit' in request.form:
            rep=request.form['rep']
            a="update complaints set reply='%s' where complaint_id='%s'"%(rep,id)
            update(a)
            return '''<script>alert('replied');window.location="/viewcmpln"</script>'''
    return render_template("sndreply.html")