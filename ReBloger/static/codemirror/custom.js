var editor;
$(document).ready(function () {
    $("#post_categorys").select2({
        theme: "classic"
    });
    $("#post_authors").select2({
        theme: "classic"
    });

    editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
        lineNumbers: true,
        mode: "markdown",
        theme: "neo",
        indentUnit: 4,
        lineWrapping: true
    });

    editor.on('change', function (cm, change) {
        var text = cm.getValue();
        var max = 20000;
        var remaining = max - text.length;
        var r = $("#content_remaining");
        r.html(remaining);
    });

    $("#topic_title").keyup(function (e) {
        var s = $("#topic_title");
        var text = s.val();
        var max = 120;
        var remaining = max - text.length;
        var r = $("#title_remaining");
        r.html(remaining);
    });

    if (post_content_md.length > 0) {
        editor.setValue(post_content_md);
    }
});