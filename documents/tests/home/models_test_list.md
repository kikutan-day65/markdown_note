## Article

### Positive cases

-   [x] Creating an article with valid title, content, and user
-   [x] created_at is automatically set on save
-   [x] modified_at can be null and still save successfully
-   [x] `__str__` returns the article title
-   [x] Accessing related user’s articles via user.articles.all()

### Negative cases

-   [x] Fails to create article without required fields

## ArticleImage

### Positive cases

-   [x] Creating an article image linked to an article
-   [x] uploaded_at is automatically set on save
-   [x] Accessing article’s images via article.images.all()
