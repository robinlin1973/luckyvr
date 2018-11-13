# coding: utf-8
from functools import wraps
from flask import Flask, render_template,url_for,redirect,request,flash,session,jsonify,make_response
from flask_mail import Mail,Message
import json
import stripe
import os
import pprint
from support import ContactForm,CreditForm,SigninForm, SignupForm,User,BookForm
from flask_bootstrap import Bootstrap
from warrant import Cognito
import cognitojwt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime
import peewee

# use the stripe keys to handle the payment
stripe_keys = {
  'secret_key': os.getenv('SECRET_KEY'),
  'publishable_key': os.getenv('PUBLISHABLE_KEY')
}
pem = os.getenv('PEM')    #todo add to production envrionment path
stripe.api_key = stripe_keys['secret_key']
application = Flask(__name__, template_folder="templates")
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'sign'
application.secret_key = os.getenv('APP_SECRET_KEY') #todo add to production envrionment path

# cognito_userpool_id = os.getenv('COGNITO_USERPOOL_ID')#todo add to production envrionment path
# cognito_userpool_region = os.getenv('COGNITO_USERPOOL_REGION')#todo add to production envrionment path
# cognito_client_id = os.getenv('COGNITO_CLIENT_ID') #todo add to production envrionment path
mail_password = os.environ.get('MAIL_PASSWORD') #todo add to production envrionment path

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'abinlaa@gmail.com',
    "MAIL_PASSWORD": mail_password
}

application.config.update(mail_settings)
mail = Mail(application)
bootstrap = Bootstrap(application)


db = peewee.MySQLDatabase("luckyvr", host="aag9gabvtjs2x6.ccc5n71qqwsa.us-east-2.rds.amazonaws.com", port=3306, user="abinla", passwd="itc98004")


class ContactModel(peewee.Model):
    name = peewee.CharField(default="")
    email = peewee.CharField(default="")
    size = peewee.CharField(default="")
    type = peewee.CharField(default="")
    promotion_code = peewee.CharField(default="")
    extra = peewee.CharField(default="")
    timestamp = peewee.DateTimeField(default=datetime.now)

    class Meta:
        database = db

ContactModel.create_table()

@login_manager.user_loader
def user_loader(session_token):
    """Populate user object, check expiry"""
    if "expires" not in session:
        return None

    expires = datetime.utcfromtimestamp(session['expires'])
    expires_seconds = (expires - datetime.utcnow()).total_seconds()
    if expires_seconds < 0:
        return None

    user = User()
    user.id = session_token
    if 'credit' in session:
         user.credit = session['credit']
    else:
        user.credit = '0'

    return user


# route to show index/home page
@application.route('/index')
@application.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@application.route("/contact", methods=['POST'])
def contact():
    try:
        data = request.form
        item = ContactModel(name=data['name'],email=data['email'],size=data['size'],type=data['type'],
                            promotion_code=data['promotion_code'],extra=data['extra'])
        item.save()
        with application.app_context():
            msg = Message(subject="Quotation Received from {}".format(data['name']),
                          sender=application.config.get("MAIL_USERNAME"),
                          recipients=["jielin88@hotmail.com",data['email']],  # replace with your email for testing
                          body=json.dumps(data))
            mail.send(msg)

        result = "OK" if item else "ERROR"
    except Exception as e:
        result = "Exception"
        print(e)
    finally:
        data = {"result":result}
        status_code = 200 if result == 'OK' else 500
        response = application.response_class(
            response=json.dumps(data),
            status=status_code,
            mimetype='application/json'
        )
        return response


@application.route("/map")
def map():
    place_id = request.args.get('place_id','ChIJJdxLbfBHDW0Rh5OtgMO10QI')
    lat = request.args.get('lat',-36.8942359)
    lng = request.args.get('lng',174.7819203)

    location = {
        "place_id":place_id,
        "lat":lat,
        "lng":lng
    }
    return render_template("map.html",location = location)

if __name__ == "__main__":
    # application.run(host="192.168.20.8",debug=True)
    application.run(host="192.168.20.8",debug=True,ssl_context='adhoc')