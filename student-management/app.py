from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from config import Config
from models import db, Student
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Auto-create tables
with app.app_context():
    db.create_all()

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/')
def index():
    total_students = Student.query.count()
    return render_template('index.html', total=total_students)

@app.route('/students')
def view_students():
    search = request.args.get('search', '')
    if search:
        # Search by name or roll number
        students = Student.query.filter(
            (Student.name.ilike(f'%{search}%')) | 
            (Student.roll_no.ilike(f'%{search}%'))
        ).all()
    else:
        students = Student.query.all()
    return render_template('students.html', students=students, search=search)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            admission_date = datetime.strptime(request.form['admission_date'], '%Y-%m-%d').date()
            new_student = Student(
                name=request.form['name'],
                roll_no=request.form['roll_no'],
                email=request.form['email'],
                phone=request.form['phone'],
                course=request.form['course'],
                year=request.form['year'],
                admission_date=admission_date
            )
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully!', 'success')
            return redirect(url_for('view_students'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: A student with this Roll Number already exists.', 'danger')
        except ValueError:
            flash('Invalid date format.', 'danger')
            
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        try:
            student.name = request.form['name']
            student.roll_no = request.form['roll_no']
            student.email = request.form['email']
            student.phone = request.form['phone']
            student.course = request.form['course']
            student.year = request.form['year']
            student.admission_date = datetime.strptime(request.form['admission_date'], '%Y-%m-%d').date()
            
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('view_students'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: Roll Number already exists.', 'danger')
            
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('view_students'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'])