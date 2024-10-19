from flask import *
from database import *

staff = Blueprint('staff', __name__)

@staff.route('/staffhome')
def staffhome():
    return render_template('staffhome.html')

@staff.route('/staff_housekeeping_requests')
def staff_housekeeping_requests():
    # Query to get all housekeeping requests
    q = "SELECT id, user_id, room_id, service_type, request_details, status FROM housekeeping_requests WHERE status='pending'"
    requests = select(q)

    return render_template('staff_housekeeping_requests.html', requests=requests)

@staff.route('/accept_request/<int:request_id>', methods=['POST'])
def accept_request(request_id):
    # Update the request status to accepted
    q = "UPDATE housekeeping_requests SET status='accepted' WHERE id=%s"  # Use 'id' here as per your SQL structure
    updated(q, (request_id,))  # Use parameterized query

    flash("Request accepted successfully!")
    return redirect(url_for('staff.staff_housekeeping_requests'))

@staff.route('/reject_request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    # Update the request status to rejected
    q = "UPDATE housekeeping_requests SET status='rejected' WHERE id=%s"  # Use 'id' here as per your SQL structure
    updated(q, (request_id,))  # Use parameterized query

    flash("Request rejected successfully!")
    return redirect(url_for('staff.staff_housekeeping_requests'))
