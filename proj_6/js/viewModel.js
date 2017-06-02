// Global variables
var map;
var markers = [];
var infoWindow;
var bounds;
var locations = [
    {title: 'Forbidden City', location: {lat: 39.9163447, lng: 116.3971546}},
    {title: 'Yuan Ming Yuan Park', location: {lat: 40.0080982, lng: 116.2982148}},
    {title: 'Beijing National Stadium', location: {lat: 39.9929431, lng: 116.3965112}},
    {title: 'The Great Wall of China', location: {lat: 40.3597596, lng: 116.0200204}},
    {title: 'Tiananmen Square', location: {lat: 39.9054895, lng: 116.3976317}},
    {title: 'CCTV Headequarters', location: {lat: 39.9152751, lng: 116.4642312}}
];
var animateDuration = 300;

// VM
function viewModel() {
    var self = this;

    this.filterCondition = ko.observable('');

    // Import locations
    this.locationList = ko.observableArray([]);
    locations.forEach(function(location){
        self.locationList.push(location);
    });
    
    // Highlight a Marker & show infowindow
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
	    for (var i=0; i<markers.length; i++){
	        marker = markers[i];
	        if (marker.title.indexOf(self.filterCondition()) == -1) {
		        marker.setMap(null);
	        }else{
		        marker.setMap(map);
	        }
	    }
        
        self.locationList.removeAll();
        locations.forEach(function(location){
            self.locationList.push(location);
        });
        self.locationList.remove(function(item){
            return item.title.indexOf(self.filterCondition()) == -1;
        });
    };

    // Toggle left menu
    var isHidden = true;
    this.toggleLeftPanel = function(){
        if(isHidden){
            $('#map').animate({left:'-=310px'}, animateDuration);
            $('#menuBar').animate({left:'-=310px'}, animateDuration, function(){
                refreshMap();
            });
        }else{  
            $('#map').animate({left:'+=310px'}, animateDuration);
            $('#menuBar').animate({left:'+=310px'}, animateDuration, function(){
                refreshMap();
            });
        }
        isHidden = !isHidden;
    };
}

ko.applyBindings(new viewModel());

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 39.9929431, lng: 116.3965112},
        zoom: 13
    });
    
    // Refresh Map when browser resizes
    google.maps.event.addDomListener(window, "resize", function() {
        refreshMap();
    });
    
    bounds = new google.maps.LatLngBounds();
    
    if(infoWindow == null){
        infoWindow = new google.maps.InfoWindow();
    }

    // Create markers
    for (var i = 0; i < locations.length; i++) {
        var position = locations[i].location;
        var title = locations[i].title;
        var marker = new google.maps.Marker({
            position: position,
            title: title,
            animation: google.maps.Animation.DROP,
            id: i
        });
        markers.push(marker);
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

// Populates infowindow when marker is clicked
function populateInfoWindow(marker, infowindow) {
    if (infowindow.marker != marker) {
        infowindow.setContent('');
        infowindow.marker = marker;
        infowindow.addListener('closeclick', function() {
            infowindow.marker = null;
        });

        infowindowContent = '<br>' + marker.title + '<br>';
        infowindow.setContent(infowindowContent);

		getWikiLinks(marker, infowindow);

        infowindow.open(map, marker);
    }
}

// Show Wikipedia Links in infoWindow                                   
function getWikiLinks(mark, infowindow) {
	var url = mark.title.replace(/ /g, '%20');
    var wikiUrl = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + url + '&format=json&callback=wikiCallback';
    //TODO: error handling
	$.ajax({
		url: wikiUrl,
		dataType: 'jsonp',
		success: function(response){
            infowindowContent += ('<br>' + 'Wikipedia Links:' + '<br>');
			var articleList = response[1];
			for (var i=0; i<articleList.length; i++) {
                articleString = articleList[i];
                var articleUrl = 'http://en.wikipedia.org/wiki/' + articleString.replace(/ /g, '%20');
                infowindowContent += ('<a href=' + articleUrl + '>' + articleString + '</a>' + '<br>');
            }
            infowindow.setContent(infowindowContent);
		},
        error: function(jqXHR, exception){
            var msg = '';
            if (jqXHR.status === 0) {
                msg = 'Not connect.\n Verify Network.';
            } else if (jqXHR.status == 404) {
                msg = 'Requested page not found. [404]';
            } else if (jqXHR.status == 500) {
                msg = 'Internal Server Error [500].';
            } else if (exception === 'parsererror') {
                msg = 'Requested JSON parse failed.';
            } else if (exception === 'timeout') {
                msg = 'Time out error.';
            } else if (exception === 'abort') {
                msg = 'Ajax request aborted.';
            } else {
                msg = 'Uncaught Error.\n' + jqXHR.responseText;
            }
            alert(msg);
        }
	});
}

// Refresh Map
function refreshMap(){
    var center = map.getCenter();
    google.maps.event.trigger(map, "resize");
    map.setCenter(center); 
}
