# delete_unused_images()

## Positive cases

-   [x] deletes `ArticleImage` where `article=None` and `user=article.user`
-   [x] deletes `ArticleImage` not used in current content
-   [x] calls `extract_image_paths()`

## Negative cases

-   [x] does not delete `ArticleImage` still used in the content
-   [ x does not delete `ArticleImage` belonging to other users
