// template/upload.html

$('button').click(function(){
	document.getElementById("output").innerHTML = '';
    document.getElementById("error").innerHTML = '';
   
    // if the file input not empty,
    if (!($('#file')[0].files.length === 0)){
        var out = '';
        var err = '';
        var datatype = $("#datatype").val();
        var formData = new FormData($('#uploadForm')[0]);

        if (datatype === 'user'){
            var url = '/up_user'  ; 
        } else if (datatype === 'staycation') {
            var url = '/up_staycation';  
        } else {
            var url = '/up_booking';
        }

        $.ajax({
            url:url,
            type: "POST",
            data: formData,
            async: true,
            cashe: false,
            contentType:false,
            processData:false,
            success:function (response) {
                if (response['status'] === 'OK'){
                    for (var i=0; i<response['message'].length; i++ ){
                        if (response['message'][i].includes('Missing') || response['message'][i].includes('existing')){
                            err += response['message'][i] + '<br>';
                        } else {
                            out += response['message'][i] + '<br>';
                        }
                    }
                    document.getElementById("output").innerHTML = out;
                    document.getElementById("error").innerHTML = err;
                } else {
                    for (var i=0; i<response['message'].length; i++ ){
                        err += response['message'][i] + '<br>';
                    }
                    document.getElementById("error").innerHTML = err;
                }
        　　}, 
　　         error: function (response) { 
                document.getElementById("error").innerHTML = 'Upload failed!';
　 　        }
        });
    } else {
        document.getElementById("error").innerHTML = 'Please select a file to upload';
    }
});