from typing import Dict

from .core import Line, Text, View
from .types import Style

def teamScore(props: Dict[str, object]):
    font = props["font"]
    data = props["data"]

    teamCode = data["teamCode"]
    score = data["score"]


    return View(
        Text(teamCode, font=font),
        Text(score, font=font),
        style=Style(direction="row", justify="space-between", width=100, gap=8),
    )

def scorebug(props: Dict[str, object]):
    font = props["font"]
    data = props["data"]

    away = data["scorebug"]["away"]
    home = data["scorebug"]["home"]
    batter = data["atBat"]["batter"]
    pitcher = data["atBat"]["pitcher"]

    return View(
        View(
            View(
                teamScore(props={"font": font, "data": away}),
                teamScore(props={"font": font, "data": home}),
                style=Style(direction="column"),
            ),
            View(
                View(
                    Text(batter["name"], font=font),
                    Text(f"{batter['wpa+']} WPA+", font=font),
                    style=Style(direction="row", justify="space-between", width=300, gap=8),
                ),
                View(
                    Text(pitcher["name"], font=font),
                    Text(f"{pitcher['era']} ERA", font=font),
                    style=Style(direction="row", justify="space-between", width=300, gap=8),
                ),
                style=Style(direction="column"),
            ),
            style=Style(direction="row"),
        ),
        View(style=Style(direction="row"))
    )
