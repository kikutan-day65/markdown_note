# ArticleDetailView

### Positive cases

-   [x] GET: existing `Article` → renders `home/article_detail.html` template
-   [x] GET: existing `Article` → context includes `article_detail`

### Negative cases

-   [x] GET: non-existent `Article` (invalid `pk`) → returns 404
