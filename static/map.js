function initialize() {
var data = JSON.parse('{{ data | safe }}');
var map = L.map('map').setView([48.833, 2.333], 6);
var size1 = data[data.length-1][0]
var size2 = data[data.length-1][1]
var size_total = size1+size2
var myIcon = L.icon({
iconUrl: 'https://www.ija-lille.fr/wpress/wp-content/uploads/2018/01/map-marker-icon.png',iconSize: [38, 45],});
for (var i = size1-1 ; i>=0;i-- ) {
    L.marker([ data[i][1] , data[i][2]]).addTo(map) .bindTooltip( (data[i][0]), {permanent: false, direction: 'bottom'});
    }
for (var i = size_total-1; i>=size1;i-- ) {
    L.marker([ data[i][1] , data[i][2]], {icon: myIcon}).addTo(map).bindTooltip( (data[i][0]), {permanent: false, direction: 'top'});
    }
var osmLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap contributors',maxZoom: 19 });
map.addLayer(osmLayer);
}