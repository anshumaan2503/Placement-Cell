
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, make_response
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime, timedelta
from bson import ObjectId
import sys
import csv
import io
from io import BytesIO
import xlsxwriter
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import secrets
import re
import smtplib
import ssl
from email.message import EmailMessage

app = Flask(__name__)
import os
app.secret_key = os.environ.get('SECRET_KEY', 'xmFKeIrNN2O6lEXXlPNizfAtpqLsCd0ytRAqhK0Kx94')  # Use environment variable in production

# Token serializer for secure links
serializer = URLSafeTimedSerializer(app.secret_key)

# Email configuration - Uses environment variables in production
EMAIL_CONFIG = {
    'smtp_server': os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.environ.get('SMTP_PORT', '587')),
    'email': os.environ.get('EMAIL_ADDRESS', 'attechno8@gmail.com'),
    'password': os.environ.get('EMAIL_PASSWORD', 'cdur zofb gwua wfur'),
    'sender_name': os.environ.get('SENDER_NAME', 'IGNTU Computer Science Placement Cell')
}

# 📧 EXAMPLE (replace with your actual details):
# EMAIL_CONFIG = {
#     'smtp_server': 'smtp.gmail.com',
#     'smtp_port': 587,
#     'email': 'placement.igntu@gmail.com',        # Your Gmail address
#     'password': 'abcd efgh ijkl mnop',           # Your App Password (16 characters)
#     'sender_name': 'IGNTU Placement Cell'
# }

# 📧 TO ENABLE REAL EMAIL SENDING:
# 1. Replace 'your-email@gmail.com' with your actual Gmail address
# 2. Replace 'your-app-password' with the 16-character App Password from Google
# 3. Restart the Flask app
# 4. Test by generating a student registration link

# MongoDB connection with error handling
try:
    # Use environment variable for MongoDB URI in production, fallback to localhost for development
    mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client['studetsdb']  # Existing database
    placed_students_collection = db['Placed']  # Existing collection
    student_tokens_collection = db['StudentTokens']  # New collection for tokens
    otp_collection = db['OTPVerification']  # New collection for OTP verification
    print("[OK] MongoDB connected successfully!")
    print(f"[INFO] Using database: {db.name}")
    print(f"[INFO] Using collections: {placed_students_collection.name}, {student_tokens_collection.name}, {otp_collection.name}")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print(f"[ERROR] MongoDB connection failed: {e}")
    print("Please make sure MongoDB is running or check MONGODB_URI environment variable")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Unexpected error connecting to MongoDB: {e}")
    sys.exit(1)

def is_admin_logged_in():
    return session.get('admin_logged_in', False)

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(secrets.randbelow(900000) + 100000)

def send_email(to_email, subject, body):
    """Send email with OTP and registration link"""
    try:
        # Check if email configuration is set up
        if EMAIL_CONFIG['email'] == 'your-email@gmail.com' or EMAIL_CONFIG['password'] == 'your-app-password':
            # Email not configured, print to console instead
            print(f"\n{'='*60}")
            print(f"⚠️  EMAIL NOT CONFIGURED - SHOWING OTP IN CONSOLE")
            print(f"{'='*60}")
            print(f"TO: {to_email}")
            print(f"SUBJECT: {subject}")
            print(f"{'='*60}")
            
            # Extract OTP from body for easy viewing
            import re
            otp_match = re.search(r'<div[^>]*>(\d{6})</div>', body)
            if otp_match:
                otp = otp_match.group(1)
                print(f"🔑 OTP CODE: {otp}")
                print(f"{'='*60}")
                print(f"📧 Configure email in app.py to send real emails")
                print(f"{'='*60}\n")
            
            return True
        
        # Create email message
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = f"{EMAIL_CONFIG['sender_name']} <{EMAIL_CONFIG['email']}>"
        msg['To'] = to_email
        msg.set_content(body, subtype='html')
        
        # Create secure SSL context
        context = ssl.create_default_context()
        
        # Send email
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls(context=context)
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        print(f"\n{'='*60}")
        print(f"📧 EMAIL FALLBACK - SHOWING OTP IN CONSOLE")
        print(f"{'='*60}")
        print(f"TO: {to_email}")
        print(f"SUBJECT: {subject}")
        
        # Extract OTP from body for easy viewing
        import re
        otp_match = re.search(r'<div[^>]*>(\d{6})</div>', body)
        if otp_match:
            otp = otp_match.group(1)
            print(f"🔑 OTP CODE: {otp}")
        
        print(f"{'='*60}\n")
        return True  # Return True so the process continues



def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None





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

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/export-csv')
def export_csv():
    # Allow public access to CSV export
    # if not is_admin_logged_in():
    #     flash('Please login as admin first!', 'error')
    #     return redirect(url_for('admin_login'))
    
    try:
        # Fetch all students from database
        students = list(placed_students_collection.find().sort([('batch', -1), ('package_lpa', -1)]))
        
        if not students:
            flash('No student data available to export!', 'error')
            return redirect(url_for('placed_students'))
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Name', 'Roll Number', 'Branch', 'Batch Year', 'Company', 
            'Package (LPA)', 'Placement Date', 'Email', 'Phone'
        ])
        
        # Write data rows
        for student in students:
            writer.writerow([
                student.get('name', ''),
                student.get('student_id', ''),
                student.get('course', ''),
                student.get('batch', ''),
                student.get('company', ''),
                student.get('package_lpa', 0),
                student.get('placement_date', ''),
                student.get('email', ''),
                student.get('phone', '')
            ])
        
        # Create response
        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename=placed_students_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return response
        
    except Exception as e:
        flash(f'Error exporting data: {str(e)}', 'error')
        return redirect(url_for('placed_students'))

@app.route('/export-excel')
def export_excel():
    # Allow public access to Excel export
    # if not is_admin_logged_in():
    #     flash('Please login as admin first!', 'error')
    #     return redirect(url_for('admin_login'))
    
    try:
        # Fetch all students from database
        students = list(placed_students_collection.find().sort([('batch', -1), ('package_lpa', -1)]))
        
        if not students:
            flash('No student data available to export!', 'error')
            return redirect(url_for('placed_students'))
        
        # Create Excel file in memory
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#283593',
            'font_color': 'white',
            'border': 1
        })
        
        data_format = workbook.add_format({
            'border': 1,
            'align': 'left'
        })
        
        number_format = workbook.add_format({
            'border': 1,
            'num_format': '0.0'
        })
        
        # Main data sheet
        worksheet1 = workbook.add_worksheet('Placed Students')
        
        # Write headers
        headers = ['Name', 'Roll Number', 'Branch', 'Batch Year', 'Company', 
                  'Package (LPA)', 'Placement Date', 'Email', 'Phone']
        
        for col, header in enumerate(headers):
            worksheet1.write(0, col, header, header_format)
        
        # Write data
        for row, student in enumerate(students, 1):
            worksheet1.write(row, 0, student.get('name', ''), data_format)
            worksheet1.write(row, 1, student.get('student_id', ''), data_format)
            worksheet1.write(row, 2, student.get('course', ''), data_format)
            worksheet1.write(row, 3, student.get('batch', ''), data_format)
            worksheet1.write(row, 4, student.get('company', ''), data_format)
            worksheet1.write(row, 5, student.get('package_lpa', 0), number_format)
            worksheet1.write(row, 6, student.get('placement_date', ''), data_format)
            worksheet1.write(row, 7, student.get('email', ''), data_format)
            worksheet1.write(row, 8, student.get('phone', ''), data_format)
        
        # Auto-adjust column widths
        worksheet1.set_column('A:A', 20)  # Name
        worksheet1.set_column('B:B', 15)  # Roll Number
        worksheet1.set_column('C:C', 10)  # Branch
        worksheet1.set_column('D:D', 12)  # Batch Year
        worksheet1.set_column('E:E', 25)  # Company
        worksheet1.set_column('F:F', 15)  # Package
        worksheet1.set_column('G:G', 15)  # Date
        worksheet1.set_column('H:H', 25)  # Email
        worksheet1.set_column('I:I', 15)  # Phone
        
        # Summary sheet
        worksheet2 = workbook.add_worksheet('Summary')
        
        # Calculate statistics
        packages = [s.get('package_lpa', 0) for s in students]
        companies = list(set([s.get('company', '') for s in students]))
        mca_count = len([s for s in students if s.get('course', '') == 'MCA'])
        bca_count = len([s for s in students if s.get('course', '') == 'BCA'])
        
        avg_package = sum(packages) / len(packages) if packages else 0
        max_package = max(packages) if packages else 0
        min_package = min(packages) if packages else 0
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Students', len(students)],
            ['Average Package (LPA)', round(avg_package, 2)],
            ['Highest Package (LPA)', max_package],
            ['Lowest Package (LPA)', min_package],
            ['Total Companies', len(companies)],
            ['MCA Students', mca_count],
            ['BCA Students', bca_count]
        ]
        
        for row, data in enumerate(summary_data):
            for col, value in enumerate(data):
                if row == 0:
                    worksheet2.write(row, col, value, header_format)
                else:
                    worksheet2.write(row, col, value, data_format)
        
        worksheet2.set_column('A:A', 25)
        worksheet2.set_column('B:B', 15)
        
        # Company Analysis sheet
        worksheet3 = workbook.add_worksheet('Company Analysis')
        
        # Calculate company statistics
        company_stats = {}
        for student in students:
            company = student.get('company', '')
            package = student.get('package_lpa', 0)
            
            if company not in company_stats:
                company_stats[company] = {'count': 0, 'packages': []}
            
            company_stats[company]['count'] += 1
            company_stats[company]['packages'].append(package)
        
        # Write company analysis headers
        company_headers = ['Company', 'Students Count', 'Avg Package', 'Max Package', 'Min Package']
        for col, header in enumerate(company_headers):
            worksheet3.write(0, col, header, header_format)
        
        # Write company data
        row = 1
        for company, stats in company_stats.items():
            packages = stats['packages']
            avg_pkg = sum(packages) / len(packages) if packages else 0
            max_pkg = max(packages) if packages else 0
            min_pkg = min(packages) if packages else 0
            
            worksheet3.write(row, 0, company, data_format)
            worksheet3.write(row, 1, stats['count'], data_format)
            worksheet3.write(row, 2, round(avg_pkg, 2), number_format)
            worksheet3.write(row, 3, max_pkg, number_format)
            worksheet3.write(row, 4, min_pkg, number_format)
            row += 1
        
        worksheet3.set_column('A:A', 25)
        worksheet3.set_column('B:E', 15)
        
        workbook.close()
        output.seek(0)
        
        # Create response
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = f'attachment; filename=placed_students_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        
        return response
        
    except Exception as e:
        flash(f'Error exporting data: {str(e)}', 'error')
        return redirect(url_for('placed_students'))

@app.route('/generate-student-link', methods=['GET', 'POST'])
def generate_student_link():
    if not is_admin_logged_in():
        flash('Please login as admin first!', 'error')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        contact_method = 'email'  # Only email supported now
        contact_value = request.form.get('contact_value', '').strip()
        
        if not all([student_name, contact_value]):
            flash('All fields are required!', 'error')
            return render_template('generate_student_link.html')
        
        # Validate email address
        if not is_valid_email(contact_value):
            flash('Please enter a valid email address!', 'error')
            return render_template('generate_student_link.html')
        
        try:
            # Generate secure token
            token_data = {
                'student_name': student_name,
                'contact_method': contact_method,
                'contact_value': contact_value,
                'timestamp': datetime.now().isoformat()
            }
            
            # Create token that expires in 5 minutes
            token = serializer.dumps(token_data)
            
            # Generate OTP
            otp = generate_otp()
            
            # Store token and OTP in database
            token_doc = {
                'token': token,
                'student_name': student_name,
                'contact_method': contact_method,
                'contact_value': contact_value,
                'otp': otp,
                'created_at': datetime.now(),
                'expires_at': datetime.now() + timedelta(minutes=5),
                'used': False
            }
            
            student_tokens_collection.insert_one(token_doc)
            
            # Generate registration link
            registration_link = url_for('student_self_register', token=token, _external=True)
            
            # Send OTP and link via email
            subject = "IGNTU Placement Cell - Student Registration Link"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #283593, #3949ab); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                        <h1 style="margin: 0; font-size: 24px;">🎓 IGNTU Placement Cell</h1>
                        <p style="margin: 10px 0 0 0; opacity: 0.9;">Student Registration Invitation</p>
                    </div>
                    
                    <div style="background: white; padding: 30px; border: 1px solid #e0e0e0; border-radius: 0 0 10px 10px;">
                        <h2 style="color: #283593; margin-top: 0;">Hello {student_name}!</h2>
                        
                        <p style="font-size: 16px; margin-bottom: 25px;">
                            You have been invited to register your placement details in the IGNTU Placement Cell database.
                        </p>
                        
                        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                            <h3 style="color: #283593; margin-top: 0;">Your OTP Code</h3>
                            <div style="font-size: 32px; font-weight: bold; color: #ffd600; background: #283593; padding: 15px; border-radius: 8px; letter-spacing: 3px;">
                                {otp}
                            </div>
                            <p style="margin: 10px 0 0 0; color: #666; font-size: 14px;">This OTP is valid for 5 minutes only</p>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <h3 style="color: #283593; margin-bottom: 15px;">📝 Click to Register</h3>
                            <a href="{registration_link}" 
                               style="background: linear-gradient(135deg, #ffd600, #ffed4e); 
                                      color: #283593; 
                                      padding: 15px 30px; 
                                      text-decoration: none; 
                                      border-radius: 25px; 
                                      font-weight: bold; 
                                      display: inline-block;
                                      box-shadow: 0 4px 12px rgba(255, 214, 0, 0.3);
                                      font-size: 16px;">
                                📝 Register Your Details
                            </a>
                        </div>
                        
                        <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 20px; border-radius: 8px; margin: 25px 0;">
                            <h4 style="color: #856404; margin-top: 0;">
                                ⚠️ Important Instructions:
                            </h4>
                            <ul style="color: #856404; margin: 10px 0 0 0; padding-left: 20px;">
                                <li style="margin-bottom: 8px;">This link will expire in <strong>5 minutes</strong></li>
                                <li style="margin-bottom: 8px;">Use the OTP code <strong>{otp}</strong> when prompted</li>
                                <li style="margin-bottom: 8px;">Fill in all your placement details accurately</li>
                                <li>Contact the placement cell if you face any issues</li>
                            </ul>
                        </div>
                        
                        <div style="border-top: 2px solid #e0e0e0; padding-top: 20px; margin-top: 30px;">
                            <p style="color: #666; font-size: 14px; margin: 0;">
                                <strong>Need help?</strong> Contact the IGNTU Placement Cell<br>
                                If you didn't expect this email, please ignore it.
                            </p>
                        </div>
                    </div>
                    
                    <div style="text-align: center; padding: 20px; color: #666; font-size: 12px;">
                        <p style="margin: 0;">© 2025 Department of Computer Science, IGNTU. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            if send_email(contact_value, subject, body):
                flash(f'Registration link and OTP sent successfully to {contact_value}!', 'success')
            else:
                flash('Failed to send email. Please check email configuration.', 'error')
            
            return redirect(url_for('admin_dashboard'))
            
        except Exception as e:
            flash(f'Error generating registration link: {str(e)}', 'error')
    
    return render_template('generate_student_link.html')

@app.route('/student-register/<token>', methods=['GET', 'POST'])
def student_self_register(token):
    try:
        # Verify token (5 minutes expiry)
        token_data = serializer.loads(token, max_age=300)  # 300 seconds = 5 minutes
    except SignatureExpired:
        flash('Registration link has expired. Please contact admin for a new link.', 'error')
        return render_template('registration_expired.html')
    except BadSignature:
        flash('Invalid registration link. Please contact admin.', 'error')
        return render_template('registration_expired.html')
    
    # Check if token exists in database and is not used
    token_doc = student_tokens_collection.find_one({
        'token': token,
        'used': False,
        'expires_at': {'$gt': datetime.now()}
    })
    
    if not token_doc:
        flash('Registration link has expired or already been used.', 'error')
        return render_template('registration_expired.html')
    
    if request.method == 'POST':
        # Verify OTP first
        entered_otp = request.form.get('otp', '').strip()
        if entered_otp != token_doc['otp']:
            flash('Invalid OTP. Please check and try again.', 'error')
            return render_template('student_self_register.html', 
                                 student_name=token_doc['student_name'],
                                 token=token)
        
        # Get form data
        roll_number = request.form.get('roll_number', '').strip()
        company = request.form.get('company', '').strip()
        package = request.form.get('package', '').strip()
        year = request.form.get('year', '').strip()
        branch = request.form.get('branch', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        
        if not all([roll_number, company, package, year, branch]):
            flash('All required fields must be filled!', 'error')
            return render_template('student_self_register.html', 
                                 student_name=token_doc['student_name'],
                                 token=token)
        
        try:
            package = float(package)
            year = int(year)
        except ValueError:
            flash('Invalid package or year value!', 'error')
            return render_template('student_self_register.html', 
                                 student_name=token_doc['student_name'],
                                 token=token)
        
        # Check if roll number already exists
        existing_student = placed_students_collection.find_one({'student_id': roll_number})
        if existing_student:
            flash('Roll number already exists in database!', 'error')
            return render_template('student_self_register.html', 
                                 student_name=token_doc['student_name'],
                                 token=token)
        
        try:
            # Create student record
            student_data = {
                'student_id': roll_number,
                'name': token_doc['student_name'],
                'course': branch,
                'batch': year,
                'company': company,
                'package_lpa': package,
                'placement_date': datetime.now().strftime('%Y-%m-%d'),
                'email': email or f"{token_doc['student_name'].lower().replace(' ', '.')}@example.com",
                'phone': phone or '+91-9876543210',
                'self_registered': True,
                'registration_date': datetime.now()
            }
            
            # Insert student data
            placed_students_collection.insert_one(student_data)
            
            # Mark token as used
            student_tokens_collection.update_one(
                {'_id': token_doc['_id']},
                {'$set': {'used': True, 'used_at': datetime.now()}}
            )
            
            flash('Your details have been successfully registered! Thank you.', 'success')
            return render_template('registration_success.html', student_name=token_doc['student_name'])
            
        except Exception as e:
            flash(f'Error saving your details: {str(e)}', 'error')
    
    return render_template('student_self_register.html', 
                         student_name=token_doc['student_name'],
                         token=token)



@app.route('/admin-email-config')
def admin_email_config():
    """Admin page to configure email settings"""
    if not is_admin_logged_in():
        flash('Please login as admin first!', 'error')
        return redirect(url_for('admin_login'))
    
    # Check current email configuration status
    email_configured = (EMAIL_CONFIG['email'] != 'your-email@gmail.com' and 
                       EMAIL_CONFIG['password'] != 'your-app-password')
    
    return render_template('admin_email_config.html', 
                         email_configured=email_configured,
                         current_email=EMAIL_CONFIG['email'])

@app.route('/admin-view-tokens')
def admin_view_tokens():
    """Admin page to view active tokens and OTPs for testing"""
    if not is_admin_logged_in():
        flash('Please login as admin first!', 'error')
        return redirect(url_for('admin_login'))
    
    try:
        # Get active tokens (not expired and not used)
        active_tokens = list(student_tokens_collection.find({
            'used': False,
            'expires_at': {'$gt': datetime.now()}
        }).sort('created_at', -1))
        
        # Get recent expired/used tokens for reference
        recent_tokens = list(student_tokens_collection.find({
            '$or': [
                {'used': True},
                {'expires_at': {'$lte': datetime.now()}}
            ]
        }).sort('created_at', -1).limit(10))
        
        return render_template('admin_view_tokens.html', 
                             active_tokens=active_tokens,
                             recent_tokens=recent_tokens)
    except Exception as e:
        flash(f'Error fetching tokens: {str(e)}', 'error')
        return redirect(url_for('admin_dashboard'))



if __name__ == '__main__':
    print("[INFO] Starting Placement Cell Application...")
    print("[INFO] MongoDB Database: studetsdb")
    print("[INFO] Collection: Placed")
    print("[INFO] Server will start at: http://localhost:5000")
    # Production-ready configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)