from flask import *
from database import *

compny=Blueprint("compny",__name__)

@compny.route("/cmp")
def cmp():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    return render_template("comp.html")

@compny.route("/viewappl")
def viewappl():
    if 'login_id' not in session:
        return redirect(url_for('public.login'))
    
    data = {}
    # Get company_id from session
    q = "SELECT company_id FROM company WHERE login_id='%s'" % (session['login_id'])
    comp = select(q)
    
    if comp:
        company_id = comp[0]['company_id']
        # Get applications for this company's jobs
        q = "SELECT a.*, j.title, u.fname, u.lname, u.email, u.phone FROM application a INNER JOIN jobs j ON a.job_id=j.job_id INNER JOIN user u ON a.user_id=u.user_id WHERE j.company_id='%s'" % (company_id)
        data['applications'] = select(q)
    
    return render_template("company_viewappl.html", data=data)