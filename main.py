import sys
from pathlib import Path
import chevron
import Map


def render_map(json_file):

    map = Map.Map.LoadFromGeoJson(json_file)

    (x1, y1, x2, y2) = map.bounding_box()

    data = {
        "classes": [
            Map.Building,
            Map.District,
            Map.Road,
            Map.Wall,
            Map.Plank,
            Map.Prism,
            Map.Square,
            Map.Green,
            Map.Field,
            Map.Tree,
            Map.Earth,
            Map.Water,
            Map.River,
        ],
        "bbox": {
            "x": x1,
            "y": y1,
            "width": x2 - x1,
            "height": y2 - y1,
        },
        "items": map.items,
    }

    output = chevron.render(open("map-template.svg"), data)
    svg_file = str(json_file).replace(".json", ".svg")
    open(svg_file, "w").write(output)
    print(f"Generated {svg_file}")


def main():
    path = Path(sys.argv[1])
    filelists = [file for file in path.iterdir() if file.suffix == ".json"]
    for file in filelists:
        render_map(file)


if __name__ == "__main__":
    main()
