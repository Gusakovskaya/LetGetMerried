var mymap = L.map('mapid').setView([51.505, -0.09], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibGVzaGthc2Fmcm9ub3YiLCJhIjoiY2piYmM3ZzZhMTUxbzM0bGx3ejgybW9zOSJ9.5AEt2XHAmnzKa3JiahlinA'
}).addTo(mymap);



var marker = L.marker([51.5, -0.09]).addTo(mymap);