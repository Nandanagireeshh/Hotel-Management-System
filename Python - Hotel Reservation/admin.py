from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')


@admin.route('/manage_room',methods=['get','post'])
def manage_room():
    data={}
    if 'btn' in request.form:
        room=request.form['room']
        det=request.form['det']
        rate=request.form['rate']
        
    
        q="insert into room values (null,'%s','%s','%s')"%(room,det,rate)
        insert(q)
        flash("Successfully Added")
        return redirect(url_for("admin.manage_room"))

    data={}
    q="select * from room"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        rid=request.args['rid'] 
    else:
        action=None

    
    if action == "update":
        q="select * from room where room_id='%s'"%(rid)
        val=select(q)
        data['raw']=val

        if 'update' in request.form:
            room=request.form['room']
            det=request.form['det']
            rate=request.form['rate']

            q="update room set room='%s',description='%s',rate='%s' where room_id='%s' "%(room,det,rate,rid)
            update(q)
            flash("Updated Successfully")
            return redirect(url_for("admin.manage_room"))
    if action == "delete":
        q="delete from room where room_id='%s' "%(rid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.manage_room"))
    return render_template('manage_room.html',data=data) 


import uuid


@admin.route('/manage_food',methods=['get','post'])
def manage_food():
    data={}
    if 'btn' in request.form:
        food=request.form['food']
        det=request.form['det']
        quantity=request.form['quantity']
        image=request.files['image']
        rate=request.form['rate']
        path="static/uploads/"+str(uuid.uuid4())+image.filename
        image.save(path)
        
    
        q="insert into food values (null,'%s','%s','%s','%s','%s')"%(food,det,path,rate,quantity)
        insert(q)
        flash("Successfully Added")
        return redirect(url_for("admin.manage_food"))

    data={}
    q="select * from food"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        fid=request.args['fid'] 
    else:
        action=None

    
    if action == "update":
        q="select * from food where food_id='%s'"%(fid)
        val=select(q)
        data['raw']=val

        if 'update' in request.form:
            food=request.form['food']
            det=request.form['det']
            rate=request.form['rate']
            quantity=request.form['quantity']
            if request.files['image']:
                image=request.files['image']
                path="static/uploads/"+str(uuid.uuid4())+image.filename
                image.save(path)

                q="update food set food='%s',description='%s',image='%s',rate='%s', quantity='%s' where food_id='%s' "%(food,det,path,rate,quantity,fid)
            else:
                q="update food set food='%s',description='%s',rate='%s', quantity='%s' where food_id='%s' "%(food,det,rate,quantity,fid)

            update(q)
            flash("Updated Successfully")
            return redirect(url_for("admin.manage_food"))   
    if action == "delete":
        q="delete from food where food_id='%s' "%(fid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.manage_food"))
    return render_template('manage_food.html',data=data) 





@admin.route('/admin_manage_staff',methods=['get','post'])
def admin_manage_staff():
    data={}


    if 'btn' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        place=request.form['place']
        phone=request.form['phone']
        email=request.form['email']
        pwd=request.form['pwd']
        uname=request.form['uname']
        
    
        q="select * from login where username='%s'"%(uname)
        res=select(q)
        if res:
            flash("This Username already exist!, try register with new one.")
        else:
            q="insert into login values(null,'%s','%s','staff')"%(uname,pwd)
            lid=insert(q)
            q="insert into staff values (NULL,'%s','%s','%s','%s','%s','%s')"%(lid,fname,lname,place,phone,email)
            insert(q)
            flash("Registration successfull")
            return redirect(url_for("admin.admin_manage_staff"))


    q="select * from staff"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        sid=request.args['sid'] 
        lid=request.args['lid'] 
    else:
        action=None

    
    if action == "update":
        q="select * from staff where staff_id='%s'"%(sid)
        val=select(q)
        data['raw']=val

        if 'update' in request.form:
            fname=request.form['fname']
            lname=request.form['lname']
            place=request.form['place']
            
            phone=request.form['phone']
            email=request.form['email']

            q="update staff set fname='%s', lname='%s', place='%s', phone='%s', email='%s' where staff_id='%s' "%(fname,lname,place,phone,email,sid)
            update(q)
            flash("Updated Successfully")
            return redirect(url_for("admin.admin_manage_staff"))
    if action == "delete":
        q="delete from staff where staff_id='%s' "%(sid)
        delete(q)
        q="delete from login where login_id='%s' "%(lid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.admin_manage_staff"))
    return render_template('admin_manage_staff.html',data=data)


@admin.route('/admin_view_room_bookings')
def admin_view_room_bookings():
    data={}
    q="SELECT * FROM `booking`,`user`,`room` WHERE `booking`.`user_id`=`user`.`user_id` AND `booking`.`room_id`=`room`.`room_id`"
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        bid=request.args['bid']
    else:
        action=None

    if action == "accept":
        q="update booking set status='Request Accepted' where booking_id='%s'"%(bid)
        update(q)
        flash("Request Accepted")
        return redirect(url_for("admin.admin_view_room_bookings"))
    
    if action == "reject":
        q="update booking set status='Rejected' where booking_id='%s'"%(bid)
        update(q)
        flash("Request Rejected")
        return redirect(url_for("admin.admin_view_room_bookings"))

    if action == "cancel":
        q="delete from booking where booking_id='%s'"%(bid)
        delete(q)
        flash("Booking Canceled")
        return redirect(url_for("admin.admin_view_room_bookings"))
    return render_template('admin_view_room_bookings.html',data=data)


@admin.route('/admin_view_food_bookings')
def admin_view_food_bookings():
    data={}
    q="SELECT * FROM `ordermaster`,`orderdetails`,`user`,`food` WHERE `ordermaster`.`ordermaster_id`=`orderdetails`.`ordermaster_id` AND `orderdetails`.`food_id`=`food`.`food_id` AND `ordermaster`.`user_id`=`user`.`user_id`"
    data['res']=select(q)
    return render_template('admin_view_food_bookings.html',data=data)


@admin.route("/adminviewcomplaints",methods=['get','post'])
def adminviewcomplaints():
    data={}
    q="select * from user inner join complaint using (user_id)"
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        cid=request.args['cid']
    else:
        action=None

    if action == "reply":
        data['replysec']=True

        if 'submit' in request.form:
            reply=request.form['reply']

            q="update complaint set reply='%s' where complaint_id='%s'"%(reply,cid)
            update(q)
            return redirect(url_for("admin.adminviewcomplaints"))
    return render_template("adminviewcomplaints.html",data=data)


@admin.route('/food_payment')
def food_payment():
    data={}
    bid=request.args['bid']
    q="select * from payment where book_id='%s' and type='food'"%(bid)
    data['res']=select(q)
    if 'action' in request.args:
        action=request.args['action']
    else:
        action=None
    if action == "accept":
        q="update ordermaster set order_status='Payment Accepted' where ordermaster_id='%s'"%(bid)
        update(q)
        flash("Payment Accepted")
        return redirect(url_for("admin.admin_view_food_bookings"))
    return render_template('food_payment.html',data=data,bid=bid)


@admin.route('/room_payment')
def room_payment():
    data={}
    bid=request.args['bid']
    q="select * from payment where book_id='%s' and type='room'"%(bid)
    data['res']=select(q)
    if 'action' in request.args:
        action=request.args['action']
    else:
        action=None
    if action == "accept":
        q="update booking set status='Payment Accepted' where booking_id='%s'"%(bid)
        update(q)
        flash("Payment Accepted")
        return redirect(url_for("admin.room_payment",bid=bid))
    return render_template('room_payment.html',data=data,bid=bid)

@admin.route('/view_feedback')
def view_feedback():
    data = {}
    q = """
        SELECT feedback.feedback_text, feedback.created_at, user.fname, user.lname 
        FROM feedback 
        JOIN user ON feedback.user_id = user.user_id
    """
    data['feedbacks'] = select(q)  # Ensure `select` is a function that executes your query and returns the results
    return render_template('view_feedback.html', data=data)
