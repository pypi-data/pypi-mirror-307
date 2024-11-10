import os
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
from dateutil.parser import parse
from datetime import datetime, date
import json
import yaml
from typing import List, Dict, Tuple, Union, Optional, Callable, Any, Literal
try:
    from .date_formatter import python_to_luxon_format
    from .utility_functions import allow_top_navigation, stringify_javascript_function, generate_js_function_from_json, stringify_file, reload_ajax_data
except Exception:
    from date_formatter import python_to_luxon_format
    from utility_functions import allow_top_navigation, stringify_javascript_function, generate_js_function_from_json, stringify_file, reload_ajax_data
# from streamlit_callback import register_callback


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

COMPONENT_NAME = "streamlit_datatables_net"

if _RELEASE:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        COMPONENT_NAME, path=build_dir)

else:
    _component_func = components.declare_component(
        COMPONENT_NAME,
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.


# @st.cache_data(show_spinner=False)
def get_datatables_net_config(dt_config: str) -> Tuple[str, list[str], list[str], Dict]:
    try:
        file_path = "config_datatables_net.yaml"
        with open(file_path, "r") as f:
            config_datatables_net: Dict = yaml.safe_load(f)
        config: Dict = config_datatables_net.get(dt_config)
        return config.get("class_name"), config.get("js_scripts"), config.get("stylesheets"), config.get("options")
    except Exception:
        return None, None, None


def df_to_denormalized_dict(df: pd.DataFrame, sep="."):
    """ The opposite of json_normalize. """
    result = []
    for idx, row in df.iterrows():
        parsed_row = {}
        for col_label, v in row.items():
            keys = col_label.split(sep)

            current = parsed_row
            for i, k in enumerate(keys):
                if i == len(keys)-1:
                    current[k] = v
                else:
                    if k not in current.keys():
                        current[k] = {}
                    current = current[k]
        result.append(parsed_row)
    return result


def apply_date_formatting(df: pd.DataFrame, date_format='%-m/%d/%Y', denormalize: bool = False):
    """Identify datetime columns and apply the desired format"""
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime(date_format)
        elif df[col].apply(lambda x: isinstance(x, date)).all():
            df[col] = df[col].apply(lambda x: x.strftime(date_format))

    return df


def setDatatableOptions(options: Dict = None, default_options: Dict = None) -> Dict:
    if options is None:
        options = {}
    if default_options is None:
        default_options = {}

    merged_options = default_options.copy()
    merged_options.update(options)

    return merged_options


def st_datatable(data: pd.DataFrame | list[dict] = None, boolean_to_string: bool = False, column_order: List[str] = None, options: Dict = None, dt_config: str = "default", class_name: str = None, common_js_functions: Dict = None, context_menu: Dict = None,  js_scripts: List[str] = None, stylesheets: List[str] = None, css_files: List[str] = None, enable_top_navigation: bool = False, date_format: str = None, is_datetime: bool = False, export_file_name: str = None, on_select: Optional[Union[Literal["ignore"], Literal["rerun"], Callable]] = "rerun", ajax_setup: Dict = None, ajax_auto_refresh_period: int = None, enable_diagnostics: bool = False, args: Optional[Tuple[Any, ...]] = None,
                 kwargs: Optional[Dict[str, Any]] = None, key=None):
    """Create a new instance of "st_datatable".

    Parameters
    ----------
    data: pandas.DataFrame, list(dict)
        The data to display.
    column_order: List[str]
        Specifies the display order of columns. This also affects which columns are visible. For example, column_order=("col2", "col1") will display 'col2' first, followed by 'col1', and will hide all other non-index columns. If None (default), the order is inherited from the original data structure.
    options: dict
        The options to set the data attributes and configuration options for the datatable.
    dt_config: str
        An optional parameter to use a YAML configuration file to specify the class_name, js_scripts, stylesheets, and options.  
        Specified options will be used by default but individual options may be overridden by providing options.

        The YAML file should be named config_datatables_net.yaml and follow this structure:

    default:
        js_scripts:\n
            -  https://cdn.datatables.net/v/dt/jq-3.7.0/jszip-3.10.1/dt-1.13.6/b-2.4.1/b-html5-2.4.1/b-print-2.4.1/r-2.5.0/datatables.min.js\n
        stylesheets:\n
            - https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css\n
        class_name: compact row-border hover nowrap\n
        options:
          scrollX: true
          stateSave: true
          stateDuration: -1
          responsive: true

    class_name: str or None
        An optional str of class names to apply to the datatable (e.g., 'compact hover').
    common_js_functions: Dict or None
        An optional dictionary of function names mapped to stringified JavaScript functions.  These functions will be instantiated as common functions 
        which are available for use by render functions.  The functions are called as window.commonJsFunctions.<<function_name>>().

        For example:
        common_js_functions = { "sayHello": "function sayHello: function sayHello(name){ return `Hello ${name}! `}" }

    context_menu: Dict or None
        An optional dictionary to configue a context men.  The context menu appears when clicking on an element with a specified class name.
        Clicking on a context menu item will return information on the row and the menu item clicked by the user.

        The context menu items are dynamically set using the provided name.  The hrefFunctionName and target attributes are optional.  The hrefFunctionName 
        attribute makes use of a JavaScript function that accepts the item and row data.  The function should be included in the common_js_functions
        and follow this signature:

        function myHrefFunctionName(item, row) {
            if (row){
                let href = `/yourlink?id=${row.id}`
                return href
            }
        }

        For example:
        content_menu = {
            "className": "fa-ellipsis-v",
            "items": [
                {
                    "name": "View",
                    "hrefFunctionName": "myHrefFunctionName",
                    "target": "_blank"
                },
                {
                    "name": "Edit",
                    "hrefFunctionName": "myHrefFunctionName",
                    "target": "_self"
                }
            ]
        }

    js_scripts: list or None
        An optional list of urls for javascripts to apply to the datatable.
    stylesheets: list or None
        An optional list of urls for stylesheets to apply to the datatable.
    css_files: list[str] or None
        An optional list of stringified css files to include in style tags to apply to the datatable.

        css_files = [stringify(CSS_A_FILEPATH), stringify(CSS_B_FILEPATH)]

    enable_top_navigation:
        An optional boolean, which allows opening html links using target="top" or target="parent". The default is False.
    date_format:
        An optional string which will display datetime fields in the specified date format (e.g. '%m/%d/%Y'). Datetime fields should be provided in the specfied string. Alternatively, you may also enable the is_datetime option to convert datetime fields to the specified date_format.  The default is None.
    is_datetime:
        An optional boolean indicating date/time fields are of Python datetime, date or time types and should be used to convert to the date_format string.  The default is False.
    export_file_name:
        An optional string to use for file name of downloaded files if using Datatable export buttons (e.g, Excel, csv).  Default value is 'datatable'.

    on_select : "ignore" or "rerun" or callable
            How the datatable should respond to user selection events. This
            controls whether or not the datatable behaves like an input widget.
            ``on_select`` can be one of the following:

            - ``"rerun"`` (default): Streamlit will rerun the app when the user selects
              rows in the datatable. In this case, ``st_datatable``
              will return the selection data as a dictionary.

            - ``"ignore"``: Streamlit will not react to any selection
              events in the datatable. The datatable will not behave like an
              input widget.

            - A ``callable``: Streamlit will rerun the app and execute the
              ``callable`` as a callback function before the rest of the app.
              In this case, ``st_datatable`` will return the selection data
              as a dictionary.

    args: tuple
        An optional tuple of args to pass to the callback.

    kwargs: dict
        An optional dict of kwargs to pass to the callback.

    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    ajax_setup: Dict or None
        An optional dictionary to configure the ajax setting.  For example:
        ajax_setup = {
            headers: {
                'Content-type': "application/x-www-form-urlencoded",
                'X-CSRFToken': csrf_token
            }
        }

    ajax_auto_refresh_period: int or None
        An optional parameter defining the number of seconds to wait before automatically refreshing the table 
        from its ajax source.  Default value is None.

    enable_diagnostics:
        An optional boolean which will display diagnostic info for the datatable in the console and terminal. The default is False.


    Returns
    -------
    dict | list
        A dict with details of the datatable row clicked by the user.

        Example response:
        {
            "data": {
                "id": "1",
                "name": "Tiger Nixon",
                "position": "System Architect",
                "salary": 320800,
                "start_date": "datetime.datetime(2012, 4, 25, 0, 0)",
                "office": "Edinburgh",
                "extn": "5421",
                "address": {
                "street": "123 Main St",
                "city": "Anytown"
                }
            },
            "datasetName": datasetValue,
            "classList": {
                "0": "sorting_1"
            },
            "time" 1721744272014
        }

    If rowReorder is enabled as an option, a rowReorder event will return a list of dictionaries.
    The list will include a dictionary for each row impacted by the reorder.

    [
    {
        "data": { ... }
        "eventType": "rowReorder",
        "rowReorderDetails": {"oldData": 1, "newData": 3, "newPosition": 2, "oldPosition": 0}
    },
    ]


    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    if options is None:
        options = {}
    default_options = {}
    if dt_config:
        config_class_name, config_js_scripts, config_stylesheets, default_options = get_datatables_net_config(
            dt_config)
    if not class_name and config_class_name:
        class_name = config_class_name
    if not js_scripts and config_js_scripts:
        js_scripts = config_js_scripts
    if not stylesheets and config_stylesheets:
        stylesheets = config_stylesheets

    options = setDatatableOptions(
        options=options, default_options=default_options)

    if column_order:
        options["columns"] = [{"data": column, "title": column, "name": column}
                              for column in column_order]
    if "ajax" in options:
        if "columns" not in options:
            st.warning(
                "Either columns or column_order must be included in options for Ajax data sources.")
            return {}

    elif isinstance(data, pd.DataFrame):
        if date_format is not None and is_datetime:
            df = apply_date_formatting(data, date_format=date_format)
            df_dict = df.to_dict(orient='records')
            options["data"] = df_dict
        else:
            options["data"] = json.loads(data.to_json(orient="records"))

        if "columns" not in options:
            options["columns"] = [{"data": column, "title": column, "name": column}
                                  for column in data.columns]
    elif isinstance(data, list):
        df_dict = None
        if date_format is not None and is_datetime:
            df = pd.json_normalize(data)
            df = apply_date_formatting(df, date_format=date_format)
            df_dict = df_to_denormalized_dict(df)
            data = df_dict
        options["data"] = data
        if "columns" not in options and data:
            if df_dict is None:
                df = pd.json_normalize(data)
                df_dict = df.to_dict(orient="records")
            columns = list(df_dict[0].keys())
            options["columns"] = [{"data": column, "title": column, "name": column}
                                  for column in columns]
        elif "columns" not in options:
            st.warning("Unable to display datatable: data is invalid")
            return {}
    else:
        st.warning("Unable to display datatable: data is invalid")
        return {}

    luxon_date_format = None
    if date_format is not None:
        luxon_date_format = python_to_luxon_format(date_format)

    on_change = None
    if on_select == "ignore":
        is_ignored = True
        on_select = None
    elif on_select == "rerun":
        is_ignored = False
        on_select = None
    elif callable(on_select):
        is_ignored = False
        on_change = on_select

    if callable(on_select) and (args or kwargs):
        args = args if args else []
        kwargs = kwargs if kwargs else {}

        def callback_function(*args, **kwargs):
            return lambda: on_select(*args, **kwargs)
        on_change = callback_function(*args, **kwargs)

    table_id = None
    if key:
        table_id = f'{key.replace(" ","_")}'
    if not key and options.get("stateSave"):
        print("st_datatable error: key is required when stateSave is enabled")
        return

    # with open(f"options_{table_id}_responsive.json", "w") as f:
    #     f.write(json.dumps(options))
    is_ajax_data = options.get("ajax", False)
    ajax_reload = None
    if is_ajax_data and "_st_datatable_ajax_reload_key" not in st.session_state:
        st.session_state["_st_datatable_ajax_reload_key"] = None
    if is_ajax_data:
        ajax_reload = st.session_state["_st_datatable_ajax_reload_key"]
    component_value = _component_func(
        options=options, boolean_to_string=boolean_to_string, class_name=class_name, context_menu=context_menu, common_js_functions=common_js_functions,  js_scripts=js_scripts, stylesheets=stylesheets, css_files=css_files, key=key, table_id=table_id, on_change=on_change, is_ignored=is_ignored, date_format=luxon_date_format, export_file_name=export_file_name, ajax_reload=ajax_reload, ajax_setup=ajax_setup, ajax_auto_refresh_period=ajax_auto_refresh_period, enable_diagnostics=enable_diagnostics, default=None)

    if enable_top_navigation:
        iframe_title = f"{COMPONENT_NAME}.{COMPONENT_NAME}"
        if __name__ == "__main__":
            iframe_title = f"__init__.{COMPONENT_NAME}"
        allow_top_navigation(iframe_title)

    if component_value and "data" in component_value and date_format is not None:
        for key, value in component_value["data"].items():
            try:
                component_value["data"][key] = datetime.strptime(
                    value, date_format)
            except Exception:
                continue

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.

    return component_value


if not _RELEASE:
    JAVASCRIPT_FILE_PATH = 'renderFunctions.js'
    CSS_LABELS_FILE_PATH = "css_labels.css"
    css_file = stringify_file(CSS_LABELS_FILE_PATH)

    def my_on_click_function(my_arg, key=None):
        print("You clicked me!", my_arg, key)

    st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
    print("script run")
    st.button("Rerun script")

    col_l, content_column, col_r = st.columns([1, 10, 1])
    with content_column:
        with st.container(border=True):
            if st.button("Reload Ajax data"):
                reload_ajax_data()
            options = {}
            options["keys"] = True
            options["scroller"] = True
            options["scrollY"] = 400
            options["scrollCollapse"] = True
            options["ajax"] = {
                "url": "https://dummyjson.com/products?delay=100",
                "type": "GET",
                "dataSrc": "products",
            }
            options["language"] = {
                "processing": "Loading...",
                "loadingRecords": "Please wait - loading...",
                "searchPlaceholder": "type here",
                "search": "Test Search:"
            },
            streamlit_action_function = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'streamlit_action_function')
            on_click_submit_table_values = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'on_click_submit_table_values')

            streamlit_action_button = {
                "text": "Trigger Streamlit Action", "action": streamlit_action_function}
            return_table_values_button = {
                "text": "Return Table Values", "action": on_click_submit_table_values}

            options["buttons"] = ['pageLength', 'colvis',
                                  'excel', streamlit_action_button, return_table_values_button]
            options["layout"] = {
                "top2Start": "buttons",
                "top1": {'searchPanes': {"initCollapsed": True}},
                'topEnd': 'search',
                'bottomStart': 'info',
                'bottomEnd': 'paging'
            }

            options["scrollX"] = True
            options["responsive"] = False
            options["processing"] = True
            options["rowReorder"] = {
                "dataSrc": "id",
                "update": False
            }

            price_settings = {"taxRate": 7.0}

            price_settings_function = generate_js_function_from_json(
                price_settings, "getPriceSettings")

            truncate_text = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'truncateText')

            price_plus_tax = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'pricePlusTax')

            show_ellipsis = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'showEllipsis')

            show_hamburger = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, 'showHamburger')

            render_learn_more_link = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, "renderLearnMoreLink")
            render_label = stringify_javascript_function(
                JAVASCRIPT_FILE_PATH, "renderLabel")

            common_js_functions = {
                "addPrefix": stringify_javascript_function(JAVASCRIPT_FILE_PATH, 'addPrefix'),
                "getPriceSettings": price_settings_function,
                "setViewHref": stringify_javascript_function(
                    JAVASCRIPT_FILE_PATH, 'setViewHref'),
                "setEditHref": stringify_javascript_function(
                    JAVASCRIPT_FILE_PATH, 'setEditHref'),
                "setDownloadHref": stringify_javascript_function(
                    JAVASCRIPT_FILE_PATH, 'setDownloadHref'),
                "setSearchHref": stringify_javascript_function(
                    JAVASCRIPT_FILE_PATH, 'setSearchHref'),
                "displayContextMenuItem": stringify_javascript_function(JAVASCRIPT_FILE_PATH, "displayContextMenuItem")
            }

            options["columns"] = [
                {"data": "id", "title": "id", "width": '20%'},
                {"data": "title", "title": "title", "width": '10%'},
                {"data": "category", "title": "category",
                    "render": render_label, "width": '10%'},
                {"data": None, "defaultContent": "", "title": "Learn More", "name": "learn_more",
                    "render": render_learn_more_link, "width": '10%'},
                {"data": "description", "title": "description",
                    "render": truncate_text, "width": '10%'},
                {"data": "price", "title": "price",
                    "className": "secondmenu", "width": '10%'},
                {"data": "price", "title": "price + tax",
                    "render": price_plus_tax, "width": '10%'},
                {"data": "reviews", "title": "reviews",
                    "render": "[, ].rating", "width": '10%'},
                {"data": None, "defaultContent": "",
                    "title": "", "orderable": False, "render": show_ellipsis, "width": '10%'},
            ]

            options["columnDefs"] = [
                {
                    "className": 'reorder',
                    "render": show_hamburger,
                    "targets": 0
                },
                {"searchPanes": {"orthogonal": "sp"},
                    "targets": "learn_more:name"},
            ]
            context_menu = []

            context_menu_1 = {}
            context_menu_1["className"] = "fa-ellipsis-v"
            context_menu_1["items"] = [
                {
                    "name": "View",
                    # "hrefFunctionName": "setViewHref",
                    # "target": "_blank"
                },
                {
                    "name": "Edit",
                    "hrefFunctionName": "setEditHref",
                    "target": "_blank"
                },
                {
                    "name": "See Special Sale Price",
                    "conditionalDisplayFunctionName": "displayContextMenuItem",
                },
                {
                    "name": "Download",
                    "hrefFunctionName": "setDownloadHref",
                    "target": "_blank"
                },
                {
                    "name": "Search",
                    "hrefFunctionName": "setSearchHref",
                    "target": "_blank"
                },
            ]

            ajax_setup = {
                "headers": {
                    'Content-type': "application/x-www-form-urlencoded",
                    'X-CSRFToken': "csrf_token"
                }
            }

            context_menu.append(context_menu_1)
            context_menu_2 = {}
            context_menu_2["className"] = "secondmenu"
            context_menu_2["items"] = [
                {
                    "name": "Open",
                    # "hrefFunctionName": "setViewHref",
                    # "target": "_blank"
                },
                {
                    "name": "Delete",
                    "hrefFunctionName": "setEditHref",
                    "target": "_blank"
                },
            ]

            context_menu.append(context_menu_2)

            filename = st.text_input("filename", "test")
            on_select = st.selectbox(
                "on_select", key="ajax_table_on_select", options=["ignore", "rerun"])

            dt_click = st_datatable(None, options=options, context_menu=context_menu, css_files=[css_file], common_js_functions=common_js_functions, ajax_setup=ajax_setup, ajax_auto_refresh_period=None,
                                    key="ajax_table", on_select=my_on_click_function, args=["args are here"], kwargs={"key": "ajax_table"}, export_file_name=filename, enable_diagnostics=False)
            if isinstance(dt_click, dict) and dt_click.get("customComponentValue"):
                print(dt_click)
            if isinstance(dt_click, List):
                for click in dt_click:
                    print(click["data"]["id"], click.get("rowReorderDetails"))
            st.write(dt_click)

        with st.container(border=True):
            st.write("Example: List of dictionaries")
            dt_container = st.container()
            with st.expander("Code"):
                with st.echo():
                    data = [
                        {
                            "id": "1",
                            "name": "Tiger Nixon",
                            "position": "System Architect",
                            "salary": 320800,
                            "start_date": "2012/04/25",
                            "office": "Edinburgh",
                            "extn": "5421",
                            "address": {"street": "123 Main St", "city": "Anytown"}
                        },
                        {
                            "id": "2",
                            "name": "Garrett Summers",
                            "position": "Accountant",
                            "salary": 170750,
                            "start_date": "2011/07/25",
                            "office": "Tokyo",
                            "extn": "8422",
                            "address": {"street": "456 Main St", "city": "Anytown"}
                        },
                        {
                            "id": "3",
                            "name": "Clark Kent",
                            "position": "Reporter",
                            "salary": 170750,
                            "start_date": "2009/09/30",
                            "office": "Gotham",
                            "extn": "8523",
                            "address": {"street": "789 Main St", "city": "Anytown"}
                        },
                    ]
                    column_order = ["name", "position", "start_date", "salary",
                                    "start_date", "office", "extn", "address.street", "address.city"]

                    options = {}
                    options["lengthChange"] = False
                    options["responsive"] = True
                    options["scrollX"] = False
                    options["stateSave"] = True
                    options["stateDuration"] = -1
                    options["select"] = {"style": "single", "info": True}
                    special_action_button = stringify_javascript_function(
                        JAVASCRIPT_FILE_PATH, "actionButton")
                    options["buttons"] = [
                        {"extend": "excel",
                         "text": "Export to Excel",
                         },
                        {"extend": "csv",
                         "text": "Export to CSV",
                         },
                        {"text": "Special Action Button",
                         "action": special_action_button}
                    ]
                    options["layout"] = {
                        "top3Start":  "buttons",
                        "top2Start": {"buttons": ['pageLength']},
                        "top1": 'searchPanes',
                        'topEnd': 'search',
                        'bottomStart': 'info',
                        'bottomEnd': 'paging'
                    }
                    options["searchPanes"] = False
                    for row in data:
                        row["start_date"] = (parse(row["start_date"])).date()

                    big_data = []
                    for i in range(10):
                        big_data.extend(data)

                    with dt_container:
                        on_select = st.selectbox("on_select", key="my-table-on-select", options=[
                            "ignore", "rerun", "callable"])
                        if on_select == "callable":
                            on_select = my_on_click_function
                        on_select = 'rerun'

                        dt_response = st_datatable(
                            big_data, column_order=column_order, options=options, key="example_1", dt_config="default", date_format="%m/%d/%Y", is_datetime=True, enable_top_navigation=False, export_file_name="Example 1", on_select=on_select, enable_diagnostics=False)
                        st.write(dt_response)
        with st.container(border=True):
            st.write("Example: List of dictionaries with columns property")
            dt_container = st.container()
            with st.expander("Code"):
                with st.echo():
                    data = [
                        {
                            "id": "1",
                            "name": "Tiger Nixon",
                            "position": "System Architect",
                            "salary": 320800,
                            "start_date": "2012/04/25",
                            "office": "Edinburgh",
                            "extn": "5421",
                            "address": {"street": "123 Main St", "city": "Anytown"}
                        },
                        {
                            "id": "2",
                            "name": "Garrett Summers",
                            "position": "Accountant",
                            "salary": 170750,
                            "start_date": "2011/07/25",
                            "office": "Tokyo",
                            "extn": "8422",
                            "address": {"street": "456 Main St", "city": "Anytown"}
                        },
                        {
                            "id": "3",
                            "name": "Clark Kent",
                            "position": "Reporter",
                            "salary": 170750,
                            "start_date": "2009/09/30",
                            "office": "Gotham",
                            "extn": "8523",
                            "address": {"street": "789 Main St", "city": "Anytown"}
                        },
                    ]
                    for item in data:
                        item["edit_link"] = "https://google.com"

                    show_action_buttons = stringify_javascript_function(
                        JAVASCRIPT_FILE_PATH, 'showActionButtons')
                    show_link = stringify_javascript_function(
                        JAVASCRIPT_FILE_PATH, 'showLink')

                    columns = [
                        {"data": "name", "title": "Name"},
                        {"data": "start_date", "title": "Start Date"},
                        {"data": "office", "title": "Office"},
                        {"data": "salary", "title": "Salary",
                            "render": ['number', ',', '.', 0, '$']},
                        {"data": None, "title": "New Actions",
                            "render": show_action_buttons},
                        {"data": None,
                            "title": "Open", "render": show_link},
                        {"data": "edit_link", "title": "Edit Link"},
                        {"data": "extn", "title": "extn", "className": "my_class"},
                    ]
                    options = {}
                    options["columns"] = columns
                    options["stateSave"] = True
                    options["stateDuration"] = -1
                    options["layout"] = {}
                    options["layout"]["top1"] = "searchBuilder"

                    with dt_container:
                        on_select = st.selectbox("on_select", options=[
                            "ignore", "rerun", "callable"])
                        if on_select == "callable":
                            on_select = my_on_click_function
                        dt_response = st_datatable(
                            data, options=options, key="example_1b", enable_top_navigation=True, date_format="%b %d %Y", is_datetime=True, on_select=on_select, enable_diagnostics=False)
                        st.write(dt_response)

        with st.container(border=True):
            st.write("Example: Pandas Dataframe")
            dt_container = st.container()
            with st.expander("Code"):
                with st.echo():
                    data = pd.DataFrame(
                        {
                            "name": ["Roadmap", "Extras", "Issues"],
                            "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
                            'date1': ['2021-11-01', '2021-02-01', '2022-01-01'],
                            "active": [True, True, True]
                        }
                    )
                    column_order = ["name"]
                    with dt_container:
                        dt_response = st_datatable(
                            data, key="example_2", date_format='%Y-%b-%d', on_select="ignore", boolean_to_string=True, enable_diagnostics=False)
                        st.write(dt_response)

        with st.container(border=True):
            st.write("Example: Empty list with columns property")
            dt_container = st.container()
            with st.expander("Code"):
                with st.echo():
                    data = []
                    options = {}
                    options["columns"] = [{"data": "name", "title": "name"}, {
                        "data": "url", "title": "url"}]
                    with dt_container:
                        st_datatable(data, options=options, key="example_3")

        with st.container(border=True):
            st.write("Example: Invalid data")
            dt_container = st.container()
            with st.expander("Code"):
                with st.echo():
                    data = None
                    with dt_container:
                        st_datatable(data, key="example_4")

        st.write(st.session_state)
