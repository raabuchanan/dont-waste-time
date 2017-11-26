



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
        console.log("First name: " + parsed[i+2])
        console.log("Last name: " + parsed[i+3])

        if(typeof parsed !== 'undefined' && i !== -1){
            document.getElementById("FirstName").value = parsed[i+2];
            document.getElementById("LastName").value = parsed[i+3];

            phraseDiv = document.getElementById("phraseDiv");

            phraseDiv.innerHTML = "";

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

        console.log("res: " + res)

        console.log("getAge" + parsed)

        var i = parsed.indexOf("years");


        console.log("Index " + i)
        console.log("Age: " + parsed[i-1])

        if(typeof parsed !== 'undefined' && i !== -1){
            document.getElementById("Age").value = parsed[i-1];


            phraseDiv = document.getElementById("phraseDiv");

            phraseDiv.innerHTML = "";



        }



    }



}


function getGender() {


    var str_text = $("#phraseDiv").text();
    

    if(str_text != ""){
        var json_text=$.parseJSON("["+str_text.replace(/}\n{/g,"},\n{")+"]");


        var res = '';
        for (var i = 0; i<json_text.length; i++) {
            res = res+" "+json_text[i]['DisplayText'];
        }


        var parsed = res.toLowerCase().replace(/[^a-zA-Z ]/g,"").split(" ")

        console.log("res: " + res)

        console.log("getgender" + parsed)

        var i = parsed.indexOf("male");

        if (i == -1){
            i = parsed.indexOf("mail");
            parsed[i] = "male"
        }


        if (i == -1){
            i = parsed.indexOf("female");
        }


        console.log("Index " + i)
        console.log("Age: " + parsed[i-1])

        if(typeof parsed !== 'undefined' && i !== -1){
            document.getElementById("Sex").value = parsed[i];


            phraseDiv = document.getElementById("phraseDiv");

            phraseDiv.innerHTML = "";



        }



    }



}