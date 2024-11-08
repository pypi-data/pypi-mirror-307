import streamlit as st
from functools import partial
from types import MethodType
from importlib.metadata import version

STREAMLIT_VERSION = version("streamlit")

CALLABLES_WITH_ADJUSTABLE_WIDTH = [
    "altair_chart",
    "area_chart",
    "bar_chart",
    "bokeh_chart",
    "button",
    "dataframe",
    "data_editor",
    "download_button",
    "pydeck_chart",
    "form_submit_button",
    "graphviz_chart",
    "image",
    "line_chart",
    "link_button",
    "map",
    "page_link",
    "plotly_chart",
    "popover",
    "pyplot",
    "scatter_chart",
    "vega_lite_chart",
]


def set_use_container_width_default(default: bool = True):
    """Set use_container_width to a default value for all Streamlit elements.

    Parameters
    ----------
    default : bool (default True)
        Default value to set use_container_width. In the case of st.image,
        use_column_width is modified instead.

    Returns
    -------
    None

    Examples
    --------
    >>> import streamlit as st
    >>> from st_default_width import set_use_container_width_default
    >>> set_use_container_width_default()
    >>> st.image("https://placehold.co/100x100")
    """

    for func_name in CALLABLES_WITH_ADJUSTABLE_WIDTH:
        kwarg = "use_container_width"

        ## API changed in version 1.40.0
        # https://github.com/streamlit/streamlit/pull/9547
        # Add use_container_width to st.image
        if func_name == "image":
            if int(STREAMLIT_VERSION.split(".")[1]) < 40:
                kwarg = "use_column_width"

        func = st.__dict__[func_name]

        if isinstance(func, MethodType):
            st.__dict__[func_name] = partial(func, **{kwarg: default})

        elif isinstance(func, partial):
            if func.keywords[kwarg] != default:
                st.__dict__[func_name].keywords[kwarg] = default


def revert_use_container_width_default():
    """Revert use_container_width to its default value for all Streamlit elements.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Examples
    --------
    >>> import streamlit as st
    >>> from st_default_width import revert_use_container_width_default
    >>> set_use_container_width_default()
    >>> revert_use_container_width_default()
    >>> st.image("https://placehold.co/100x100")
    """

    for func_name in CALLABLES_WITH_ADJUSTABLE_WIDTH:
        func = st.__dict__[func_name]

        if isinstance(func, partial):
            st.__dict__[func_name] = func.func
