# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Paper(Component):
    """A Paper component.
Paper component using Material-UI.
It can be customized with various optional props like elevation and variant.
The 'id' prop is required for Dash callbacks.

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the Paper component.

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- elevation (number; default 1):
    The elevation of the Paper component. Accepts values from 0 to 24.

- variant (a value equal to: 'elevation', 'outlined'; default 'elevation'):
    The variant to use. Either 'elevation' or 'outlined'."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Paper'
    @_explicitize_args
    def __init__(self, children=None, id=Component.REQUIRED, elevation=Component.UNDEFINED, variant=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'elevation', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'elevation', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Paper, self).__init__(children=children, **args)
