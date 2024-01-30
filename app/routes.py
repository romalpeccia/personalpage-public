from flask import render_template, redirect, flash, url_for, jsonify, request, Response
from app import app, db, DEBUG
from app.forms import FeedbackForm, DownloadForm, LoginForm, RegisterForm, ContactForm
from app.models import User, Feedback, Download
from flask_login import current_user, login_user, logout_user
from flask_mail import Mail, Message
from app import mail, stripe
import os
import json
from requests.auth import HTTPBasicAuth

POLYGNOME_DOWNLOAD_LINK = "https://drive.google.com/drive/folders/1JtaoFvAfogAsFCTQ0m7W9YS275ojEH8-?usp=sharing"
METROGNOME_DOWNLOAD_LINK = "https://drive.google.com/drive/folders/19DuQxUXG-cz_5Wk1kcUxee0uLOInGCvt?usp=sharing"
POLYGNOME_VERSION = 1.0
METROGNOME_VERSION = 1.0
MGNOME_TEST_PAYMENT_LINK = "****"
PGNOME_TEST_PAYMENT_LINK = "****"
MGNOME_PAYMENT_LINK = "****"
PGNOME_PAYMENT_LINK = "****"

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        msg = Message('', sender = form.email.data, recipients = ["software.romal.peccia@gmail.com"])
        msg.body = f"FROM: {form.email.data} BODY: {form.message.data}"
        mail.send(msg)
        flash(f'Email sent from {form.email.data}!')
        return render_template('index.html', title='Home', form = form)
    return render_template('index.html', title='Home', form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', subtitle="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thank you for registering')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/polygnome/feedback', methods=['GET', 'POST'])
def polygnome_feedback():
    if current_user.is_authenticated:
        form = FeedbackForm(_pluginName = "PolyGnome")
        if form.validate_on_submit():
            added_to_db = False
            try:
                feedback = Feedback(user = current_user, pluginName = form.pluginName, daw = form.daw.data, answer1 = form.question1.data, answer2 = form.question2.data, answer3 = form.question3.data, answer4 = form.question4.data)
                db.session.add(feedback)
                db.session.commit()
                added_to_db = True
            except Exception as e:
                print(e)
            if (added_to_db):
                flash('Submitted feedback by user {}'.format(current_user.email))
        savedFeedback = Feedback.query.filter_by(user_id = current_user.id, pluginName = form.pluginName)
        return render_template('/polygnome/feedback.html', title='PolyGnome', subtitle = 'Feedback', form = form, savedFeedback = savedFeedback)
    else:
        return render_template('/unauth.html', subtitle='Log in')

@app.route('/polygnome/instructions')
def polygnome_instructions():
    return render_template('/polygnome/instructions.html', title='PolyGnome', subtitle = 'Instructions')

@app.route('/polygnome/download', methods=['GET', 'POST'])
def polygnome_download():
    
    if not current_user.is_authenticated:
        return render_template('/unauth.html', subtitle='Log in')
    else:
        form = DownloadForm(_pluginName = "PolyGnome")
        userDownload = Download.query.filter_by(user_id = current_user.id, pluginName = "PolyGnome").first()
        if userDownload is None and form.validate_on_submit():
            added_to_db = False
            try:
                download = Download(user = current_user, pluginName = form.pluginName, updateSignup = form.updateSignup.data, version=POLYGNOME_VERSION)
                db.session.add(download)
                db.session.commit()
                added_to_db = True
            except Exception as e:
                print(e)
            if (added_to_db):
                msg = Message('Your PolyGnome Download link', sender = 'downloads.romal.peccia@gmail.com', recipients = [current_user.email])
                msg.body = POLYGNOME_DOWNLOAD_LINK
                mail.send(msg)
                flash('Download successful for user {}. Please check your email'.format(current_user.email))
                return render_template('/polygnome/download.html', title= "PolyGnome", subtitle = "Download"  ,form = form, link = POLYGNOME_DOWNLOAD_LINK, download = download)
        else:
            return render_template('/polygnome/download.html', title= "PolyGnome", subtitle = "Download"  ,form = form, link = POLYGNOME_DOWNLOAD_LINK, download = userDownload)

        

@app.route('/polygnome/presets', methods=['GET'])
def polygnome_presets():
    return render_template('/polygnome/presets.html', title= "PolyGnome", subtitle = "Presets" )


@app.route('/metrognome/feedback', methods=['GET', 'POST'])
def metrognome_feedback():
    if current_user.is_authenticated:
        form = FeedbackForm(_pluginName = "MetroGnome")
        if form.validate_on_submit():
            added_to_db = False
            try:
                feedback = Feedback(user = current_user, pluginName = form.pluginName, daw = form.daw.data, answer1 = form.question1.data, answer2 = form.question2.data, answer3 = form.question3.data, answer4 = form.question4.data)
                db.session.add(feedback)
                db.session.commit()
                added_to_db = True
            except Exception as e:
                print(e)
            if (added_to_db):
                flash('Submitted feedback by user {}'.format(current_user.email))
        savedFeedback = Feedback.query.filter_by(user_id = current_user.id, pluginName = form.pluginName)
        return render_template('/metrognome/feedback.html', title='MetroGnome', subtitle = 'Feedback', form = form, savedFeedback = savedFeedback)
    else:
        return render_template('/unauth.html', subtitle='Log in')

@app.route('/metrognome/instructions')
def metrognome_instructions():
    return render_template('/metrognome/instructions.html', title='MetroGnome', subtitle = 'Instructions')

@app.route('/metrognome/download', methods=['GET', 'POST'])
def metrognome_download():
    
    if not current_user.is_authenticated:
        return render_template('/unauth.html', subtitle='Log in')
    else:
        form = DownloadForm(_pluginName = "MetroGnome")
        userDownload = Download.query.filter_by(user_id = current_user.id, pluginName = "MetroGnome").first()
        if userDownload is None and form.validate_on_submit():
            added_to_db = False
            try:
                download = Download(user = current_user, pluginName = form.pluginName, updateSignup = form.updateSignup.data, version=METROGNOME_VERSION)
                db.session.add(download)
                db.session.commit()
                added_to_db = True
            except Exception as e:
                print(e)
            if (added_to_db):
                msg = Message('Your MetroGnome Download link', sender = 'downloads.romal.peccia@gmail.com', recipients = [current_user.email])
                msg.body = METROGNOME_DOWNLOAD_LINK
                mail.send(msg)
                flash('Download successful for user {}. Please check your email'.format(current_user.email))
                return render_template('/metrognome/download.html', title= "MetroGnome", subtitle = "Download"  ,form = form, link = METROGNOME_DOWNLOAD_LINK, download = download)
        else:
            return render_template('/metrognome/download.html', title= "MetroGnome", subtitle = "Download"  ,form = form, link = METROGNOME_DOWNLOAD_LINK, download = userDownload)

@app.route('/mydownloads', methods=['GET'])
def myDownloads():
    if current_user.is_authenticated:
        #allPayments = stripe.PaymentIntent.list()
        mgnome_total = 0
        pgnome_total = 0
        sessions = stripe.checkout.Session.list()
        for session in sessions:
            if session.customer_email == current_user.email and session.payment_status == "paid":
                
                print(session)
                print("*************************************************************************************\n")

                if (session.payment_link == MGNOME_TEST_PAYMENT_LINK or session.payment_link == MGNOME_PAYMENT_LINK ):
                    mgnome_total = mgnome_total + float((session.amount_total))/100
                elif (session.payment_link == PGNOME_TEST_PAYMENT_LINK or session.payment_link == PGNOME_PAYMENT_LINK ):
                    pgnome_total = pgnome_total + float((session.amount_total))/100
                
        downloads = Download.query.filter_by(user_id = current_user.id)
        for download in downloads:
            print(download)
        return render_template('/mydownloads.html', subtitle='My Downloads', downloads = downloads, mgnome_total = format(mgnome_total, ".2f"), pgnome_total = format(pgnome_total, ".2f")  )
    else:
        return render_template('/unauth.html', subtitle='Log in')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404       
