String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

var map = L.map('mapid').setView([53.93664114639455, 27.498858521576043], 4);
console.log("HELLO");

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibGVzaGthc2Fmcm9ub3YiLCJhIjoiY2piZHo0ZTlvMWVzaTJxbm4yeHV5eGV6ZiJ9.q8DmMNrED0Tta9mXjhJcfw'
}).addTo(map);

$.ajax({
  type: "GET",
  url: '/api/users',
  success: function(data) {
    for (var i = 0; i < data.length; i++) {
        var marker = L.marker([data[i].latitude, data[i].longitude]).addTo(map);
        marker.bindPopup("<div class='container-picture'><img src={0} class='user-picture img-circle' alt='Cinque Terre'/></div><div class='container-text'><b>{1}</b></div>".format(
            data[i].image,
            data[i].username
        ), {autoClose:false,
            closeOnClick: false}).openPopup();
    }
  }
});

