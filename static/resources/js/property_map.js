        var icon = {
            url:"/static/images/streetview.png",
        };
        var marker;

        function get_para(vars) {
           return vars
        }

        function clickMarker(marker){
                window.location.href = marker.url;
        }

        function placeMarkerAndPanTo(latLng, map) {
            var marker = new google.maps.Marker({
                position: latLng,
                map: map,
                icon:icon
            });
            var geocoder= new google.maps.Geocoder();
            geocoder.geocode( { 'location': marker.getPosition()}, function(results, status) {
                if (status == 'OK') {
                    place_id = JSON.stringify(results[0]["place_id"]);
                    place_id = place_id.replace(/^"(.*)"$/, '$1');
                    marker.addListener('click', function(){clickMarker(marker)});
                }else {
                    alert('Geocode was not successful for the following reason: ' + status);
                }
            });
        }

        function showLocationButton(map, marker)
        {
            var controlDiv = document.createElement('div');

            var firstChild = document.createElement('button');
            firstChild.style.backgroundColor = '#fff';
            firstChild.style.border = 'none';
            firstChild.style.outline = 'none';
            firstChild.style.width = '40px';
            firstChild.style.height = '40px';
            firstChild.style.borderRadius = '2px';
            firstChild.style.boxShadow = '0 1px 4px rgba(0,0,0,0.3)';
            firstChild.style.cursor = 'pointer';
            firstChild.style.marginRight = '10px';
            firstChild.style.padding = '0px';
            firstChild.title = 'Your Location';
            controlDiv.appendChild(firstChild);

            var secondChild = document.createElement('div');
            secondChild.style.margin = '11px';
            secondChild.style.width = '18px';
            secondChild.style.height = '18px';
            secondChild.style.backgroundImage = 'url(https://maps.gstatic.com/tactile/mylocation/mylocation-sprite-1x.png)';
            secondChild.style.backgroundSize = '180px 18px';
            secondChild.style.backgroundPosition = '0px 0px';
            secondChild.style.backgroundRepeat = 'no-repeat';
            secondChild.id = 'you_location_img';
            firstChild.appendChild(secondChild);

            google.maps.event.addListener(map, 'dragend', function() {
                $('#you_location_img').css('background-position', '0px 0px');
            });

            firstChild.addEventListener('click', function() {
                var imgX = '0';
                var animationInterval = setInterval(function(){
                    if(imgX == '-18') imgX = '0';
                    else imgX = '-18';
                    $('#you_location_img').css('background-position', imgX+'px 0px');
                }, 500);
                if(navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(function(position) {
                        var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
//                        marker.setPosition(latlng);
                        map.setCenter(latlng);
                        clearInterval(animationInterval);
                        $('#you_location_img').css('background-position', '-144px 0px');
                    });
                }
                else{
                    clearInterval(animationInterval);
                    $('#you_location_img').css('background-position', '0px 0px');
                }
            });

            controlDiv.index = 1;
            map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
        }


        function initAutocomplete(){
            place_id = "ChIJJdxLbfBHDW0Rh5OtgMO10QI";
            lat = -36.8942359;
            lng = 174.7819203;

            var map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: lat,lng: lng},
                zoom: 12,
                mapTypeId: 'roadmap',
                disableDoubleClickZoom : true,
                fullscreenControl: false,
                mapTypeControl: false,
            });

            var markers = [];
            // Create the search box and link it to the UI element.
            var input = document.getElementById('pac-input');
            var searchBox = new google.maps.places.SearchBox(input);
//            map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

            // Bias the SearchBox results towards current map's viewport.
            map.addListener('bounds_changed', function() {
                searchBox.setBounds(map.getBounds());
            });

            latlng = new google.maps.LatLng(lat, lng);

            var res_icon = new google.maps.MarkerImage("/static/resources/img/bnb.png",null,null,null, new google.maps.Size(70, 70));
            var boat_icon = new google.maps.MarkerImage("/static/resources/img/boat.png",null,null,null, new google.maps.Size(40, 40));
            var com_icon = new google.maps.MarkerImage("/static/resources/img/dollar.png",null,null,null, new google.maps.Size(40, 40));
            var icon;
            for (var i=0;i<markers_data.length;i++){
                row = markers_data[i];
                console.log(row['lat']);
                console.log(row['lng']);
                console.log(row['mlink']);
                console.log(row['address']);
                if (row['listing_type'].includes("com")){
                    icon = com_icon;
                }else if (row['listing_type'].includes("boat")){
                    icon = boat_icon;
                }else{
                    icon = res_icon;
                }

                latlng = new google.maps.LatLng(parseFloat(row['lat']), parseFloat(row['lng']));
                marker = new google.maps.Marker({
                    map: map,icon:icon,title: row['address'],position: latlng,
                    url: row['mlink']
                });

                google.maps.event.addListener(marker, 'click', function() {
                    window.location.href = this.url;
                });
                markers.push(marker)
            }

            map.addListener('dblclick', function(e) {
                marker.setMap(null);
//                placeMarkerAndPanTo(e.latLng, map);
                e.stop();
            });

            showLocationButton(map, marker);

            // Listen for the event fired when the user selects a prediction and retrieve
            // more details for that place.
            searchBox.addListener('places_changed', function() {
              var places = searchBox.getPlaces();

              if (places.length == 0) {
                return;
              }

              // Clear out the old markers.
//              markers.forEach(function(marker) {
//                marker.setMap(null);
//              });
//              markers = [];

              // For each place, get the icon, name and location.
              var bounds = new google.maps.LatLngBounds();
              places.forEach(function(place) {
                if (!place.geometry) {
                  console.log("Returned place contains no geometry");
                  return;
                }

//                // Create a marker for each place.
//                marker = new google.maps.Marker({
//                  map: map,
//                  icon: icon,
//                  title: place.name,
//                  position: place.geometry.location
//                })

                console.log("lat:"+ place.geometry.location.lat()+" lng:"+place.geometry.location.lng());
                console.log(place.name);

//                marker.addListener('click', function(){clickMarker(marker,place.place_id)})
//                markers.push(marker);

                if (place.geometry.viewport) {
                  // Only geocodes have viewport.
                  bounds.union(place.geometry.viewport);
                } else {
                  bounds.extend(place.geometry.location);
                }
              });
              map.fitBounds(bounds);
            });
        }