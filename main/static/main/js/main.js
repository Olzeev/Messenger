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
                    $("#chat_list").append(`<li class="chat_list_element">
                                                <img class="chat_list_element_image" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSshtD-7RtqN_oJMs3UfPKF7SQaUDHZjkuQoA&usqp=CAU">
                                                <p class="chat_list_element_title">${response.users_found[i]}</p>
                                            </li>`)
                }
            }
        });
    });
});