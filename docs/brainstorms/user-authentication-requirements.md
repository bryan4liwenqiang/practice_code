# User Authentication System – Requirements Document

**Document Date:** May 2026
**Status:** Ready for Planning
**Scope:** Adding email/password and social authentication to enable multi-device todo sync

---

## 1. Problem Statement

Users need to access their todos across multiple devices with data persisted in the cloud. Currently, todos are stored locally or in-memory. Adding authentication enables:
- **Multi-device sync** – Users can view and manage todos from phone, tablet, laptop
- **Data persistence** – Todos survive browser refresh, device changes, or app restart
- **Account control** – Users own their data; todos remain private until explicitly shared

---

## 2. Core User Flows

### 2.1 Signup / Registration
**Actors:** New user (prospective)

**Primary Flow:**
1. User clicks "Sign up" → lands on signup page
2. User sees two options: email/password OR social login (Google, GitHub)
3. **Email/password path:**
   - User enters email, password, password confirmation
   - System validates email format, password strength (minimum 8 chars, mixed case recommended)
   - On success: Account created, user auto-logged in, redirected to empty todo list
   - On error: Clear error message (email already in use, password too weak, etc.)
4. **Social login path (Google/GitHub):**
   - User clicks button → redirected to OAuth provider
   - After authorization, system creates account using provider email and unique provider ID
   - User auto-logged in, redirected to empty todo list

**Edge Cases:**
- Email already registered → Show "Account exists. Try logging in" with link to login
- User cancels OAuth flow → Return to signup page, no account created

### 2.2 Login
**Actors:** Returning user

**Primary Flow:**
1. User clicks "Log in" → lands on login page
2. User enters email and password
3. System authenticates:
   - Email found in database
   - Password hash matches stored value
4. On success: User session created, redirected to todo list
5. On error: Generic message "Email or password incorrect" (do not reveal which is wrong)

**Alternate Flow (Social Login):**
1. User clicks "Log in with Google/GitHub"
2. Redirected to provider → already logged in? Skips auth, auto-returns account
3. User auto-logged in, redirected to todo list

**Edge Cases:**
- Unverified email (if we add email verification later): Show message to verify email
- Account locked (too many failed attempts): Show message with unlock mechanism

### 2.3 Logout
**Actors:** Authenticated user

**Flow:**
1. User clicks "Log out" button (top nav or settings)
2. System invalidates session/token
3. User redirected to unauthenticated landing page
4. Local storage cleared (no todos visible without login)

### 2.4 Account Recovery
**Actors:** User who forgot password

**Flow:**
1. On login page, user clicks "Forgot password?"
2. User enters email address
3. System sends password-reset link (valid for 24 hours) to email
4. User clicks link in email → lands on password-reset form
5. User enters new password (validated for strength)
6. On success: Password updated, user directed to login

**Security Notes:**
- Reset link is single-use and time-limited
- If user tries expired link: Show "Link expired. Request a new reset."
- If user requests multiple resets: Only the most recent link is valid

---

## 3. Data & Persistence

### 3.1 User Identity
- **Email** (unique, indexed) – Used for login; case-insensitive
- **Password hash** – Stored using modern algorithm (bcrypt or Argon2)
- **Display name** (optional) – User's profile name, defaults to email domain
- **Created at** – Timestamp for account creation
- **Social provider links** (optional) – Google/GitHub ID, provider email

### 3.2 Session / Authentication Token
- System maintains active sessions or tokens (JWT recommended for stateless design)
- Tokens include: user ID, email, issued-at, expiration (e.g., 30 days)
- Logout invalidates token (blacklist or session revocation)
- **Secure cookie or localStorage with HttpOnly flag** to prevent XSS attacks

### 3.3 User-Specific Todos
- Todos linked to authenticated user_id
- Unauthenticated users cannot view, create, or modify todos
- **On login:** User sees only their todos (fresh start; no guest todo migration)
- **On logout:** Todo list cleared from UI

---

## 4. Security Requirements

### 4.1 Password Security
- Minimum 8 characters
- No stored passwords in logs or error messages
- Password hashed with bcrypt (cost ≥ 10) or Argon2
- Account lockout after 5 failed login attempts (unlock after 15 minutes or via email)

### 4.2 Session Security
- Sessions expire after 30 days of inactivity (configurable)
- Logout immediately invalidates session
- HttpOnly and Secure flags on auth cookies (if used)
- HTTPS-only communication (enforce at deployment)

### 4.3 Social Auth Security
- OAuth 2.0 best practices (PKCE for SPAs, etc.)
- Store provider ID + email; never store provider access tokens without explicit need
- Verify redirect URIs to prevent open redirect attacks

### 4.4 Data Privacy
- User todos are private by default
- No analytics or ads based on user todo content (unless explicitly opted in)
- Users can request data export or account deletion (future scope, but design for it)

---

## 5. Success Criteria

**Functional:**
- User can sign up with email/password and login from any device
- User can optionally login with Google or GitHub
- After login, user sees a fresh, empty todo list (no guest data)
- User can logout and their session is invalidated
- User can reset a forgotten password via email
- Two failed logins on the same IP/device do not lock the account

**Reliability:**
- Auth system is available 99.5% of the time (SLA target)
- Login completes within 1 second (< 500ms on fast connection)
- No user data loss on logout or session expiration

**Security:**
- Passwords are hashed before storage (no plain text in database)
- Sessions expire and cannot be reused
- Account lockout prevents brute force attacks
- OAuth tokens are never logged or exposed

**User Experience:**
- Signup + login pages are mobile-friendly and accessible (WCAG AA)
- Error messages are clear and actionable
- Transition from unauthenticated to authenticated is seamless

---

## 6. Scope Boundaries

### In This Release
- Email/password authentication
- Social login (Google, GitHub) – optional sign-up method
- Session management & logout
- Password recovery via email
- Basic account lockout (5 attempts, 15-min lockout)
- User-specific todo lists

### Deferred for Later
- Email address verification (send confirmation email on signup)
- Two-factor authentication (2FA)
- Password history / change history
- Biometric login (fingerprint, Face ID)
- Team/shared todos (requires role-based access design)
- Single sign-on (SSO) for enterprise users
- Account deletion or data export (data privacy UI)

### Outside This Product's Identity
- Social features (follow users, share todos, comments)
- Analytics dashboard on user activity
- Advertising or premium tier features

---

## 7. Design Principles for Future Expansion

To prepare for multi-user and team features later:
- **User-centric data model:** All todos are always linked to a user_id
- **Permission-ready schema:** Structure allows adding `shared_with` or `access_level` fields without data migration
- **Stateless auth:** Use tokens/JWTs so the system can scale to multiple backend servers
- **Email as user identifier:** Email is unique, but design to allow username/profile links later

---

## 8. Dependencies & Assumptions

**Assumptions:**
- Users have valid email addresses and can receive reset emails
- OAuth providers (Google, GitHub) remain available and stable
- HTTPS is enforced at deployment
- Email service is reliable and fast

**External Dependencies:**
- OAuth providers (Google, GitHub API)
- Email service for password resets
- Database for user and session storage
- Hashing library (bcrypt, Argon2)

**Unknowns / Risks:**
- Volume of concurrent logins (scalability unknown)
- Email delivery latency for password resets
- User preference: Will they choose social login or email/password?

---

## 9. Next Steps

1. **Planning phase:** Finalize tech stack, design data schema, plan API endpoints
2. **Implementation:** Build signup/login flows, integrate OAuth, add session middleware
3. **Testing:** Security testing, password reset flow validation, multi-device sync verification
4. **Launch:** Deploy with HTTPS, verify email service, monitor auth metrics

---

## Acceptance Criteria Checklist

- [ ] User can create account with email/password
- [ ] User can login with email/password from multiple devices
- [ ] User can optionally login with Google or GitHub
- [ ] User can logout and session is cleared
- [ ] User can reset forgotten password via email
- [ ] Todos created before login are not migrated (start fresh)
- [ ] All auth communication is over HTTPS
- [ ] Passwords are hashed (never stored plain-text)
- [ ] Account lockout works (5 attempts, 15 min lockout)
- [ ] Error messages are user-friendly and do not leak system info
