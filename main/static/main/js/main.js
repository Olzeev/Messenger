
id_reciever = -1
chat_list = []

function show_chat_list(){
    $.ajax({
        url: 'search_person', 
        type: 'get',
        data: {
            search_input_text: document.getElementById("search_input").value,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        }, 
        success: function(response) {
            $('#chat_list').empty()
            chat_list = []
            for (let i = 0; i < response.users_found.length; i++){
                user = response.users_found[i]  // 0 - username, 1 - status, 2 - avatar url, 3 - id
                text = `<li class="chat_list_element" id="chat_list_element_${i}" onclick="show_chat('${user[2]}', '${user[0]}', '${user[1]}', '${user[3]}', 
                                        '${i}', '${response.users_found.length}')">
                                            <img class="chat_list_element_image" src="${user[2]}">
                                            <div>
                                                <p class="chat_list_element_title">${user[0]}</p>
                                                <p class="chat_list_element_text">${user[1]}</p>
                                            </div>
                                            <div style="width: 10px; height: 10px; background-color: red; visibility="hidden""></div>
                                        </li>`
                $("#chat_list").append(text)
                chat_list.push([user[3], text])
            }
        }
    });
}

$(document).ready(function() {
    show_chat_list()
    let url = `WSS://${window.location.host}/ws/global-socket/`
    const chatSocket = new WebSocket(url)
    chatSocket.onmessage = function(e){
        let data = JSON.parse(e.data)
        if (data.type === 'chat'){
            
            $.ajax({
                url: 'get_id', 
                type: 'get', 
                data: {
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                }, 
                success: function(response){
                    if (data.id_reciever == response.id) {
                        if (id_reciever == data.id_sender){
                            $('#messages').append(
                                `<li class="message">
                                    <p class="message-box-0">${data.message}</p>
                                    
                                </li>`
                            )  
                            $("#messages").animate({
                                scrollTop: $(
                                  '#messages').get(0).scrollHeight
                            }, 500);
                        } else{
                            
                            for (var i = 0; i < chat_list.length; ++i){
                                if (chat_list[i][0] == data.id_sender){
                                    console.log(1)
                                }
                            }
                        }
                    } else if (data.id_sender == response.id){
                        $('#messages').append(
                            `<li class="message">
                                <p class="message-box-1">${data.message}</p>
                                
                            </li>`
                        )  
                        $("#messages").animate({
                            scrollTop: $(
                              '#messages').get(0).scrollHeight
                        }, 500);
                    } 
                }
            })

            

            
        }
    }

    $(document.getElementById("search_input")).change(show_chat_list);
    $(document.getElementById('chat-input')).change(function (){
        
        $.ajax({
            url: 'send_message', 
            type: 'get', 
            data: {
                message_text: document.getElementById("chat-input").value, 
                id: id_reciever,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            }, 
            success: function(response){
                chatSocket.send(JSON.stringify({
                    message: document.getElementById("chat-input").value,
                    time: response.time,
                    id_sender: response.id_sender, 
                    id_reciever: id_reciever
                }))
                
                document.getElementById("chat-input").value = ""
                
            }
        })
    
        
    })
    
});


function resize(){
    document.getElementById('messages').style.height = (parseInt(window.innerHeight) - 100).toString() + "px"
    document.getElementById('chat-input').style.width = (window.innerWidth - 120 - 40).toString() + "px"
    
}
$(window).on("resize", resize);
resize(); // call once initially


function readURL(input) {
    if (input.files && input.files[0]) {
  
        var reader = new FileReader();
  
        reader.onload = function(e) {
            $('.image-upload-wrap').hide();
    
            $('.file-upload-image').attr('src', e.target.result);
            $('.file-upload-content').show();
    
            $('.image-title').html(input.files[0].name);
        };
    
        reader.readAsDataURL(input.files[0]);
        
    } else {
        removeUpload();
    }
}
  
function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function () {
    $('.image-upload-wrap').addClass('image-dropping');
});

$('.image-upload-wrap').bind('dragleave', function () {
    $('.image-upload-wrap').removeClass('image-dropping');
});



function show_chat(avatar, username, status, id, chat_list_index, chat_list_length){
    $.ajax({
        url: 'get_messages', 
        type: 'get', 
        data: {
            id: id,  
            csrfmiddlewaretoken: '{{ csrf_token }}'
        }, 
        success: function(response){
            
            $('#messages').empty()

            id_reciever = id;
            messages = response.messages
            for (let i = 0; i < messages.length; ++i){
                $('#messages').append(
                    `<li class="message">
                        <p class="message-box-${messages[i][2]}">${messages[i][0]}</p>
                        
                    </li>`
                )  
            }
            $("#messages").animate({
                scrollTop: $(
                  '#messages').get(0).scrollHeight
            }, 1000);

            if (response.blocked){
                input = document.getElementById('chat-input')
                input.disabled = true;
                input.placeholder = 'Вы заблокировали этого пользователя'
                input.style.textAlign = 'center'
                document.getElementById('block_user_text').textContent = 'Разблокировать'
                document.getElementById('block_user').onclick = function(){
                    unblock_user(response.user_id)
                }
            } else{
                if (response.is_blocked){
                    input = document.getElementById('chat-input')
                    input.disabled = true;
                    input.placeholder = 'Пользователь ограничил общение с вами'
                    input.style.textAlign = 'center'
                }
            }
        }
    })

    chat = document.getElementById('chat');
    chat.style.marginLeft = "400px";

    document.getElementById('avatar').src = avatar;
    document.getElementById('chat-title-text').textContent = username
    
    document.getElementById('profile-avatar').src = avatar;
    document.getElementById('profile-status').textContent = status
    document.getElementById('profile-id').textContent = "@" + id
    document.getElementById('profile-username').textContent = username

    for (let i = 0; i < chat_list_length; ++i){
        document.getElementById(`chat_list_element_${i}`).style.backgroundColor = "#252525"
    }
    document.getElementById(`chat_list_element_${chat_list_index}`).style.backgroundColor = "#BE9E79"
    document.getElementById('exit_chat').onclick = function (){
        hide_chat(chat_list_index);
    }
    

}

function hide_chat(chat_list_index){
    chat = document.getElementById('chat');
    chat.style.marginLeft = "100%";
    document.getElementById(`chat_list_element_${chat_list_index}`).style.backgroundColor = "#252525";
    id_reciever = -1;
}


function show_profile(){
    document.getElementById('profile').style.visibility = "visible";
    document.getElementById('profile').style.opacity = "1";
    document.getElementById('main-content').style.filter = "blur(4px)"
}
document.getElementById('profile').onclick = function(e){
    if (e.target == this){
        document.getElementById('profile').style.visibility = "hidden";
        document.getElementById('profile').style.opacity = "0";
        document.getElementById('main-content').style.filter = "blur(0px)"
    }
}

function hide_profile(){
    document.getElementById('profile').style.visibility = "hidden";
    document.getElementById('profile').style.opacity = "0";
    document.getElementById('main-content').style.filter = "blur(0px)"
}

function block_user(user_id_blocking){
    user_id_blocked = document.getElementById('profile-id').textContent.substring(1)
    $.ajax({
        url: 'block_user', 
        type: 'get', 
        data: {
            user_id_blocking: user_id_blocking, 
            user_id_blocked: user_id_blocked, 
            csrfmiddlewaretoken: '{{ csrf_token }}'
        }, 
        success: function(response){
            element = document.getElementById('block_user')
            element.onclick = function(){
                unblock_user(user_id_blocking)
            }
            element_text = document.getElementById('block_user_text')
            element_text.textContent = "Разблокировать"
            
            input = document.getElementById('chat-input')
            input.disabled = true;
            input.placeholder = 'Вы заблокировали этого пользователя'
            input.style.color = '#FF4444'
            input.style.textAlign = 'center'
                
            
        }
    })
}
function unblock_user(user_id_unblocking){
    user_id_unblocked = document.getElementById('profile-id').textContent.substring(1)
    $.ajax({
        url: 'unblock_user', 
        type: 'get', 
        data: {
            user_id_unblocking: user_id_unblocking, 
            user_id_unblocked: user_id_unblocked, 
            csrfmiddlewaretoken: '{{ csrf_token }}'
        }, 
        success: function(response){
            element = document.getElementById('block_user')
            element.onclick = function(){
                block_user(user_id_unblocking)
            }
            element_text = document.getElementById('block_user_text')
            element_text.textContent = "Заблокировать"

            if (response.is_blocked){
                input = document.getElementById('chat-input')
                input.placeholder = 'Пользователь ограничил общение с вами'
            } else{
                input = document.getElementById('chat-input')
                input.disabled = false;
                input.placeholder = 'Сообщение...'
                input.style.color = 'white'
                input.style.textAlign = 'left'
            }
            
                
            
        }
    })
}

function show_warning_clear_history(user_id){
    el_to_remove = document.getElementById('clear_history_text')
    el_to_remove.remove()
    element = document.getElementById('clear_history')
    el_to_add = document.createElement("div")
    el_to_add.style.display = "flex"
    el_to_add.innerHTML = `<p id="clear-history-permission">Вы уверены?</p>
                        <button class='clear-history-button-yes' id="clear-history-permission-yes" onclick="clear_history('${user_id}')">Да</button>
                        <button class='clear-history-button-no' id="clear-history-permission-no" onclick="clear_history_show_initial('${user_id}')">Нет</button>`
    element.append(el_to_add)
}

function clear_history_show_initial(user_id){
    element = document.getElementById('clear_history')
    el_to_remove = document.getElementById('clear-history-permission')
    el_to_remove.remove()
    el_to_remove = document.getElementById('clear-history-permission-yes')
    el_to_remove.remove()
    el_to_remove = document.getElementById('clear-history-permission-no')
    el_to_remove.remove()
    el_to_add = document.createElement("p")
    el_to_add.innerHTML = `<p class="profile-text-dangerous" id="clear_history_text" onclick="show_warning_clear_history('${user_id}')">Очистить историю</p>`
    element.append(el_to_add)
}

function clear_history(user_id){
    $.ajax({
        url: 'clear_history', 
        type: 'get', 
        data: {
            user_id: document.getElementById('profile-id').textContent.substring(1)
        }, 
        success: function(response){
            $('#messages').empty()
            clear_history_show_initial(user_id)
        }
    })
}
