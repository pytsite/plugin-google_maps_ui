"""PytSite Google Maps UI Plugin
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman

if _plugman.is_installed(__name__):
    # Public API
    from . import _widget as widget


def _register_assetman_resources():
    from plugins import assetman

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.js_module('google-maps', __name__ + '@js/google-maps')
        assetman.js_module('google-maps-widget-address-input', __name__ + '@js/google-maps-widget-address-input')
        assetman.js_module('google-maps-widget-static-map', __name__ + '@js/google-maps-widget-static-map')
        assetman.t_less(__name__)
        assetman.t_js(__name__)
        assetman.t_copy_static(__name__)

    return assetman


def plugin_install():
    _register_assetman_resources().build(__name__)


def plugin_load():
    _register_assetman_resources()


def plugin_load_uwsgi():
    from pytsite import lang, tpl, router
    from plugins import permissions, settings, google_maps
    from . import _eh, _settings_form

    # Resources
    lang.register_package(__name__)
    lang.register_global('google_maps_admin_settings_url', lambda language, args: settings.form_url('google_maps'))
    tpl.register_global('google_maps_map_link', google_maps.maps.link)

    # Permissions
    permissions.define_permission('google_maps_ui@manage_settings', 'google_maps_ui@manage_google_maps_settings', 'app')

    # Settings
    settings.define('google_maps', _settings_form.Form, 'google_maps_ui@google_maps', 'fa fa-map',
                    'google_maps_ui@manage_settings')

    # Event handlers
    router.on_dispatch(_eh.on_router_dispatch)
