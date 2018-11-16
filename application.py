# coding: utf-8
from flask import Flask, render_template, url_for, redirect, request, flash, session, jsonify, make_response
from flask_mail import Mail,Message
import os
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import json

# use the stripe keys to handle the payment
stripe_keys = {
    'secret_key': os.getenv('SECRET_KEY'),
    'publishable_key': os.getenv('PUBLISHABLE_KEY')
}
pem = os.getenv('PEM')  # todo add to production envrionment path
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
application = Flask(__name__, template_folder="templates")
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config[
    'SQLALCHEMY_DATABASE_URI'] = r'mysql+pymysql://{}:{}@aag9gabvtjs2x6.ccc5n71qqwsa.us-east-2.rds.amazonaws.com:3306/luckyvr'.format(db_username,db_password)
application.secret_key = os.getenv('APP_SECRET_KEY')
mail_password = os.environ.get('MAIL_PASSWORD')  # todo add to production envrionment path

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

# SQLAlchemy database solution
database = SQLAlchemy(application)
admin = Admin(application)


class Contact(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(30), nullable=False)
    email = database.Column(database.String(30))
    size = database.Column(database.String(30))
    type = database.Column(database.String(30))
    promotion_code = database.Column(database.String(30))
    extra = database.Column(database.String(200))
    timestamp = database.Column(database.DateTime, default=datetime.utcnow)

class Unsubscribe(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    mobile = database.Column(database.String(20),unique=True)
    created_date = database.Column(database.DateTime, default=datetime.utcnow)

class Scanned(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    pid = database.Column(database.String(30), nullable=False) #property id used in luckyvr.net/property/<id>
    lat = database.Column(database.Numeric(12,7), nullable=False)                 #property's latlng
    lng = database.Column(database.Numeric(12,7), nullable=False)                 #property's latlng
    mlink = database.Column(database.String(120),unique=True,nullable=False)    #matterport scan link
    address = database.Column(database.String(120),unique=True)    #property address
    listing_type = database.Column(database.String(20),default="res_sal")    #property type:residential&commertial&boat
    created_date = database.Column(database.DateTime, default=datetime.utcnow)


admin.add_view(ModelView(Unsubscribe, database.session))
admin.add_view(ModelView(Scanned, database.session))
admin.add_view(ModelView(Contact, database.session))


database.create_all()

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

# route to show index/home page
@application.route('/index')
@application.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

# route to show property directly
@application.route('/property/<id>')
def property(id):
    # redirect(url_for('index') + '#myModal')
    record = Scanned.query.filter_by(pid=id.lower()).first()
    if record.mlink:
        # mlink = 'https://my.matterport.com/show/?m=cpm1cEf5uuX'
        return render_template("property.html",mlink=record.mlink)
    else:
        return redirect(url_for('index'))

@application.route("/contact", methods=['POST'])
def contact():
    try:
        data = request.form
        # item = ContactModel(name=data['name'], email=data['email'], size=data['size'], type=data['type'],
        #                     promotion_code=data['promotion_code'], extra=data['extra'])
        item = Contact(name=data['name'], email=data['email'], size=data['size'], type=data['type'],
                            promotion_code=data['promotion_code'], extra=data['extra'])
        database.session.add(item)
        database.session.commit()
        with application.app_context():
            msg = Message(subject="Quotation Received from {}".format(data['name']),
                          sender=application.config.get("MAIL_USERNAME"),
                          recipients=["jielin88@hotmail.com", data['email']],  # replace with your email for testing
                          body=json.dumps(data))
            mail.send(msg)

        result = "OK" if item else "ERROR"
    except Exception as e:
        result = "Exception"
        print(e)
    finally:
        data = {"result": result}
        status_code = 200 if result == 'OK' else 500
        response = application.response_class(
            response=json.dumps(data),
            status=status_code,
            mimetype='application/json'
        )
        return response




@application.route('/scannedmap')
def scannedmap():
    query = Scanned.query.all()
    return render_template("scannedmap.html",data=json.dumps([ row2dict(row) for row in query ]))

if __name__ == "__main__":
    # application.run(host="192.168.20.8",debug=True)
    application.run(host="192.168.20.8", debug=True, ssl_context='adhoc')
