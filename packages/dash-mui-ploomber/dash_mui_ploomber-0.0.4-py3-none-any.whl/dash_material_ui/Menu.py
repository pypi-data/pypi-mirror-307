# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Menu(Component):
    """A Menu component.


Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- buttonText (string; default 'Open Menu'):
    The text displayed on the button that opens the menu.

- menuItems (list of dicts; optional):
    Array of menu item labels or objects.

    `menuItems` is a list of string | dict with keys:

    - disabled (boolean; optional)

    - icon (string; optional)

    - label (string; required)s

- selectedIndex (number; optional):
    Index of the selected menu item."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Menu'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, buttonText=Component.UNDEFINED, menuItems=Component.UNDEFINED, onItemClick=Component.UNDEFINED, selectedIndex=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'buttonText', 'menuItems', 'selectedIndex']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'buttonText', 'menuItems', 'selectedIndex']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Menu, self).__init__(**args)
