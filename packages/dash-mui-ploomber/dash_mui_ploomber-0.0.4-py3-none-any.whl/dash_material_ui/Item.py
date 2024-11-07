# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Item(Component):
    """An Item component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the item.

- size (string | number; default 'auto'):
    The size of the item."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Item'
    @_explicitize_args
    def __init__(self, children=None, size=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'size']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'size']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Item, self).__init__(children=children, **args)
