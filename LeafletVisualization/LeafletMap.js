var LeafletModule = function (view, zoom, map_width, map_height) {
  // Create the map tag:
  var map_tag = "<div style='width:" + map_width + "px; height:" + map_height + "px; border:1px dotted' id='mapid'></div>";
  // Append it to body:
  $('#elements').append($(map_tag)[0])
  $('head').append('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="crossorigin=""/>');

  // Create Leaflet map and Agent layers
  var Lmap = L.map('mapid').setView(view, zoom);
  var agents = L.layerGroup();

  // create the OSM tile layer with correct attribution
  // var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
  // var osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
  // var osmUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}'
  // var osmAttrib = 'Tiles &copy; Esri &mdash; Source: USGS, Esri, TANA, DeLorme, and NPS';
  // var osmUrl = 'https://{s}.tile.openstreetmap.se/hydda/base/{z}/{x}/{y}.png';
  // var osmAttrib = 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';
  // var osm = new L.TileLayer(osmUrl, {minZoom: 0, maxZoom: 18, attribution: osmAttrib})
  // Lmap.addLayer(osm)

  var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    minZoom: 1,
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  });

  Lmap.addLayer(osm);

  var bikeIcon = L.icon({
    iconUrl: 'local/resources/bike.svg',
    iconSize: 40
  });

  var riderIcon = L.icon({
    iconUrl: 'local/resources/person.svg',
    iconSize: 40
  });

  this.render = function (nodes) {

    agents.clearLayers();

    for (var i = nodes.length - 1; i >= 0; i--) {
      
      for (var j = nodes[i].agents.length; j >= 0; j--){
        switch(nodes[i].agents[j]){
          case "Rider":
            L.marker([nodes[i]['lat'], nodes[i]['long']], 
              {
                  icon: riderIcon,
              }).addTo(agents).bindPopup(`<b>${nodes[i].agents[j]}</b></br>${nodes[i]['lat']}, ${nodes[i]['long']}`);
            break;
          case "Bike":
            marker = L.marker([nodes[i]['lat'], nodes[i]['long']], 
              {
                  icon: bikeIcon
              }).addTo(agents).bindPopup(`<b>${nodes[i].agents[j]}</b></br>${nodes[i]['lat']}, ${nodes[i]['long']}`);
            break;
          case "Station":
            marker = L.marker([nodes[i]['lat'], nodes[i]['long']])
              .addTo(agents)
              .bindPopup(`<b>${nodes[i].agents[j]}</b></br>${nodes[i]['lat']}, ${nodes[i]['long']}`);
        }
      }
    }

    Lmap.addLayer(agents);

  }

  this.reset = function () {
    Lmap.remove();
    Lmap = L.map('mapid').setView(view, zoom);
    Lmap.addLayer(osm);
    Lmap.removeLayer(agents);
  }
}
