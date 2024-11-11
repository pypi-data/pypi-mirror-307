# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashPictureAnnotation(Component):
    """A DashPictureAnnotation component.
DashPictureAnnotation is a Dash porting version for the React component:
`react-picture-annotation/ReactPictureAnnotation`.

This component provides a annotator that allows users to create, modify, or delete
the annotation information for a specific picture. This dash version has been
upgraded by adding the following features:
1. Responsive size with respect to the parent component.
2. Annotation type specified by a selector rather than an input box.
3. Only trigger the data update when the mouse is released.
4. Extensive functionalities for fine-grained customization of colors.
5. Disabling the annotator by a flag.
6. Setting a lower boundary of the annotation size to prevent small annotations
   created by mistake.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- class_name (string; optional):
    The css-class of the component. Use ` ` to separate different
    names. Often used with CSS to style elements with common
    properties.

- clearable_dropdown (boolean; default False):
    A flag. Set it to allow the annotation comment to be cleared when
    the dropdown box is being used.

- colors (dict with strings as keys and values of type string; optional):
    A dictionary of colors. The keys and the values represent the
    annotation name (specified by the `comment` property of `data`)
    and the color string, respectively. This method is used for
    specifying the annotation colors manually. It has a higher
    priority compared to `is_color_dynamic`.

- data (dict; optional):
    The annotation data. This value is a sequence of annotation items.
    Each item contain the positional information and the annotation
    comment (the object type). This value will can be updated by
    callbacks or user operations on the annotator.

    `data` is a dict with keys:

    - timestamp (number; optional):
        The time stamp of the current data. This value is used for
        identify the version of the data. It can also notify dash that
        the callback should be fired when this value changes.

    - data (list of dicts; optional):
        The body of the data. Returned from the React annotation data.

        `data` is a list of dicts with keys:

        - id (string; optional):

            The ID of the annotation item. It is only used for locating

            which annotation item is selected by users.

        - mark (dict; optional):

            The bounding box information of the annotation item.

            `mark` is a dict with keys:

            - x (number; optional):

                The X (horizontal) position of the upper left corner.

            - y (number; optional):

                The Y (vertical) position of the upper left corner.

            - width (number; optional):

                The width of the annotation item.

            - height (number; optional):

                The height of the annotation item.

            - type (a value equal to: "RECT"; optional):

                The shape of the annotation item. Currently, we only

                support \"RECT\".

        - comment (string; optional):

            The text comment on this annotation item. Typically, this

            value is specified by the type of the label.

- disabled (boolean; default False):
    A flag for disabling the annotator (make unclickable).

- image (string; optional):
    The URL to the image to be currently displayed on the annotator.
    The usage is similar to the property of the HTML image tag: `<img
    src={...}>`.

- is_color_dynamic (boolean; default False):
    A flag. If this flag is turned on, will make the color of each
    annotation box dynamically calculated based on the text of the
    annotation. An annotation box without a text comment will not be
    influenced.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

    - component_name (string; optional):
        Holds the name of the component that is loading.

- options (list of dicts; optional):
    The available options of the annotator. The usage is like the
    selector component `dcc.Dropdown(options=...)`. Each item
    represents an available choice of the annotation type. If this
    value is empty, will use a input box that allows users to specify
    any type names.

    `options` is a list of dicts with keys:

    - label (string; required):
        Label (displayed text) of the option.

    - value (boolean | number | string | dict | list; required):
        The value of the option which will be applied to the
        annotation data.

    - disabled (boolean; optional):
        A flag. If specified, this option item will be not selectable. | list of string | number | booleans | dict | a value equal to: null

- placeholder_dropdown (string; default "Select a tag"):
    The placeholder text when the editor is the dropdown component
    (the property `options` contains valid items).

- placeholder_input (string; default "Input tag here"):
    The placeholder text when the editor is the input box (the
    property `options` is empty).

- selected_id (string | a value equal to: null; optional):
    The ID of the currently selected annotator. This property is
    read-only. It will be automatically set when users select an
    annotator. A valid ID is a string. When no annotator is selected,
    this property returns `None`.

- size_minimal (dict; default {  width: 0,  height: 0,}):
    The requirement of the minimal annotation size. Any newly created
    annotation with a size smaller than this size will be dropped. If
    this value is configured as a scalar, will use it for both `width`
    and `height`. If any of the value is not set or configured as
    invalid values, will use `0`.

    `size_minimal` is a number | dict with keys:

    - width (number; optional):
        Requirement of the minimal width of an annotator.

    - height (number; optional):
        Requirement of the minimal height of an annotator.

- style (dict; default {height: "60vh"}):
    The css-styles which will override styles of the component
    container.

- style_annotation (dict; optional):
    The css-styles of the annotation marker (box). If this value is
    specified as a string, the string will be parsed as the default
    color of the annotation boxes.

    `style_annotation` is a string | dict with keys:

    - padding (number; optional):
        Shape style: text padding.

    - fontSize (number; optional):
        Shape style: text font size.

    - fontColor (string; optional):
        Shape style: text font color.

    - fontBackground (string; optional):
        Shape style: text background color.

    - fontFamily (string; optional):
        Shape style: text font name.

    - lineWidth (number; optional):
        Shape style: stroke width.

    - shapeBackground (string; optional):
        Shape style: background color in the middle of the marker.

    - shapeStrokeStyle (string; optional):
        Shape style: shape stroke color.

    - shadowBlur (number; optional):
        Shape style: stroke shadow blur.

    - shapeShadowStyle (string; optional):
        Shape style: shape shadow color.

    - transformerBackground (string; optional):
        Shape style: color of the scalable dots around the selected
        box.

    - transformerSize (number; optional):
        Shape style: size of the scalable dots around the selected
        box."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_picture_annotation'
    _type = 'DashPictureAnnotation'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, class_name=Component.UNDEFINED, style=Component.UNDEFINED, style_annotation=Component.UNDEFINED, colors=Component.UNDEFINED, image=Component.UNDEFINED, data=Component.UNDEFINED, options=Component.UNDEFINED, selected_id=Component.UNDEFINED, placeholder_input=Component.UNDEFINED, placeholder_dropdown=Component.UNDEFINED, clearable_dropdown=Component.UNDEFINED, disabled=Component.UNDEFINED, is_color_dynamic=Component.UNDEFINED, size_minimal=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'class_name', 'clearable_dropdown', 'colors', 'data', 'disabled', 'image', 'is_color_dynamic', 'loading_state', 'options', 'placeholder_dropdown', 'placeholder_input', 'selected_id', 'size_minimal', 'style', 'style_annotation']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'class_name', 'clearable_dropdown', 'colors', 'data', 'disabled', 'image', 'is_color_dynamic', 'loading_state', 'options', 'placeholder_dropdown', 'placeholder_input', 'selected_id', 'size_minimal', 'style', 'style_annotation']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DashPictureAnnotation, self).__init__(**args)
