"""PytSite Google Maps Plugin Widgets
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union as _Union
from copy import deepcopy as _deepcopy
from json import dumps as _json_dumps, loads as _json_loads
from frozendict import frozendict as _frozendict
from pytsite import html as _html, router as _router, validation as _validation
from plugins import widget as _pytsite_widget, geo as _geo, google_maps as _google_maps


class AddressInput(_pytsite_widget.Abstract):
    """Geo Address Input Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        if 'default' not in kwargs:
            kwargs['default'] = {
                'address': '',
                'lng': 0.0,
                'lat': 0.0,
                'address_components': ()
            }

        super().__init__(uid, **kwargs)

        self._autodetect = kwargs.get('autodetect', False)
        self._css += ' widget-google-address-input'
        self._js_module = 'google-maps-widget-address-input'

        # Validation rule for 'required' widget
        if self._required:
            self.clr_rules().add_rules([r for r in self.get_rules() if not isinstance(r, _validation.rule.NonEmpty)])
            self.add_rule(_geo.validation_rule.AddressNonEmpty())

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        if value:
            self.add_rule(_geo.validation_rule.AddressNonEmpty())
        else:
            # Clear all added NonEmpty and AddressNonEmpty rules
            rules = [r for r in self.get_rules() if not isinstance(r, (
                _validation.rule.NonEmpty,
                _geo.validation_rule.AddressNonEmpty
            ))]
            self.clr_rules().add_rules(rules)

        self._required = value

    @property
    def autodetect(self) -> bool:
        return self._autodetect

    @autodetect.setter
    def autodetect(self, value: bool):
        self._autodetect = value

    def set_val(self, val: _Union[dict, _frozendict], **kwargs):
        """Set value of the widget.
        """
        if isinstance(val, (dict, _frozendict)) and val:
            # Checking for required keys
            for k in ['lng', 'lat', 'address', 'address_components']:
                if k not in val:
                    raise ValueError("Value does not contain '{}' key.".format(k))

            # Loading address components
            if isinstance(val['address_components'], str):
                components = _json_loads(val['address_components'])
            else:
                components = val['address_components']

            val = {
                'address': val['address'],
                'lng': float(val['lng']),
                'lat': float(val['lat']),
                'address_components': components
            }
        elif val is None:
            val = self._default
        else:
            raise ValueError('Dict or None expected.')

        return super().set_val(val, **kwargs)

    def get_val(self, **kwargs):
        """Set value of the widget.
        """
        return super().get_val(**kwargs) or _deepcopy(self._default)

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        lng = self.value['lng']
        lat = self.value['lat']
        address = self.value['address']
        address_components = _json_dumps(self.value['address_components'])

        inputs = _html.TagLessElement()
        inputs.append(_html.Input(type='text', name=self._uid + '[search]', css='form-control', value=address))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[lng]', value=lng))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[lat]', value=lat))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[address]', value=address))
        inputs.append(_html.Input(type='hidden', name=self._uid + '[address_components]', value=address_components))

        self._data['autodetect'] = self._autodetect

        return inputs


class StaticMap(_pytsite_widget.Abstract):
    """Google Static Map.

    https://developers.google.com/maps/documentation/static-maps/intro
    """

    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._point = _google_maps.types.Location(kwargs.get('lat', 50.4501), kwargs.get('lng', 30.5234))
        self._zoom = kwargs.get('zoom', 15)
        self._scale = kwargs.get('scale', 1)
        self._markers = kwargs.get('markers', [])
        self._linked = kwargs.get('linked', True)
        self._link_target = kwargs.get('link_target', '_blank')
        self._img_css = kwargs.get('img_css', 'img-responsive')
        self._js_module = 'google-maps-widget-static-map'

    def _get_element(self, **kwargs):
        self._data['img_class'] = self._img_css

        self._data['img_url'] = _router.url('https://maps.googleapis.com/maps/api/staticmap', query={
            'center': '{},{}'.format(self._point.lat, self._point.lng),
            'zoom': self._zoom,
            'scale': self._scale,
            'markers': '|'.join(x for x in self._markers),
            'key': _google_maps.helpers.get_google_api_key(),
        })

        if self._linked:
            self._data['link'] = _google_maps.maps.link(self._point, zoom=self._zoom)
            self._data['link_target'] = self._link_target

        return _html.TagLessElement()
