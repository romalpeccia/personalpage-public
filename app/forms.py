from flask_wtf import FlaskForm
from wtforms import Label, DecimalField, HiddenField, StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class FeedbackForm(FlaskForm):
    daw = StringField('Which DAW do you use? (please include edition/version #)', validators=[DataRequired()])
    q4Text = f'Do you have any other comments to add?'
    question1 = TextAreaField()
    question2 = TextAreaField()
    question3 = TextAreaField()
    question4 = TextAreaField(q4Text)
    submit = SubmitField('Submit Feedback')

    def __init__(self, _pluginName):
        super().__init__()
        self.q1Text = f'What issues did you have with {_pluginName}?'
        self['question1'].label = Label(self['question1'].id, self.q1Text)
        self.q2Text = f'What did you like about {_pluginName}?'
        self['question2'].label = Label(self['question2'].id, self.q2Text)
        self.q3Text = f'What features would you like added to {_pluginName}?'
        self['question3'].label = Label(self['question2'].id, self.q3Text)
        self.pluginName = _pluginName




class DownloadForm(FlaskForm):
    updateSignup = BooleanField()
    #donationBool = BooleanField('Add a Donation', render_kw={"onclick": "dontationBoolOnClick()", "checked":"" })
    submit = SubmitField() #SubmitField(render_kw={"style":"display:none", "onclick": "submitOnClick()"})
    
    #paymentAmount = DecimalField('Pay what you can', validators=[GreaterThanZero] )
    
    def __init__(self, _pluginName):
        super().__init__()
        self['updateSignup'].label = Label(self['updateSignup'].id, f'Email me if {_pluginName} has major updates')
        self['submit'].label = Label(self['submit'].id, f'Unlock {_pluginName} for free')
        self.pluginName = _pluginName
    def GreaterThanZero(form, field):
        if field.data < 0:
            raise ValidationError('Value must be 0 or greater')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is taken. Please use a different email address.')


class ContactForm(FlaskForm):
  #name = StringField("Name", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired(), Email()])
  #subject = StringField("Subject", validators=[DataRequired()])
  message = TextAreaField("Message", validators=[DataRequired()])
  submit = SubmitField("Send") 