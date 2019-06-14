function getData(){
        $('#action').append('<img src="/static/img/leading.gif">');
        var username = $('#username').val();
        var password = $('#password').val();
        var message = JSON.stringify({
                "username": username,
                "password": password
            });

        $.ajax({
            url:'/authenticate',
            type:'POST',
            contentType: 'application/json',
            data : message,
            dataType:'json',
            error: function(response){
                $('#action').html('');
                if(response['status']==401)
                $('#action').append('<img width: 100px; height: 100px src="/static/img/cross.png" width="100" height="100"/>');
            if(response['status']==200){
                $('#action').append('<img width: 100px; height: 100px src="/static/img/check.png" width="100" height="100"/>');
                $('#action').append('<input  type="button" value="go to chat" onclick="location.href=\'chat.html\'" />');
                $('#action').append('<input  type="button" value="read messages" onclick="location.href=\'crud_messages.html\'" />');
            }


            }
        });
    }