# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Form(Component):
    """A Form component.
Form component using Material-UI.
It creates a form with text fields and select fields based on the provided configuration.

Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- fields (list of dicts; optional):
    A list of field objects to be rendered in the Form. Each object
    should have properties like 'id', 'label', 'type', etc.

    `fields` is a list of dicts with keys:

    - defaultValue (string; optional)

    - disabled (boolean; optional)

    - helperText (string; optional)

    - id (string; required)

    - label (string; required)

    - native (boolean; optional)

    - options (list of dicts; optional)

        `options` is a list of dicts with keys:

        - label (string; required)

        - value (string; required)

    - readOnly (boolean; optional)

    - required (boolean; optional)

    - shrinkLabel (boolean; optional)

    - type (string; optional)

    - variant (a value equal to: 'outlined', 'filled', 'standard'; optional)

- values (dict; optional):
    An object containing the current values of the form fields. Keys
    are field IDs and values are the current values."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Form'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, fields=Component.UNDEFINED, values=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'fields', 'values']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'fields', 'values']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Form, self).__init__(**args)
