# Secure Authentication System

## Overview

AutoMech AI now has a **highly secure** authentication system with:
- ✅ User registration with email validation
- ✅ Secure password hashing (bcrypt)
- ✅ JWT token-based authentication
- ✅ Database storage (SQLite/PostgreSQL)
- ✅ Session management
- ✅ No demo/bypass modes

## Security Features

### 1. Password Security
- **Bcrypt Hashing**: Passwords are hashed using bcrypt with salt
- **Minimum Length**: 8 characters required
- **Never Stored Plain**: Only hashed passwords in database
- **One-way Encryption**: Cannot be reversed

### 2. JWT Tokens
- **Secure Tokens**: JSON Web Tokens for session management
- **Expiration**: 7 days (configurable)
- **Secret Key**: 32+ character secret key
- **Signed**: Cryptographically signed to prevent tampering

### 3. Database Security
- **Unique Constraints**: Username and email must be unique
- **Indexed Fields**: Fast lookups, prevent duplicates
- **Active Status**: Can deactivate accounts
- **Last Login Tracking**: Monitor account activity

### 4. API Security
- **Bearer Authentication**: Token required for protected routes
- **HTTPS Ready**: Designed for SSL/TLS
- **CORS Protection**: Configured allowed origins
- **Input Validation**: Pydantic models validate all inputs

## User Flow

### Registration
1. User clicks "Don't have an account? Register"
2. Fills form:
   - Username (required, unique)
   - Email (required, unique, validated)
   - Password (required, min 8 chars)
   - Confirm Password (must match)
   - Full Name (optional)
3. Backend validates and creates account
4. Password is hashed with bcrypt
5. User record saved to database
6. JWT token generated and returned
7. User automatically logged in

### Login
1. User enters username and password
2. Backend finds user by username
3. Password verified against hash
4. JWT token generated
5. Last login timestamp updated
6. Token returned to frontend
7. Token stored in localStorage

### Session Management
- Token stored in `localStorage`
- Sent with every API request
- Backend verifies token
- Auto-logout on token expiration

## API Endpoints

### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "mechanic1",
  "email": "mechanic@example.com",
  "password": "SecurePass123",
  "full_name": "John Mechanic"
}

Response 200:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "mechanic1",
    "email": "mechanic@example.com",
    "full_name": "John Mechanic",
    "created_at": "2024-01-01T00:00:00"
  }
}

Error 400:
{
  "detail": "Username already registered"
}
{
  "detail": "Email already registered"
}
{
  "detail": "Password must be at least 8 characters long"
}
```

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "mechanic1",
  "password": "SecurePass123"
}

Response 200:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "mechanic1",
    "email": "mechanic@example.com",
    "full_name": "John Mechanic",
    "created_at": "2024-01-01T00:00:00"
  }
}

Error 401:
{
  "detail": "Incorrect username or password"
}

Error 403:
{
  "detail": "Account is inactive"
}
```

### Get Current User
```http
GET /api/auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

Response 200:
{
  "id": 1,
  "username": "mechanic1",
  "email": "mechanic@example.com",
  "full_name": "John Mechanic",
  "created_at": "2024-01-01T00:00:00"
}

Error 401:
{
  "detail": "Invalid or expired token"
}
```

## Database Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    full_name VARCHAR,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

## Configuration

### Backend (.env)
```env
# JWT Secret Key - CHANGE THIS IN PRODUCTION!
JWT_SECRET_KEY=your-super-secret-key-min-32-characters-long-change-in-production

# Token expiration (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

### Generate Secure Secret Key
```python
import secrets
print(secrets.token_urlsafe(32))
```

Or use:
```bash
openssl rand -hex 32
```

## Frontend Integration

### Registration
```javascript
const response = await axios.post('http://localhost:8000/api/auth/register', {
  username: 'mechanic1',
  email: 'mechanic@example.com',
  password: 'SecurePass123',
  full_name: 'John Mechanic'
})

localStorage.setItem('automech_token', response.data.access_token)
localStorage.setItem('automech_user', response.data.user.username)
```

### Login
```javascript
const response = await axios.post('http://localhost:8000/api/auth/login', {
  username: 'mechanic1',
  password: 'SecurePass123'
})

localStorage.setItem('automech_token', response.data.access_token)
localStorage.setItem('automech_user', response.data.user.username)
```

### Authenticated Requests
```javascript
const token = localStorage.getItem('automech_token')

const response = await axios.get('http://localhost:8000/api/auth/me', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
```

## Security Best Practices

### Production Checklist

1. **Change JWT Secret**
   ```env
   JWT_SECRET_KEY=<generate-new-32+-char-secret>
   ```

2. **Use HTTPS**
   - Never send tokens over HTTP
   - Use SSL/TLS certificates
   - Redirect HTTP to HTTPS

3. **Secure Headers**
   ```python
   app.add_middleware(
       SecurityHeadersMiddleware,
       csp="default-src 'self'",
       hsts="max-age=31536000; includeSubDomains"
   )
   ```

4. **Rate Limiting**
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/api/auth/login")
   @limiter.limit("5/minute")
   async def login(...):
       ...
   ```

5. **Password Requirements**
   - Minimum 8 characters (current)
   - Consider: uppercase, lowercase, numbers, symbols
   - Implement password strength meter

6. **Account Lockout**
   - Lock after N failed attempts
   - Temporary lockout (15-30 minutes)
   - Email notification on lockout

7. **Email Verification**
   - Send verification email on registration
   - Require email confirmation before login
   - Resend verification option

8. **Two-Factor Authentication (2FA)**
   - TOTP (Time-based One-Time Password)
   - SMS verification
   - Backup codes

9. **Session Management**
   - Logout endpoint to invalidate tokens
   - Refresh tokens for long sessions
   - Device tracking

10. **Audit Logging**
    - Log all authentication attempts
    - Track IP addresses
    - Monitor suspicious activity

## Testing

### Test Registration
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123",
    "full_name": "Test User"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123"
  }'
```

### Test Protected Route
```bash
TOKEN="your_token_here"

curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

## Troubleshooting

### "Username already registered"
- Username must be unique
- Try different username
- Check database for existing users

### "Email already registered"
- Email must be unique
- Use different email
- Check if you already have an account

### "Password must be at least 8 characters"
- Password too short
- Use minimum 8 characters
- Consider longer for better security

### "Incorrect username or password"
- Check username spelling
- Check password (case-sensitive)
- Verify account exists

### "Invalid or expired token"
- Token expired (7 days default)
- Token corrupted
- Login again to get new token

### "Account is inactive"
- Account has been deactivated
- Contact administrator
- Check is_active field in database

## Migration from Demo Mode

If you had demo mode before:

1. **Clear Old Data**
   ```javascript
   localStorage.removeItem('automech_user')
   localStorage.removeItem('automech_user_email')
   localStorage.removeItem('automech_user_picture')
   ```

2. **Register New Account**
   - Use registration form
   - Create secure password
   - Verify email

3. **Login**
   - Use new credentials
   - Token will be stored automatically

## Database Management

### View Users
```sql
SELECT id, username, email, full_name, created_at, last_login 
FROM users;
```

### Deactivate User
```sql
UPDATE users 
SET is_active = 0 
WHERE username = 'baduser';
```

### Reset Password (Manual)
```python
from auth import get_password_hash

new_hash = get_password_hash("NewPassword123")
# Update in database
```

### Delete User
```sql
DELETE FROM users WHERE username = 'testuser';
```

## Performance

- **Bcrypt**: ~100ms per hash (intentionally slow)
- **JWT Generation**: <1ms
- **Token Verification**: <1ms
- **Database Lookup**: <10ms (indexed)

## Compliance

### GDPR
- Users can request data deletion
- Export user data on request
- Clear privacy policy required
- Cookie consent for tokens

### Data Retention
- Keep user data as long as account active
- Delete on account deletion request
- Archive inactive accounts after N days

## Summary

AutoMech AI now has enterprise-grade authentication:
- 🔒 Secure password hashing
- 🎫 JWT token authentication
- 💾 Database-backed user management
- ✅ Email validation
- 🚫 No bypass/demo modes
- 🛡️ Production-ready security

Users must register before accessing the system. All passwords are securely hashed and never stored in plain text. JWT tokens provide secure, stateless authentication.
