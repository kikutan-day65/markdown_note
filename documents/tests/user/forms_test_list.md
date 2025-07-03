## Register form

### Positive cases

-   [x] Registering user with valid data

### Negative cases

-   [x] Registering user without required fields
-   [x] Password1 and Password2 don't match
-   [x] Password1 is blank or only white space
-   [x] Registering with existent username

## Login form

### Positive cases

-   [x] Login user with username
-   [x] Login user with email

### Negative cases

-   [x] Login user with non-existent user
-   [x] Login user with username and wrong password
-   [x] Login user without required fields
-   [x] Login user with non-existent email
-   [x] Login user with email and wrong password

## Update form

### Positive cases

-   [x] Update user with valid data

### Negative cases

-   [x] Update with existent username
-   [x] Update without required fields

## Password change form

### Positive cases

-   [x] Update password with valid data

### Negative cases

-   [x] Change password without required fields
-   [x] Change password with the same as old one
-   [x] Change password with the wrong old password
-   [x] Change password with new password mismatch
-   [x] Change password with weak one
