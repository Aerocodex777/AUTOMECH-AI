# Authentication System

## Overview

AutoMech AI now includes a complete authentication flow with:
- Loading screen with progress animation
- Professional login page
- Session management
- Logout functionality

## Features

### 1. Loading Screen
- **Duration**: ~3 seconds
- **Progress bar**: Animated 0-100%
- **Status messages**: 
  - "Initializing AI Engine..."
  - "Loading Diagnostic Database..."
  - "Preparing Tools..."
  - "Ready to Diagnose"
- **Design**: Industrial orange theme with scanline animation

### 2. Login Page
- **Left Panel**: Branding with features showcase
- **Right Panel**: Login form
- **Demo Mode**: Quick access without credentials
- **Session Persistence**: Remembers logged-in users

### 3. User Session
- **Storage**: localStorage
- **Display**: Username shown in header
- **Logout**: Button in header to end session

## Usage

### For Users

#### First Time
1. App loads → Loading screen (3 seconds)
2. Login page appears
3. Options:
   - Enter username/password → Click "LOGIN"
   - Click "CONTINUE AS DEMO USER" for quick access

#### Returning Users
- If previously logged in, skips login page
- Goes directly to main app after loading screen

#### Logout
- Click "Logout" button in header
- Returns to login page
- Session cleared

### For Developers

#### Login Logic
```javascript
// Demo mode - accepts any credentials
// In production, replace with actual API call

const handleSubmit = (e) => {
  e.preventDefault()
  // Call backend API here
  // POST /api/auth/login
  // { username, password }
}
```

#### Session Check
```javascript
useEffect(() => {
  const savedUser = localStorage.getItem('automech_user')
  if (savedUser) {
    setIsLoggedIn(true)
  }
}, [])
```

#### Logout
```javascript
const handleLogout = () => {
  localStorage.removeItem('automech_user')
  setIsLoggedIn(false)
}
```

## Backend Integration (Future)

### Endpoints Needed

#### 1. Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}

Response:
{
  "token": "jwt_token",
  "user": {
    "id": 1,
    "username": "mechanic1",
    "role": "mechanic"
  }
}
```

#### 2. Verify Token
```http
GET /api/auth/verify
Authorization: Bearer {token}

Response:
{
  "valid": true,
  "user": { ... }
}
```

#### 3. Logout
```http
POST /api/auth/logout
Authorization: Bearer {token}

Response:
{
  "message": "Logged out successfully"
}
```

### Database Schema

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) DEFAULT 'user',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  token VARCHAR(255) UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Security Considerations

### Current (Demo Mode)
- ⚠️ No actual authentication
- ⚠️ Accepts any credentials
- ⚠️ No password encryption
- ⚠️ Session stored in localStorage (not secure)

### Production Requirements
1. **Password Hashing**: Use bcrypt or argon2
2. **JWT Tokens**: Implement proper token-based auth
3. **HTTPS**: Always use HTTPS in production
4. **Rate Limiting**: Prevent brute force attacks
5. **Session Expiry**: Auto-logout after inactivity
6. **CSRF Protection**: Add CSRF tokens
7. **Input Validation**: Sanitize all inputs

## Design Details

### Loading Screen
- **Background**: Deep dark (#080c12)
- **Logo**: Large wrench icon with orange gradient
- **Progress Bar**: Orange gradient with glow effect
- **Animation**: Floating logo, scanning line, pulsing glow

### Login Page
- **Layout**: Split screen (branding left, form right)
- **Branding Panel**:
  - Large AUTOMECH logo
  - Feature highlights with icons
  - Orange accent border on top
- **Form Panel**:
  - Clean input fields
  - Orange gradient login button
  - Demo mode button (dashed border)
  - Error messages in red
- **Background**: Animated grid pattern with orange glow

### Responsive Design
- **Desktop**: Side-by-side layout
- **Mobile**: Stacked layout, features hidden
- **Breakpoint**: 900px

## User Roles (Future)

### Mechanic
- Full diagnostic access
- Vehicle management
- History tracking
- Parts ordering

### Customer
- Limited diagnostic access
- View own vehicles only
- Read-only history

### Admin
- User management
- System configuration
- Analytics dashboard

## Testing

### Test Scenarios

1. **First Visit**
   - Loading screen → Login page → Main app

2. **Demo Login**
   - Click "CONTINUE AS DEMO USER"
   - Should login immediately

3. **Manual Login**
   - Enter any username/password
   - Should login after 1.5s

4. **Session Persistence**
   - Login → Refresh page
   - Should stay logged in

5. **Logout**
   - Click logout button
   - Should return to login page
   - Refresh → Should show login page

6. **Error Handling**
   - Submit empty form
   - Should show error message

## Customization

### Change Loading Duration
```javascript
// In LoadingScreen.jsx
const interval = setInterval(() => {
  setProgress(prev => {
    if (prev >= 100) return 100
    return prev + 2  // Change this value
  })
}, 30)  // Change this value (milliseconds)
```

### Change Login Delay
```javascript
// In LoginPage.jsx
setTimeout(() => {
  onLogin(username)
}, 1500)  // Change this value (milliseconds)
```

### Customize Branding
Edit `LoginPage.jsx`:
- Change logo icon
- Update feature list
- Modify colors in CSS

## Files Modified

- `frontend/src/App.jsx` - Added auth flow
- `frontend/src/components/LoadingScreen.jsx` - New
- `frontend/src/components/LoginPage.jsx` - New
- `frontend/src/App.css` - Added auth styles

## Next Steps

1. **Backend API**: Implement actual authentication endpoints
2. **Database**: Set up users table
3. **JWT**: Implement token-based auth
4. **Password Reset**: Add forgot password flow
5. **Registration**: Add new user signup
6. **2FA**: Optional two-factor authentication
7. **OAuth**: Social login (Google, Facebook)

## Summary

The authentication system provides a professional, secure-looking entry point to AutoMech AI. While currently in demo mode, it's designed to easily integrate with a real backend authentication system. The industrial orange theme is consistent throughout, creating a cohesive user experience from login to diagnosis.
