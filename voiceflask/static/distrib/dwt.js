



function getName() {


    var str_text = $("#phraseDiv").text();
    

    if(str_text != ""){
        var json_text=$.parseJSON("["+str_text.replace(/}\n{/g,"},\n{")+"]");


        var res = '';
        for (var i = 0; i<json_text.length; i++) {
            res = res+" "+json_text[i]['DisplayText'];
        }


        var parsed = res.toLowerCase().replace(/[^a-zA-Z ]/g,"").split(" ")

        console.log("getName" + parsed)

        var i = parsed.indexOf("name");


        console.log("Index " + i)
        console.log("First name: " + parsed[i+1])
        console.log("Last name: " + parsed[i+2])

        if(typeof parsed !== 'undefined' && i !== -1){
            document.getElementById("FirstName").value = parsed[i+1];
            document.getElementById("LastName").value = parsed[i+2];
        } else{
            document.getElementById("FirstName").value = "Russell";
            document.getElementById("LastName").value = "Buchanan";
        }



    }

}


function getAge() {


    var str_text = $("#phraseDiv").text();
    

    if(str_text != ""){
        var json_text=$.parseJSON("["+str_text.replace(/}\n{/g,"},\n{")+"]");


        var res = '';
        for (var i = 0; i<json_text.length; i++) {
            res = res+" "+json_text[i]['DisplayText'];
        }


        var parsed = res.toLowerCase().replace(/[^a-zA-Z0-9 ]/g,"").split(" ")

        console.log("getName" + parsed)

        var i = parsed.indexOf("years");


        console.log("Index " + i)
        console.log("Age: " + parsed[i-1])

        if(typeof parsed !== 'undefined' && i !== -1){
            document.getElementById("Age").value = parsed[i-1];
        } else{
            document.getElementById("Age").value = "24";
        }



    }

}