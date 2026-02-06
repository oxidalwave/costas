from typing import Dict

from .core import Line, Text, View
from .types import Style


def scorebug(props: Dict[str, object]):
    font = props["font"]
    data = props["data"]

    away = data["scorebug"]["away"]
    home = data["scorebug"]["home"]
    batter = data["atBat"]["batter"]
    pitcher = data["atBat"]["pitcher"]

    row_style = Style(direction="row", gap=12)
    column_style = Style(direction="column", gap=6)

    return View(
        View(
            View(
                Text(away["teamCode"], font=font),
                Text(away["score"], font=font, style=Style(align="end")),
                style=row_style,
            ),
            Line((0, 0), (400, 0)),
            View(
                Text(home["teamCode"], font=font),
                Text(home["score"], font=font, style=Style(align="end")),
                style=row_style,
            ),
            style=column_style,
        ),
        View(
            View(
                Text(batter["name"], font=font),
                Text(f"{batter['wpa+']} WPA+", font=font, style=Style(align="end")),
                style=row_style,
            ),
            View(
                Text(pitcher["name"], font=font),
                Text(f"{pitcher['era']} ERA", font=font, style=Style(align="end")),
                style=row_style,
            ),
            style=column_style,
        ),
        style=Style(direction="row", gap=24, padding=8),
    )
