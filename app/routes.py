from flask import render_template,flash,redirect,url_for,session,request
from app import app,db
from app.forms import LoginForm, SignupForm, SubForm,SearchSubForm,CreateSubForm
from app.models import User,Admin,Subject

@app.route("/",methods = ["GET","POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # If the form is valid, let's see what's coming from it
        username = form.username.data
        password = form.password.data
        print(f"Form submitted! Username: {username}, Password: {password}")  # Debugging line

        user = User.query.filter_by(username=username).first()
        admin = Admin.query.filter_by(username = username).first()

        if admin and admin.password == password:
            print("Login successful!")  # Debugging line
            session['username'] = username
            return redirect(url_for("admin_dashboard"))

        elif user and user.password == password:
            print("Login successful!")  # Debugging line
            session['username'] = username
            return redirect(url_for('dashboard'))
            
        else:
            flash('Invalid credentials, please try again.', 'danger')
            print("Invalid credentials entered.")  # Debugging line
            return redirect(url_for('login'))

    # If form is not valid, log the errors
    else:
        print(f"Form validation failed. Errors: {form.errors}")  # Debugging line

    return render_template("login.html", form=form)


@app.route("/signup",methods = ["GET","POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        qualification = form.qualification.data
        dob = form.dob.data

        user = User.query.filter_by(username=username).first()
        admin = Admin.query.filter_by(username = username).first()
        if user or admin:
            flash("Username Taken, Choose another",'danger')
            return redirect(url_for("signup"))
        else:
            new_user = User(username = username,password = password, name = name ,qualification = qualification, dob = dob)
            db.session.add(new_user)
            db.session.commit()
    elif request.method == "POST":
        flash("Passwords must match","danger")
    return render_template("signup.html",form = form)

@app.route("/admin_dashboard")
def admin_dashboard():
    username = session.get('username')
    return render_template("admin_dashboard.html",username = username)

@app.route("/admin_dashboard/subjects",methods = ["GET","POST"])
def subjects():
    form1 = CreateSubForm()
    form2 = SearchSubForm()
    form3 = SubForm()
    all_subjects = Subject.query.order_by(Subject.sub_id.desc()).limit(5).all()
    subject = None

    if request.method == "POST":
        if form1.validate_on_submit():
            sub_name = form1.sub_name1.data
            sub_description = form1.sub_description1.data
            
            sub = Subject.query.filter_by(sub_name = sub_name).first()
            if sub:
                flash("Subject already exists","danger")
            else:
                new_sub = Subject(sub_name = sub_name, sub_description = sub_description)
                db.session.add(new_sub)
                db.session.commit()
                flash("Subject added","success")
                return redirect(url_for("subjects"))
        else:
            pass
        if form2.validate_on_submit():
            search_term = form2.sub_name.data
            subject = Subject.query.filter(Subject.sub_name.ilike(f"%{search_term}%")).first()

            if not subject:
                flash("Subject not found","danger")
            else :
                form3 = SubForm(obj = subject)
        if subject and 'action' in request.form:
            action = request.form['action']
            print(f"Action: {action}, Subject: {subject}")

            if action == 'edit' and form3.validate_on_submit():
                # If the 'edit' button is clicked, update the subject
                subject.sub_name = form3.sub_name.data
                subject.sub_description = form3.sub_description.data
                print(form3.sub_description.data)
                db.session.commit()
                flash("Subject updated successfully!", "success")
                subject = None
            elif action == "delete":
                # If the 'delete' button is clicked, delete the subject
                db.session.delete(subject)
                db.session.commit()
                flash("Subject deleted successfully!", "danger")
                subject = None
            return redirect(url_for("subjects"))
    return render_template("subjects.html", form1 = form1,form2 = form2,
                           form3 = form3, subject = subject,all_subjects = all_subjects)

@app.route("/admin_dashboard/chapters",methods = ["GET","POST"])
def chapters():
    pass

@app.route("/dashbboard")
def dashboard():
    username = session.get('username')
    return render_template("dashboard.html",username = username)
