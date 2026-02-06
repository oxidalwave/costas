from typing import Tuple

from PIL import Image, ImageDraw

from .types import Style
from .layout import LayoutNode


def _draw_text(draw: ImageDraw.ImageDraw, layout: LayoutNode) -> None:
    props = layout.node.props
    style: Style = props["style"]
    text = props["text"]
    font = props.get("font")
    color = props.get("color", 0)
    x = layout.x + style.padding
    y = layout.y + style.padding
    draw.text((x, y), text, font=font, fill=color)


def _draw_line(draw: ImageDraw.ImageDraw, layout: LayoutNode) -> None:
    props = layout.node.props
    style: Style = props["style"]
    start = props["start"]
    end = props["end"]
    width = props.get("width", 1)
    color = props.get("color", 0)
    x = layout.x + style.padding
    y = layout.y + style.padding
    draw.line((x + start[0], y + start[1], x + end[0], y + end[1]), fill=color, width=width)


def _draw_box(draw: ImageDraw.ImageDraw, layout: LayoutNode) -> None:
    props = layout.node.props
    style: Style = props["style"]
    color = props.get("color", 0)
    x = layout.x
    y = layout.y
    draw.rectangle((x, y, x + layout.width, y + layout.height), outline=color)
    if style.padding:
        inner = (
            x + style.padding,
            y + style.padding,
            x + layout.width - style.padding,
            y + layout.height - style.padding,
        )
        draw.rectangle(inner, outline=color)


def _draw_image(canvas: Image.Image, layout: LayoutNode) -> None:
    props = layout.node.props
    style: Style = props["style"]
    image = props["image"]
    x = layout.x + style.padding
    y = layout.y + style.padding
    canvas.paste(image, (x, y))


def _render_node(canvas: Image.Image, draw: ImageDraw.ImageDraw, layout: LayoutNode) -> None:
    node_type = layout.node.type
    if node_type == "text":
        _draw_text(draw, layout)
    elif node_type == "line":
        _draw_line(draw, layout)
    elif node_type == "box":
        _draw_box(draw, layout)
    elif node_type == "image":
        _draw_image(canvas, layout)

    for child in layout.children:
        _render_node(canvas, draw, child)


def render_layout(layout: LayoutNode, *, width: int, height: int, background: int) -> Image.Image:
    canvas = Image.new("1", (width, height), background)
    draw = ImageDraw.Draw(canvas)
    _render_node(canvas, draw, layout)
    return canvas
