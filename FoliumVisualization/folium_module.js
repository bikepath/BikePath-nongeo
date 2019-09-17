var Folium_Module = function(height, width) {
	// Create the element
	// ------------------

	// Create the tag:
	var folium_iframe = "<iframe height='" + height + "' width='" + width + "'></iframe>";

	// Append it to body:
	// var canvas = $(folium_iframe)[0];
	$("#elements").append(folium_iframe);

	this.render = function(data) {
		folium_iframe.srcdoc = data;
		console.log("render");
	};

	this.reset = function() {
		console.log("reset");
	};

};