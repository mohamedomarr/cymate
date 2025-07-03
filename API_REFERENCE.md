# CyMate API Reference

## Overview

This document provides a comprehensive reference for all API endpoints available in the CyMate platform. All endpoints require authentication unless explicitly stated otherwise.

**Base URL**: `http://127.0.0.1:8000`

**Authentication**: Token-based authentication
```
Authorization: Token your_auth_token_here
```

---

## Authentication Endpoints

### User Registration
**Endpoint**: `/auth/registration/`  
**Method**: POST  
**Description**: Register a new user account  
**Authentication**: Not required

**Payload**:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password1": "securepassword123",
  "password2": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response**:
```json
{
  "key": "auth_token_here",
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Enhanced Registration with Email Verification
**Endpoint**: `/api/auth/enhanced-registration/`  
**Method**: POST  
**Description**: Register with pre-verified email  
**Authentication**: Not required

**Payload**:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password1": "securepassword123",
  "password2": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "verification_code": "123456"
}
```

### User Login
**Endpoint**: `/auth/login/`  
**Method**: POST  
**Description**: Authenticate user credentials  
**Authentication**: Not required

**Payload**:
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response**:
```json
{
  "key": "auth_token_here",
  "user": {
    "id": 1,
    "username": "username",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### User Logout
**Endpoint**: `/auth/logout/`  
**Method**: POST  
**Description**: Log out current user  
**Payload**: None

### Get Current User Details
**Endpoint**: `/auth/user/`  
**Method**: GET  
**Description**: Get current authenticated user information

**Response**:
```json
{
  "id": 1,
  "username": "username",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "profile_picture": "https://example.com/media/profile/image.jpg",
  "toolkit_tokens": 50
}
```

### Password Reset Request (Traditional Method)
**Endpoint**: `/auth/password/reset/`  
**Method**: POST  
**Description**: Request password reset email via Django's built-in system  
**Authentication**: Not required

**Payload**:
```json
{
  "email": "user@example.com"
}
```

### Password Reset Confirmation (Traditional Method)
**Endpoint**: `/auth/password/reset/confirm/`  
**Method**: POST  
**Description**: Confirm password reset with UID/token from email  
**Authentication**: Not required

**Payload**:
```json
{
  "uid": "MQ",
  "token": "bckm5d-token-example",
  "new_password1": "newpassword123",
  "new_password2": "newpassword123"
}
```

### Password Reset via Email Verification (Enhanced Method)
**Description**: Alternative password reset flow using 6-digit verification codes

**Step 1 - Send Verification Code**:
```json
POST /api/email-verification/send-code/
{
  "email": "user@example.com",
  "verification_type": "password_reset"
}
```

**Step 2 - Verify Code and Get Token**:
```json
POST /api/email-verification/verify-code/
{
  "email": "user@example.com",
  "code": "123456",
  "verification_type": "password_reset"
}
```

**Step 3 - Reset Password with Token**:
```json
POST /api/email-verification/reset-password-confirm/
{
  "email": "user@example.com",
  "new_password": "newpassword123",
  "confirm_password": "newpassword123",
  "verification_token": "token_from_step_2"
}
```

### Password Change
**Endpoint**: `/auth/password/change/`  
**Method**: POST  
**Description**: Change password for authenticated user

**Payload**:
```json
{
  "old_password": "currentpassword",
  "new_password1": "newpassword123",
  "new_password2": "newpassword123"
}
```

### Modify Toolkit Tokens
**Endpoint**: `/api/user/toolkit-tokens/modify/`  
**Method**: POST  
**Description**: Add or deduct toolkit tokens from current user's balance

**Payload**:
```json
{
  "operation": "add",
  "amount": 10
}
```
*operation options: "add", "deduct"*

**Response**:
```json
{
  "toolkit_tokens": 60
}
```

**Error Responses**:
- **400 Bad Request** (Invalid operation):
```json
{
  "error": "Invalid operation. Must be \"add\" or \"deduct\""
}
```

- **400 Bad Request** (Invalid amount):
```json
{
  "error": "Amount must be a positive number"
}
```

- **400 Bad Request** (Insufficient tokens):
```json
{
  "error": "Insufficient tokens. Cannot deduct more than available balance"
}
```

---

## Email Verification System

This system provides secure 6-digit verification codes for both user registration and password reset workflows. Codes expire after 15 minutes and are single-use only.

### Send Verification Code
**Endpoint**: `/api/email-verification/send-code/`  
**Method**: POST  
**Description**: Send 6-digit verification code via email  
**Authentication**: Not required

**Payload**:
```json
{
  "email": "user@example.com",
  "verification_type": "registration"
}
```
*verification_type options: "registration", "password_reset"*

**Response**:
```json
{
  "message": "Verification code sent successfully",
  "email": "user@example.com", 
  "expires_in_minutes": 15
}
```

### Verify Code
**Endpoint**: `/api/email-verification/verify-code/`  
**Method**: POST  
**Description**: Verify 6-digit code and get verification token  
**Authentication**: Not required

**Payload**:
```json
{
  "email": "user@example.com",
  "code": "123456",
  "verification_type": "registration"
}
```

**Response (Password Reset)**:
```json
{
  "message": "Verification successful",
  "verification_token": "secure_token_for_password_reset"
}
```

**Response (Registration)**:
```json
{
  "message": "Email verified successfully"
}
```

### Resend Verification Code
**Endpoint**: `/api/email-verification/resend-code/`  
**Method**: POST  
**Description**: Resend verification code (if previous expired)  
**Authentication**: Not required

**Payload**:
```json
{
  "email": "user@example.com",
  "verification_type": "registration"
}
```

### Password Reset Confirmation
**Endpoint**: `/api/email-verification/reset-password-confirm/`  
**Method**: POST  
**Description**: Complete password reset using verification token  
**Authentication**: Not required

**Payload**:
```json
{
  "email": "user@example.com",
  "new_password": "newpassword123", 
  "confirm_password": "newpassword123",
  "verification_token": "token_from_verify_step"
}
```

**Response**:
```json
{
  "message": "Password reset successful"
}
```

### Check Verification Status
**Endpoint**: `/api/email-verification/status/`  
**Method**: GET  
**Description**: Check if there's an active verification code  
**Authentication**: Not required

**Query Parameters**: `?email=user@example.com&type=registration`

**Response**:
```json
{
  "has_active_code": true,
  "expires_at": "2024-01-15T10:45:00Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Password Reset Methods

CyMate provides **two different password reset approaches**:

### Method 1: Traditional Django Password Reset
- Uses Django's built-in password reset system
- Sends email with UID/token link
- Endpoints: `/auth/password/reset/` → `/auth/password/reset/confirm/`
- **Use case**: Standard email-based password reset with clickable links

### Method 2: Email Verification Code Reset  
- Uses 6-digit verification codes (same system as registration)
- Three-step process: send code → verify code → reset password
- Endpoints: `/api/email-verification/send-code/` → `/api/email-verification/verify-code/` → `/api/email-verification/reset-password-confirm/`
- **Use case**: Mobile-friendly, modern UX with short codes instead of long URLs

Both methods are fully functional and can be used based on your frontend requirements.

---

## Post Endpoints

### List/Create Posts
**Endpoint**: `/api/posts/`  
**Methods**: GET, POST  
**Description**: List all posts (paginated) or create new post

**GET Query Parameters**:
- `page`: Page number
- `page_size`: Posts per page (default: 10, max: 100)  
- `tags`: Filter by tags (e.g., `?tags=tech,python`)

**POST Payload**:
```json
{
  "title": "My New Post",
  "content": "Post content here",
  "post_type": "post",
  "tags": ["tech", "python"],
  "image": "file_upload_optional"
}
```
*post_type options: "post", "blog", "question", "event"*

**Response**:
```json
{
  "id": 1,
  "author": {
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "profile_picture": "https://example.com/profile.jpg"
  },
  "title": "My New Post",
  "content": "Post content here",
  "post_type": "post",
  "image": "https://example.com/media/image.jpg",
  "tags": ["tech", "python"],
  "created_at": "2024-01-15T10:30:00Z",
  "comments_count": 5,
  "shares_count": 2,
  "saves_count": 3,
  "reactions": {
    "Love": 4,
    "Dislike": 1,
    "Thunder": 2
  },
  "user_reaction": "Love",
  "is_shared": false,
  "is_saved": true,
  "comments": [
    {
      "id": 1,
      "user": "commenter",
      "first_name": "Jane",
      "last_name": "Smith",
      "author": {
        "username": "commenter",
        "first_name": "Jane",
        "last_name": "Smith",
        "profile_picture": "https://example.com/profile2.jpg"
      },
      "content": "Great post!",
      "created_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

### Get Post Details
**Endpoint**: `/api/posts/{post_id}/`  
**Method**: GET  
**Description**: Get details of specific post

### Post Interactions
**Endpoint**: `/api/posts/{post_id}/interact/`  
**Methods**: GET, POST  
**Description**: View or interact with post (react, save, share)

**GET**: Returns post with interaction status

**POST Payloads**:

*React to post*:
```json
{
  "action_type": "react",
  "react_type": "Love"
}
```
*react_type options: "Love", "Dislike", "Thunder"*

*Save post*:
```json
{
  "action_type": "save"
}
```

*Share post*:
```json
{
  "action_type": "share"
}
```

### Comment on Post
**Endpoint**: `/api/posts/{post_id}/comment/`  
**Method**: POST  
**Description**: Add comment to post

**Payload**:
```json
{
  "content": "This is my comment"
}
```

### List Saved Posts
**Endpoint**: `/api/posts/saved/`  
**Method**: GET  
**Description**: Get all posts saved by current user

### Edit Post
**Endpoint**: `/api/posts/{post_id}/edit/`  
**Method**: PUT  
**Description**: Edit existing post (owner only)

**Payload**:
```json
{
  "title": "Updated Title",
  "content": "Updated content",
  "post_type": "blog",
  "tags": ["updated", "tags"]
}
```

### Delete Post
**Endpoint**: `/api/posts/{post_id}/edit/`  
**Method**: DELETE  
**Description**: Delete post (owner or admin)  
**Response**: 204 No Content

---

## Comment Endpoints

### Edit Comment
**Endpoint**: `/api/comments/{comment_id}/`  
**Method**: PATCH  
**Description**: Edit existing comment (owner only)

**Payload**:
```json
{
  "content": "Updated comment content"
}
```

### Delete Comment
**Endpoint**: `/api/comments/{comment_id}/`  
**Method**: DELETE  
**Description**: Delete comment (owner only)  
**Response**: 204 No Content

---

## Profile Endpoints

### View User Profile
**Endpoint**: `/api/profile/{username}/`  
**Method**: GET  
**Description**: View any user's profile

**Response**:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "job_title": "Software Developer",
  "job_status": "Full-time",
  "brief": "Passionate developer",
  "years_of_experience": 5,
  "profile_image": "https://example.com/profile.jpg",
  "profile_picture": "https://example.com/profile.jpg",
  "phone_number": "+1234567890",
  "posts_count": 25,
  "posts": [
    {
      "id": 1,
      "title": "User's Post",
      "content": "Post content...",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Create Profile (Class-based)
**Endpoint**: `/api/profile/create/`  
**Method**: POST  
**Content-Type**: `multipart/form-data` or `application/json`  
**Description**: Create user profile

**Payload**:
```json
{
  "job_title": "Software Engineer",
  "job_status": "Full-time",
  "brief": "Experienced developer",
  "years_of_experience": 5,
  "phone_number": "+1234567890",
  "profile_image": "file_upload",
  "profile_picture": "file_upload"
}
```

### Create Profile (Function-based)
**Endpoint**: `/api/profile-create/`  
**Method**: POST  
**Content-Type**: `multipart/form-data` or `application/json`  
**Description**: Create user profile (alternative endpoint)

### Edit Profile (Class-based)
**Endpoint**: `/api/profile/edit/`  
**Methods**: PUT, PATCH  
**Content-Type**: `multipart/form-data` or `application/json`  
**Description**: Edit current user's profile

**Payload**:
```json
{
  "first_name": "Updated",
  "last_name": "Name",
  "job_title": "Senior Developer",
  "profile_picture": "file_upload"
}
```

### Edit Profile (Function-based)
**Endpoint**: `/api/profile-update/`  
**Methods**: POST, PUT, PATCH  
**Content-Type**: `multipart/form-data` or `application/json`  
**Description**: Edit current user's profile (alternative endpoint)

---

## Notification Endpoints

### List Notifications
**Endpoint**: `/api/notifications/`  
**Method**: GET  
**Description**: Get all unread notifications for current user

**Response**:
```json
[
  {
    "id": 1,
    "user": "username",
    "sender": {
      "username": "sender_user",
      "first_name": "John",
      "last_name": "Doe",
      "profile_picture": "https://example.com/profile.jpg"
    },
    "notification_type": "like",
    "message": "sender_user liked your post",
    "is_read": false,
    "created_at": "2024-01-15T10:30:00Z",
    "post_id": 123,
    "liked": true,
    "disliked": false,
    "thundered": false
  }
]
```

### Mark Notification as Read
**Endpoint**: `/api/notifications/{notification_id}/mark-read/`  
**Method**: POST  
**Description**: Mark specific notification as read  
**Response**: 200 OK

### Mark All Notifications as Read
**Endpoint**: `/api/notifications/mark-all-read/`  
**Method**: POST  
**Description**: Mark all notifications as read  
**Response**: 200 OK

---

## Error Responses

All endpoints return appropriate HTTP status codes with error details:

**400 Bad Request**:
```json
{
  "error": "Validation error message",
  "detail": "Additional error details"
}
```

**401 Unauthorized**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden**:
```json
{
  "error": "Permission denied"
}
```

**404 Not Found**:
```json
{
  "error": "Resource not found"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal server error message"
}
```

---

## Notes

### File Uploads
- Maximum file size: 5MB
- Supported formats: JPEG, PNG, GIF
- Use `multipart/form-data` content type for file uploads

### Pagination
List endpoints return paginated results:
```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": []
}
```

### Reaction Types
Only three reaction types are supported:
- `Love`
- `Dislike` 
- `Thunder`

### Post Types
Available post types:
- `post`
- `blog`
- `question`
- `event`

### API Testing
Test endpoints using:
```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
-H "Authorization: Token YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{"title":"Test","content":"Content","post_type":"post"}'
``` 