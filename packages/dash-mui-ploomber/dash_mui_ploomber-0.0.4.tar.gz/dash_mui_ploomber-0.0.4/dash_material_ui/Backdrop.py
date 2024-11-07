# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Backdrop(Component):
    """A Backdrop component.
Backdrop component using Material-UI.
It shows an overlay backdrop, useful for loading or other UI feedback.

Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- invisible (boolean; default False):
    If True, the backdrop is invisible.

- open (boolean; default False):
    If True, the backdrop is open."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Backdrop'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, open=Component.UNDEFINED, invisible=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'invisible', 'open']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'invisible', 'open']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Backdrop, self).__init__(**args)
