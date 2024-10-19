from flask import *
from database import *
import razorpay
import smtplib
from email.mime.text import MIMEText

user = Blueprint('user', __name__)


@user.route('/userhome')
def userhome():
    q = "SELECT * FROM user WHERE login_id='%s'" % (session['loginid'])
    res = select(q)
    name = res[0]['fname'] + " " + res[0]['lname']
    return render_template('userhome.html', name=name)


@user.route('/view_food')
def view_food():
    data = {}
    q = "SELECT * FROM food"
    data['res'] = select(q)
    return render_template('view_food.html', data=data)


@user.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    data = {}
    iid = request.args['iid']
    cp = request.args['cp']
    item = request.args['item']

    q = "SELECT * FROM food WHERE food_id='%s'" % (iid)
    orgstock = select(q)[0]['quantity']

    if 'btn' in request.form:
        total = request.form['total']
        rstock = request.form['rstock']

        if int(rstock) < int(orgstock):
            q = "SELECT * FROM ordermaster WHERE order_status='pending' AND user_id='%s'" % (session['uid'])
            res = select(q)
            if res:
                oid = res[0]['ordermaster_id']
            else:
                q = "INSERT INTO ordermaster VALUES (NULL, '%s', 0, CURDATE(), 'pending')" % (session['uid'])
                oid = insert(q)
            q = "SELECT * FROM orderdetails WHERE food_id='%s' AND ordermaster_id='%s'" % (iid, oid)
            val = select(q)
            if val:
                q = "UPDATE orderdetails SET quantity=quantity+'%s', total_amount=total_amount+'%s' WHERE food_id='%s' AND ordermaster_id='%s'" % (
                rstock, total, iid, oid)
                update(q)
            else:
                q = "INSERT INTO orderdetails VALUES (NULL, '%s', '%s', '%s', '%s', 'pending')" % (
                oid, iid, rstock, total)
                insert(q)
            q = "UPDATE ordermaster SET totalamount=totalamount+'%s' WHERE ordermaster_id='%s'" % (total, oid)
            update(q)
            flash("Successfully added to Cart")
            return redirect(url_for("user.view_food"))
        else:
            flash("Insufficient Quantity")

    return render_template('add_to_cart.html', data=data, item=item, cp=cp)


@user.route('/cart')
def cart():
    data = {}
    q = "SELECT *, orderdetails.quantity AS quantity FROM ordermaster, orderdetails, food WHERE ordermaster.ordermaster_id = orderdetails.ordermaster_id AND orderdetails.food_id = food.food_id AND ordermaster.user_id = '%s' AND order_status = 'pending'" % (
    session['uid'])
    data['res'] = select(q)

    action = request.args.get('action')
    ccid = request.args.get('ccid')
    cmid = request.args.get('cmid')
    price = request.args.get('price')

    if action == "remove":
        q = "DELETE FROM orderdetails WHERE orderdetails_id='%s'" % (ccid)
        delete(q)
        q = "UPDATE ordermaster SET totalamount = totalamount - '%s' WHERE ordermaster_id = '%s'" % (price, cmid)
        update(q)
        q = "SELECT * FROM orderdetails WHERE ordermaster_id='%s'" % (cmid)
        val = select(q)
        if not val:
            q = "DELETE FROM ordermaster WHERE ordermaster_id='%s'" % (cmid)
            delete(q)
        return redirect(url_for("user.cart"))

    if action == "add":
        q = "UPDATE orderdetails SET quantity = quantity + 1, total_amount = total_amount + '%s' WHERE orderdetails_id = '%s'" % (
        price, ccid)
        update(q)
        q = "UPDATE ordermaster SET totalamount = totalamount + '%s' WHERE ordermaster_id = '%s'" % (price, cmid)
        update(q)
        return redirect(url_for("user.cart"))

    if action == "minus":
        q = "UPDATE orderdetails SET quantity = quantity - 1, total_amount = total_amount - '%s' WHERE orderdetails_id = '%s'" % (
        price, ccid)
        update(q)
        q = "UPDATE ordermaster SET totalamount = totalamount - '%s' WHERE ordermaster_id = '%s'" % (price, cmid)
        update(q)
        return redirect(url_for("user.cart"))

    return render_template('cart.html', data=data)

@user.route('/customer_make_payment', methods=['GET', 'POST'])
def customer_make_payment():
    data = {}
    omid = request.args['omid']
    amount = request.args['amount']
    if 'btn' in request.form:
        q = "INSERT INTO payment VALUES (NULL, '%s', 'food', '%s', CURDATE())" % (omid, amount)
        insert(q)
        q = "UPDATE ordermaster SET order_status = 'payment completed' WHERE ordermaster_id = '%s'" % (omid)
        update(q)
        flash("Payment Completed")
        return redirect(url_for("user.userhome"))
    return render_template('customer_make_payment.html', data=data, total=amount)


@user.route('/user_room_payment', methods=['GET', 'POST'])
def user_room_payment():
    data = {}
    omid = request.args['omid']
    amount = request.args['amount']
    if 'btn' in request.form:
        q = "INSERT INTO payment VALUES (NULL, '%s', 'room', '%s', CURDATE())" % (omid, amount)
        insert(q)
        q = "UPDATE booking SET status = 'payment completed' WHERE booking_id = '%s'" % (omid)
        update(q)
        flash("Payment Completed")
        return redirect(url_for("user.userhome"))
    return render_template('user_room_payment.html', data=data, total=amount)


@user.route('/food_bookings')
def food_bookings():
    data = {}
    q = "SELECT * FROM ordermaster, orderdetails, food WHERE ordermaster.ordermaster_id = orderdetails.ordermaster_id AND orderdetails.food_id = food.food_id AND ordermaster.user_id = '%s' AND order_status <> 'pending'" % (
    session['uid'])
    data['res'] = select(q)
    return render_template("food_bookings.html", data=data)


@user.route('/user_room_bookings')
def user_room_bookings():
    data = {}
    q = "SELECT * FROM booking, room WHERE booking.room_id = room.room_id AND booking.user_id = '%s'" % (session['uid'])
    data['res'] = select(q)

    action = request.args.get('action')
    bid = request.args.get('bid')

    if action == "cancel":
        q = "DELETE FROM booking WHERE booking_id = '%s'" % (bid)
        delete(q)
        flash("Booking Canceled")
        return redirect(url_for("user.user_room_bookings"))
    return render_template("user_room_bookings.html", data=data)

'''
@user.route('/view_rooms')
def view_rooms():
    data = {}
    q = "SELECT * FROM room"
    data['res'] = select(q)
    return render_template("view_rooms.html", data=data)
'''

@user.route('/view_rooms')
def view_rooms():
    data = {}

    # Query to fetch all room details, including the booking status
    q = "SELECT * FROM room"

    # Assuming select(q) executes the SQL query and returns the results
    data['res'] = select(q)

    # Pass the data to the HTML template
    return render_template("view_rooms.html", data=data)

'''
@user.route('/confirm_booking', methods=['GET', 'POST'])
def confirm_booking():
    data = {}
    from datetime import date

    today = date.today()
    rid = request.args['rid']
    rate = request.args['rate']

    if 'btn' in request.form:
        booking_date = request.form['date']
        days = request.form['days']
        num_persons = request.form['num_persons']

        # Check if the room is already booked for the given date
        q = "SELECT * FROM booking WHERE room_id = '%s' AND date = '%s'" % (rid, booking_date)
        res = select(q)

        if res:
            flash("You have already booked this room for the selected date.")
        else:
            # Insert the booking into the database
            q = """
                INSERT INTO booking (user_id, room_id, amount, date, booking_for, no_of_days, num_persons, status) 
                VALUES ('%s', '%s', '%s', CURDATE(), '%s', '%s', '%s', 'pending')
                """ % (session['uid'], rid, rate, booking_date, days, num_persons)
            insert(q)
            flash("Room Booked Successfully")
            return redirect(url_for("user.userhome"))

    return render_template("confirm_booking.html", data=data, today=today)
'''
@user.route('/confirm_booking', methods=['GET', 'POST'])
def confirm_booking():
    data = {}
    from datetime import date

    today = date.today()
    rid = request.args['rid']  # Room ID
    rate = request.args['rate']  # Room rate

    if 'btn' in request.form:
        booking_date = request.form['date']  # Booking date
        days = request.form['days']  # Number of days for the booking
        num_persons = request.form['num_persons']  # Number of persons for the booking

        # Check if the room is already booked for the given date
        q = "SELECT * FROM booking WHERE room_id = '%s' AND date = '%s'" % (rid, booking_date)
        res = select(q)

        if res:
            flash("You have already booked this room for the selected date.")
        else:
            # Insert the booking into the database
            q = """
                INSERT INTO booking (user_id, room_id, amount, date, booking_for, no_of_days, num_persons, status) 
                VALUES ('%s', '%s', '%s', CURDATE(), '%s', '%s', '%s', 'pending')
                """ % (session['uid'], rid, rate, booking_date, days, num_persons)
            insert(q)

            # Update the room status to 'booked'
            q_update_status = "UPDATE room SET booking_status = 'booked' WHERE room_id = '%s'" % rid
            update(q_update_status)  # Call your update function to execute the query

            flash("Room Booked Successfully")
            return redirect(url_for("user.userhome"))

    return render_template("confirm_booking.html", data=data, today=today)


@user.route("/customer_send_complaint", methods=['GET', 'POST'])
def customer_send_complaint():
    data = {}

    cid = session['uid']

    if 'btn' in request.form:
        comp = request.form['comp']

        q = "INSERT INTO complaint VALUES (NULL, '%s', '%s', 'pending', CURDATE())" % (cid, comp)
        insert(q)
        return redirect(url_for("user.customer_send_complaint"))

    q = "SELECT * FROM complaint WHERE user_id = '%s'" % (cid)
    data['res'] = select(q)
    return render_template("customer_send_complaint.html", data=data)


@user.route('/housekeeping_request', methods=['GET', 'POST'])
def housekeeping_request():


    if request.method == 'POST':
        service_type = request.form['serviceType']
        request_details = request.form['request_details']  # Fixed the space issue


        # Save the request to your database
        q = "INSERT INTO housekeeping_requests (user_id, service_type, request_details, status) VALUES ('%s','%s', '%s', 'pending')" % (
        session['uid'],  service_type, request_details)
        insert(q)

        flash("Your housekeeping request has been submitted successfully!", "success")
        return redirect(url_for('user.housekeeping_request'))

    return render_template('housekeeping_request.html')





''''
@user.route('/housekeeping_request', methods=['GET', 'POST'])
def housekeeping_request():
    if request.method == 'POST':
        service_type = request.form['serviceType']
        request_details = request.form['request_details']  # Fixed the space issue

        # Fetch the room_id associated with the user
        user_id = session['uid']
        room_query = "SELECT room_id FROM user WHERE user_id = %s"  # Replace with your actual user table name
        room_id = fetch_one(room_query, (user_id,))  # This should return the room_id for the current user

        # If room_id is found, proceed to insert the request
        if room_id:
            # Save the request to your database
            q = "INSERT INTO housekeeping_requests (user_id, room_id, service_type, request_details, status) VALUES (%s, %s, %s, %s, 'pending')"
            insert(q, (user_id, room_id, service_type, request_details))  # Assuming `insert` handles parameterized queries

            flash("Your housekeeping request has been submitted successfully!", "success")
            return redirect(url_for('user.housekeeping_request'))
        else:
            flash("No room associated with your account.", "error")
            return redirect(url_for('user.housekeeping_request'))

    return render_template('housekeeping_request.html')
'''

@user.route('/view_housekeeping_requests')
def view_housekeeping_requests():
    data = {}
    q = "SELECT * FROM housekeeping_requests WHERE user_id='%s'" % (session['uid'])
    data['requests'] = select(q)

    return render_template('view_housekeeping_requests.html', data=data)


@user.route('/feedback', methods=['GET', 'POST'])
def feedback():
    data = {}
    if request.method == 'POST':
        feedback_text = request.form['feedback_text']
        user_id = session['uid']  # Fetch the logged-in user's ID from session

        if not feedback_text:
            flash("Feedback cannot be empty.", "danger")
        else:
            q = "INSERT INTO feedback (user_id, feedback_text, created_at) VALUES ('%s', '%s', NOW())" % (user_id, feedback_text)
            insert(q)
            flash("Feedback submitted successfully.", "success")
            return redirect(url_for('user.feedback'))

    # Fetch feedback from other users to display on the page
    q = """
        SELECT u.fname, u.lname, f.feedback_text, f.created_at 
        FROM feedback f 
        JOIN user u ON f.user_id = u.user_id 
        ORDER BY f.created_at DESC
    """
    data['feedbacks'] = select(q)

    return render_template('feedback.html', data=data)

@user.route('/view_feedback')
def view_feedback():
    data = {}
    q = """
        SELECT u.fname, u.lname, f.feedback_text, f.created_at 
        FROM feedback f 
        JOIN user u ON f.user_id = u.user_id 
        ORDER BY f.created_at DESC
    """
    data['feedbacks'] = select(q)
    return render_template('view_feedback.html', data=data)



