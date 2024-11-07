# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CheckBoxTable(Component):
    """A CheckBoxTable component.


Keyword arguments:

- id (string; optional)

- columns (list of dicts; optional)

    `columns` is a list of dicts with keys:

    - disablePadding (boolean; optional)

    - field (string; required)

    - headerName (string; required)

    - numeric (boolean; optional)

    - width (number; optional)

- data (list of dicts; optional)

- selected (list of string | numbers; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'CheckBoxTable'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, columns=Component.UNDEFINED, selected=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'columns', 'data', 'selected']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'columns', 'data', 'selected']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(CheckBoxTable, self).__init__(**args)
