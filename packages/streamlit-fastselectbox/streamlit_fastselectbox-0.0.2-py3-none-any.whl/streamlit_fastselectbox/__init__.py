import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "st_fastselectbox",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "st_fastselectbox", path=build_dir)


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.


def st_fastselectbox(
        label,
        options,
        index=0,
        max_results=None,
        key=None,
        on_change=None,
        args=None,
        kwargs=None,
        *,
        placeholder="Choose an option",
        disabled=False,
        label_visibility="visible",
        is_searchable=False,
        is_clearable=False,
):
    """
    A streamlit component that displays a selectbox with autocompletion and allows limiting the results.

    Parameters
    ----------
    options: list of str or list of dict such as {'label': str, 'value': str}
        The list of options to select from.
    max_results: int
        The maximum number of options to return.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    on_change: callable
        A callback function to be called when the user selects an option.
        The callback will receive the selected value as an argument.
    args: list or None
        Additional arguments to pass to the callback function.
    kwargs: dict or None
        Additional keyword arguments to pass to the callback function.

    Returns
    -------
    str
        The selected value of the selectbox.
    """
    def _format_options(options):
        """Ensure options are in the form [{'label': ..., 'value': ...}]"""
        if isinstance(options, list) and all(isinstance(opt, str) for opt in options):
            # If options is a list of strings, create {label, value} pairs
            return [{"label": opt, "value": opt} for opt in options]
        elif isinstance(options, list) and all(isinstance(opt, dict) for opt in options):
            # If options are already in the correct format, return as is
            return options
        else:
            raise ValueError(
                "Options must be a list of strings or a list of {'label': ..., 'value': ...} dictionaries.")

    options = _format_options(options)

    on_change_callback = None
    if callable(on_change):
        args = args if args else []
        kwargs = kwargs if kwargs else {}

        def callback_function(*args, **kwargs):
            return lambda: on_change(*args, **kwargs)
        on_change_callback = callback_function(*args, **kwargs)

    component_value = _component_func(
        label=label,
        options=options,
        index=index,
        maxResults=max_results,
        key=key,
        on_change=on_change_callback,
        placeholder=placeholder,
        isDisabled=disabled,
        labelVisibility=label_visibility,
        isSearchable=is_searchable,
        isClearable=is_clearable,
    )
    return component_value
