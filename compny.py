from flask import *
from database import *
compny=Blueprint("compny",__name__)
@compny.route("/cmp")
def cmp():
    return render_template("comp.html")

@compny.route("/upjob")
def upjob():
    return render_template("job.html")

@compny.route("/viewappl")
def viewappl():
    return render_template("viewappl.html")