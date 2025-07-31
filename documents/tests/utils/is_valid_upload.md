# is_valid_upload()

## Positive cases

-   [x] valid image file with size < `MAX_IMAGE_SIZE` and file counts below limits → returns `(True, None)`

## Negative cases

-   [x] image file size > `MAX_IMAGE_SIZE` → returns `(False, IMAGE_SIZE_ERROR)`
-   [x] unassociated images >= `MAX_UNASSOCIATED_FILES_PER_USER` → returns `(False, MAX_UNASSOCIATED_FILES_ERROR)`
-   [x] total images >= `MAX_FILES_PER_USER` → returns `(False, MAX_FILES_ERROR)`
