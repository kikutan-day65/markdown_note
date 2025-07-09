// Get upload_article_images url
const uploadArticleImagesUrl = document.getElementById("markdown-form").dataset.uploadArticleImagesUrl;

function initEditor() {
    var editor = ace.edit("md-editor", {
        theme: "ace/theme/monokai",
        mode: "ace/mode/markdown",
        selectionStyle: "text",
        fontSize: 14,
        highlightActiveLine: true,
        highlightSelectedWord: true,
        showPrintMargin: false,
        showInvisibles: true,
    });

    var mdContent = document.getElementById("md-content");

    if (mdContent && mdContent.value.trim()) {
        editor.setValue(mdContent.value, -1);
    } else {
        editor.setValue("", -1);
    }

    var viewer = parseMarkdown(editor);

    fixScrollBar(editor, viewer);

    enableDragAndDrop(editor);

    editor.getSession().on("change", () => {
        parseMarkdown(editor);

        // Sync editor input to the textarea
        if (mdContent) {
            mdContent.value = editor.getValue();
        }
    });
}

function parseMarkdown(editor) {
    var viewer = document.getElementById("md-viewer");
    var data = editor.getValue();

    data = marked.parse(data);
    viewer.innerHTML = data;

    viewer.querySelectorAll("pre > code").forEach(function (block) {
        hljs.highlightElement(block);
    });

    return viewer;
}

function fixScrollBar(editor, viewer) {
    const session = editor.getSession();
    const renderer = editor.renderer;

    session.on("changeScrollTop", () => {
        const scrollTop = session.getScrollTop();

        const editorScrollHeight = renderer.layerConfig.maxHeight;
        const editorClientHeight = renderer.$size.scrollerHeight;
        const editorScrollable = editorScrollHeight - editorClientHeight;

        const ratio = editorScrollable > 0 ? scrollTop / editorScrollable : 0;

        const viewerScrollable = viewer.scrollHeight - viewer.clientHeight;
        viewer.scrollTop = ratio * viewerScrollable;
    });
}

function enableDragAndDrop(editor) {
    const editorElement = editor.container;
    editorElement.addEventListener("dragover", (ev) => {
        dragOverHandler(ev);
    });
    editorElement.addEventListener("drop", (ev) => {
        dropHandler(ev, editor);
    });
}

function dragOverHandler(ev) {
    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();
}

function dropHandler(ev, editor) {
    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();

    if (ev.dataTransfer.files) {
        // Use DataTransfer interface to access the file(s)
        [...ev.dataTransfer.files].forEach((file, i) => {
            if (isImageFile(file)) {
                console.log(`… file[${i}].name = ${file.name}`);
                uploadImages(file, editor);
            } else {
                alert("Allowed only image files");
            }
        });
    }
}

function isImageFile(file) {
    return file.type.startsWith("image/");
}

function uploadImages(file, editor) {
    const formData = new FormData();
    formData.append("image", file);

    fetch(uploadArticleImagesUrl, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken(),
        },
        credentials: "include",
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success && data.url) {
                editor.insert(`![alt text](${data.url})\n`);
            } else {
                alert("Image upload failed");
            }
        })
        .catch((err) => {
            console.error("Upload error", err);
        });
}

function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
            return decodeURIComponent(cookie.slice(name.length + 1));
        }
    }
    return "";
}

initEditor();
