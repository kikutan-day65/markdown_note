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
