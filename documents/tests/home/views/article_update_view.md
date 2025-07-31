# ArticleUpdateView

## Positive cases

-   [x] GET: authenticated user (own article) → renders `home/article_form.html` template
-   [x] GET: authenticated user (own article) → context includes `is_update=True`
-   [x] POST: valid form data → updates the `Article` instance
-   [x] POST: valid form data → calls `convert_to_html()`, `associate_images_with_article()` and `delete_unused_images()`
-   [x] POST: valid form data → redirects to `success_url`
-   [x] POST: valid form data → shows `ARTICLE_UPDATE_SUCCESS` message via Django messages framework

## Negative cases

-   [x] GET: authenticated user (other user's article) → returns 404
-   [x] POST: authenticated user (other user's article) → returns 404
-   [x] GET: unauthenticated user → redirects to `login_url`
-   [x] POST: unauthenticated user → redirects to `login_url`
-   [x] POST: missing required fields → `form_invalid()` is called
-   [x] POST: missing required fields → error messages are added using `messages.error()`
