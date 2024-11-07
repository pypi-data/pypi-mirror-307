# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Select(Component):
    """A Select component.
Select component using Material-UI.
It allows selecting from multiple options.
The 'id' prop is required.

Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- disabled (boolean; default False):
    If True, the select is disabled.

- error (boolean; default False):
    If True, the select displays an error.

- helperText (string; default ''):
    Optional helper text to display below the select.

- label (string; optional):
    The label for the select input.

- options (list of dicts; required):
    The available options for the select.

    `options` is a list of dicts with keys:

    - label (string; required)

    - value (string; required)

- readOnly (boolean; default False):
    If True, the select is read-only.

- required (boolean; default False):
    If True, the select input is required.

- value (string; default ''):
    The currently selected value."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Select'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, label=Component.UNDEFINED, value=Component.UNDEFINED, options=Component.REQUIRED, disabled=Component.UNDEFINED, error=Component.UNDEFINED, readOnly=Component.UNDEFINED, required=Component.UNDEFINED, helperText=Component.UNDEFINED, onChange=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'disabled', 'error', 'helperText', 'label', 'options', 'readOnly', 'required', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'disabled', 'error', 'helperText', 'label', 'options', 'readOnly', 'required', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'options']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Select, self).__init__(**args)
