# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CustomSpeedDial(Component):
    """A CustomSpeedDial component.
Custom SpeedDial component using Material-UI.

Keyword arguments:

- id (string; required)

- actions (list of dicts; required)

    `actions` is a list of dicts with keys:

    - icon (string; required)

    - id (string; required)

    - tooltip (string; required)

- ariaLabel (string; required)

- direction (a value equal to: 'up', 'down', 'left', 'right'; default "up")

- n_clicks (string; default "")"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'CustomSpeedDial'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, ariaLabel=Component.REQUIRED, direction=Component.UNDEFINED, actions=Component.REQUIRED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'actions', 'ariaLabel', 'direction', 'n_clicks']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'actions', 'ariaLabel', 'direction', 'n_clicks']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'actions', 'ariaLabel']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(CustomSpeedDial, self).__init__(**args)
