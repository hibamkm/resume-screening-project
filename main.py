from flask import *
from public import public
from admin import admin
from compny import compny
from api import api

app=Flask(__name__)

app.secret_key="estdrftgyuh"

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(compny)
app.register_blueprint(api)


app.run(debug=True,port=5005,host="0.0.0.0")
