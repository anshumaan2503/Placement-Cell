from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime
from bson import ObjectId
import sys

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# MongoDB connection with error handling
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client['studetsdb']  # Existing database
    placed_students_collection = db['Placed']  # Existing collection
    print("✅ MongoDB connected successfully!")
    print(f"📊 Using database: {db.name}")
    print(f"👥 Using collection: {placed_students_collection.name}")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("Please make sure MongoDB is running on localhost:27017")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error connecting to MongoDB: {e}")
    sys.exit(1)

def is_admin_logged_in():
    return session.get('admin_logged_in', False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '123':
            session['admin_logged_in'] = True
            flash('Successfully logged in as admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    return render_template('admin_login.html')

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Successfully logged out!', 'success')
    return redirect(url_for('index'))

@app.route('/admin-dashboard')
def admin_dashboard():
    if not is_admin_logged_in():
        flash('Please login as admin first!', 'error')
        return redirect(url_for('admin_login'))
    try:
        students = list(placed_students_collection.find().sort('placement_date', -1))
        return render_template('admin_dashboard.html', students=students)
    except Exception as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('admin_dashboard.html', students=[])

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if not is_admin_logged_in():
        flash('Please login as admin first!', 'error')
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        name = request.form.get('name')
        roll_number = request.form.get('roll_number')
        company = request.form.get('company')
        package = request.form.get('package')
        year = request.form.get('year')
        branch = request.form.get('branch')

        if not all([name, roll_number, company, package, year, branch]):
            flash('All fields are required!', 'error')
            return render_template('add_student.html')

        try:
            package = float(package)
            year = int(year)
        except ValueError:
            flash('Invalid package or year value!', 'error')
            return render_template('add_student.html')

        try:
            existing_student = placed_students_collection.find_one({'student_id': roll_number})
            if existing_student:
                flash('Roll number already exists!', 'error')
                return render_template('add_student.html')

            student_data = {
                'student_id': roll_number,
                'name': name,
                'course': branch,          # MCA/BCA
                'batch': year,             # Year
                'company': company,
                'package_lpa': package,    # LPA
                'placement_date': datetime.now().strftime('%Y-%m-%d'),
                'email': f"{name.lower().replace(' ', '.')}@example.com",
                'phone': '+91-9876543210'
            }

            placed_students_collection.insert_one(student_data)
            flash('Student added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f'Error adding student: {str(e)}', 'error')

    return render_template('add_student.html')

@app.route('/delete-student/<student_id>')
def delete_student(student_id):
    if not is_admin_logged_in():
        flash('Please login as admin first!', 'error')
        return redirect(url_for('admin_login'))

    try:
        result = placed_students_collection.delete_one({'_id': ObjectId(student_id)})
        if result.deleted_count > 0:
            flash('Student deleted successfully!', 'success')
        else:
            flash('Student not found!', 'error')
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'error')

    return redirect(url_for('admin_dashboard'))

@app.route('/placed-students')
def placed_students():
    try:
        students = list(placed_students_collection.find().sort([('batch', -1), ('package_lpa', -1)]))
        return render_template('placed_students.html', students=students)
    except Exception as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('placed_students.html', students=[])

@app.route('/academic-programs')
def academic_programs():
    return render_template('academic_programs.html')

@app.route('/alumni')
def alumni():
    return render_template('alumni.html')

if __name__ == '__main__':
    print("🚀 Starting Placement Cell Application...")
    print("📊 MongoDB Database: studetsdb")
    print("👥 Collection: Placed")
    print("🌐 Server will start at: http://localhost:5000")
    app.run(debug=True)