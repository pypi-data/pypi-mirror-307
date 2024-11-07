# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Card(Component):
    """A Card component.


Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- buttonText (string; optional):
    The text for the button.

- content (string; optional):
    The content of the card.

- n_clicks (number; default 0):
    Number of times the button has been clicked.

- subtitle (string; optional):
    The subtitle of the card.

- title (string; optional):
    The title of the card.

- topic (string; optional):
    The topic of the card."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Card'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, topic=Component.UNDEFINED, title=Component.UNDEFINED, subtitle=Component.UNDEFINED, content=Component.UNDEFINED, buttonText=Component.UNDEFINED, n_clicks=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'buttonText', 'content', 'n_clicks', 'subtitle', 'title', 'topic']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'buttonText', 'content', 'n_clicks', 'subtitle', 'title', 'topic']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Card, self).__init__(**args)
