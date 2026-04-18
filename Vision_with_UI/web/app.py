from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/course')
def course():
    students = Student.query.all()
    return render_template('course.html', students=students)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    student = Student(name=name, email=email)
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('course'))

if __name__ == '__main__':
    app.run(debug=True)