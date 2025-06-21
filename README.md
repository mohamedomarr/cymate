# CyMate

## About

CyMate is a full-featured blog and social platform built with Django and Django REST Framework. It enables users to create, share, and interact with posts, manage profiles, and receive notifications.

## Features

- **User Authentication** - Registration, login, password reset
- **Email Verification** - Secure 6-digit verification codes with 15-minute expiration
- **Post Management** - Create, edit, delete posts with rich content
- **Social Interactions** - React (Love/Dislike/Thunder), save, share, and comment on posts
- **Profile Management** - User profiles with image uploads
- **Notifications** - Real-time notifications for interactions
- **Tag System** - Organize and filter posts by tags
- **Admin Panel** - Full Django admin interface

## Quick Start

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mohamedomarr/cymate.git
cd cymate
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Start development server:
```bash
python manage.py runserver
```

7. Access the application:
   - API: http://127.0.0.1:8000/api/
   - Admin: http://127.0.0.1:8000/admin/
   - Auth: http://127.0.0.1:8000/auth/

## API Documentation

For complete API documentation including all endpoints, payload formats, and response examples, see [API_REFERENCE.md](API_REFERENCE.md).

## Management Commands

Cleanup expired verification codes:
```bash
python manage.py cleanup_verification_codes --hours 24
```

## Features Status

- **✅ Email Verification** - Secure 6-digit codes for registration and password reset
- **✅ User Authentication** - Complete login/logout with token-based auth
- **✅ Post Management** - Create, edit, delete posts with admin support
- **✅ Social Features** - React (Love/Dislike/Thunder), save, share, comment
- **✅ Tag System** - Filter and organize posts by tags
- **✅ Profile Management** - User profiles with image uploads
- **✅ Notifications** - Real-time interaction notifications
- **✅ Comment System** - Full CRUD operations for comments

## API Testing

Test the API using:
- Django REST Framework browsable API interface
- Postman or similar tools
- curl commands

Example:
```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
-H "Authorization: Token YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{"title":"Test","content":"Content","post_type":"post"}'
```

## Environment Configuration

For production deployment, consider:

1. Setting `DEBUG = False` in settings.py
2. Configuring a proper database (PostgreSQL recommended)
3. Setting up a proper email backend
4. Using a production-ready web server (like Gunicorn with Nginx)
5. Setting secure and unique `SECRET_KEY`
6. Configuring `ALLOWED_HOSTS`

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Contact

For questions or support, please contact the development team. 