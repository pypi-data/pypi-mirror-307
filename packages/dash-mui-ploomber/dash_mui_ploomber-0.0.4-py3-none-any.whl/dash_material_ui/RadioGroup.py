# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class RadioGroup(Component):
    """A RadioGroup component.
RadioGroup component using Material-UI.
It allows users to select one option from a set of mutually exclusive choices.

Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- direction (a value equal to: 'row', 'column'; default 'column'):
    The direction of the radio group. Can be 'row' or 'column'.

- label (string; optional):
    The label for the radio group.

- options (list of dicts; required):
    An array of objects, each containing a value and a label for the
    radio options.

    `options` is a list of dicts with keys:

    - disabled (boolean; optional)

    - label (string; required)

    - value (string; required)

- value (string; optional):
    The currently selected value."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'RadioGroup'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, label=Component.UNDEFINED, options=Component.REQUIRED, value=Component.UNDEFINED, onChange=Component.UNDEFINED, direction=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'direction', 'label', 'options', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'direction', 'label', 'options', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'options']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(RadioGroup, self).__init__(**args)
