# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Alert(Component):
    """An Alert component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The main content displayed in the alert.

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- action (a list of or a singular dash component, string or number; optional):
    The action to display. It renders after the message, at the end of
    the alert.

- open (boolean; default True):
    If True, the alert is displayed.

- severity (a value equal to: 'error', 'warning', 'info', 'success'; default 'success'):
    The severity of the alert.

- variant (a value equal to: 'standard', 'filled', 'outlined'; default 'standard'):
    The variant to use."""
    _children_props = ['action']
    _base_nodes = ['action', 'children']
    _namespace = 'dash_material_ui'
    _type = 'Alert'
    @_explicitize_args
    def __init__(self, children=None, id=Component.REQUIRED, severity=Component.UNDEFINED, variant=Component.UNDEFINED, onClose=Component.UNDEFINED, action=Component.UNDEFINED, open=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'action', 'open', 'severity', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'action', 'open', 'severity', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Alert, self).__init__(children=children, **args)
