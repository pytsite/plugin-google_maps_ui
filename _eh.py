"""PytSite Google Maps Plugins Event Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import metatag, router, lang
from plugins import auth, google_maps


def on_router_dispatch():
    try:
        api_key = google_maps.helpers.get_google_api_key()
        metatag.t_set('pytsite-google-maps-api-key', api_key)
    except google_maps.error.GoogleApiKeyNotDefined:
        if auth.get_current_user().has_role('dev'):
            router.session().add_warning_message(lang.t('google_maps_ui@plugin_setup_required_warning'))
