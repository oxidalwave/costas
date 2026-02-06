from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from PIL import ImageFont

from .types import Node, Style


@dataclass
class LayoutNode:
    node: Node
    x: int
    y: int
    width: int
    height: int
    children: List["LayoutNode"] = field(default_factory=list)


def _measure_text(text: str, font) -> Tuple[int, int]:
    if font is None:
        return (0, 0)
    bbox = font.getbbox(text)
    return (bbox[2] - bbox[0], bbox[3] - bbox[1])


def _resolve_size(node: Node) -> Tuple[Optional[int], Optional[int]]:
    style = node.props.get("style")
    if not isinstance(style, Style):
        return (None, None)
    return (style.width, style.height)


def _layout_leaf(node: Node) -> Tuple[int, int]:
    style = node.props["style"]
    if node.type == "text":
        text = node.props["text"]
        font = node.props.get("font")
        width, height = _measure_text(text, font)
    elif node.type == "line":
        start = node.props["start"]
        end = node.props["end"]
        width = abs(end[0] - start[0]) + 1
        height = abs(end[1] - start[1]) + 1
    elif node.type == "image":
        image = node.props["image"]
        width, height = image.size
    else:
        width = 0
        height = 0

    if style.width is not None:
        width = style.width
    if style.height is not None:
        height = style.height

    width += style.padding * 2
    height += style.padding * 2

    return (width, height)


def _layout_children(
    node: Node,
    x: int,
    y: int,
    width: int,
    height: int,
) -> List[LayoutNode]:
    style = node.props["style"]
    cursor_x = x + style.padding
    cursor_y = y + style.padding
    available_width = max(0, width - style.padding * 2)
    available_height = max(0, height - style.padding * 2)
    children: List[LayoutNode] = []

    sizes = []
    for child in node.children:
        sizes.append(_layout_leaf_or_container(child))

    if style.direction == "row":
        total_main = sum(width for width, _ in sizes)
        gap = style.gap
        if style.justify == "center":
            cursor_x += max(0, (available_width - (total_main + gap * max(0, len(sizes) - 1))) // 2)
        elif style.justify == "end":
            cursor_x += max(0, available_width - (total_main + gap * max(0, len(sizes) - 1)))
        elif style.justify == "space-between" and len(sizes) > 1:
            remaining = available_width - total_main
            gap = max(0, remaining // (len(sizes) - 1))

        for (child_width, child_height), child in zip(sizes, node.children):
            align_offset = 0
            if style.align == "center":
                align_offset = max(0, (available_height - child_height) // 2)
            elif style.align == "end":
                align_offset = max(0, available_height - child_height)
            child_node = LayoutNode(
                node=child,
                x=cursor_x,
                y=cursor_y + align_offset,
                width=child_width,
                height=child_height,
            )
            child_style = child.props.get("style")
            if isinstance(child_style, Style):
                if child_style.x is not None:
                    child_node.x = x + child_style.x
                if child_style.y is not None:
                    child_node.y = y + child_style.y
            children.append(child_node)
            cursor_x += child_width + gap
    else:
        total_main = sum(height for _, height in sizes)
        gap = style.gap
        if style.justify == "center":
            cursor_y += max(0, (available_height - (total_main + gap * max(0, len(sizes) - 1))) // 2)
        elif style.justify == "end":
            cursor_y += max(0, available_height - (total_main + gap * max(0, len(sizes) - 1)))
        elif style.justify == "space-between" and len(sizes) > 1:
            remaining = available_height - total_main
            gap = max(0, remaining // (len(sizes) - 1))

        for (child_width, child_height), child in zip(sizes, node.children):
            align_offset = 0
            if style.align == "center":
                align_offset = max(0, (available_width - child_width) // 2)
            elif style.align == "end":
                align_offset = max(0, available_width - child_width)
            child_node = LayoutNode(
                node=child,
                x=cursor_x + align_offset,
                y=cursor_y,
                width=child_width,
                height=child_height,
            )
            child_style = child.props.get("style")
            if isinstance(child_style, Style):
                if child_style.x is not None:
                    child_node.x = x + child_style.x
                if child_style.y is not None:
                    child_node.y = y + child_style.y
            children.append(child_node)
            cursor_y += child_height + gap

    for child in children:
        _layout_container_children(child)

    return children


def _measure_container(node: Node) -> Tuple[int, int]:
    style = node.props["style"]
    total_width = 0
    total_height = 0
    measured_children = []
    for child in node.children:
        child_width, child_height = _layout_leaf_or_container(child)
        measured_children.append((child_width, child_height))
        if style.direction == "row":
            total_width += child_width
            total_height = max(total_height, child_height)
        else:
            total_height += child_height
            total_width = max(total_width, child_width)

    if style.direction == "row":
        total_width += max(0, len(measured_children) - 1) * style.gap
    else:
        total_height += max(0, len(measured_children) - 1) * style.gap

    width = style.width or (total_width + style.padding * 2)
    height = style.height or (total_height + style.padding * 2)
    return (width, height)


def _layout_leaf_or_container(node: Node) -> Tuple[int, int]:
    style = node.props.get("style")
    if node.type in ("view",):
        if style.width is not None or style.height is not None:
            measured_width, measured_height = _measure_container(node)
            width = style.width if style.width is not None else measured_width
            height = style.height if style.height is not None else measured_height
            return (width, height)
        return _measure_container(node)
    return _layout_leaf(node)


def _layout_container_children(layout_node: LayoutNode) -> None:
    node = layout_node.node
    if node.type != "view":
        return

    style = node.props["style"]
    width = layout_node.width
    height = layout_node.height

    if width == 0 or height == 0:
        width, height = _measure_container(node)
        layout_node.width = width
        layout_node.height = height

    children = _layout_children(node, layout_node.x, layout_node.y, width, height)

    for child in children:
        if child.node.type == "view":
            if child.width == 0 or child.height == 0:
                _layout_container_children(child)

    layout_node.children = children


def layout_tree(root: Node, *, width: int, height: int) -> LayoutNode:
    root_node = LayoutNode(node=root, x=0, y=0, width=width, height=height)
    _layout_container_children(root_node)

    style = root.props.get("style")
    if isinstance(style, Style):
        if style.x is not None:
            root_node.x = style.x
        if style.y is not None:
            root_node.y = style.y

    return root_node
