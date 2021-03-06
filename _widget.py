"""PytSite Google Maps Plugin Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import json
import htmler
from typing import Union
from copy import deepcopy
from frozendict import frozendict
from pytsite import router, validation
from plugins import widget, geo, google_maps


class AddressInput(widget.Abstract):
    """Geo Address Input Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init
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
        self._types = kwargs.get('types', ['establishment'])
        self._component_restrictions = kwargs.get('component_restrictions', [])
        self._css += ' widget-google-address-input'

        # Validation rule for 'required' widget
        if self._required:
            self.clr_rules().add_rules([r for r in self.get_rules() if not isinstance(r, validation.rule.NonEmpty)])
            self.add_rule(geo.validation.AddressNonEmpty())

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        if value:
            self.add_rule(geo.validation.AddressNonEmpty())
        else:
            # Clear all added NonEmpty and AddressNonEmpty rules
            rules = [r for r in self.get_rules() if not isinstance(r, (
                validation.rule.NonEmpty,
                geo.validation.AddressNonEmpty
            ))]
            self.clr_rules().add_rules(rules)

        self._required = value

    @property
    def types(self) -> bool:
        return self._types

    @types.setter
    def types(self, value: bool):
        # https://developers.google.com/places/supported_types#table3
        self._types = value

    @property
    def autodetect(self) -> bool:
        return self._autodetect

    @autodetect.setter
    def autodetect(self, value: bool):
        self._autodetect = value

    @property
    def component_restrictions(self) -> bool:
        return self._component_restrictions

    @component_restrictions.setter
    def component_restrictions(self, value: bool):
        # https://developers.google.com/maps/documentation/javascript/reference/3/places-widget#ComponentRestrictions
        self._component_restrictions = value

    def set_val(self, val: Union[dict, frozendict]):
        """Set value of the widget.
        """
        if isinstance(val, (dict, frozendict)) and val:
            # Checking for required keys
            for k in ['lng', 'lat', 'address', 'address_components']:
                if k not in val:
                    raise ValueError("Value does not contain '{}' key.".format(k))

            # Loading address components
            if isinstance(val['address_components'], str):
                components = json.loads(val['address_components'])
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

        return super().set_val(val)

    def get_val(self, **kwargs):
        """Set value of the widget.
        """
        return super().get_val(**kwargs) or deepcopy(self._default)

    def _get_element(self, **kwargs) -> htmler.Element:
        """Render the widget.
        :param **kwargs:
        """
        lng = self.value['lng']
        lat = self.value['lat']
        address = self.value['address']
        address_components = json.dumps(self.value['address_components'])

        inputs = htmler.TagLessElement()
        inputs.append_child(htmler.Input(type='text', name=self._uid + '[search]', css='form-control', value=address,
                                         placeholder=self._placeholder))
        inputs.append_child(htmler.Input(type='hidden', name=self._uid + '[lng]', value=lng))
        inputs.append_child(htmler.Input(type='hidden', name=self._uid + '[lat]', value=lat))
        inputs.append_child(htmler.Input(type='hidden', name=self._uid + '[address]', value=address))
        inputs.append_child(
            htmler.Input(type='hidden', name=self._uid + '[address_components]', value=address_components))

        if self._autodetect:
            self._data['autodetect'] = self._autodetect

        if self._types:
            self._data['types'] = json.dumps(self._types)

        if self._component_restrictions:
            self._data['component_restrictions'] = json.dumps({'country': self._component_restrictions})

        return inputs


class CityInput(AddressInput):
    def __init__(self, uid: str, **kwargs):
        cr = kwargs.get('countries', [])
        super().__init__(uid, component_restrictions=cr, types=['(cities)'], **kwargs)


class StaticMap(widget.Abstract):
    """Google Static Map.

    https://developers.google.com/maps/documentation/static-maps/intro
    """

    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._has_messages = False

        lat = kwargs.get('lat', 50.4501)
        lng = kwargs.get('lng', 30.5234)

        self._point = geo.types.Location(lat, lng)
        self._zoom = kwargs.get('zoom', 15)
        self._scale = kwargs.get('scale', 1)
        self._markers = kwargs.get('markers', ['{},{}'.format(lat, lng)])
        self._width = kwargs.get('width', 0)
        self._height = kwargs.get('height', 0)
        self._linked = kwargs.get('linked', True)
        self._link_target = kwargs.get('link_target', '_blank')
        self._img_css = kwargs.get('img_css', 'img-responsive img-fluid')

    def _get_element(self, **kwargs):
        self._data['img_class'] = self._img_css
        self._data['width'] = self._width
        self._data['height'] = self._height

        self._data['img_url'] = router.url('https://maps.googleapis.com/maps/api/staticmap', query={
            'center': '{},{}'.format(self._point.lat, self._point.lng),
            'zoom': self._zoom,
            'scale': self._scale,
            'markers': '|'.join(x for x in self._markers),
            'key': google_maps.helpers.get_google_api_key(),
        })

        if self._linked:
            self._data['link'] = google_maps.maps.link(self._point, zoom=self._zoom)
            self._data['link_target'] = self._link_target

        return htmler.TagLessElement()
