// Get upload_article_images url
const uploadArticleImagesUrl = document.getElementById("markdown-form").dataset.uploadArticleImagesUrl;

function initEditor() {
    // Ace editor settings
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

    // Check if markdown_content exists
    //      If true → set it in the editor
    //      If false → set an empty string in the editor
    var mdContent = document.getElementById("md-content");
    if (mdContent && mdContent.value.trim()) {
        editor.setValue(mdContent.value);
    } else {
        editor.setValue("");
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

async function dropHandler(ev, editor) {
    // Prevent default behavior (Prevent file from being opened)
    ev.preventDefault();

    if (ev.dataTransfer.files) {
        // List of files added by user
        const files = [...ev.dataTransfer.files];

        for (const file of files) {
            // Check if its filetype and filesize
            if (isImageFile(file) && isLessThan3MB(file)) {
                const uploadSuccess = await uploadImages(file, editor);
                if (!uploadSuccess) {
                    break;
                }
            } else {
                alert("Only image files smaller than 3MB are allowed.");
                break;
            }
        }
    }
}

function isImageFile(file) {
    return file.type.startsWith("image/");
}

function isLessThan3MB(file) {
    return file.size <= 3 * 1024 * 1024;
}

async function uploadImages(file, editor) {
    try {
        const formData = new FormData();

        // Enable to access the image with request.FILES["image"]
        formData.append("image", file);

        const response = await fetch(uploadArticleImagesUrl, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCSRFToken(),
            },
            credentials: "include",
        });

        const data = await response.json();
        if (response.ok && data.image_url) {
            editor.insert(`![alt text](${data.image_url})\n`);
            return true;
        } else {
            alert(data.error || "Upload failed");
            return false;
        }
    } catch (err) {
        console.log(err);
        return false;
    }
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
