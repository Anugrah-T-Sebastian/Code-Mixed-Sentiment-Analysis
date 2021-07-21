from flask import Flask, render_template, request
from Sentiment.plotlyCode import getChart
from Sentiment import app
from flask import render_template, redirect, url_for, flash, request, Flask
from Sentiment.models import Item, User 
from Sentiment.forms import RegisterForm, LoginForm, StatementInputForm, AddItemform, ExtractSentimentForm, EditItemForm, EditButtonForm, RemoveButtonForm
from Sentiment import db
from flask_login import login_user, logout_user, login_required, current_user
from Sentiment.ml_model import run


@app.route('/')
@app.route('/home')                 
def home_page():
    return render_template('home.html')        


@app.route('/sentiment', methods=['GET', 'POST'])
@login_required                          
def sentiment_page():
    extract_sentiment_form = ExtractSentimentForm()
    edit_item_form = EditButtonForm()
    remove_item_form = RemoveButtonForm()

    if request.method == "POST":
        #Show Dashboard 
        selected_item = request.form.get('selected_item')
        if selected_item:
            return render_template('chartsajax.html', name=selected_item)

        #Edit Item
        e_item = request.form.get('ed_item')
        if e_item:
            Item.query.filter_by(id=e_item).delete()
            db.session.commit()
            return redirect(url_for('edit_item_page'))

        #Remove Item
        rmv_item = request.form.get('rm_item')
        if rmv_item:
            Item.query.filter_by(id=rmv_item).delete()
            db.session.commit()
            flash("Item removed successfully!", category='success')
            return redirect(url_for('sentiment_page'))

    if request.method == "GET":
        items = Item.query.all()
        return render_template('sentiment.html', items = items, extract_sentiment_form = extract_sentiment_form, edit_item_form=edit_item_form, remove_item_form=remove_item_form)
   

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as: {user_to_create.username}', category='success')
        return redirect(url_for('login_page'))
    
    if form.errors != {}:     
        for err_msg in form.errors.values():
            flash(f'There was an error with creating user: {err_msg}', category='danger')   
    return render_template('register.html', form = form)


@app.route('/login', methods=['GET', 'POST'])                 
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('sentiment_page'))
        else:
            flash('Username and Password do not match! Please try again', category='danger')
    return render_template('login.html', form=form)            #Handles requestes and directs them to HTML file


@app.route('/logout')                 
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/code', methods=['GET', 'POST'])
def code_page():
    form = StatementInputForm(request.form)
    if request.method == 'POST':
        name = form.input_string.data
        out = run(name)
        return render_template("code.html", form=form, out = out)
    return render_template('code.html', form=form, out = {})


@app.route('/add_item', methods=['GET', 'POST'])
def add_item_page():
    form = AddItemform(request.form)
    if request.method == "POST" and form.validate_on_submit():
        item = Item(name=form.name.data, company=form.company.data, description=form.description.data)
        db.session.add(item)
        db.session.commit()
        flash('Item added successfully!', category='success')
        return redirect(url_for('sentiment_page'))
    return render_template('new_item.html', form=form)


@app.route('/edit_item', methods=['GET', 'POST'])
def edit_item_page():
    form = EditItemForm(request.form)
    if request.method == "POST" and form.validate_on_submit(): 
        item = Item(name=form.name.data, company=form.company.data, description=form.description.data)   
        db.session.add(item)
        db.session.commit()
        flash('Item edited successfully!', category='success')
        return redirect(url_for('sentiment_page'))
    return render_template('edit_item.html', form=form)


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return getChart(int(request.args.get('days')),
                    int(request.args.get('hours')),
                    int(request.args.get('mins')),
                    request.args.get('freq'),
                    request.args.get('brand'));


