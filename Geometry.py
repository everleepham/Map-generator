from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple


class GeometryObject(ABC):
    @staticmethod
    @abstractmethod
    def FromDict(data: dict) -> "GeometryObject":
        if data["type"] == "Point":
            return Point.FromDict(data)
        if data["type"] == "LineString":
            return LineString.FromDict(data)
        elif data["type"] == "Polygon":
            return Polygon.FromDict(data)
        elif data["type"] in (
            "MultiPoint",
            "MultiLineString",
            "MultiPolygon",
            "GeometryCollection",
        ):
            return Composite.FromDict(data)
        # Do the same for LineString, Polygon and Composite...

    def bounding_box(self) -> Tuple[float, float, float, float]:
        pass

    @abstractmethod
    def to_svg(self) -> str:
        pass


@dataclass
class Point(GeometryObject):
    x: float
    y: float

    @staticmethod
    def FromDict(data: dict) -> "Point":
        coordinates = data["coordinates"]
        return Point(coordinates[0], coordinates[1])  # constructor

    def bounding_box(self) -> Tuple[float, float, float, float]:
        return self.x, self.y, self.x, self.y

    def to_svg(self, classname: str) -> str:
        return f'<circle class="{classname}" cx="{self.x}" cy="{self.y}" />'


# Do the same for LineString, Polygon and Composite
@dataclass
class LineString(GeometryObject):
    coordinates: List[Point]

    @staticmethod
    def FromDict(data: dict) -> "LineString":
        coord = []
        for x, y in data["coordinates"]:
            coord.append(Point(x, y))
        return LineString(coord)

    def bounding_box(self) -> Tuple[float, float, float, float]:
        x_lst = [p.x for p in self.coordinates]
        y_lst = [p.y for p in self.coordinates]
        return (min(x_lst), min(y_lst), max(x_lst), max(y_lst))

    def to_svg(self, classname: str) -> str:
        s = f'<polyline class="{classname}" points="'
        for p in self.coordinates:
            s += f"{p.x}, {p.y} "
        s += '" /> '
        return s


@dataclass
class Polygon(GeometryObject):
    line_1: List[LineString]

    @staticmethod
    def FromDict(data: dict) -> "Polygon":
        line_1 = LineString([Point(x, y) for (x, y) in data["coordinates"][0]])

        return Polygon(line_1)

    def bounding_box(self) -> Tuple[float, float, float, float]:
        return self.line_1.bounding_box()

    def to_svg(self, classname: str) -> str:
        s = f'<polygon class="{classname}" points="'
        for p in self.line_1.coordinates:
            s += f"{p.x}, {p.y} "
        s += '" /> '
        return s


@dataclass
class Composite(GeometryObject):
    objects: List[GeometryObject]

    @staticmethod
    def FromDict(data: dict) -> "Composite":
        objects = []
        if data["type"] == "MultiPoint":
            return Composite([Point(x, y) for (x, y) in data["coordinates"]])
        elif data["type"] == "MultiLineString":
            return Composite(
                [
                    LineString([Point(x, y) for (x, y) in line])
                    for line in data["coordinates"]
                ]
            )
        elif data["type"] == "MultiPolygon":
            for polygon in data["coordinates"]:
                line = polygon[0]
                pts = LineString([Point(x, y) for (x, y) in line])
                objects.append(pts)
            return Composite(objects)
        else:
            return Composite([GeometryObject.FromDict(x) for x in data["geometries"]])

    def bounding_box(self) -> Tuple[float, float, float, float]:
        # return the bounding box of the union of the bounding boxes of the objects
        if len(self.objects) == 0:
            return super().bounding_box()

        bbox = [o.bounding_box() for o in self.objects]
        xmin = min([xmin for (xmin, ymin, xmax, ymax) in bbox])
        ymin = min([ymin for (xmin, ymin, xmax, ymax) in bbox])
        xmax = max([xmax for (xmin, ymin, xmax, ymax) in bbox])
        ymax = max([ymax for (xmin, ymin, xmax, ymax) in bbox])

        return (xmin, ymin, xmax, ymax)

    def to_svg(self, classname: str) -> str:
        s = ""
        for o in self.objects:
            s += o.to_svg(classname) + "\n"
        return s
