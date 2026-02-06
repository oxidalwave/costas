from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Style:
    width: Optional[int] = None
    height: Optional[int] = None
    padding: int = 0
    gap: int = 0
    direction: str = "column"
    align: str = "start"
    x: Optional[int] = None
    y: Optional[int] = None


@dataclass
class Node:
    type: str
    props: Dict[str, object]
    children: List["Node"] = field(default_factory=list)
