# CyMate Community Documentation

## About CyMate

CyMate is a full-featured blog and social platform built with Django and Django REST Framework. It enables users to create, share, and interact with posts, manage profiles, and receive notifications.

## Setup Guide

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation Steps

1. Clone the repository:
```bash
git clone git clone https://github.com/mohamedomarr/cymate/tree/main
cd cymate
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser account:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application:
   - Admin interface: http://127.0.0.1:8000/admin/
   - API root: http://127.0.0.1:8000/api/
   - Authentication: http://127.0.0.1:8000/auth/

## API Endpoints Guide

### 1. Authentication Endpoints

#### 1.1 User Registration

- **URL**: `http://127.0.0.1:8000/auth/registration/`
- **Method**: POST
- **Description**: Register a new user account
- **Payload**:

```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password1": "securepassword123",
  "password2": "securepassword123",
  "first_name": "New",
  "last_name": "User"
}
```

- **Response**: Returns user details and authentication token

#### 1.2 User Login

- **URL**: `http://127.0.0.1:8000/auth/login/`
- **Method**: POST
- **Description**: Log in with existing credentials
- **Payload**:

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

- **Response**: Returns authentication token and user details

#### 1.3 User Logout

- **URL**: `http://127.0.0.1:8000/auth/logout/`
- **Method**: POST
- **Description**: Log out the current user
- **Payload**: Empty (no data required)
- **Response**: Success message

#### 1.4 Password Reset Request

- **URL**: `http://127.0.0.1:8000/auth/password/reset/`
- **Method**: POST
- **Description**: Request a password reset email
- **Payload**:

```json
{
  "email": "user@example.com"
}
```

- **Response**: Success message

#### 1.5 Password Reset Confirmation

- **URL**: `http://127.0.0.1:8000/auth/password/reset/confirm/`
- **Method**: POST
- **Description**: Confirm password reset with token
- **Payload**:

```json
{
  "uid": "MQ",
  "token": "bckm5d-token-example",
  "new_password1": "newpassword123",
  "new_password2": "newpassword123"
}
```

- **Response**: Success message

#### 1.6 Password Change

- **URL**: `http://127.0.0.1:8000/auth/password/change/`
- **Method**: POST
- **Description**: Change password for authenticated user
- **Payload**:

```json
{
  "old_password": "currentpassword",
  "new_password1": "newpassword123",
  "new_password2": "newpassword123"
}
```

- **Response**: Success message

#### 1.7 User Details

- **URL**: `http://127.0.0.1:8000/auth/user/`
- **Method**: GET
- **Description**: Get current user details
- **Response**: Returns user information

### 2. Post Management Endpoints

#### 2.1 List/Create Posts

- **URL**: `http://127.0.0.1:8000/api/posts/`
- **Method**: GET
- **Description**: List all posts (paginated)
- **Query Parameters**:
  - `page`: Page number
  - `page_size`: Number of posts per page (default: 10, max: 100)
- **Response**: Returns paginated list of posts

- **Method**: POST
- **Description**: Create a new post
- **Payload**:

```json
{
  "title": "My New Post",
  "content": "This is the content of my new post.",
  "post_type": "post",
  "tags": ["tag1", "tag2"]
}
```

- **Notes**: Available post_types are: `post`, `blog`, `question`, `event`
- **Response**: Returns created post details

#### 2.2 Get Post Details

- **URL**: `http://127.0.0.1:8000/api/posts/{post_id}/`
- **Method**: GET
- **Description**: Get details of a specific post
- **Response**: Returns post details

#### 2.3 Post Interactions (React, Save, Share)

- **URL**: `http://127.0.0.1:8000/api/posts/{post_id}/interact/`
- **Method**: GET
- **Description**: Get post with interaction details
- **Response**: Returns post with user's interaction status

- **Method**: POST
- **Description**: React to a post (like, love, etc.)
- **Payload**:

```json
{
  "action_type": "react",
  "react_type": "like"
}
```

- **Available react_types**: `like`, `love`, `haha`, `sad`, `angry` 
  (Note: The `wow` type is listed in the documentation but not implemented in the model)
- **Response**: Returns updated post details

- **Method**: POST
- **Description**: Save a post
- **Payload**:

```json
{
  "action_type": "save"
}
```

- **Response**: Returns updated post details

- **Method**: POST
- **Description**: Share a post
- **Payload**:

```json
{
  "action_type": "share"
}
```

- **Response**: Returns updated post details

#### 2.4 Comment on a Post

- **URL**: `http://127.0.0.1:8000/api/posts/{post_id}/comment/`
- **Method**: POST
- **Description**: Add a comment to a post
- **Payload**:

```json
{
  "content": "This is my comment on the post."
}
```

- **Response**: Returns the created comment

#### 2.5 List Saved Posts

- **URL**: `http://127.0.0.1:8000/api/posts/saved/`
- **Method**: GET
- **Description**: Get all posts saved by the current user
- **Response**: Returns list of saved posts

#### 2.6 Edit a Post

- **URL**: `http://127.0.0.1:8000/api/posts/{post_id}/edit/`
- **Method**: PUT
- **Description**: Edit an existing post (only available to post author)
- **Payload**:

```json
{
  "title": "Updated Title",
  "content": "Updated content for my post.",
  "post_type": "blog",
  "tags": ["updated", "tags"]
}
```

- **Response**: Returns updated post details

### 3. Profile Management Endpoints

#### 3.1 View User Profile

- **URL**: `http://127.0.0.1:8000/api/profile/{username}/`
- **Method**: GET
- **Description**: View a user's profile
- **Response**: Returns user profile details, posts, and follow information

#### 3.2 Create Profile

- **URL**: `http://127.0.0.1:8000/api/profile/create/`
- **Method**: POST
- **Description**: Create or update profile details
- **Payload**:

```json
{
  "job_title": "Software Developer",
  "job_status": "Full-time",
  "brief": "Passionate about coding and technology",
  "years_of_experience": 5,
  "phone_number": "+1234567890"
}
```

- **Response**: Returns created/updated profile

#### 3.3 Edit Profile

- **URL**: `http://127.0.0.1:8000/api/profile/edit/`
- **Method**: PUT
- **Description**: Edit current user's profile
- **Payload**:

```json
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

```json
{
  "job_title": "Senior Developer"
}
```

- **Response**: Returns updated profile

### 4. Notification Endpoints

#### 4.1 List Notifications

- **URL**: `http://127.0.0.1:8000/api/notifications/`
- **Method**: GET
- **Description**: Get all unread notifications for current user
- **Response**: Returns list of unread notifications

#### 4.2 Mark Notification as Read

- **URL**: `http://127.0.0.1:8000/api/notifications/{notification_id}/mark-read/`
- **Method**: POST
- **Description**: Mark a specific notification as read
- **Payload**: Empty (no data required)
- **Response**: Success status

#### 4.3 Mark All Notifications as Read

- **URL**: `http://127.0.0.1:8000/api/notifications/mark-all-read/`
- **Method**: POST
- **Description**: Mark all notifications as read
- **Payload**: Empty (no data required)
- **Response**: Success status

### 5. Advanced Usage Examples

#### 5.1 Creating a Post with an Image

- **URL**: `http://127.0.0.1:8000/api/posts/`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Form Data**:
  - `title`: "Post with Image"
  - `content`: "This post includes an image"
  - `post_type`: "post"
  - `tags`: "image,example"
  - `image`: [file upload]
- **Response**: Returns created post details with image URL

#### 5.2 Filtering Posts by Tag

- **URL**: `http://127.0.0.1:8000/api/posts/?tags=technology`
- **Method**: GET
- **Description**: Get posts with specific tag
- **Response**: Returns filtered posts

### 6. Authentication Notes

1. Most endpoints require authentication using Token Authentication
2. Include the token in the Authorization header:
   - `Authorization: Token your_token_here`
3. JWT authentication is also configured if you prefer:
   - `Authorization: Bearer your_jwt_token_here`

### 7. Common HTTP Status Codes

- **200 OK**: Request succeeded
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Authenticated but not authorized
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side error

### 8. Pagination

List endpoints return paginated results with the following structure:

```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": [
    // items for current page
  ]
}
```

### 9. Testing the API

You can test these endpoints using:

1. The browsable API interface provided by Django REST Framework
2. Postman or similar API testing tools
3. curl commands from the terminal

For example, to create a post using curl:

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
-H "Authorization: Token YOUR_AUTH_TOKEN" \
-H "Content-Type: application/json" \
-d '{"title":"Test Post","content":"This is a test post","post_type":"post","tags":["test","api"]}'
```

## Known Issues and Solutions

1. **React Types Inconsistency**: The documentation mentions a `wow` reaction type, but this is not implemented in the model. The available reaction types are: `like`, `love`, `haha`, `sad`, and `angry`.

2. **Profile URL Inconsistency**: There are two URLs for profile creation:
   - `/api/profile/create/` - The standard endpoint
   - `/api/profile-create/` - An alternate endpoint
   
   And two URLs for profile updating:
   - `/api/profile/edit/` - The standard endpoint
   - `/api/profile-update/` - An alternate endpoint

   It's recommended to use the standard endpoints for consistency.

## Environment Configuration

For production deployment, consider:

1. Setting `DEBUG = False` in settings.py
2. Configuring a proper database (PostgreSQL recommended)
3. Setting up a proper email backend
4. Using a production-ready web server (like Gunicorn with Nginx)
5. Setting secure and unique `SECRET_KEY`
6. Configuring `ALLOWED_HOSTS`

## Connecting with a React Frontend

### Prerequisites
- Node.js (v14.0 or higher)
- npm or yarn package manager
- Familiarity with React concepts

### Step 1: Create a React Project

```bash
# Using npm
npx create-react-app cymate-frontend
cd cymate-frontend

# OR using Yarn
yarn create react-app cymate-frontend
cd cymate-frontend
```

### Step 2: Install Required Dependencies

```bash
# Using npm
npm install axios react-router-dom formik yup jwt-decode

# OR using Yarn
yarn add axios react-router-dom formik yup jwt-decode
```

### Step 3: Configure CORS on the Django Backend

1. Install django-cors-headers:

```bash
pip install django-cors-headers
```

2. Add it to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    # ... other apps
    'corsheaders',
    # ... other apps
]
```

3. Add the middleware to settings.py:

```python
MIDDLEWARE = [
    # Add this at the top of the middleware list
    'corsheaders.middleware.CorsMiddleware',
    # ... other middleware
    'django.middleware.common.CommonMiddleware',
    # ... other middleware
]
```

4. Configure CORS settings (for development):

```python
# Development settings
CORS_ALLOW_ALL_ORIGINS = True

# OR for production, specify allowed origins
# CORS_ALLOWED_ORIGINS = [
#     "https://yourdomain.com",
#     "https://www.yourdomain.com",
# ]

# Allow credentials like cookies, authorization headers
CORS_ALLOW_CREDENTIALS = True
```

### Step 4: Create API Service in React

Create a file `src/services/api.js`:

```javascript
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; // Django API URL

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add request interceptor for auth token
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Authentication services
export const authService = {
  register: (userData) => apiClient.post('/auth/registration/', userData),
  login: (credentials) => apiClient.post('/auth/login/', credentials),
  logout: () => apiClient.post('/auth/logout/'),
  getCurrentUser: () => apiClient.get('/auth/user/'),
};

// Post services
export const postService = {
  getPosts: (page = 1) => apiClient.get(`/api/posts/?page=${page}`),
  getPost: (id) => apiClient.get(`/api/posts/${id}/`),
  createPost: (postData) => apiClient.post('/api/posts/', postData),
  updatePost: (id, postData) => apiClient.put(`/api/posts/${id}/edit/`, postData),
  interactWithPost: (id, interactionData) => apiClient.post(`/api/posts/${id}/interact/`, interactionData),
  commentOnPost: (id, commentData) => apiClient.post(`/api/posts/${id}/comment/`, commentData),
  getSavedPosts: () => apiClient.get('/api/posts/saved/'),
};

// Profile services
export const profileService = {
  getProfile: (username) => apiClient.get(`/api/profile/${username}/`),
  createProfile: (profileData) => apiClient.post('/api/profile/create/', profileData),
  updateProfile: (profileData) => apiClient.put('/api/profile/edit/', profileData),
};

// Notification services
export const notificationService = {
  getNotifications: () => apiClient.get('/api/notifications/'),
  markAsRead: (id) => apiClient.post(`/api/notifications/${id}/mark-read/`),
  markAllAsRead: () => apiClient.post('/api/notifications/mark-all-read/'),
};

export default apiClient;
```

### Step 5: Set Up Authentication Context

Create a file `src/context/AuthContext.js`:

```javascript
import React, { createContext, useState, useEffect, useContext } from 'react';
import { authService } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check if user is logged in on page load
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const response = await authService.getCurrentUser();
          setCurrentUser(response.data);
        }
      } catch (err) {
        console.error("Failed to fetch user:", err);
        localStorage.removeItem('token');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const login = async (credentials) => {
    try {
      setError(null);
      const response = await authService.login(credentials);
      const { key } = response.data;
      localStorage.setItem('token', key);
      
      // Get user data
      const userResponse = await authService.getCurrentUser();
      setCurrentUser(userResponse.data);
      return true;
    } catch (err) {
      setError(err.response?.data || { non_field_errors: ['Login failed'] });
      return false;
    }
  };

  const register = async (userData) => {
    try {
      setError(null);
      const response = await authService.register(userData);
      const { key } = response.data;
      localStorage.setItem('token', key);
      
      // Get user data
      const userResponse = await authService.getCurrentUser();
      setCurrentUser(userResponse.data);
      return true;
    } catch (err) {
      setError(err.response?.data || { non_field_errors: ['Registration failed'] });
      return false;
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
    } catch (err) {
      console.error("Logout error:", err);
    } finally {
      localStorage.removeItem('token');
      setCurrentUser(null);
    }
  };

  const contextValue = {
    currentUser,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!currentUser,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

export default AuthContext;
```

### Step 6: Set Up React Router

Update your `src/App.js`:

```jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Import pages
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import PostDetail from './pages/PostDetail';
import Profile from './pages/Profile';
import CreatePost from './pages/CreatePost';
import EditProfile from './pages/EditProfile';
import NotFound from './pages/NotFound';

// Private route component
const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Protected routes */}
            <Route path="/" element={<PrivateRoute><Home /></PrivateRoute>} />
            <Route path="/posts/:id" element={<PrivateRoute><PostDetail /></PrivateRoute>} />
            <Route path="/create-post" element={<PrivateRoute><CreatePost /></PrivateRoute>} />
            <Route path="/profile/:username" element={<PrivateRoute><Profile /></PrivateRoute>} />
            <Route path="/edit-profile" element={<PrivateRoute><EditProfile /></PrivateRoute>} />
            
            {/* Not found */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
```

### Step 7: Create Login and Register Components

Example `src/pages/Login.js`:

```jsx
import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useAuth } from '../context/AuthContext';

const loginSchema = Yup.object().shape({
  email: Yup.string().email('Invalid email').required('Email is required'),
  password: Yup.string().required('Password is required'),
});

function Login() {
  const { login, error, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  // Redirect if already logged in
  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);

  const handleSubmit = async (values, { setSubmitting }) => {
    const success = await login(values);
    setSubmitting(false);
    if (success) {
      navigate('/');
    }
  };

  return (
    <div className="login-container">
      <h1>Login to CyMate</h1>
      
      <Formik
        initialValues={{ email: '', password: '' }}
        validationSchema={loginSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <Field type="email" name="email" className="form-control" />
              <ErrorMessage name="email" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <Field type="password" name="password" className="form-control" />
              <ErrorMessage name="password" component="div" className="error" />
            </div>

            {error && error.non_field_errors && (
              <div className="alert alert-danger">
                {error.non_field_errors.join(', ')}
              </div>
            )}

            <button type="submit" disabled={isSubmitting} className="btn btn-primary">
              {isSubmitting ? 'Logging in...' : 'Login'}
            </button>
          </Form>
        )}
      </Formik>
      
      <div className="mt-3">
        <p>Don't have an account? <Link to="/register">Register</Link></p>
        <p><Link to="/auth/password/reset/">Forgot Password?</Link></p>
      </div>
    </div>
  );
}

export default Login;
```

### Step 8: Create a Post List Component

Example `src/components/PostList.js`:

```jsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { postService } from '../services/api';

function PostList() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const fetchPosts = async (pageNum) => {
    try {
      setLoading(true);
      const response = await postService.getPosts(pageNum);
      
      if (pageNum === 1) {
        setPosts(response.data.results);
      } else {
        setPosts(prev => [...prev, ...response.data.results]);
      }
      
      setHasMore(!!response.data.next);
    } catch (err) {
      setError('Failed to load posts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts(page);
  }, [page]);

  const handleInteraction = async (postId, actionType, reactType = null) => {
    try {
      const data = { action_type: actionType };
      if (reactType) {
        data.react_type = reactType;
      }
      
      await postService.interactWithPost(postId, data);
      
      // Refresh the post list
      fetchPosts(1);
    } catch (err) {
      console.error('Failed to interact with post:', err);
    }
  };

  if (loading && posts.length === 0) {
    return <div>Loading posts...</div>;
  }

  if (error && posts.length === 0) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="post-list">
      {posts.map(post => (
        <div key={post.id} className="post-card">
          <div className="post-header">
            <h3><Link to={`/posts/${post.id}`}>{post.title}</Link></h3>
            <div className="post-meta">
              <span>By: {post.author}</span>
              <span>Type: {post.post_type}</span>
              <span>Created: {new Date(post.created_at).toLocaleDateString()}</span>
            </div>
          </div>
          
          <div className="post-content">
            <p>{post.content.substring(0, 200)}...</p>
            {post.image && <img src={post.image} alt={post.title} className="post-image" />}
          </div>
          
          <div className="post-tags">
            {post.tags.map(tag => (
              <span key={tag} className="tag">{tag}</span>
            ))}
          </div>
          
          <div className="post-actions">
            <div className="reactions">
              <button onClick={() => handleInteraction(post.id, 'react', 'like')} 
                className={post.user_reaction === 'like' ? 'active' : ''}>
                Like ({post.reacts_count})
              </button>
              <button onClick={() => handleInteraction(post.id, 'react', 'love')}
                className={post.user_reaction === 'love' ? 'active' : ''}>
                Love
              </button>
              <button onClick={() => handleInteraction(post.id, 'save')}
                className={post.is_saved ? 'active' : ''}>
                {post.is_saved ? 'Saved' : 'Save'}
              </button>
              <button onClick={() => handleInteraction(post.id, 'share')}>
                Share ({post.shares_count})
              </button>
            </div>
            <div className="comments-count">
              <Link to={`/posts/${post.id}`}>
                Comments ({post.comments_count})
              </Link>
            </div>
          </div>
        </div>
      ))}
      
      {hasMore && (
        <button 
          onClick={() => setPage(prev => prev + 1)}
          disabled={loading}
          className="load-more-btn"
        >
          {loading ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}

export default PostList;
```

### Step 9: Create a Basic Homepage

Example `src/pages/Home.js`:

```jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import PostList from '../components/PostList';

function Home() {
  const { currentUser, logout } = useAuth();

  return (
    <div className="home-container">
      <header className="app-header">
        <h1>CyMate</h1>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/create-post">New Post</Link>
          <Link to={`/profile/${currentUser.username}`}>Profile</Link>
          <button onClick={logout}>Logout</button>
        </nav>
      </header>

      <main>
        <h2>Latest Posts</h2>
        <PostList />
      </main>
    </div>
  );
}

export default Home;
```

### Step 10: Create Post Detail Page

Example `src/pages/PostDetail.js`:

```jsx
import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { postService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const commentSchema = Yup.object().shape({
  content: Yup.string().required('Comment text is required').max(2000, 'Maximum 2000 characters')
});

function PostDetail() {
  const { id } = useParams();
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        setLoading(true);
        const response = await postService.getPost(id);
        setPost(response.data);
      } catch (err) {
        setError('Failed to load post details');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [id]);

  const handleInteraction = async (actionType, reactType = null) => {
    try {
      const data = { action_type: actionType };
      if (reactType) {
        data.react_type = reactType;
      }
      
      const response = await postService.interactWithPost(id, data);
      setPost(response.data);
    } catch (err) {
      console.error('Failed to interact with post:', err);
    }
  };

  const handleComment = async (values, { resetForm }) => {
    try {
      await postService.commentOnPost(id, values);
      // Refresh post to show new comment
      const response = await postService.getPost(id);
      setPost(response.data);
      resetForm();
    } catch (err) {
      console.error('Failed to add comment:', err);
    }
  };

  if (loading) {
    return <div>Loading post...</div>;
  }

  if (error || !post) {
    return <div className="error-message">{error || 'Post not found'}</div>;
  }

  return (
    <div className="post-detail">
      <nav className="back-link">
        <Link to="/">← Back to Posts</Link>
      </nav>
      
      <article className="post">
        <header>
          <h1>{post.title}</h1>
          <div className="post-meta">
            <span>By: {post.author}</span>
            <span>Type: {post.post_type}</span>
            <span>Created: {new Date(post.created_at).toLocaleDateString()}</span>
          </div>
          
          {currentUser.username === post.author && (
            <div className="post-actions">
              <button onClick={() => navigate(`/posts/${id}/edit`)}>Edit Post</button>
            </div>
          )}
        </header>
        
        <div className="post-content">
          <p>{post.content}</p>
          {post.image && <img src={post.image} alt={post.title} className="post-image" />}
        </div>
        
        <div className="post-tags">
          {post.tags.map(tag => (
            <span key={tag} className="tag">{tag}</span>
          ))}
        </div>
        
        <div className="interaction-bar">
          <button 
            onClick={() => handleInteraction('react', 'like')}
            className={post.user_reaction === 'like' ? 'active' : ''}
          >
            Like ({post.reacts_count})
          </button>
          <button 
            onClick={() => handleInteraction('react', 'love')}
            className={post.user_reaction === 'love' ? 'active' : ''}
          >
            Love
          </button>
          <button 
            onClick={() => handleInteraction('save')}
            className={post.is_saved ? 'active' : ''}
          >
            {post.is_saved ? 'Saved' : 'Save'}
          </button>
          <button onClick={() => handleInteraction('share')}>
            Share ({post.shares_count})
          </button>
        </div>
      </article>
      
      <section className="comments-section">
        <h2>Comments ({post.comments_count})</h2>
        
        <Formik
          initialValues={{ content: '' }}
          validationSchema={commentSchema}
          onSubmit={handleComment}
        >
          {({ isSubmitting }) => (
            <Form className="comment-form">
              <div className="form-group">
                <Field 
                  as="textarea" 
                  name="content" 
                  placeholder="Add a comment..." 
                  className="form-control"
                />
                <ErrorMessage name="content" component="div" className="error" />
              </div>
              <button type="submit" disabled={isSubmitting} className="btn btn-primary">
                {isSubmitting ? 'Posting...' : 'Post Comment'}
              </button>
            </Form>
          )}
        </Formik>
        
        <div className="comments-list">
          {post.comments && post.comments.map(comment => (
            <div key={comment.id} className="comment">
              <div className="comment-header">
                <span className="comment-author">{comment.user}</span>
                <span className="comment-date">
                  {new Date(comment.created_at).toLocaleString()}
                </span>
              </div>
              <div className="comment-content">{comment.content}</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default PostDetail;
```

### Step 11: Add Basic CSS Styling

Create `src/index.css`:

```css
/* Base styles */
:root {
  --primary-color: #3498db;
  --secondary-color: #2c3e50;
  --accent-color: #e74c3c;
  --background-color: #f5f5f5;
  --card-color: #ffffff;
  --text-color: #333333;
  --border-color: #dddddd;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
  line-height: 1.6;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 15px;
}

/* Navigation */
.app-header {
  background-color: var(--secondary-color);
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-header nav {
  display: flex;
  gap: 20px;
}

.app-header a, .app-header button {
  color: white;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
}

.app-header a:hover, .app-header button:hover {
  text-decoration: underline;
}

/* Forms */
.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 16px;
}

textarea.form-control {
  min-height: 100px;
}

.error {
  color: var(--accent-color);
  font-size: 14px;
  margin-top: 5px;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:disabled {
  background-color: #a0a0a0;
  cursor: not-allowed;
}

/* Post list */
.post-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.post-card {
  background-color: var(--card-color);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.post-header h3 {
  margin-top: 0;
  margin-bottom: 10px;
}

.post-header a {
  color: var(--secondary-color);
  text-decoration: none;
}

.post-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
}

.post-content {
  margin-bottom: 15px;
}

.post-image {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 4px;
  margin-top: 10px;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.tag {
  background-color: #f0f0f0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.post-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 10px;
  border-top: 1px solid var(--border-color);
}

.reactions {
  display: flex;
  gap: 10px;
}

.reactions button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px 8px;
  border-radius: 4px;
}

.reactions button:hover {
  background-color: #f0f0f0;
}

.reactions button.active {
  background-color: #e1f5fe;
  color: var(--primary-color);
}

.load-more-btn {
  padding: 10px;
  background-color: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 15px auto;
  display: block;
  width: 150px;
}

/* Post detail */
.post-detail {
  max-width: 800px;
  margin: 20px auto;
  background-color: var(--card-color);
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  padding: 25px;
}

.back-link {
  margin-bottom: 20px;
}

.back-link a {
  color: var(--primary-color);
  text-decoration: none;
}

.interaction-bar {
  display: flex;
  gap: 15px;
  padding-top: 15px;
  border-top: 1px solid var(--border-color);
  margin-top: 20px;
}

.interaction-bar button {
  padding: 8px 12px;
  background: none;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
}

.interaction-bar button.active {
  background-color: #e1f5fe;
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.comments-section {
  margin-top: 30px;
}

.comment-form {
  margin-bottom: 20px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.comment {
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 6px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: bold;
}

.comment-date {
  font-size: 12px;
  color: #777;
}
```

### Step 12: Configure React App for Production

Create a `.env.production` file in your React app root:

```
REACT_APP_API_URL=https://your-production-api-url.com
```

### Step 13: Deployment Considerations

#### For Django Backend:

1. Set `DEBUG = False` in production
2. Use environment variables for sensitive settings:
   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
   ```
3. Use a production database like PostgreSQL
4. Configure CORS properly:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "https://yourdomain.com",
   ]
   CORS_ALLOW_CREDENTIALS = True
   ```
5. Set up proper static file serving
6. Use a production-ready server like Gunicorn behind Nginx

#### For React Frontend:

1. Build the production bundle:
   ```bash
   npm run build
   # or
   yarn build
   ```
2. Serve the static files using Nginx or a CDN
3. Consider using environment-specific variables for API endpoints

### Step 14: Final Notes

1. **Error Handling**: Consider implementing more robust error handling and loading states.
2. **Authentication**: Implement token refresh logic for long-lived sessions.
3. **Security**: Always validate user inputs and handle permissions carefully.
4. **Performance**: Consider implementing pagination, lazy loading, and caching where appropriate.
5. **Testing**: Write tests for your components and services.

This guide covers the basic setup to connect a React frontend with the Django backend. Feel free to expand and modify according to your specific requirements.
