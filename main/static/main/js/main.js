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
                    user = response.users_found[i]
                    $("#chat_list").append(`<li class="chat_list_element">
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