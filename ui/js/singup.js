var input = document.getElementById('location');
var autocomplete = new google.maps.places.Autocomplete(input);

var submit_button = $("#submit-button")
submit_button.click(function( event ) {
    console.log("SUBMIT BUTTON");

    var data = {
        "username": $("#username").val(),
        "email": $("#email").val(),
        "password": $("#password").val(),
        "twitter_handle": $("#twitter-handle").val()
    }

    var place = autocomplete.getPlace();
    if (place) {
        console.log("I AM IN PLACE!!!")
        data["latitude"] = place.geometry.location.lat();
        data["longitude"] = place.geometry.location.lng();
    }

    console.log(data);

    $.ajax({
      type: "POST",
      url: '/api/users',
      data: data,
    });
});