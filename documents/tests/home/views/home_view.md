# HomeView

### Positive cases

-   [x] GET: renders `home/home.html` template
-   [x] GET: context includes `articles` (paginated queryset of `Article`)
-   [x] GET: articles are ordered by `-created_at`
-   [x] GET: paginates results (10 articles per page)
-   [x] GET: filters articles via `ArticleFilter`

### Negative cases

-   [x] GET: page query parameter is out of range → returns 404
