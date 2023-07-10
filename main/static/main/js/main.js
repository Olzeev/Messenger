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
                    $("#chat_list").append('<li class="chat_list_element">' + response.users_found[i] + '</li>')
                }
                
            }
        });
    });
});