from floods_html import json_format as jf


def json_to_html(input, svg_location=""):
    """
    Converts a flooding JSON object to flooding HTML object.

    Parameters
    ----------
    input : str or dict or FHJSON
        Input JSON object.
    svg_location='': str
        Location of the SVG files.

    Returns
    -------
    html_output : List[str]
        List of HTML strings for each entry in the JSON object.

    """
    if type(input) is str:
        pydantic_data_object = jf.FHJSON.model_validate_json(input)
    elif type(input) is dict:
        pydantic_data_object = jf.FHJSON(**input)
    elif isinstance(input, jf.FHJSON):
        pydantic_data_object = input
    else:
        raise ValueError("Invalid input type. Must be either a JSON string, JSON object, or a FHJSON class instance.")
    html_output = []
    for entry in pydantic_data_object.data:
        html_entry = entry_to_html(entry, svg_location)
        html_output.append(html_entry)
    return html_output


def entry_to_html(entry, svg_location):
    if entry.type == "table":
        return table_to_html(entry.data)
    elif entry.type == "svg_figure":
        return svg_figure_to_html(entry.data, svg_location)
    else:
        raise ValueError("Unknown entry type: {}".format(entry.type))


def table_to_html(json):
    html_table_header = ""
    html_table_rows = ""

    table_header_html_template = "<th{style}{classname}{id}{colspan}>{value}</th>"

    for table_header_entry in json.header:
        html_table_header += table_header_html_template.format(
            style=""
            if table_header_entry.style is None
            else ' style="' + ";".join([f"{k}:{v}" for k, v in table_header_entry.style.items()]) + '"',
            classname="" if table_header_entry.class_name is None else f' class="{table_header_entry.class_name}"',
            id="" if table_header_entry.id is None else f' id="{table_header_entry.id}"',
            colspan="" if table_header_entry.col_span is None else f" colspan={table_header_entry.col_span}",
            value=table_header_entry.value or "",
        )

    table_row_html_template = "<td{style}{classname}{id}{colspan}>{value}</td>"

    for table_row in json.rows:
        html_table_row = ""
        for table_entry in table_row:
            html_table_row += table_row_html_template.format(
                style=""
                if table_entry.style is None
                else ' style="' + ";".join([f"{k}:{v}" for k, v in table_entry.style.items()]) + '"',
                classname="" if table_entry.class_name is None else f' class="{table_entry.class_name}"',
                id="" if table_entry.id is None else f' id="{table_entry.id}"',
                colspan="" if table_entry.col_span is None else f" colspan={table_entry.col_span}",
                value=table_entry.value or "",
            )
        html_table_row = "<tr>" + html_table_row + "</tr>"
        html_table_rows += html_table_row

    table_html_template = """
    <h3>{title}</h3>
    <table class="table table-bordered">
        <thead><tr>{header}</tr></thead>
        <tbody>{body}</tbody>
    </table>
    """

    table_html = table_html_template.format(title=json.title, header=html_table_header, body=html_table_rows)

    return table_html


def svg_figure_to_html(json, svg_location):
    svg_file = svg_location + json.filename

    if svg_file[:4] == "http":
        figure_html_template = """
            <span>
                <h4>{title}</h4>
                <img src={imgname}/>
            </span>
        """

        figure_html = figure_html_template.format(
            title=json.title,
            imgname=svg_file,
        )
    else:
        figure_html_template = """
        <div>
            <span>
                <h4>{title}</h4>
                {svg}
            </span>
        </div>
        """

        svg_contents = open(svg_file, "r").read()

        figure_html = figure_html_template.format(
            title=json.title,
            svg=svg_contents,
        )

    return figure_html
