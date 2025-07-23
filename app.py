from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TelField, DateField, SelectField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

# In-memory storage for demo purposes (use a database in production)
users_db = []

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ])
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ])
    
    email = EmailField('Email Address', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    phone = TelField('Phone Number', validators=[
        DataRequired(message='Phone number is required'),
        Length(min=10, max=15, message='Phone number must be between 10 and 15 digits')
    ])
    
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=20, message='Username must be between 3 and 20 characters')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    
    date_of_birth = DateField('Date of Birth', validators=[
        DataRequired(message='Date of birth is required')
    ])
    
    gender = RadioField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], validators=[DataRequired(message='Please select your gender')])
    
    country = SelectField('Country', choices=[
        ('', 'Choose your country...'),
        ('us', 'United States'),
        ('ca', 'Canada'),
        ('uk', 'United Kingdom'),
        ('au', 'Australia'),
        ('de', 'Germany'),
        ('fr', 'France'),
        ('jp', 'Japan'),
        ('in', 'India'),
        ('br', 'Brazil'),
        ('mx', 'Mexico'),
        ('other', 'Other')
    ], validators=[DataRequired(message='Please select your country')])
    
    terms = BooleanField('Terms and Conditions', validators=[
        DataRequired(message='You must agree to the terms and conditions')
    ])
    
    newsletter = BooleanField('Newsletter Subscription')
    
    submit = SubmitField('Create Account')
    
    def validate_email(self, email):
        """Custom email validation to check if email already exists"""
        for user in users_db:
            if user['email'] == email.data:
                raise ValidationError('Email address already registered. Please choose a different one.')
    
    def validate_username(self, username):
        """Custom username validation to check if username already exists"""
        for user in users_db:
            if user['username'] == username.data:
                raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_phone(self, phone):
        """Custom phone validation"""
        phone_pattern = re.compile(r'^\d{10,15}$')
        if not phone_pattern.match(phone.data):
            raise ValidationError('Phone number must contain only digits and be 10-15 characters long.')
    
    def validate_date_of_birth(self, date_of_birth):
        """Custom date validation to ensure user is at least 13 years old"""
        today = datetime.now().date()
        age = today.year - date_of_birth.data.year - ((today.month, today.day) < (date_of_birth.data.month, date_of_birth.data.day))
        if age < 13:
            raise ValidationError('You must be at least 13 years old to register.')

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration form route"""
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Create user data dictionary
        user_data = {
            'id': len(users_db) + 1,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'username': form.username.data,
            'password': form.password.data,  # In production, hash this password
            'date_of_birth': form.date_of_birth.data.strftime('%Y-%m-%d'),
            'gender': form.gender.data,
            'country': form.country.data,
            'newsletter': form.newsletter.data,
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save user to database (in-memory for demo)
        users_db.append(user_data)
        
        flash(f'Registration successful! Welcome {user_data["first_name"]}!', 'success')
        return redirect(url_for('success', user_id=user_data['id']))
    
    return render_template('register.html', form=form)

@app.route('/success/<int:user_id>')
def success(user_id):
    """Registration success page"""
    user = next((user for user in users_db if user['id'] == user_id), None)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('register'))
    
    return render_template('success.html', user=user)

@app.route('/users')
def list_users():
    """List all registered users (for demo purposes)"""
    return render_template('users.html', users=users_db)

@app.route('/api/users', methods=['GET'])
def api_users():
    """API endpoint to get all users as JSON"""
    # Remove passwords from the response for security
    safe_users = []
    for user in users_db:
        safe_user = user.copy()
        safe_user.pop('password', None)
        safe_users.append(safe_user)
    
    return jsonify({
        'status': 'success',
        'count': len(safe_users),
        'users': safe_users
    })

@app.route('/api/register', methods=['POST'])
def api_register():
    """API endpoint for registration"""
    try:
        data = request.get_json()
        
        # Basic validation
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password', 'date_of_birth', 'gender', 'country']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'{field} is required'}), 400
        
        # Check if email or username already exists
        for user in users_db:
            if user['email'] == data['email']:
                return jsonify({'status': 'error', 'message': 'Email already registered'}), 400
            if user['username'] == data['username']:
                return jsonify({'status': 'error', 'message': 'Username already taken'}), 400
        
        # Create user
        user_data = {
            'id': len(users_db) + 1,
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'phone': data['phone'],
            'username': data['username'],
            'password': data['password'],  # Hash in production
            'date_of_birth': data['date_of_birth'],
            'gender': data['gender'],
            'country': data['country'],
            'newsletter': data.get('newsletter', False),
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        users_db.append(user_data)
        
        # Return success response without password
        response_data = user_data.copy()
        response_data.pop('password')
        
        return jsonify({
            'status': 'success',
            'message': 'Registration successful',
            'user': response_data
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)