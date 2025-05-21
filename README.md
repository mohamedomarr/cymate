# CyMate Community Documentation

# **Comprehensive API Endpoints Guide for the Blog Project**

## **1- Authentication Endpoints**

### **1. User Registration**

- **URL**: `http://127.0.0.1:8000/auth/registration/`
- **Method**: POST
- **Description**: Register a new user account
- **Payload**:

```jsx
{
"username": "newuser",
"email": "[newuser@example.com](mailto:newuser@example.com)",
"password1": "securepassword123",
"password2": "securepassword123",
"first_name": "New",
"last_name": "User"
}
```

• **Response**: Returns user details and authentication token

### **2. User Login**

- **URL**: `http://127.0.0.1:8000/auth/login/`
- **Method**: POST
- **Description**: Log in with existing credentials
- **Payload**:

```jsx
{
"email": "user@example.com",
"password": "yourpassword"
}
```

- **Response**: Returns authentication token and user details

### **3. User Logout**

- **URL**: `http://127.0.0.1:8000/auth/logout/`
- **Method**: POST
- **Description**: Log out the current user
- **Payload**: Empty (no data required)
- **Response**: Success message

### **4. Password Reset Request**

- **URL**: `http://127.0.0.1:8000/auth/password/reset/`
- **Method**: POST
- **Description**: Request a password reset email
- **Payload**:

```jsx
{
"email": "[user@example.com](mailto:user@example.com)"
}
```

- **Response**: Success message

### **5. Password Reset Confirmation**

- **URL**: `http://127.0.0.1:8000/auth/password/reset/confirm/`
- **Method**: POST
- **Description**: Confirm password reset with token
- **Payload**:

```jsx
{
"uid": "MQ",
"token": "bckm5d-token-example",
"new_password1": "newpassword123",
"new_password2": "newpassword123"
}
```

- **Response**: Success message

### **6. Password Change**

- **URL**: `http://127.0.0.1:8000/auth/password/change/`
- **Method**: POST
- **Description**: Change password for authenticated user
- **Payload**:

```jsx
{
"old_password": "currentpassword",
"new_password1": "newpassword123",
"new_password2": "newpassword123"
}
```

- **Response**: Success message

### **7. User Details**

- **URL**: `http://127.0.0.1:8000/auth/user/`
- **Method**: GET
- **Description**: Get current user details
- **Response**: Returns user information

## **2- Post Management Endpoints**

### **1. List/Create Posts**

- **URL**: `http://127.0.0.1:8000/api/posts/`
- **Method**: GET
- **Description**: List all posts (paginated)
- **Query Parameters**:
    - `page`: Page number
    - `page_size`: Number of posts per page (default: 10, max: 100)
- **Response**: Returns paginated list of posts
- **Method**: POST
- **Description**: Create a new post
- **Payload**:

```jsx
{
"title": "My New Post",
"content": "This is the content of my new post.",
"post_type": "post",
"tags": ["tag1", "tag2"]
}
```

- **Response**: Returns created post details

### **2. Get Post Details**

- **URL**: `http://127.0.0.1:8000/api/posts/{post_id}/`
- **Method**: GET
- **Description**: Get details of a specific post
- **Response**: Returns post details

### **3. Post Interactions (React, Save, Share)**

- **URL**: `http://127.0.0.1:8000/api/posts/{post_id}/interact/`
- **Method**: GET
- **Description**: Get post with interaction details
- **Response**: Returns post with user's interaction status
- **Method**: POST
- **Description**: React to a post (like, love, etc.)
- **Payload**:

```jsx
{
"action_type": "react",
"react_type": "like"
}
```

- **Available react_types**: `like`, `love`, `haha`, `wow`, `sad`, `angry`
- **Response**: Returns updated post details
- **Method**: POST
- **Description**: Save a post
- **Payload**:

```jsx
{
"action_type": "save"
}
```

- **Response**: Returns updated post details
- **Method**: POST
- **Description**: Share a post
- **Payload**:

```jsx
{
"action_type": "share"
}
```

- **Response**: Returns updated post details

### **4. Comment on a Post**

- **URL**: `http://127.0.0.1:8000/api/posts/{post_id}/comment/`
- **Method**: POST
- **Description**: Add a comment to a post
- **Payload**:

```jsx
{
"content": "This is my comment on the post."
}
```

- **Response**: Returns the created comment

### **5. List Saved Posts**

- **URL**: `http://127.0.0.1:8000/api/posts/saved/`
- **Method**: GET
- **Description**: Get all posts saved by the current user
- **Response**: Returns list of saved posts

### **6. Edit a Post**

- **URL**: `http://127.0.0.1:8000/api/posts/{post_id}/edit/`
- **Method**: PUT
- **Description**: Edit an existing post (only available to post author)
- **Payload**:

```jsx
{
"title": "Updated Title",
"content": "Updated content for my post.",
"post_type": "blog",
"tags": "updated,tags"
}
```

- **Response**: Returns updated post details

## **3- Profile Management Endpoints**

### **1. View User Profile**

- **URL**: `http://127.0.0.1:8000/api/profile/{username}/`
- **Method**: GET
- **Description**: View a user's profile
- **Response**: Returns user profile details, posts, and follow information

### **2. Create Profile**

- **URL**: `http://127.0.0.1:8000/api/profile-create/`
- **Method**: POST
- **Description**: Create or update profile details
- **Payload**:

```jsx
{
"job_title": "Software Developer",
"job_status": "Full-time",
"brief": "Passionate about coding and technology",
"years_of_experience": 5,
"phone_number": "+1234567890"
}
```

- **Response**: Returns created/updated profile

### **3. Edit Profile**

- **URL**: `http://127.0.0.1:8000/api/profile-update/`
- **Method**: PUT
- **Description**: Edit current user's profile
- **Payload**:

```jsx
{
"job_title": "Senior Developer",
"job_status": "Full-time",
"brief": "Updated profile description",
"years_of_experience": 7,
"phone_number": "+1234567890"
}
```

- **Response**: Returns updated profile
- **Method**: PATCH
- **Description**: Partially update current user's profile
- **Payload**:

```jsx
{
"job_title": "Senior Developer"
}
```

- **Response**: Returns updated profile

## **4- Notification Endpoints**

### **1. List Notifications**

- **URL**: `http://127.0.0.1:8000/api/notifications/`
- **Method**: GET
- **Description**: Get all unread notifications for current user
- **Response**: Returns list of unread notifications

### **2. Mark Notification as Read**

- **URL**: `http://127.0.0.1:8000/api/notifications/{notification_id}/mark-read/`
- **Method**: POST
- **Description**: Mark a specific notification as read
- **Payload**: Empty (no data required)
- **Response**: Success status

### **3. Mark All Notifications as Read**

- **URL**: `http://127.0.0.1:8000/api/notifications/mark-all-read/`
- **Method**: POST
- **Description**: Mark all notifications as read
- **Payload**: Empty (no data required)
- **Response**: Success status

## **5- Advanced Usage Examples**

### **Creating a Post with an Image**

- **URL**: `http://127.0.0.1:8000/api/posts/`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Form Data**:
    - `title`: "Post with Image"
    - `content`: "This post includes an image"
    - `post_type`: "post"
    - `tags`: "image,example"
    - `image`: [file upload]
- **Response**: Returns created post details with image URL

### **Filtering Posts by Tag**

- **URL**: `http://127.0.0.1:8000/api/posts/?tags=technology`
- **Method**: GET
- **Description**: Get posts with specific tag
- **Response**: Returns filtered posts

## **6- Authentication Notes**

1. Most endpoints require authentication using Token Authentication
2. Include the token in the Authorization header:

`Authorization: Token your_token_here`

1. JWT authentication is also configured if you prefer:

`Authorization: Bearer your_jwt_token_here`

## **7- Common HTTP Status Codes**

- **200 OK**: Request succeeded
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side error

## **Pagination**

List endpoints return paginated results with the following structure:

```jsx
{
"count": 100,
"next": "http://127.0.0.1:8000/api/posts/?page=2",
"previous": null,
"results": [
// items for current page
]
}
```

## **8- Testing the API**

You can test these endpoints using:

1. The browsable API interface provided by Django REST Framework
2. Postman or similar API testing tools
3. curl commands from the terminal

For example, to create a post using curl:

```jsx
curl -X POST http://127.0.0.1:8000/api/posts/ \
-H "Authorization: Token YOUR_AUTH_TOKEN" \
-H "Content-Type: application/json" \
-d '{"title":"Test Post","content":"This is a test post","post_type":"post","tags":["test","api"]}'
```

This comprehensive guide covers all the API endpoints available in your blog project. Each endpoint includes the URL, method, required data, and example payloads to help you fully test and utilize the application.