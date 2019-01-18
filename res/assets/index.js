import $ from 'jquery';
import {lang} from '@pytsite/assetman';

window.pytsiteGoogleMapsReady = false;
window.pytsiteGoogleMapsInit = () => {
    $(window).trigger('pytsiteGoogleMaps.ready');
    window.pytsiteGoogleMapsReady = true;
};

const apiKey = $('meta[name=pytsite-google-maps-api-key]').attr('content');
if (apiKey) {
    const googleUrl = 'https://maps.googleapis.com/maps/api/js?key=' + apiKey + '&callback=pytsiteGoogleMapsInit' +
        '&language=' + lang.current();
    $('body').append('<script src="' + googleUrl + '" async defer></script>');
}


export default callback => {
    window.pytsiteGoogleMapsReady ? callback() : $(window).on('pytsiteGoogleMaps.ready', callback);
};
