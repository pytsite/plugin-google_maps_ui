"""PytSite Google Maps UI Plugin
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _widget as widget


def plugin_load():
    from plugins import assetman

    assetman.register_package(__name__)
    assetman.js_module('google-maps', __name__ + '@js/google-maps')
    assetman.js_module('google-maps-widget-address-input', __name__ + '@js/google-maps-widget-address-input')
    assetman.js_module('google-maps-widget-static-map', __name__ + '@js/google-maps-widget-static-map')
    assetman.t_less(__name__)
    assetman.t_js(__name__)
    assetman.t_copy_static(__name__)


def plugin_install():
    from plugins import assetman

    assetman.build(__name__)


def plugin_load_uwsgi():
    from pytsite import lang, tpl, router
    from plugins import settings, google_maps
    from . import _eh, _settings_form

    # Resources
    lang.register_package(__name__)
    lang.register_global('google_maps_admin_settings_url', lambda language, args: settings.form_url('google_maps'))
    tpl.register_global('google_maps_map_link', google_maps.maps.link)

    # Settings
    settings.define('google_maps', _settings_form.Form, 'google_maps_ui@google_maps', 'fa fa-map', 'dev')

    # Event handlers
    router.on_dispatch(_eh.on_router_dispatch)
