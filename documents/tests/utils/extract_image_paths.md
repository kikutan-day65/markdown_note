# extract_image_paths()

## Positive cases

-   [x] extracts a valid image path from a single `img` tag

## Negative cases

-   [x] ignores `img` tags with `src` not matching the expected pattern
-   [x] returns an empty list when content does not contain `img` tag
