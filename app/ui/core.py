from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union

from .layout import layout_tree
from .renderer import render_layout
from .types import Node, Style


Color = int


def _normalize_children(children: Optional[Sequence["Node"]]) -> List["Node"]:
    if not children:
        return []
    return list(children)


Component = Callable[[Dict[str, object]], Node]


def Text(text: str, *, font=None, color: Color = 0, style: Optional[Style] = None) -> Node:
    return Node(
        type="text",
        props={"text": text, "font": font, "color": color, "style": style or Style()},
    )


def Line(
    start: Tuple[int, int],
    end: Tuple[int, int],
    *,
    width: int = 1,
    color: Color = 0,
    style: Optional[Style] = None,
) -> Node:
    return Node(
        type="line",
        props={
            "start": start,
            "end": end,
            "width": width,
            "color": color,
            "style": style or Style(),
        },
    )


def Box(*, style: Optional[Style] = None, color: Color = 0) -> Node:
    return Node(
        type="box",
        props={"style": style or Style(), "color": color},
    )


def ImageView(image, *, style: Optional[Style] = None) -> Node:
    return Node(
        type="image",
        props={"image": image, "style": style or Style()},
    )


def View(*children: Node, style: Optional[Style] = None) -> Node:
    return Node(
        type="view",
        props={"style": style or Style()},
        children=_normalize_children(children),
    )


def render(
    root: Union[Node, Component],
    props: Optional[Dict[str, object]],
    *,
    width: int,
    height: int,
    background: Color = 255,
):
    if callable(root):
        node = root(props or {})
    else:
        node = root

    layout = layout_tree(node, width=width, height=height)
    return render_layout(layout, width=width, height=height, background=background)
