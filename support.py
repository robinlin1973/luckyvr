from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,HiddenField,TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, Length
import flask_login
import datetime
from datetime import timedelta
from wtforms.validators import ValidationError

class TimeCondition:
    def __init__(self, date: 'datetime.date or DateField'):
        self.date = date

    @staticmethod
    def date_from_field(datefield, form):
        """Set self.date to a `datetime.date` object if it currently is a `DateField`"""
        try:
            date = form[datefield].data
        except KeyError:
            raise ValidationError(f'Invalid field name {datefield}')

        if not isinstance(date, datetime.date):
            raise TypeError('Not a DateField')

        return date

    def check_date(self, form):
        if not isinstance(self.date, datetime.date):
            self.date = self.date_from_field(self.date, form)

class After(TimeCondition):
    def __init__(self, date, message=None):
        super().__init__(date)
        if not message:
            message = f'The chosen date must be after the {date}'
        self.message = message

    def __call__(self, form, field):
        self.check_date(form)
        if field.data < self.date:
            raise ValidationError(self.message)

class ContactForm(FlaskForm):
    name = StringField("Contact")
    email = StringField("Email")
    phone = StringField("Phone")
    size = SelectField('Size of Space', choices=[('150 sq.m. or less ', '150 sq.m. or less'),
                                                 ('250 sq.m. or less ', '250 sq.m. or less'),
                                                 ('350 sq.m. or less ', '350 sq.m. or less'),
                                                 ('> 350 sq.m.', '> 350 sq.m.')])
    type = SelectField('Property Type', choices=[('Single Family ','Single Family'),
                                                 ('Condo','Condo'),
                                                 ('Commercial','Commercial'),
                                                 ('Retail','Retail'),
                                                 ('Boat','Boat'),
                                                 ('Aircraft','Aircraft')])
    date = SelectField('Date Needed', choices=[('1-2 days ','1-2 days'),
                                               ('1-4 days','1-4 days'),
                                               ('1-7 days','1-7 days'),
                                               ('7-14 days','7-14 days'),
                                               ('no preference','no preference')])
    detail = TextAreaField('Detail')
    submit = SubmitField("Submit Request")


def from_date_validator(form, field):

    print("custom validator called")
    print(field)


class BookForm(FlaskForm):
    from_date = DateField('Check-in Date',
                          default=datetime.date.today(),
                          validators=[InputRequired(),],
                          format='%Y-%m-%d')

    to_date = DateField('Check-out Date',
                        default=datetime.date.today()+timedelta(days=1),
                        validators=[InputRequired(),],
                        format='%Y-%m-%d')#,


    adult_number = SelectField('Adult Guest', choices=[('1 adult', '1 adult'),
                                                 ('2 adults', '2 adults'),
                                                 ('3 adults', '3 adults'),
                                                 ('4 adults', '4 adults'),
                                                 ('5 adults', '5 adults'),
                                                 ('6 adults', '6 adults'),
                                                 ('7 adults', '7 adults'),
                                                 ('8 adults', '8 adults')])
    child_number = SelectField('Child Guest', choices=[('0 child','0 child'),
                                                 ('1 child','1 child'),
                                                 ('2 children', '2 children'),
                                                 ('3 children', '3 children'),
                                                 ('4 children', '4 children'),
                                                 ('5 children', '5 children'),
                                                 ('6 children', '6 children'),
                                                 ('7 children', '7 children'),
                                                 ('8 children', '8 children')])
    email = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])

    submit = SubmitField("Book Now!")



class CreditForm(FlaskForm):
    subscribe_amount = StringField("Topup Amount($NZD):")
    submit = SubmitField("Credit Account")


class SigninForm(FlaskForm):
    # formname = HiddenField()
    username = StringField('用户名', validators=[InputRequired(), Length(min=6, max=15)])
    password = PasswordField('密码', validators=[InputRequired(), Length(min=6, max=80)])
    # remember = BooleanField('remember me')

class SignupForm(FlaskForm):
    # formname = HiddenField()
    email = StringField('电子邮件地址', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('用户名', validators=[InputRequired(), Length(min=6, max=15)])
    password = PasswordField('密码', validators=[InputRequired(), Length(min=6, max=80)])
    agreement = BooleanField()

class User(flask_login.UserMixin):
    """Standard flask_login UserMixin"""
    pass




class Before(TimeCondition):
    def __init__(self, date, message=None):
        super().__init__(date)
        if not message:
            message = f'The chosen date must be before the {date}'
        self.message = message

    def __call__(self, form, field):
        self.check_date(form)
        if field.data > self.date:
            raise ValidationError(self.message)

