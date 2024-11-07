# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Switch(Component):
    """A Switch component.


Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- checked (boolean; default False):
    If True, the switch is checked.

- color (a value equal to: 'default', 'primary', 'secondary', 'error', 'info', 'success', 'warning'; optional):
    The color of the component.

- disabled (boolean; optional):
    If True, the switch will be disabled.

- size (a value equal to: 'small', 'medium'; optional):
    The size of the component."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Switch'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, checked=Component.UNDEFINED, disabled=Component.UNDEFINED, color=Component.UNDEFINED, size=Component.UNDEFINED, onChange=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'checked', 'color', 'disabled', 'size']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'checked', 'color', 'disabled', 'size']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Switch, self).__init__(**args)
