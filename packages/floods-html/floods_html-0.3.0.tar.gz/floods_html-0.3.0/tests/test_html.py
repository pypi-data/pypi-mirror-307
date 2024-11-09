import pytest
import html5lib
import floods_html as fh

test_obj_1 = fh.FHJSON(
    data=[
        fh.FHObject(
            type="svg_figure",
            data=fh.FHFigure(title="Test Figure", filename="https://website/test.svg"),
        ),
        fh.FHObject(
            type="table",
            data=fh.FHTable(
                title="Table One",
                header=[
                    fh.FHTableEntry(value=40, style={"background-color": "FFFFFF"}),
                    fh.FHTableEntry(value="Name", style={"background-color": "FFFFFF"}),
                ],
                rows=[
                    [fh.FHTableEntry(value="540", style={"text-align": "center"}), fh.FHTableEntry(value=None)],
                    [
                        fh.FHTableEntry(value="540", style={"background-color": "FF0000"}),
                        fh.FHTableEntry(value=670, style={"color": "FFFFFF"}),
                    ],
                ],
            ),
        ),
    ]
)

test_obj_2 = fh.FHJSON(
    data=[
        fh.FHObject(
            type="table",
            data=fh.FHTable(
                title="Table One",
                header=[
                    fh.FHTableEntry(value="Naming", col_span=3),
                ],
                rows=[
                    [
                        fh.FHTableEntry(value="540", style={"background-color": "FFFFFF"}),
                        fh.FHTableEntry(value=None, id="test"),
                        fh.FHTableEntry(value=517863, class_name="test"),
                    ],
                ],
            ),
        ),
        fh.FHObject(
            type="svg_figure",
            data=fh.FHFigure(title="Test Figure 1", filename="https://website/test.svg"),
        ),
        fh.FHObject(type="svg_figure", data=fh.FHFigure(title="Test Figure 2", filename="https://website/test.png")),
    ]
)


@pytest.mark.parametrize(
    "json_info, export_type",
    [
        (test_obj_1, "str"),
        (test_obj_2, "str"),
        (test_obj_1, "dict"),
        (test_obj_2, "dict"),
        (test_obj_1, "object"),
        (test_obj_2, "object"),
    ],
)
def test_valid_html_default_construction(json_info, export_type):
    if export_type == "str":
        exported_object = json_info.model_dump_json()
    elif export_type == "dict":
        exported_object = json_info.model_dump()
    elif export_type == "object":
        exported_object = json_info

    html5parser = html5lib.HTMLParser(strict=True)
    for html in fh.json_to_html(exported_object):
        html5parser.parseFragment(html)


@pytest.mark.parametrize("export_type", ["str", "dict", "object"])
def test_valid_html_manual_construction(export_type):
    json_object = fh.FHJSON()
    figure = fh.FHFigure(title="Test Figure", filename="https://website/test.svg")
    json_object.add_svg_figure(figure)
    table = fh.FHTable(title="Table One")
    table.add_header([fh.FHTableEntry(value=40, style={"background-color": "FFFFFF"}), fh.FHTableEntry(value="Name")])
    table.add_row([fh.FHTableEntry(value="540", class_name="test"), fh.FHTableEntry(value=None)])
    table.add_row([fh.FHTableEntry(value="540", id="test1 test2"), fh.FHTableEntry(value=670)])
    json_object.add_table(table)

    if export_type == "str":
        exported_object = json_object.model_dump_json()
    elif export_type == "dict":
        exported_object = json_object.model_dump()
    elif export_type == "object":
        exported_object = json_object

    html5parser = html5lib.HTMLParser(strict=True)
    for html in fh.json_to_html(exported_object):
        html5parser.parseFragment(html)
