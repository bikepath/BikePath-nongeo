var LeafletModule = function (view, zoom, map_width, map_height) {
  // Create the map tag:
  var map_tag = "<div style='width:" + map_width + "px; height:" + map_height + "px; border:1px dotted' id='mapid'></div>";
  // Append it to body:
  $('#elements').append($(map_tag)[0])
  $('head').append('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="crossorigin=""/>');

  // Create Leaflet map and Agent layers
  var Lmap = L.map('mapid').setView(view, zoom);

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

  this.render = function (nodes) {

    console.log(nodes);

    for (var i = nodes.length - 1; i >= 0; i--) {
      
      var marker = L.marker([nodes[i]['lat'], nodes[i]['long']], 
        {
            icon: new L.DivIcon({
                className: 'my-div-icon',
                html: `<b>${nodes[i]['id']}</b>`
            })
        }).addTo(Lmap);
        // });
      Lmap.addLayer(marker);
      // oms.addMarker(marker);
      marker.bindPopup(`<b>${nodes[i]['id']}</b></br>${nodes[i]['lat']}, ${nodes[i]['long']}`);
    }

  }

  this.reset = function () {
    Lmap.remove()
    Lmap = L.map('mapid').setView(view, zoom)
    Lmap.addLayer(osm)
  }
}
