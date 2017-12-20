$.ajax({
  type: "GET",
  url: '/api/users/is-auth',
  success: function(data) {
    console.log(data);
    var image = $('#logo');
    image.attr('src', data.image);

    $('#username').text(data.username);
    $('#email').text(data.email);
    $('#twitter-handle').text(data.twitter_handle);
    $('#location').text(data.location);

    var geocoder = new google.maps.Geocoder();

    var latlng = new google.maps.LatLng(data.latitude, data.longitude);
    geocoder.geocode({
        'latLng': latlng
    }, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
          if (results[1]) {
             $('#location').text(results[1].formatted_address);
          } else {
            $('#location').text('No results found');
          }
        } else {
          $('#location').text('Geocoder failed');
        }
      }
    )
    var update_button = $('#update-data')
    update_button.on('click', function(e) {
        console.log(e);
        $.ajax({
        type: "POST",
        url: '/api/users/' + data.id + '/update-statistics',
        success: function(data) {
            var needs = data.statistics.needs;
            for (var i = 0; i < needs.length; i++) {
                var percentile = Math.floor(needs[i].percentile * 100);
                console.log(percentile);

                if (percentile >= 0 && percentile <= 25) {
                    $('#' + needs[i].name).addClass('progress-bar-danger');
                }

                if (percentile >= 25 && percentile <= 50) {
                    $('#' + needs[i].name).addClass('progress-bar-warning');
                }

                if (percentile >= 50 && percentile <= 75) {
                    $('#' + needs[i].name).addClass('progress-bar-info');
                }

                if (percentile >= 75 && percentile <= 100) {
                    $('#' + needs[i].name).addClass('progress-bar-info');
                }

                $('#' + needs[i].name).attr('style', 'width: ' + percentile + '%');
                $('#' + needs[i].name).attr('aria-valuenow', percentile);
                $('#' + needs[i].name).text(percentile);
            }
           }
        });

    });
  }
});
