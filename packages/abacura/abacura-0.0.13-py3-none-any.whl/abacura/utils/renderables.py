from itertools import zip_longest
from rich.table import Table
from rich import box
from rich.text import Text
from rich.console import Group
from rich.panel import Panel
from rich.style import Style

from typing import Iterable
from dataclasses import dataclass, fields, is_dataclass, astuple
from typing import Union


@dataclass
class OutputColors:
    output: str = "#101018"
    panel: str = "#334455"    # Charcoal
    border: str = "#DDEEFF"
    section: str = "#11EEFF"  # Cyan
    title: str = section
    field: str = "#FFFFFF"
    value: str = "#DDDDDD"
    caption: str = "gray50"
    success: str = "#11FF22"  # green
    exception: str = "#FF1133"  # Red
    error: str = "#FF7711"   # Orange
    warning: str = "#FFDD55"  # Yellow


class AbacuraTable(Table):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("title_style", Style(color=OutputColors.title))
        kwargs.setdefault("title_justify", "left")
        kwargs.setdefault("style", OutputColors.value)
        kwargs.setdefault("caption_style", OutputColors.caption)
        kwargs.setdefault("caption_justify", "left")
        kwargs.setdefault("header_style", Style(color=OutputColors.field, bold=True))
        kwargs.setdefault("footer_style", Style(color=OutputColors.field, bold=True))
        kwargs.setdefault("border_style", OutputColors.border)
        kwargs.setdefault("box", box.HORIZONTALS)
        super().__init__(*args, **kwargs)


class AbacuraPropertyGroup(Group):
    def __init__(self, obj: Union[dict, dataclass], title="Properties", exclude: set = None):
        if is_dataclass(obj):
            obj = {f.name: getattr(obj, f.name) for f in fields(obj)}

        kl = max([len(k) for k in obj.keys()])
        lines = [Text.assemble((title, OutputColors.section), ("\n", ""))]
        for k, v in obj.items():
            if exclude and k in exclude:
                continue
            text = Text.assemble((f"{k:>{kl}.{kl}}: ", Style(color=OutputColors.field, bold=True)),
                                 (str(v), OutputColors.value))
            lines.append(text)

        super().__init__(*lines)


class AbacuraPanel(Panel):
    def __init__(self, renderable, title: str = '', *args, **kwargs):
        kwargs.setdefault("highlight", True)
        kwargs.setdefault("expand", False)
        kwargs.setdefault("border_style", Style(bold=True, bgcolor=OutputColors.panel))
        kwargs.setdefault("style", Style(bgcolor=OutputColors.panel))
        kwargs.setdefault("padding", 1)
        kwargs.setdefault("box", box.ROUNDED)
        kwargs.setdefault("title_align", "left")
        p = Panel(*args, renderable=renderable, title=title, **kwargs)
        super().__init__(p, box=box.SIMPLE, padding=1, expand=False)


class AbacuraWarning(AbacuraPanel):
    def __init__(self, renderable, title: str, *args, **kwargs):
        kwargs.setdefault("border_style", Style(color=OutputColors.warning, bold=True))
        kwargs.setdefault("box", box.SQUARE)
        super().__init__(renderable=renderable, title=title, *args, **kwargs)


class AbacuraError(AbacuraPanel):
    def __init__(self, renderable, title: str, *args, **kwargs):
        kwargs.setdefault("border_style", Style(color=OutputColors.error, bold=True))
        kwargs.setdefault("box", box.SQUARE)
        super().__init__(renderable=renderable, title=title, *args, **kwargs)


def tabulate(tabular_data, headers=(), float_format="9.3f", row_styler=None, **kwargs) -> AbacuraTable:
    """
    Create a rich Table with automatic justification for numbers and a configurable floating point format.

    tabular_data can be a List[List], List[Dict], List[Tuple], List[dataclass], List[str]
    headers should be an interable list/tuple of header names
    kwargs are passed through to rich Table

    """
    # title="", title_justify="left", title_style=None,
    # caption="", caption_justify="left", caption_style=None,
    # header_style=None, border_style=None,

    tbl = AbacuraTable(**kwargs)

    if isinstance(headers, str):
        headers = [headers]

    if len(tabular_data) == 0:
        if len(headers) == 0:
            return tbl
        column_types = [str for _ in headers]
    elif isinstance(tabular_data[0], dict):
        keys = tabular_data[0].keys()
        headers = headers if len(headers) else list(keys)
        tabular_data = [[row.get(k, None) for k in keys] for row in tabular_data]
        column_types = [type(v) for v in tabular_data[0]]
    elif is_dataclass(tabular_data[0]):
        df = fields(tabular_data[0])
        headers = headers if len(headers) else list([f.name for f in df])
        tabular_data = [astuple(row) for row in tabular_data]
        column_types = [f.type for f in df]
    elif not isinstance(tabular_data[0], Iterable) or isinstance(tabular_data[0], str):
        tabular_data = [[row] for row in tabular_data]
        column_types = [type(v) for v in tabular_data[0]]
    else:
        column_types = [type(v) for v in tabular_data[0]]

    row_styles = [""] * len(tabular_data)
    if row_styler:
        row_styles = [row_styler(row) for row in tabular_data]

    for h, ct in zip_longest(headers, column_types):
        if h and h.startswith("_"):
            justify = "right"
        elif ct in (int, 'int', float, 'float'):
            justify = "right"
        else:
            justify = "left"
        hdr = h.lstrip("_") if h else ""
        tbl.add_column(header=hdr, justify=justify)

    for i, row in enumerate(tabular_data):
        values = [format(v, float_format) if ct in (float, "float") else str(v) for ct, v in zip(column_types, row)]
        tbl.add_row(*values, style=row_styles[i])

    return tbl
