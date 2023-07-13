$(document).ready(function() {
    $(document.getElementById("search_input")).change(function(){
        $.ajax({
            url: 'search_person', 
            type: 'get',
            data: {
                search_input_text: document.getElementById("search_input").value,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            }, 
            success: function(response) {
                $('#chat_list').empty()
                for (let i = 0; i < response.users_found.length; i++){
                    user = response.users_found[i]  // 0 - username, 1 - status, 2 - avatar url, 3 - id
                    $("#chat_list").append(`<li class="chat_list_element" id="chat_list_element_${i}" onclick="show_chat('${user[2]}', '${user[0]}', '${user[1]}', '${user[3]}', 
                                            '${i}', '${response.users_found.length}')">
                                                <img class="chat_list_element_image" src="${user[2]}">
                                                <div>
                                                    <p class="chat_list_element_title">${user[0]}</p>
                                                    <p class="chat_list_element_text">${user[1]}</p>
                                                </div>
                                                
                                            </li>`)
                }
            }
        });
    });
    $(document.getElementById('chat-input')).change(function (){
        $.ajax({
            url: 'send_message', 
            type: 'get', 
            data: {
                message_text: document.getElementById("chat-input").value, 
                id: document.getElementById('profile-id').textContent, 
                csrfmiddlewaretoken: '{{ csrf_token }}'
            }, 
            success: function(response){
                document.getElementById("chat-input").value = ""
            }
        })
    })
    
});



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
    chat = document.getElementById('chat');
    chat.style.marginLeft = "400px";

    document.getElementById('avatar').src = avatar;
    document.getElementById('chat-title-text').textContent = username
    document.getElementById('chat-input').style.width = (window.screen.width - 400 - 250).toString() + "px"
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
