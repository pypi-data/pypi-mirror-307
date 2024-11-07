# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Slider(Component):
    """A Slider component.


Keyword arguments:

- id (string; default ''):
    The ID used to identify this component in Dash callbacks.

- ariaLabel (string; default 'Slider'):
    The aria-label for the slider.

- defaultValue (number; default 30):
    The default value of the slider.

- disabled (boolean; default False):
    If True, the slider will be disabled.

- max (number; default 100):
    The maximum allowed value of the slider.

- min (number; default 0):
    The minimum allowed value of the slider.

- step (number; default 1):
    The step interval of the slider.

- value (number; default undefined):
    The current value of the slider."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Slider'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, defaultValue=Component.UNDEFINED, disabled=Component.UNDEFINED, ariaLabel=Component.UNDEFINED, min=Component.UNDEFINED, max=Component.UNDEFINED, step=Component.UNDEFINED, value=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'ariaLabel', 'defaultValue', 'disabled', 'max', 'min', 'step', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ariaLabel', 'defaultValue', 'disabled', 'max', 'min', 'step', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Slider, self).__init__(**args)
