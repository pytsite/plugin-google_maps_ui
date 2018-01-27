"""PytSite Google Maps Plugins Event Handlers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import metatag as _metatag, router as _router, lang as _lang
from plugins import auth as _auth, google_maps as _google_maps


def on_router_dispatch():
    try:
        api_key = _google_maps.helpers.get_google_api_key()
        _metatag.t_set('pytsite-google-maps-api-key', api_key)
    except _google_maps.error.GoogleApiKeyNotDefined:
        if _auth.get_current_user().has_role('dev'):
            _router.session().add_warning_message(_lang.t('google_maps_ui@plugin_setup_required_warning'))
