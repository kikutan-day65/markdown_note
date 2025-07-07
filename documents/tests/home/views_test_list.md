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
