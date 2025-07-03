const markdownData = JSON.parse(document.getElementById("markdown-data").textContent);
marked.setOptions({
    highlight: function (code) {
        return hljs.highlightAuto(code).value;
    },
});
document.getElementById("markdown-view").innerHTML = marked.parse(markdownData);
hljs.highlightAll();
