"""PytSite Google Maps UI Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _widget as widget


def plugin_load_wsgi():
    from pytsite import lang, router
    from plugins import settings
    from . import _eh, _settings_form

    # Resources
    lang.register_global('google_maps_admin_settings_url', lambda language, args: settings.form_url('google_maps'))

    # Settings
    settings.define('google_maps', _settings_form.Form, 'google_maps_ui@google_maps', 'fa fa-map', 'dev')

    # Event handlers
    router.on_dispatch(_eh.on_router_dispatch)
