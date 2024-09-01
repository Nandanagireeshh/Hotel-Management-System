from flask import *
from database import *

public = Blueprint('public', __name__)

@public.route('/')
def home():
    return render_template('home.html')

@public.route('/login', methods=['post', 'get'])
def login():
    if 'btn' in request.form:
        uname = request.form['uname']
        pasw = request.form['pasw']

        q = "select * from login where username='%s' and password='%s'" % (uname, pasw)
        res = select(q)

        if res:
            session['loginid'] = res[0]["login_id"]
            session['utype'] = res[0]["usertype"]
            utype = res[0]["usertype"]
            if utype == "admin":
                flash("Login Success")
                return redirect(url_for("admin.adminhome"))
            elif utype == "user":
                q = "select * from user where login_id='%s'" % (session['loginid'])
                val1 = select(q)
                if val1:
                    session['uid'] = val1[0]['user_id']
                    flash("Login Success")
                    return redirect(url_for("user.userhome"))
            else:
                flash("failed try again")
                return redirect(url_for("public.login"))
        else:
            flash("Invalid Username or Password!")
            return redirect(url_for("public.login"))

    return render_template("login.html")

@public.route("/userreg", methods=['get', 'post'])
def userreg():
    if 'btn' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']

        pwd = request.form['pwd']
        uname = request.form['uname']

        q = "select * from login where username='%s'" % (uname)
        res = select(q)
        if res:
            flash("This Username already exist!, try register with new one.")
        else:
            q = "insert into login values(null,'%s','%s','user')" % (uname, pwd)
            lid = insert(q)
            q = "insert into user values (NULL,'%s','%s','%s','%s','%s','%s')" % (lid, fname, lname, place, phone, email)
            insert(q)
            flash("Registration successful")
            return redirect(url_for("public.login"))
    return render_template("userreg.html")
