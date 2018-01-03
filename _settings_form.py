"""PytSite Google Maps Plugin Settings Form
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang as _lang, reg as _reg
from plugins import widget as _widget, settings as _settings


class Form(_settings.Form):
    def _on_setup_widgets(self):
        """Hook.
        """
        self.add_widget(_widget.input.Text(
            uid='setting_api_key',
            weight=10,
            label=_lang.t('google_maps@api_key'),
            help=_lang.t('google_maps@api_key_setup_help'),
            default=_reg.get('google_maps.api_key'),
        ))

        super()._on_setup_widgets()
