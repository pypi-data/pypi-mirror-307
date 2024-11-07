#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Saga Inc.
# Distributed under the terms of the GPL License.

import io
from typing import Any, Dict, List, Optional

import plotly.graph_objects as go

from mitosheet.state import State
from mitosheet.types import ColumnHeader

# Graph types should be kept consistent with the GraphType in GraphSidebar.tsx
SCATTER = "scatter"
LINE = "line"
BAR = "bar"
HISTOGRAM = "histogram"
BOX = "box"
STRIP = "strip"
VIOLIN = "violin"
ECDF = "ecdf"
DENSITY_HEATMAP = "density heatmap"
DENSITY_CONTOUR = "density contour"

# Label for each type of graph used in the graph title
GRAPH_TITLE_LABELS = {
    SCATTER: "scatter plot",
    LINE: "line",
    BAR: "bar chart",
    BOX: "box plot",
    HISTOGRAM: "histogram",
    STRIP: "strip",
    VIOLIN: "violin",
    ECDF: "ecdf",
    DENSITY_HEATMAP: "density heatmap",
    DENSITY_CONTOUR: "density contour",
}


def get_graph_title(
    x_axis_column_headers: List[ColumnHeader],
    y_axis_column_headers: List[ColumnHeader],
    filtered: bool,
    graph_type: str,
) -> str:
    """
    Helper function for determing the title of the graph
    """
    # Get the label to let the user know that their graph had a filter applied.
    graph_filter_label: Optional[str] = "(first 1000 rows)" if filtered else None

    # Compile all of the column headers into one comma separated string
    all_column_headers = (", ").join(
        str(s) for s in x_axis_column_headers + y_axis_column_headers
    )
    # Get the title of the graph based on the type of graph
    graph_title_label = GRAPH_TITLE_LABELS[graph_type]

    # Combine all of the non empty graph title components into one list
    graph_title_components = (
        [all_column_headers, graph_filter_label, graph_title_label]
        if graph_filter_label is not None
        else [all_column_headers, graph_title_label]
    )

    # Return a string with all of the graph_title_components separated by a space
    return " ".join(graph_title_components)


def get_new_graph_tab_name(graph_data_array: List[Dict[str, Any]]) -> str:
    """
    Creates the name for the new graph tab sheet using the format
    graph0, graph1, etc.
    """
    all_graph_names = []
    for graph_data in graph_data_array:
        all_graph_names.append(graph_data["graph_tab_name"])
    
    graph_number_indicator = 0
    new_graph_name = f'graph{graph_number_indicator}'

    while new_graph_name in all_graph_names:
        graph_number_indicator += 1
        new_graph_name = f'graph{graph_number_indicator}'
        
    return new_graph_name

def get_graph_index_by_graph_id(graph_data_array: List[Dict[str, Any]], graph_id: str) -> int:
    """
    Given a graph_id, returns the index of the graph_data_array that has that graph_id
    """
    for index, graph_data in enumerate(graph_data_array):
        if "graph_id" in graph_data and graph_data["graph_id"] == graph_id:
            return index

    return -1

def get_html_and_script_from_figure(
    fig: go.Figure, height: str, width: str,
    include_plotlyjs: bool,
) -> Dict[str, str]:
    """
    Given a plotly figure, generates HTML from it, and returns
    a dictonary with the div and script for the frontend.

    The plotly HTML generated by the write_html function call is a div with two children:
    1. a div that contains the id for the graph itself
    2. a script that actually builds the graph

    Because we have to dynamically execute the script, we split these into two
    strings, to make them easier to do what we need on the frontend
    """
    # Send the graph back to the frontend
    buffer = io.StringIO()
    fig.write_html(
        buffer,
        full_html=False,
        include_plotlyjs=include_plotlyjs,
        default_height=height,
        default_width=width,
    )

    original_html = buffer.getvalue()


    # Everything in a script tag we want to treat as one big script

    # The get the graph div, which looks like: <div id="9c21d143-3fcd-4958-9295-ac7ada668186" class="plotly-graph-div" style="height:425px; width:970px;"></div>
    # This is the only div we need to put on the frontend.
    div = original_html[original_html.find('<div id='):original_html.find('</div>', original_html.find('<div id='))]

    # Get all the scripts that are between the <script> tags, and join them together. If include_plotlyjs is true, this includes
    # the plotly js script, and otherwise, it's just the data and the script that uses Plotly to build the graph on the div above
    script = ''
    index = 0
    while index < len(original_html):
        script_start = original_html.find('<script type="text/javascript">', index)
        script_end = original_html.find('</script>', script_start)

        if script_start == -1 or script_end == -1:
            break

        # Get rid of the initial script
        script_start += len('<script type="text/javascript">')
        script = script + original_html[script_start:script_end] + ';\n'
        index = script_end + 9

    return {"html": div, "script": script}

def get_column_header_from_optional_column_id_graph_param(
    state: State, 
    graph_creation_params: Dict[str, Any], 
    param_name: str
) -> Optional[ColumnHeader]:
    sheet_index = graph_creation_params['sheet_index']
    if param_name in graph_creation_params.keys() and graph_creation_params[param_name] in state.column_ids.column_id_to_column_header[sheet_index].keys():
        return state.column_ids.get_column_header_by_id(sheet_index, graph_creation_params[param_name])
    else: return None

