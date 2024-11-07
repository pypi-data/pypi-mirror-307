# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Popover(Component):
    """A Popover component.
Popover component using Material-UI.
A customizable popover with a button to control its visibility.

Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- anchorOrigin (dict; default { vertical: 'bottom', horizontal: 'left' }):
    Anchor origin for the popover positioning.

    `anchorOrigin` is a dict with keys:

    - horizontal (a value equal to: 'left', 'center', 'right'; optional)

    - vertical (a value equal to: 'top', 'center', 'bottom'; optional)

- content (string; required):
    The content to display within the Popover.

- open (boolean; optional):
    Controls the open state of the Popover."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Popover'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, content=Component.REQUIRED, anchorOrigin=Component.UNDEFINED, open=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'anchorOrigin', 'content', 'open']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'anchorOrigin', 'content', 'open']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'content']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Popover, self).__init__(**args)
