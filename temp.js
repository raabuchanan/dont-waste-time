var st = $("#phraseDiv").text();
    st = "["+st.replace(/}\n{/g,"},\n{")+"]";
$.parseJSON(st)

function getname(j) {
var res = '';
for (var i = 0; i<j.length; i++) {
res = res+" "+j[i]['DisplayText'];
}
var i = res.toLowerCase().replace(/[^a-zA-Z ]/g,"").split(" ");
if (i>0) {
return res[i+i];
} else {
return -1
}
}

