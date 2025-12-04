from flask import *
from database import *
api=Blueprint("api",__name__)



@api.route("/user_reg")
def user_reg():
  
    data={}
    fname=request.args['fname']
    lname=request.args['lname']
    place=request.args['place']
    mail=request.args['mail']
    phone=request.args['phone']
    uname=request.args['uname']
    pas=request.args['pass']

    a="insert into login values(null,'%s','%s','user')"%(uname,pas)
    id=insert(a)

    a1="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(id,fname,lname,place,mail,phone)
    res1=insert(a1)

    print(res1,"/////////////////")

    if res1:
        data['status']='success'
    else:
        data['status']='failed'
    return str(data)

@api.route("/login_users")
def userslogin():
    data={}
    username=request.args['username']
    pwd=request.args['psw']
    print(username,pwd)

    qry="select * from login where username='%s' and password='%s'"%(username,pwd)
    res=select(qry)
    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
 
    return str(data)

        
        


