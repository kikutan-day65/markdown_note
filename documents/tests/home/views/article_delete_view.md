# ArticleDeleteView

### Positive cases

-   [x] GET: authenticated user → renders `common/delete.html` template
-   [x] POST: valid request → deletes the `Article` instance
-   [x] POST: valid request → redirects to `success_url`
-   [x] POST: valid request → shows `ARTICLE_DELETE_SUCCESS` message via Django messages framework

### Negative cases

-   [x] GET: unauthenticated user → redirects to `login_url`
-   [x] POST: unauthenticated user → redirects to `login_url`
-   [x] GET or POST: attempting to delete another user's `Article` → returns 404
