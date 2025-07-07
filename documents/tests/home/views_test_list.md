## HomeView

### Positive cases

-   [x] GET: home page renders successfully
-   [x] Response contains list of articles
-   [x] Context includes filter object (`filter`)
-   [x] Pagination works correctly when articles exceed paginate_by

### Negative cases

-   [x] Invalid GET parameter does not crash the view

## ArticleDetailView

### Positive cases

-   [x] GET: article detail page renders successfully
-   [x] Context contains article_detail
-   [x] Context contains article_html (HTML-converted markdown)

## Negative cases

-   [x] 404 when article does not exist

## ArticleCreateView

### Positive cases

-   [x] GET: create page renders successfully for logged-in user
-   [x] POST: article creation succeeds with valid data
-   [x] Success message is shown on successful creation
-   [x] context["is_update"] is False

### Negative cases

-   [x] GET: redirects to login when not authenticated
-   [x] POST: redirects to login when not authenticated
-   [x] POST: article creation fails with missing required fields
-   [x] Error messages are shown when form is invalid

## ArticleUpdateView

### Positive cases

-   [x] GET: update page renders successfully for authenticated user
-   [x] POST: article is updated successfully with valid data
-   [x] Context includes is_update=True
-   [x] modified_at is set automatically
-   [x] Shows success message after update

### Negative cases

-   [x] GET: unauthenticated user is redirected to login
-   [x] POST: unauthenticated user is redirected to login
-   [x] POST: post without_required_fields
-   [x] Error messages are shown on invalid form
-   [x] GET: authenticated user cannot access another user’s article
-   [x] POST: authenticated user cannot update another user’s article

## ArticleDeleteView

### Positive cases

-   [x] GET: delete confirmation page renders successfully
-   [x] POST: article is deleted with confirmation
-   [x] Success message is shown on successful delete
-   [x] Redirects to home page after successful delete

### Negative cases

-   [x] GET: unauthenticated user is redirected to login page
-   [x] POST: unauthenticated user is redirected to login page
-   [x] GET: authenticated user cannot access another user’s article
-   [x] POST: authenticated user cannot delete another user’s article
-   [x] Article with invalid PK returns 404
