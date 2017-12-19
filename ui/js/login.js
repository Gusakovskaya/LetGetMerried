var submit_button = $("#submit-button")
submit_button.click(function( event ) {
    var data = {
        "username": $("#username").val(),
        "password": $("#password").val(),
    }

    $.ajax({
      type: "POST",
      url: '/api/users/login',
      data: data,
    });

});