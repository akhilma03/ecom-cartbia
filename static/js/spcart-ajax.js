$(document).ready(function(){
    $("form").submit(function(e) {
        e.preventDefault();
        let actionurl = $('form button').parent().prop('action');
        $.ajax({
            type: "POST",
            url: actionurl,
            data: $('form').serialize(), // serializes the form's elements.
            success: function(data)
            {
            alert(data); // show response from the php script.
            }
        });
    });
});
