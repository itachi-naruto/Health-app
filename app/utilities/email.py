from flask_cors import CORS, cross_origin
from flask import Blueprint, request, jsonify, abort, make_response, render_template

from app.security import roles, mail
from app.security.mail import send_email

mails = Blueprint('mails', __name__)

@mails.route('/', methods=['POST'])
@cross_origin()
@roles.token_required
def send_email_template(self):
    print(request.json)
    if not request.json or not 'subject' in request.json:
        abort(404)

    data = request.json
    
    html = render_template('email.html', message=data['message'])
    subject = data['subject']
    send_email(data['email'], subject, html)

    return jsonify({'status': None})