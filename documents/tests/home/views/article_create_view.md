# CreateArticleView

### Positive cases

-   [x] GET: authenticated user → renders `home/article_form.html` template
-   [x] GET: authenticated user → context includes `is_update=False`
-   [x] POST: valid form data → creates `Article` instance
-   [x] POST: valid form data → calls `convert_to_html()`, `associate_images_with_article()` and `delete_unused_images()`
-   [x] POST: valid form data → redirects to `success_url`
-   [x] POST: valid form data → shows `ARTICLE_CREATE_SUCCESS` message via Django messages framework

### Negative cases

-   [x] GET: unauthenticated user → redirects to `login_url`
-   [x] POST: unauthenticated user → redirects to `login_url`
-   [x] POST: missing required fields → `form_invalid()` is called
-   [x] POST: missing required fields → error messages are added using `messages.error()`
