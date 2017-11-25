function myfunc() {
    var st = $("#phraseDiv").text()
    st = "["+st.replace(/}\n{/g,"},\n{")+"]"
    $.ajax({url: "http://localhost:8000",
        type: "POST",
        data: JSON.stringify($.parseJSON(st)),
        contentType: "application/json; charset=utf-8",
        dataType: "JSON"});
}

window.setInterval(myfunc()
}, 1000);
