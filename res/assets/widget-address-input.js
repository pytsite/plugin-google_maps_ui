import $ from 'jquery';
import setupWidget from "@pytsite/widget";
import onGoogleMapsReady from './index';

setupWidget('plugins.google_maps_ui._widget.AddressInput', widget => {
    function setBounds(autcomplete) {
        if ('geolocation' in navigator) {
            navigator.geolocation.updateCurrentPosition(function (position) {
                const geolocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                const circle = new google.maps.Circle({center: geolocation, radius: position.coords.accuracy});

                autcomplete.setBounds(circle.getBounds());
            });
        }
    }

    onGoogleMapsReady(() => {
        const uid = widget.em.data('uid');
        const searchInput = widget.em.find('input[name="' + uid + '[search]"]');
        const addressInput = widget.em.find('input[name="' + uid + '[address]"]');
        const lngInput = widget.em.find('input[name="' + uid + '[lng]"]');
        const latInput = widget.em.find('input[name="' + uid + '[lat]"]');
        const componentsInput = widget.em.find('input[name="' + uid + '[address_components]"]');
        const autocomplete = new google.maps.places.Autocomplete(searchInput[0], {
            types: widget.data('types'),
            componentRestrictions: widget.data('componentRestrictions')
        });

        widget.em.keydown(function (event) {
            if (event.keyCode === 13) {
                event.preventDefault();
                return false;
            }
        });

        searchInput.focus(function () {
            this.select()
        });

        searchInput.blur(function () {
            if (!$(this).val().length) {
                addressInput.val('');
                latInput.val('0.0');
                lngInput.val('0.0');
                componentsInput.val('[]');
            }
        });

        // Update our hidden fields with data provided by Google
        google.maps.event.addListener(autocomplete, 'place_changed', function () {
            const place = autocomplete.getPlace();
            if (place.hasOwnProperty('geometry')) {
                const loc = place.geometry.location;
                addressInput.val(place.formatted_address);
                latInput.val(loc.lat());
                lngInput.val(loc.lng());
                componentsInput.val(JSON.stringify(place.address_components));
            }
        });

        widget.update = function () {
            setBounds(autocomplete);
            navigator.geolocation.updateCurrentPosition(function (position) {
                const geoCoder = new google.maps.Geocoder();
                const latLng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
                geoCoder.geocode({'latLng': latLng}, function (results, status) {
                    if (status === google.maps.GeocoderStatus.OK && results.length) {
                        const place = results[0];
                        const loc = place.geometry.location;

                        searchInput.val(place.formatted_address);
                        addressInput.val(place.formatted_address);
                        lngInput.val(loc.lng());
                        latInput.val(loc.lat());
                        componentsInput.val(JSON.stringify(place.address_components));
                    }
                });
            });
        };

        // Automatic location detection
        if (widget.data('autodetect') === 'True') {
            widget.update();
            setInterval(widget.update, 10000)
        }
    })
});
