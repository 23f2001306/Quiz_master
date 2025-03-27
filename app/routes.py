from flask import render_template,flash,redirect,url_for,session,request,render_template_string,jsonify
from app import app,db
from app.forms import LoginForm, SignupForm, SubForm,CreateSubForm
from app.forms import CreateChapForm,ChapForm
from app.forms import CreateQuizForm,QuizForm,SelectQuizForm
from app.forms import AddQtnForm,AttendQuizForm
from app.models import User,Admin,Subject,Chapter,Quiz,Question,Score
from datetime import datetime,time
import math

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

        if admin:
            if admin.password == password:
                print("Login successful!")  # Debugging line
                session['username'] = username
                return redirect(url_for("admin_dashboard"))
            else:
                flash("Incorrect Password","danger")
        elif user: 
            if user.password == password:
                print("Login successful!")  # Debugging line
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect Password","danger")
        else:
            flash("User does not exist","danger")
            

    else:
        print(f"Form validation failed. Errors: {form.errors}")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear() 
    return redirect(url_for("login")) 

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
            flash("Registration Successful","success")
            return render_template("signup.html", form=form, redirect=True)
    elif request.method == "POST":
        flash("Passwords must match","danger")
    return render_template("signup.html",form = form,redirect=False)

@app.route("/admin_dashboard")
def admin_dashboard():
    username = session.get('username')
    return render_template("admin_dashboard.html",username = username)

@app.route("/get_subjects",methods = ["GET"])
def get_subjects():
    subjects = Subject.query.all()
    subjects_data = [{"id":subject.sub_id,"subject_name": subject.sub_name} for subject in subjects]  
    return jsonify(subjects_data)

@app.route("/admin_dashboard/subjects",methods = ["GET","POST"])
def subjects():
    form1 = CreateSubForm()

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
    return render_template("subjects.html", form1 = form1)

@app.route("/admin_dashboard/edit_subject",methods = ["GET","POST"])
def edit_subject():
    subject_id = request.args.get("subject_id")
    subject = Subject.query.get(subject_id)
    form = SubForm(obj=subject)

    if request.method == "POST":
        print(request.form)
        if 'action' in request.form:
            action = request.form['action']
            
            if action == "edit" and form.validate_on_submit():
                subject.sub_name = form.sub_name.data
                subject.sub_description = form.sub_description.data
                db.session.commit()
                flash("Question Updated")

                return render_template_string("""
                    <html>
                        <head>
                            <script>
                                setTimeout(function() {
                                    if (window.opener) {
                                        window.opener.location.reload();
                                    }
                                    window.close(); 
                                }, 1000); 
                            </script>
                        </head>
                        <body>
                            <p>Subject updated. This window will close shortly...</p>
                        </body>
                    </html>
                """)
            elif action == "delete":
                db.session.delete(subject)
                db.session.commit()
                flash("Question deleted successfully!", "danger")

                return render_template_string("""
                    <html>
                        <head>
                            <script>
                                setTimeout(function() {
                                    if (window.opener) {
                                        window.opener.location.reload(); 
                                    }
                                    window.close(); 
                                }, 1000); 
                            </script>
                        </head>
                        <body>
                            <p>Subject deleted. This window will close shortly...</p>
                        </body>
                    </html>
                """)

    return render_template("edit_subjects.html",form=form)

@app.route("/get_chapters")
def get_chapters():
    chapters = Chapter.query.all()
    chapters_data = [{"id":chapter.chap_id,"chapter_name": chapter.chap_name} for chapter in chapters]  
    return jsonify(chapters_data)

@app.route("/admin_dashboard/chapters",methods = ["GET","POST"])
def chapters():
    form1 = CreateChapForm()
    form1.subject_id.choices = [(subject.sub_id,subject.sub_name) for subject in Subject.query.all()]
    if request.method == "POST":
        if form1.validate_on_submit():
            subject_id = form1.subject_id.data
            chap_name = form1.chap_name1.data
            chap_description = form1.chap_description1.data
            
            chapter = Chapter.query.filter_by(chap_name = chap_name).first()
            if chapter:
                flash("Chapter already exists","danger")
            else:
                new_chap = Chapter(sub_id = subject_id,chap_name = chap_name, chap_description = chap_description)
                db.session.add(new_chap)
                db.session.commit()
                flash("Chapter added","success")
                return redirect(url_for("chapters"))
    return render_template("chapters.html",form1 = form1)

@app.route("/admin_dashboard/edit_chapter",methods = ["GET","POST"])
def edit_chapter():
    chapter_id = request.args.get("chapter_id")
    chapter = Chapter.query.get(chapter_id)
    form = ChapForm(obj=chapter)

    if request.method == "POST":
        print(request.form)
        if 'action' in request.form:
            action = request.form['action']
            
            if action == "edit" and form.validate_on_submit():
                chapter.chap_name = form.chap_name.data
                chapter.chap_description = form.chap_description.data
                db.session.commit()
                flash("Question Updated")

                return render_template_string("""
                    <html>
                        <head>
                            <script>
                                setTimeout(function() {
                                    if (window.opener) {
                                        window.opener.location.reload();
                                    }
                                    window.close(); 
                                }, 1000); 
                            </script>
                        </head>
                        <body>
                            <p>Chapter updated. This window will close shortly...</p>
                        </body>
                    </html>
                """)
            elif action == "delete":
                db.session.delete(chapter)
                db.session.commit()
                flash("Question deleted successfully!", "danger")

                return render_template_string("""
                    <html>
                        <head>
                            <script>
                                setTimeout(function() {
                                    if (window.opener) {
                                        window.opener.location.reload(); 
                                    }
                                    window.close(); 
                                }, 1000); 
                            </script>
                        </head>
                        <body>
                            <p>Chapter deleted. This window will close shortly...</p>
                        </body>
                    </html>
                """)

    return render_template("edit_chapters.html",form=form)

@app.route("/get_quizzes")
def get_quizzes():
    quizzes = Quiz.query.all()
    quizzes_data = [{"id":quiz.quiz_id,"quiz_name": quiz.quiz_name} for quiz in quizzes]  
    return jsonify(quizzes_data)

@app.route("/admin_dashboard/quizzes",methods = ["GET","POST"])
def quizzes():
    form1 = CreateQuizForm()
    form1.chap_id1.choices = [(chapter.chap_id, chapter.chap_name) for chapter in Chapter.query.all()]

    if request.method == "POST":
        if form1.validate_on_submit():
            quiz_name = form1.quiz_name1.data
            
            quiz1 = Quiz.query.filter_by(quiz_name = quiz_name).first()
            if quiz1:
                flash("Quiz already exists","danger")
            else:
                new_quiz = Quiz(chapter_id = form1.chap_id1.data,quiz_name = form1.quiz_name1.data,
                                date_of_quiz = form1.date_of_quiz1.data,
                                time_duration = datetime.strptime(form1.time_duration1.data, "%H:%M:%S").time(),
                                remarks = form1.remarks1.data)
                db.session.add(new_quiz)
                db.session.commit()
                flash("Quiz added","success")
                return redirect(url_for("quizzes"))
    return render_template("quizzes.html",form1=form1)

@app.route("/admin_dashboard/edit_quiz",methods =["GET","POST"])
def edit_quiz():
    quiz_id = request.args.get("quiz_id")
    quiz = Quiz.query.get(quiz_id)
    time_duration = time.strftime(quiz.time_duration,"%H:%M:%S")
    form = QuizForm(quiz_name = quiz.quiz_name,date_of_quiz=quiz.date_of_quiz,time_duration = time_duration,remarks=quiz.remarks)

    if request.method == "POST":
        print(request.form)
        if 'action' in request.form:
            action = request.form['action']
            
            if action == "edit" and form.validate_on_submit():
                quiz.quiz_name = form.quiz_name.data
                quiz.date_of_quiz = form.date_of_quiz.data
                quiz.time_duration = datetime.strptime(form.time_duration.data, "%H:%M:%S").time()
                quiz.remarks = form.remarks.data
                db.session.commit()
                flash("Quiz Updated")

                return render_template_string("""
                    <html>
                        <head>
                            <script>
                                setTimeout(function() {
                                    if (window.opener) {
                                        window.opener.location.reload();
                                    }
                                    window.close(); 
                                }, 1000); 
                            </script>
                        </head>
                        <body>
                            <p>Quiz updated. This window will close shortly...</p>
                        </body>
                    </html>
                """)
            elif action == "delete":
                db.session.delete(quiz)
                db.session.commit()
                flash("Quiz deleted successfully!", "danger")

                return render_template_string("""
                    <html>
                        <head>
                            <script>
                                setTimeout(function() {
                                    if (window.opener) {
                                        window.opener.location.reload(); 
                                    }
                                    window.close(); 
                                }, 1000); 
                            </script>
                        </head>
                        <body>
                            <p>Quiz deleted. This window will close shortly...</p>
                        </body>
                    </html>
                """)
    return render_template("edit_quizzes.html",form=form)


@app.route("/admin_dashboard/Questions",methods = ["GET","POST"])
def qtns():
    quiz_id = None
    form1 = SelectQuizForm()
    form2 = AddQtnForm()
    form1.quiz_id.choices = [(quiz.quiz_id, quiz.quiz_name) for quiz in Quiz.query.all()]
    all_questions = None
    if session.get("quiz_id"):
        quiz_id = session.get("quiz_id")
        print(quiz_id)
        quiz =Quiz.query.get(quiz_id)
        if quiz:
            form1 = SelectQuizForm(quiz_id = quiz_id)
            form1.quiz_id.choices = [(quiz.quiz_id, quiz.quiz_name) for quiz in Quiz.query.all()]
            all_questions = quiz.questions
        
    if  request.method == "POST":
        if "select_quiz" in request.form and form1.validate_on_submit():
            session["quiz_id"] = form1.quiz_id.data
            quiz_id = form1.quiz_id.data
            quiz =Quiz.query.get(quiz_id)
            all_questions = quiz.questions
        if "add_question" in request.form and form2.validate_on_submit():
            quiz_id = session.get("quiz_id")
            new_qtn = Question(quiz_id = quiz_id,question_statement = form2.question_statement.data,
                               option1 = form2.option1.data,option2 = form2.option2.data,option3 = form2.option3.data,
                               option4 = form2.option4.data,correct_option = form2.correct_option.data )
            db.session.add(new_qtn)
            db.session.commit()
            flash("Question Added", "success")
            return redirect(url_for('qtns'))
    print(session.get("quiz_id"))   
    return render_template('questions.html',form1 = form1,form2 = form2,all_questions = all_questions,quiz_id = session.get("quiz_id"))

@app.route("/admin_dashboard/edit_qtn",methods = ["GET","POST"])
def update_qtn():
    form = AddQtnForm()
    qtn_id = request.args.get("qtn_id")
    question = Question.query.get(qtn_id)
    form = AddQtnForm(obj = question)

    if request.method == "POST":
        print(request.form)
        if 'action' in request.form:
            action = request.form['action']
            
            if action == "edit" and form.validate_on_submit():
                question.question_statement = form.question_statement.data
                question.option1 = form.option1.data
                question.option2 = form.option2.data
                question.option3 = form.option3.data
                question.option4 = form.option4.data
                question.correct_option = form.correct_option.data
                db.session.commit()
                flash("Question Updated")

                return render_template_string("""
                    <html>
                        <head>
                            <script>
                                setTimeout(function() {
                                    if (window.opener) {
                                        window.opener.location.reload();
                                    }
                                    window.close(); 
                                }, 1000); 
                            </script>
                        </head>
                        <body>
                            <p>Question updated. This window will close shortly...</p>
                        </body>
                    </html>
                """)
            elif action == "delete":
                db.session.delete(question)
                db.session.commit()
                flash("Question deleted successfully!", "danger")

                return render_template_string("""
                    <html>
                        <head>
                            <script>
                                setTimeout(function() {
                                    if (window.opener) {
                                        window.opener.location.reload(); 
                                    }
                                    window.close(); 
                                }, 1000); 
                            </script>
                        </head>
                        <body>
                            <p>Question deleted. This window will close shortly...</p>
                        </body>
                    </html>
                """)

    return render_template("edit_qtns.html",form = form)


@app.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [{"id":user.usr_id,"username": user.username} for user in users]  
    return jsonify(users_data)

@app.route('/admin_dashboard/view_user',methods = ["GET"])
def view_user():
    user_id = request.args.get("user_id")
    user = User.query.get(user_id)
    form = SignupForm(username=user.username,name=user.name,password=user.password,qualification=user.qualification,dob=user.dob)
    print(form.username.data)
    return render_template("view_user.html",form = form,user=user)

@app.route("/admin_dashboard/users")
def users():

    return render_template("users.html")

@app.route("/admin_dashboard/summary",methods = ["GET"])
def admin_summary():
    subject_top_scores = db.session.query(
        Subject.sub_name, 
        db.func.max(Score.total_scored).label("top_score")
    ).join(Chapter, Subject.sub_id == Chapter.sub_id
    ).join(Quiz, Chapter.chap_id == Quiz.chapter_id
    ).join(Score, Quiz.quiz_id == Score.quiz_id
    ).group_by(Subject.sub_name).all()
    print(subject_top_scores)
    subjects = [row[0] for row in subject_top_scores]
    scores = [row[1] for row in subject_top_scores]

    subject_attempts = db.session.query(
        Subject.sub_name,  # Subject name
        db.func.count(Score.id).label('attempts')  
    ).join(Chapter, Chapter.sub_id == Subject.sub_id  
    ).join(Quiz, Quiz.chapter_id == Chapter.chap_id 
    ).join(Score, Score.quiz_id == Quiz.quiz_id 
    ).group_by(Subject.sub_name).all()

    attempts = [row[1] for row in subject_attempts ]

    return render_template("admin_summary.html",subjects = subjects,scores = scores,attempts = attempts)

@app.route("/dashbboard")
def dashboard():
    username = session.get('username')
    quizzes = db.session.query(Quiz, db.func.count(Question.qtn_id).label("question_count")
            ).join(Question, Question.quiz_id == Quiz.quiz_id, isouter=True
            ).filter(Quiz.date_of_quiz >= db.func.current_date()
            ).group_by(Quiz.quiz_id
            ).having(db.func.count(Question.qtn_id) > 0 
            ).all()
    
    return render_template("main_quiz_page.html",username = username,quizzes = quizzes)

@app.route("/dashboard/viewquiz")
def view_quiz():
    quiz_id = request.args.get("quiz_id")
    quiz = db.session.query(
            Quiz, db.func.count(Question.qtn_id).label("question_count")
            ).join(Question, Question.quiz_id == Quiz.quiz_id, isouter=True
            ).filter(Quiz.quiz_id == quiz_id
            ).group_by(Quiz.quiz_id).first()
    quiz[0].time_duration = quiz[0].time_duration.strftime("%H:%M:%S")
    form = QuizForm(obj = quiz[0])
    return render_template("view_quiz.html",form = form,quiz = quiz)

@app.route("/dashboard/takequiz",methods = ["GET","POST"])
def take_quiz():
    quiz_id = request.args.get("quiz_id")
    session["timer"] = request.args.get("timer")
    quiz = Quiz.query.get(quiz_id)
    duration = quiz.time_duration.hour * 3600 + quiz.time_duration.minute * 60 + quiz.time_duration.second
    print(duration)
    questions = Question.query.filter_by(quiz_id = quiz_id).all()
    current_index = int(request.args.get("q", 0))
    print(current_index)
    if current_index >= len(questions):
        return redirect(url_for("dashboard"))
    current_question = questions[current_index]

    form = AttendQuizForm()
    
    if "quiz_answers" not in session:
        session["quiz_answers"] = {}

    saved_answer = session["quiz_answers"].get(str(current_question.qtn_id))

    form = AttendQuizForm(answer = saved_answer)
    form.answer.choices = [('1',current_question.option1),('2',current_question.option2),
                           ('3',current_question.option3),('4',current_question.option4)]

    if request.method == 'POST':
        print(request.form)
        session.setdefault("quiz_answers", {})  # Ensure dictionary exists
        session["quiz_answers"][str(current_question.qtn_id)] = form.answer.data
        session.modified = True

        if "jump-btn" in request.form:
            current_index = int(request.form["jump-btn"])
        elif 'prev-btn' in request.form  and current_index >= 1:
                current_index -= 1
        elif 'next-btn' in request.form and current_index < len(questions):
                current_index += 1
        elif "submit-btn" in request.form:
            correct_answers = 0
            total_questions = len(questions)
            result_data = []

            for question in questions:
                options = [question.option1,question.option2,question.option3,question.option4]
                if session["quiz_answers"].get(str(question.qtn_id)):
                    user_answer = options[int(session["quiz_answers"].get(str(question.qtn_id)))-1]
                else:
                    user_answer = None
                correct_answer = options[question.correct_option-1]
                result_data.append({
                    "question": question.question_statement,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer
                })

                if user_answer:
                    if user_answer == correct_answer:
                        correct_answers += 1
            print(correct_answers, "/", total_questions)
            user_id = User.query.filter_by(username=session.get("username")).with_entities(User.usr_id).first()[0]
            submission_time = datetime.now()
            raw_score = (correct_answers / total_questions) * 100
            final_score = math.ceil(raw_score) if (raw_score - int(raw_score)) > 0.5 else math.floor(raw_score)
            new_score = Score(user_id=user_id, quiz_id=quiz_id, time_stamp_of_attempt=submission_time, total_scored=final_score)
            db.session.add(new_score)
            db.session.commit()

            if "quiz_answers" in session:
                session.pop("quiz_answers")

            return render_template_string("""
                <html>
                    <head>
                    </head>
                    <body>
                        <h3>Quiz Submitted</h3>
                        <p>Your results are as follows:</p>
                        <table border="1" cellpadding="5">
                            <thead>
                                <tr>
                                    <th>Question</th>
                                    <th>Your Answer</th>
                                    <th>Correct Answer</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for result in result_data %}
                                <tr>
                                    <td>{{ result.question }}</td>
                                    <td>{{ result.user_answer if result.user_answer else 'No answer' }}</td>
                                    <td>{{ result.correct_answer }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                        <p>You scored {{ correct_answers }} out of {{ total_questions }}.</p>
                    </body>
                </html>
            """, result_data=result_data, correct_answers=correct_answers, total_questions=total_questions)

        return redirect(url_for('take_quiz', quiz_id=quiz_id, q=current_index,timer = session.get("timer")))

    return render_template("quiz_qtn.html",form = form,current_question = current_question,quiz = quiz,total = len(questions),current_index=current_index + 1,delta = duration,timer = session.get("timer"))


@app.route("/clear_quiz_session", methods=["POST"])
def clear_quiz_session():
    if "quiz_answers" in session:
        session.pop("quiz_answers")  
    return "", 204 

@app.route("/get_scores")
def get_scores():
    user_id = request.args.get("user_id")

    if user_id:
        scores = Score.query.filter(Score.user_id == user_id).all()
    else:
        scores = Score.query.all()

    scores_data = [{"quiz_name":score.quiz.quiz_name,"total_scored": score.total_scored,"timestamp":score.time_stamp_of_attempt} for score in scores]

    return jsonify(scores_data)

@app.route("/dashboard/scores", methods=["GET","POST"])
def scores():
    user_id = User.query.filter_by(username=session["username"]).with_entities(User.usr_id).first()[0]

    user = User.query.get(user_id)
    
    return render_template("scores.html",user_scores = user.scores,user_id = user_id,username = session.get("username"))

@app.route("/dashboard/summary",methods = ["GET"])
def user_summary():
    user_id = User.query.filter_by(username=session["username"]).with_entities(User.usr_id).first()[0]
    subject_attempts = db.session.query(Subject.sub_name, db.func.count(Score.quiz_id)
                        ).join(Chapter, Subject.sub_id == Chapter.sub_id
                        ).join(Quiz, Quiz.chapter_id == Chapter.chap_id
                        ).join(Score, Score.quiz_id == Quiz.quiz_id
                        ).filter(Score.user_id == user_id
                        ).group_by(Subject.sub_name).all()

    subjects = [row[0] for row in subject_attempts]
    print(subject_attempts)
    quiz_counts = [row[1] for row in subject_attempts]

    monthly_attempts = db.session.query(
        db.func.extract('month', Score.time_stamp_of_attempt).label("month"), 
        db.func.count(Score.quiz_id)
    ).filter(Score.user_id == user_id
    ).group_by("month"
    ).order_by("month"
    ).all()

    print(monthly_attempts)
    months = [row[0] for row in monthly_attempts]
    attempts = [row[1] for row in monthly_attempts]


    return render_template("user_summary.html", subjects=subjects, quiz_counts=quiz_counts,months = months,attempts = attempts,username = session.get("username"))