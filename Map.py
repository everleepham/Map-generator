from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, ClassVar
from Geometry import GeometryObject
import json


@dataclass
class MapElement(ABC):
    geometry: GeometryObject
    stroke: ClassVar[str] = "black"
    stroke_width: ClassVar[float] = 1.0
    fill: ClassVar[str] = "none"
    marker: ClassVar[str] = "none"
    z_order: ClassVar[int] = 0
    filter: ClassVar[str] = "none"

    def __str__(self) -> str:
        return self.geometry.to_svg(self.__class__.__name__)

    @staticmethod
    def FromDict(data: dict) -> "MapElement":
        # Create a GeometryObject from the data
        g = GeometryObject.FromDict(data)
        if data["id"] == "roads":
            return Road(geometry=g)
        elif data["id"] == "buildings":
            return Building(geometry=g)
        elif data["id"] == "rivers":
            return River(geometry=g)
        elif data["id"] == "walls":
            return Wall(geometry=g)
        elif data["id"] == "planks":
            return Plank(geometry=g)
        elif data["id"] == "prisms":
            return Prism(geometry=g)
        elif data["id"] == "squares":
            return Square(geometry=g)
        elif data["id"] == "greens":
            return Green(geometry=g)
        elif data["id"] == "fields":
            return Field(geometry=g)
        elif data["id"] == "districts":
            return District(geometry=g)
        elif data["id"] == "trees":
            return Tree(geometry=g)
        elif data["id"] == "earth":
            return Earth(geometry=g)
        elif data["id"] == "water":
            return Water(geometry=g)


class Road(MapElement):
    stroke: ClassVar[str] = "#FFF2C8"
    stroke_width: ClassVar[float] = 8.0
    z_order: ClassVar[int] = 1


class Building(MapElement):
    stroke: ClassVar[str] = "none"
    fill: ClassVar[str] = "#D6A36E"
    filter: ClassVar[str] = "url(#shadow)"


class River(MapElement):
    stroke: ClassVar[str] = "#779988"
    stroke_width: ClassVar[float] = 36.79280025660657


class Wall(MapElement):
    marker: ClassVar[str] = "url(#wall)"
    stroke: ClassVar[str] = "#606661"
    stroke_width: ClassVar[float] = 7.6


class Plank(MapElement):
    stroke: ClassVar[str] = "FFF2C8"


class Prism(MapElement):
    stroke: ClassVar[str] = "none"


class Square(MapElement):
    fill: ClassVar[str] = "#F2F2DA"


class Green(MapElement):
    stroke: ClassVar[str] = "#99AA77"
    fill: ClassVar[str] = "url(#green)"


class Field(MapElement):
    stroke: ClassVar[str] = "#99AA77"
    fill: ClassVar[str] = "url(#green)"


class Tree(MapElement):
    fill: ClassVar[str] = "#667755"


class District(MapElement):
    stroke: ClassVar[str] = "none"


class Earth(MapElement):
    stroke: ClassVar[str] = "none"


class Water(MapElement):
    stroke: ClassVar[str] = "none"
    fill: ClassVar[str] = "#779988"


@dataclass
class Map:
    items: List[MapElement]

    def LoadFromGeoJson(filename: str) -> "Map":
        items = []
        # Load the data from the json file
        # Create the map elements and store them in a list that will be returned
        with open(filename, "r") as f:
            data = json.load(f)
            for feature in data["features"]:
                myobject = MapElement.FromDict(feature)
                if myobject is not None:
                    items.append(myobject)
        return Map(items)

    def bounding_box(self) -> Tuple[float, float, float, float]:
        bbox = []
        for o in self.items:
            if isinstance(o, District):
                bbox.append(o.geometry.bounding_box())
        if len(bbox) == 0:
            return (0, 0, 0, 0)
        else:
            xmin = min([xmin for (xmin, ymin, xmax, ymax) in bbox])
            ymin = min([ymin for (xmin, ymin, xmax, ymax) in bbox])
            xmax = max([xmax for (xmin, ymin, xmax, ymax) in bbox])
            ymax = max([ymax for (xmin, ymin, xmax, ymax) in bbox])
        w = xmax - xmin
        h = ymax - ymin
        return (xmin - w * 0.1, ymin - h * 0.1, xmax + w * 0.1, ymax + h * 0.1)
