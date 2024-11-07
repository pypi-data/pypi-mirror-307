# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ButtonGroup(Component):
    """A ButtonGroup component.
ButtonGroup component using Material-UI.
It provides a group of buttons with customizable variant, size, color, orientation, and aria-label.
The component updates a property with the ID of the last clicked button.

Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- ariaLabel (string; default 'button group'):
    The aria-label for the ButtonGroup.

- buttons (list of dicts; optional):
    A list of button objects to be rendered in the ButtonGroup. Each
    object should have 'id' and 'label' properties.

    `buttons` is a list of dicts with keys:

    - id (string; required)

    - label (string; required)

- color (a value equal to: 'primary', 'secondary', 'error', 'info', 'success', 'warning'; default 'primary'):
    The color of the ButtonGroup.

- lastClicked (string; optional):
    The ID of the last clicked button.

- orientation (a value equal to: 'horizontal', 'vertical'; default 'horizontal'):
    The orientation of the ButtonGroup.

- size (a value equal to: 'small', 'medium', 'large'; default 'medium'):
    The size of the ButtonGroup.

- variant (a value equal to: 'text', 'outlined', 'contained'; default 'contained'):
    The variant to use for the ButtonGroup."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'ButtonGroup'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, variant=Component.UNDEFINED, size=Component.UNDEFINED, color=Component.UNDEFINED, orientation=Component.UNDEFINED, ariaLabel=Component.UNDEFINED, buttons=Component.UNDEFINED, lastClicked=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'ariaLabel', 'buttons', 'color', 'lastClicked', 'orientation', 'size', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ariaLabel', 'buttons', 'color', 'lastClicked', 'orientation', 'size', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(ButtonGroup, self).__init__(**args)
