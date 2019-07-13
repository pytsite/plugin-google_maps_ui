"""PytSite Google Maps Plugin Settings Form
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang, reg
from plugins import widget, settings


class Form(settings.Form):
    def _on_setup_widgets(self):
        """Hook.
        """
        self.add_widget(widget.input.Text(
            uid='setting_api_key',
            weight=10,
            label=lang.t('google_maps_ui@api_key'),
            help=lang.t('google_maps_ui@api_key_setup_help'),
            default=reg.get('google_maps.api_key'),
        ))

        super()._on_setup_widgets()
