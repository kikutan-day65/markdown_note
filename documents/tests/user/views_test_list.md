## Register view

### Positive cases

-   [x] GET: register page renders successfully
-   [x] POST: user registration succeeds with valid data
-   [x] Success message is shown on successful registration
-   [x] Context contains `register_form`

### Negative cases

-   [x] POST: registration fails with missing required fields
-   [x] POST: registration fails with duplicate username
-   [x] POST: registration fails with mismatched passwords

## Login view

### Positive cases

-   [x]GET: login page renders successfully
-   [x] POST: login with valid username and password
-   [x] POST: login with valid email and password
-   [x] Success message is shown on successful login
-   [x] Context contains `login_form`

### Negative cases

-   [x] POST: login fails with missing required fields
-   [x] POST login fails with wrong password
-   [x] POST login fails with wrong username/email
-   [x] POST login fails with username/email but empty password

## Logout view

### Positive cases

-   [x] GET: logout successfully redirects to home page
-   [x] User is no longer authenticated after logout
-   [x] Logout success message is shown via signal

## User Detail view

### Positive cases

-   [x] GET: detail page renders successfully
-   [x] Correct template is used
-   [x] Context contains correct user object

### Negative cases

-   [x] GET: non-existent user returns 404

## User password change view

### Positive cases

-   [x] GET: Authenticated user can access the password change page
-   [x] POST: Valid old password and matching new passwords
-   [x] Password change success message is shown via signal

# Negative cases

-   [x] GET: unauthenticated user is redirected to login page
-   [x] POST: unauthenticated user is redirected to login page
-   [x] POST: form is invalid with incorrect old password
-   [x] POST: form is invalid with mismatched new passwords

## User Delete view

### Positive cases

-   [x] GET: delete confirmation page renders successfully for logged-in user
-   [x] POST: user is successfully deleted after confirmation
-   [x] Success message is shown after deletion
-   [x] Context includes user_delete flag

### Negative cases

-   [x] GET: unauthenticated user is redirected to login page
-   [x] POST: unauthenticated user cannot delete account
-   [x] GET: authenticated user cannot delete another user’s account
-   [x] POST: authenticated user cannot delete another user’s account

## User update view

### Positive cases

-   [x] GET: update page renders successfully
-   [x] Context contains user_update_form
-   [x] POST: user info is updated with valid data
-   [x] Success message is shown

### Negative cases

-   [x] GET: unauthenticated user is redirected to login page
-   [x] POST: unauthenticated user is redirected to login page
-   [x] GET: other user’s pk returns 404
-   [x] POST: other user’s pk returns 404
-   [x] POST: duplicate username results in validation error
-   [x] POST: required fields missing

## Password reset view

### Positive cases

-   [x] GET: reset page renders successfully
-   [x] Context contains password_reset_form
-   [x] POST: valid email sends reset mail and redirects

### Negative

-   [x] POST: missing email field

## Password reset done view

### Positive cases

-   [x] GET: done page renders successfully

## Password reset confirm view

### Positive cases

-   [x] GET with valid token and uid returns 200
-   [x] Template user/user_password_reset_confirm.html is used
-   [x] Context contains password_reset_confirm_form
-   [x] POST with matching valid passwords resets password
-   [x] redirect to the password reset complete page

### Negative cases

-   [x] invalid or expired token shows error
-   [x] POST with mismatched passwords returns validation error
-   [x] POST with weak or invalid password returns validation error
-   [x] POST with missing required fields returns validation error

## Password reset complete view

### Positive cases

-   [x] GET: Password reset complete page renders successfully
