# Python Flask Registration Form with Bootstrap 5

A complete user registration system built with Python Flask and Bootstrap 5, featuring form validation, responsive design, and a modern UI.

## Features

### 🎨 **Modern UI/UX**
- Bootstrap 5 responsive design
- Gradient backgrounds and smooth animations
- Bootstrap Icons for visual enhancement
- Mobile-first responsive layout

### 📝 **Registration Form Fields**
- **Personal Information**: First Name, Last Name
- **Contact Details**: Email Address, Phone Number
- **Account Info**: Username, Password with toggle visibility, Confirm Password
- **Additional Info**: Date of Birth, Gender (radio buttons), Country (dropdown)
- **Legal**: Terms & Conditions checkbox, Newsletter subscription (optional)

### ✅ **Form Validation**
- Server-side validation using Flask-WTF and WTForms
- Custom validators for email uniqueness, username uniqueness
- Age validation (minimum 13 years old)
- Phone number format validation
- Password confirmation matching

### 🔧 **Technical Features**
- Flask web framework with Jinja2 templating
- Form handling with Flask-WTF
- In-memory user storage (easily replaceable with database)
- RESTful API endpoints
- Flash messaging system
- CSRF protection

## Installation & Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Application Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template with Bootstrap 5
│   ├── index.html        # Home page
│   ├── register.html     # Registration form
│   ├── success.html      # Registration success page
│   └── users.html        # List of registered users
└── README_PYTHON.md      # This file
```

## Routes

### Web Routes
- `/` - Home page with application overview
- `/register` - Registration form (GET/POST)
- `/success/<user_id>` - Registration success page
- `/users` - List all registered users

### API Routes
- `GET /api/users` - Get all users as JSON (passwords excluded)
- `POST /api/register` - Register user via JSON API

## API Usage Examples

### Get All Users
```bash
curl -X GET http://localhost:5000/api/users
```

### Register User via API
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "username": "johndoe",
    "password": "password123",
    "date_of_birth": "1990-01-01",
    "gender": "male",
    "country": "us",
    "newsletter": true
  }'
```

## Form Validation Rules

- **First/Last Name**: 2-50 characters, required
- **Email**: Valid email format, unique, required
- **Phone**: 10-15 digits only, required
- **Username**: 3-20 characters, unique, required
- **Password**: Minimum 8 characters, required
- **Date of Birth**: Must be at least 13 years old, required
- **Gender**: Must select one option, required
- **Country**: Must select from dropdown, required
- **Terms**: Must agree to terms, required
- **Newsletter**: Optional

## Customization

### Database Integration
Replace the in-memory `users_db` list with your preferred database:
- SQLite with SQLAlchemy
- PostgreSQL
- MySQL
- MongoDB

### Password Security
In production, implement proper password hashing:
```python
from werkzeug.security import generate_password_hash, check_password_hash

# When saving password
user_data['password'] = generate_password_hash(form.password.data)
```

### Email Verification
Add email verification functionality:
- Send confirmation emails
- Verify email addresses before activation
- Password reset functionality

## Security Features

- CSRF protection via Flask-WTF
- Form validation on both client and server side
- XSS protection through Jinja2 template escaping
- Input sanitization and validation

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Dependencies

- **Flask**: Web framework
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation
- **email-validator**: Email validation
- **Bootstrap 5**: CSS framework (via CDN)
- **Bootstrap Icons**: Icon library (via CDN)

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please open an issue on the repository or contact the development team.