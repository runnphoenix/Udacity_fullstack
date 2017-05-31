var map;

// These are the real estate listings that will be shown to the user.
// Normally we'd have these in a database instead.
var locations = [
    {title: 'Forbidden City', location: {lat: 39.9163447, lng: 116.3971546}},
    {title: 'Yuan Ming Yuan Park', location: {lat: 40.0080982, lng: 116.2982148}},
    {title: 'Beijing National Stadium', location: {lat: 39.9929431, lng: 116.3965112}},
    {title: 'The Great Wall of China', location: {lat: 40.3597596, lng: 116.0200204}},
    {title: 'Tiananmen Square', location: {lat: 39.9054895, lng: 116.3976317}},
    {title: 'CCTV Headequarters', location: {lat: 39.9152751, lng: 116.4642312}}
];

// Create a new blank array for all the listing markers.
var markers = [];

// This global polygon variable is to ensure only ONE polygon is rendered.
var polygon = null;

// Create placemarkers array to use in multiple functions to have control
// over the number of places that show.
var placeMarkers = [];

var infoWindow;

function viewModel() {
    var self = this;

    // Import locations
    this.locationList = ko.observableArray([]);
    locations.forEach(function(location){
        self.locationList.push(location);
    });
    
    // Highlight a Marker
    this.highlightMarker = function() {
        if(infoWindow == null){
            infoWindow = new google.maps.InfoWindow();
        }

        for (var i=0; i<markers.length; i++) {
            marker = markers[i];
            if (marker.title == this.title){
                // Animation
                if (marker.getAnimation() !== null){
                    marker.setAnimation(null);
                }else{
                    marker.setAnimation(google.maps.Animation.DROP);
                }
                // InfoWindow
                populateInfoWindow(marker, infoWindow);
            }
        }
    };

    // Filter function
    this.filterLocations = function() {
        var filterCondition = document.getElementById('places-search').value;
	    // 
	    for (var i=0; i<markers.length; i++){
	        marker = markers[i];
	        if (marker.title.indexOf(filterCondition) == -1) {
		        marker.setMap(null);
	        }else{
		        marker.setMap(map);
	        }
	    }
        
        //TODO: improve performance
        self.locationList.removeAll();
        locations.forEach(function(location){
            self.locationList.push(location);
        });
        self.locationList.remove(function(item){
            return item.title.indexOf(filterCondition) == -1;
        });
    };
}

ko.applyBindings(new viewModel());


function initMap() {
    // Constructor creates a new map - only center and zoom are required.
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.7413549, lng: -73.9980244},
        zoom: 13,
        mapTypeControl: false
    });

    // Style the markers a bit. This will be our listing marker icon.
    var defaultIcon = makeMarkerIcon('0091ff');

    var bounds = new google.maps.LatLngBounds();
    
    if(infoWindow == null){
        infoWindow = new google.maps.InfoWindow();
    }

    // The following group uses the location array to create an array of markers on initialize.
    for (var i = 0; i < locations.length; i++) {
        // Get the position from the location array.
        var position = locations[i].location;
        var title = locations[i].title;
        // Create a marker per location, and put into markers array.
        var marker = new google.maps.Marker({
            position: position,
            title: title,
            animation: google.maps.Animation.DROP,
            icon: defaultIcon,
            id: i
        });
        // Push the marker to our array of markers.
        markers.push(marker);
        // Create an onclick event to open the large infowindow at each marker.
        marker.addListener('click', function() {
            populateInfoWindow(this, infoWindow);
            // Animation
            if (this.getAnimation() !== null){
                this.setAnimation(null);
            }else{
                this.setAnimation(google.maps.Animation.DROP);
            }
        });
        marker.setMap(map);
        bounds.extend(marker.position);
    }

    map.fitBounds(bounds);
}

function resizeMap(){
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0; i < markers.length; i++) {
        var marker = markers[i];
        marker.setMap(map);
        bounds.extend(marker.position);
    }
    map.fitBounds(bounds);
}

// This function populates the infowindow when the marker is clicked. We'll only allow
// one infowindow which will open at the marker that is clicked, and populate based
// on that markers position.
function populateInfoWindow(marker, infowindow) {
    // Check to make sure the infowindow is not already opened on this marker.
    if (infowindow.marker != marker) {
        // Clear the infowindow content to give the streetview time to load.
        infowindow.setContent('');
        infowindow.marker = marker;
        // Make sure the marker property is cleared if the infowindow is closed.
        infowindow.addListener('closeclick', function() {
            infowindow.marker = null;
        });

        infowindowContent = '<br>' + marker.title + '<br>';
        infowindow.setContent(infowindowContent);

		getWikiLinks(marker);

        // Open the infowindow on the correct marker.
        infowindow.open(map, marker);
    }
}

// This function takes in a COLOR, and then creates a new marker
// icon of that color. The icon will be 21 px wide by 34 high, have an origin
// of 0, 0 and be anchored at 10, 34).
function makeMarkerIcon(markerColor) {
    var markerImage = new google.maps.MarkerImage(
        'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +
        '|40|_|%E2%80%A2',
        new google.maps.Size(21, 34),
        new google.maps.Point(0, 0),
        new google.maps.Point(10, 34),
        new google.maps.Size(21,34));
    return markerImage;
}
// Show Wikipedia Links                                    
function getWikiLinks(mark) {
	var url = mark.title.replace(/ /g, '%20');
    var wikiUrl = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + url + '&format=json&callback=wikiCallback';
	$.ajax({
		url: wikiUrl,
		dataType: 'jsonp',
		success: function(response){
			var articleList = response[1];
			for (var i=0; i<articleList.length; i++) {
                articleString = articleList[i];
                var articleUrl = 'http://en.wikipedia.org/wiki/' + articleString.replace(/ /g, '%20');
                infowindowContent += ('<a href=' + articleUrl + '>' + articleString + '</a>' + '<br>');
            }
            infowindow.setContent(infowindowContent);
		}
	});
}

$(document).ready(function(){  
    var isHiden = true;  
    $('#menu').click(function(){
        if(isHiden){
            $('#map').animate({left:'-=320px'});
            $('#menuBar').animate({left:'-=320px'});
        }else{  
            $('#map').animate({left:'+=320px'});
            $('#menuBar').animate({left:'+=320px'});
        }
        isHiden = !isHiden;
        //TODO: Still not working.
        resizeMap();
    });
});
