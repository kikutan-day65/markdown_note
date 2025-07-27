# upload_article_images()

## Positive cases

-   [x] POST: authenticated user with valid image → returns 200 with `image_url`
-   [x] POST: authenticated user with valid image → creates `ArticleImage` with `user` and `article=None`
-   [x] POST: valid image upload → calls `is_valid_upload()` during processing

## Negative cases

-   [x] POST: unauthenticated user → returns 403 with error message from `forbid_anonymous`
-   [x] POST: authenticated user with no image file → returns 400 with `"Image was not uploaded"`
