document.addEventListener("keydown", function (event) {
    // Go previous page with left arrow key
    if (event.key === "ArrowLeft") {
        const prevLink = document.getElementById("prev-page");
        if (prevLink) {
            window.location.href = prevLink.href;
        }
    }

    // Go next page with right arrow key
    if (event.key === "ArrowRight") {
        const nextLink = document.getElementById("next-page");
        if (nextLink) {
            window.location.href = nextLink.href;
        }
    }
});
