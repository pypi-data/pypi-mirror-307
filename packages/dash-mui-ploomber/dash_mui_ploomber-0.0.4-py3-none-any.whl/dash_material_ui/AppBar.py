# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AppBar(Component):
    """An AppBar component.
AppBar component using Material-UI.
It provides a header with customizable title, menu button, and navigation sections.

Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- color (a value equal to: 'default', 'primary', 'secondary', 'inherit', 'transparent'; default 'primary'):
    The color of the AppBar.

- position (a value equal to: 'fixed', 'absolute', 'sticky', 'static', 'relative'; default 'static'):
    The position of the AppBar.

- sections (dict with strings as keys and values of type string; optional):
    A dictionary of sections to be displayed in the AppBar. The keys
    are the section names and the values are the section paths.

- showMenuButton (boolean; default True):
    Whether to show the menu button.

- title (string; default 'App Bar'):
    The title to be displayed in the AppBar."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'AppBar'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, title=Component.UNDEFINED, showMenuButton=Component.UNDEFINED, position=Component.UNDEFINED, color=Component.UNDEFINED, sections=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'color', 'position', 'sections', 'showMenuButton', 'title']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'color', 'position', 'sections', 'showMenuButton', 'title']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(AppBar, self).__init__(**args)
