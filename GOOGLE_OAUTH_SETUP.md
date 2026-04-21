# Google OAuth Setup Guide

## Overview

AutoMech AI now supports Google Sign-In for easy authentication. Users can log in with their Google account instead of creating separate credentials.

## Features

✅ One-click Google Sign-In
✅ Automatic profile picture display
✅ Secure JWT token handling
✅ Session persistence
✅ Seamless integration with existing auth flow

## Setup Instructions

### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. Create a new project (or select existing):
   - Click "Select a project" → "New Project"
   - Name: "AutoMech AI"
   - Click "Create"

3. Enable Google+ API:
   - Go to "APIs & Services" → "Library"
   - Search for "Google+ API"
   - Click "Enable"

4. Create OAuth Credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Web application"
   - Name: "AutoMech AI Web Client"
   
5. Configure Authorized Origins:
   ```
   http://localhost:5173
   http://localhost:3000
   http://127.0.0.1:5173
   ```
   
6. Configure Authorized Redirect URIs:
   ```
   http://localhost:5173
   http://localhost:3000
   ```

7. Click "Create"

8. Copy your Client ID (looks like: `1234567890-abc...xyz.apps.googleusercontent.com`)

### Step 2: Configure Frontend

1. Create `.env` file in `frontend/` directory:
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. Edit `frontend/.env`:
   ```env
   VITE_GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE.apps.googleusercontent.com
   ```

3. Replace `YOUR_CLIENT_ID_HERE` with your actual Client ID from Step 1

### Step 3: Restart Frontend

```bash
cd frontend
npm run dev
```

## How It Works

### User Flow

1. User opens app → Loading screen
2. Login page appears with 3 options:
   - **Username/Password** (demo mode)
   - **Google Sign-In** (OAuth)
   - **Demo User** (quick access)

3. User clicks "Sign in with Google"
4. Google popup appears
5. User selects Google account
6. App receives JWT token
7. Token is decoded to extract:
   - Name
   - Email
   - Profile picture
8. User is logged in
9. Profile picture shown in header

### Data Storage

```javascript
localStorage.setItem('automech_user', userName)
localStorage.setItem('automech_user_email', email)
localStorage.setItem('automech_user_picture', pictureUrl)
```

### Security

- JWT tokens are decoded client-side
- No passwords stored
- Google handles authentication
- Tokens expire automatically
- Session persists in localStorage

## Code Implementation

### Frontend Components

#### index.jsx
```javascript
import { GoogleOAuthProvider } from '@react-oauth/google'

<GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
  <App />
</GoogleOAuthProvider>
```

#### LoginPage.jsx
```javascript
import { GoogleLogin } from '@react-oauth/google'
import { jwtDecode } from 'jwt-decode'

const handleGoogleSuccess = (credentialResponse) => {
  const decoded = jwtDecode(credentialResponse.credential)
  const userName = decoded.name || decoded.email
  localStorage.setItem('automech_user', userName)
  localStorage.setItem('automech_user_email', decoded.email)
  localStorage.setItem('automech_user_picture', decoded.picture)
  onLogin(userName)
}

<GoogleLogin
  onSuccess={handleGoogleSuccess}
  onError={handleGoogleError}
  theme="filled_black"
  size="large"
/>
```

#### App.jsx
```javascript
const userPicture = localStorage.getItem('automech_user_picture')

{userPicture && (
  <img src={userPicture} alt="Profile" />
)}
```

## Testing

### Test Scenarios

1. **Google Sign-In Success**
   - Click "Sign in with Google"
   - Select Google account
   - Should login and show profile picture

2. **Google Sign-In Cancel**
   - Click "Sign in with Google"
   - Close popup without selecting account
   - Should show error message

3. **Session Persistence**
   - Login with Google
   - Refresh page
   - Should stay logged in with profile picture

4. **Logout**
   - Click logout button
   - Should clear all Google data
   - Return to login page

5. **Multiple Login Methods**
   - Try Google login
   - Logout
   - Try demo login
   - Should work seamlessly

## Troubleshooting

### Issue: "Invalid Client ID"

**Solution:**
- Check `.env` file has correct Client ID
- Restart frontend: `npm run dev`
- Clear browser cache

### Issue: "Redirect URI Mismatch"

**Solution:**
- Go to Google Cloud Console
- Add your exact URL to Authorized Redirect URIs
- Include both `http://localhost:5173` and `http://127.0.0.1:5173`

### Issue: "Google Sign-In button not showing"

**Solution:**
- Check console for errors
- Verify `@react-oauth/google` is installed: `npm list @react-oauth/google`
- Check internet connection (Google CDN required)

### Issue: "Token decode error"

**Solution:**
- Verify `jwt-decode` is installed: `npm list jwt-decode`
- Check browser console for specific error
- Try clearing localStorage: `localStorage.clear()`

## Production Deployment

### Update Authorized Origins

When deploying to production, add your domain:

```
https://yourdomain.com
https://www.yourdomain.com
```

### Environment Variables

Set production Client ID:

```env
VITE_GOOGLE_CLIENT_ID=your_production_client_id.apps.googleusercontent.com
```

### HTTPS Required

Google OAuth requires HTTPS in production. Use:
- Netlify
- Vercel
- AWS CloudFront
- Nginx with SSL certificate

## Backend Integration (Optional)

### Verify Google Token

```python
from google.oauth2 import id_token
from google.auth.transport import requests

def verify_google_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        return {
            'email': idinfo['email'],
            'name': idinfo['name'],
            'picture': idinfo['picture'],
            'sub': idinfo['sub']  # Unique Google ID
        }
    except ValueError:
        return None
```

### Store User in Database

```python
@app.post("/api/auth/google")
async def google_login(token: str, db: Session = Depends(get_db)):
    user_info = verify_google_token(token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Find or create user
    user = db.query(User).filter(User.email == user_info['email']).first()
    if not user:
        user = User(
            email=user_info['email'],
            name=user_info['name'],
            picture=user_info['picture'],
            google_id=user_info['sub']
        )
        db.add(user)
        db.commit()
    
    # Create session token
    token = create_jwt_token(user.id)
    return {"token": token, "user": user}
```

## Privacy & Compliance

### Data Collected

- Name (from Google profile)
- Email address
- Profile picture URL
- Google account ID

### Data Usage

- Authentication only
- No data shared with third parties
- Stored locally in browser
- Can be deleted anytime (logout)

### GDPR Compliance

- Users can delete data (logout)
- Clear privacy policy required
- Cookie consent banner recommended
- Data retention policy needed

## Benefits

### For Users
- ✅ No password to remember
- ✅ Fast one-click login
- ✅ Secure (Google handles auth)
- ✅ Profile picture automatically set
- ✅ Works across devices

### For Developers
- ✅ No password storage
- ✅ No password reset flow
- ✅ Reduced security risk
- ✅ Better user experience
- ✅ Easy to implement

## Limitations

- Requires internet connection
- Users must have Google account
- Popup blockers may interfere
- Third-party cookies must be enabled
- Google API rate limits apply

## Next Steps

1. ✅ Google OAuth implemented
2. ⏳ Add Facebook login
3. ⏳ Add GitHub login
4. ⏳ Add email/password registration
5. ⏳ Add password reset flow
6. ⏳ Add 2FA (two-factor authentication)
7. ⏳ Add role-based access control

## Resources

- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [React OAuth Library](https://www.npmjs.com/package/@react-oauth/google)
- [JWT Decode](https://www.npmjs.com/package/jwt-decode)
- [Google Cloud Console](https://console.cloud.google.com/)

## Support

For issues or questions:
1. Check browser console for errors
2. Verify Client ID configuration
3. Test with different Google accounts
4. Check Google Cloud Console quotas
5. Review authorized origins/redirects

## Summary

Google OAuth is now fully integrated into AutoMech AI! Users can sign in with their Google account for a seamless, secure authentication experience. The system automatically displays their profile picture and maintains their session across page refreshes.
