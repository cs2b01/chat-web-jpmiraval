var currentUserId = 0;
var userID=0;

function whoami(){
        $.ajax({
            url:'/current',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                $('#cu_username').html(response['username'])
                var name = response['name']+" "+response['fullname'];
                currentUserId = response['id'];
                $('#cu_name').html(name);
                allusers();
            },
            error: function(response){
                alert(JSON.stringify(response));
            }
        });
    }




    function allusers(){
            $.ajax({
                url:'/users',
                type:'GET',
                contentType: 'application/json',
                dataType:'json',
                success: function(response){
                    //alert(JSON.stringify(response));
                    var i = 0;
                    $.each(response, function(){
                        f = '<div class="alert alert-secondary" role="alert" onclick=loadMessages('+currentUserId+','+response[i].id+') >';
                        f = f + response[i].username;
                        f = f + '</div>';
                        i = i+1;
                        $('#allusers').append(f);
                    });
                },
                error: function(response){
                    alert(JSON.stringify(response));
                }
            });
    }

    function loadMessages(user_from_id, user_to_id){
            //alert(user_from_id);
            //alert(user_to_id);
            blank();


            $.ajax({
                url:'/messages/'+user_from_id+"/"+user_to_id,
                type:'GET',
                contentType: 'application/json',
                dataType:'json',

                success: function(response){
                  var i = 0;
document.getElementById("nombre_chat").innerHTML=user_to_id
                  $.each(response, function(){
                      f = '<div id='+i+'>';
                      f = f + response[i].content;
                      f = f + '</div>';
                      i = i+1;
                      $('#messages').append(f);
                  });
                },
                error: function(response){
                    alert(JSON.stringify(response));
                }
            });
    }

    function blank(){
       document.getElementById("messages").innerHTML="";
    }

    function sendMessage(){
    var nombre_chat = document.getElementById("nombre_chat").innerHTML;


            $.ajax({
                url:'/users',
                type:'GET',
                contentType: 'application/json',
                dataType:'json',
                success: function(response){
                    var i = 0;
                    $.each(response, function(){

                       if(response[i].id == nombre_chat){
                       send(response[i].id);
                       }
                       i=i+1;

                    });
                },
                error: function(response){
                    alert(JSON.stringify(response));
                }
            });
}

    function send(id){
    var mensaje = $('#contenido').val();
            var message = JSON.stringify({
                    "content": mensaje,
                    "user_from_id": currentUserId,
                    "user_to_id": id,
                });

           $.ajax({
                     url:'/sendMessage',
                     type:'POST',
                     contentType: 'application/json',
                     data : message,
                     dataType:'json'
                   });

                   loadMessages(currentUserId, id);
    }
