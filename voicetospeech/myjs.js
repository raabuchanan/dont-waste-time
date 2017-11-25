
function myfunc() {
    var st = $("#phraseDiv").text();
    st = "["+st.replace(/}\n{/g,"},\n{")+"]";
    $.ajax({url: "http://localhost:8000",
        type: "POST",
        data: JSON.stringify($.parseJSON(st)),
        contentType: "application/json; charset=utf-8",
        dataType: "JSON"});
}

window.setInterval(function(){myfunc()}, 1000);

function reset() {
    $.ajax({url: "http://localhost:8000/reset",
        type: "POST",
        dataType: "JSON"});
}

var but = document.getElementById('startBtn');
but.addEventListener("click", reset);

