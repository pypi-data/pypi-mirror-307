# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Pagination(Component):
    """A Pagination component.


Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- boundaryCount (number; default 1):
    Number of always visible pages at the beginning and end.

- color (a value equal to: 'standard', 'primary', 'secondary'; default 'standard'):
    The color of the component.

- count (number; default 1):
    The total number of pages.

- defaultPage (number; default 1):
    The default page number (uncontrolled component).

- disabled (boolean; default False):
    If True, the pagination component will be disabled.

- hideNextButton (boolean; default False):
    If True, hide the next-page button.

- hidePrevButton (boolean; default False):
    If True, hide the previous-page button.

- page (number; default 1):
    The current page number.

- shape (a value equal to: 'circular', 'rounded'; default 'circular'):
    The shape of the pagination items.

- showFirstButton (boolean; default False):
    If True, show the first-page button.

- showLastButton (boolean; default False):
    If True, show the last-page button.

- siblingCount (number; default 1):
    Number of always visible pages before and after the current page.

- size (a value equal to: 'small', 'medium', 'large'; default 'medium'):
    The size of the pagination component.

- variant (a value equal to: 'text', 'outlined'; default 'text'):
    The variant to use."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_ui'
    _type = 'Pagination'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, count=Component.UNDEFINED, page=Component.UNDEFINED, defaultPage=Component.UNDEFINED, siblingCount=Component.UNDEFINED, boundaryCount=Component.UNDEFINED, variant=Component.UNDEFINED, shape=Component.UNDEFINED, size=Component.UNDEFINED, color=Component.UNDEFINED, disabled=Component.UNDEFINED, showFirstButton=Component.UNDEFINED, showLastButton=Component.UNDEFINED, hidePrevButton=Component.UNDEFINED, hideNextButton=Component.UNDEFINED, onChange=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'boundaryCount', 'color', 'count', 'defaultPage', 'disabled', 'hideNextButton', 'hidePrevButton', 'page', 'shape', 'showFirstButton', 'showLastButton', 'siblingCount', 'size', 'variant']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'boundaryCount', 'color', 'count', 'defaultPage', 'disabled', 'hideNextButton', 'hidePrevButton', 'page', 'shape', 'showFirstButton', 'showLastButton', 'siblingCount', 'size', 'variant']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Pagination, self).__init__(**args)
