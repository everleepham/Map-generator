# import json

# def count_items(feature):
#     type = feature['type']
#     # if the type is a multi* type, then we need to count the number of items in the coordinates array
#     if type in ["MultiPolygon", "MultiLineString", "MultiPoint"]:
#         return len(feature['coordinates'])
#     # if the type is a *Collection type, then we need to count recursively the number of items in the geometries array
#     elif type == "GeometryCollection":
#         # return sum([count_items(geometry) for geometry in data['geometries']])
#         lst = []
#         for geometry in feature['geometries']:
#             lst.append(count_items(geometry))
#         return sum(lst)

#     else:
#         return 1

# def map_summary(filename):
#     with open(filename, 'r') as f:
#         data = json.load(f)

#     for feature in data['features']:
#         id = feature['id']
#         type = feature['type']
#         count = count_items(feature)
#         print(f"Feature {id} is a {type} with {count} items.")


# map_summary("examples/thunty_city.json")
# import Map
# map = Map.Map.LoadFromGeoJson("examples/silverrocks.json")
# print(map.items)

# import Map
# map = Map.Map.LoadFromGeoJson("examples/silverrocks.json")
# print("Silverrocks bounding box:", map.bounding_box())
# map = Map.Map.LoadFromGeoJson("examples/bluemill_fort.json")
# print("Bluemill Fort bounding box:", map.bounding_box())
# map = Map.Map.LoadFromGeoJson("examples/thunty_city.json")
# print("Thunty City bounding box:", map.bounding_box())


# from pathlib import Path
# import sys
# import chevron
# import Map


# map = Map.Map.LoadFromGeoJson("examples/bluemill_fort.json")
# map = Map.Map.LoadFromGeoJson("examples/silverrocks.json")
# map = Map.Map.LoadFromGeoJson("examples/thunty_city.json")
# (x1, y1, x2, y2) = map.bounding_box()

# # print(map.items)

# data = {
#     "classes": [Map.Building, Map.District, Map.Road, Map.Wall, Map.Plank, Map.Prism, Map.Square, 
#                 Map.Green, Map.Field, Map.Tree, Map.Earth, Map.Water, Map.River],
#     "bbox": {
#         "x": x1, 
#         "y": y1,
#         "width": x2 - x1,
#         "height": y2 - y1,
#     },
#     "items": map.items
# }
# # write the string `svg` to a file `map.svg` and see the results in a SVG viewer

# output = chevron.render(open("map-template.svg"), data)
# open("output.svg", "w").write(output)
# print("Generated map.svg")

# import Map 
# map = Map.Map.LoadFromGeoJson("examples/silverrocks.json")
# print("River thickness:", Map.River.stroke)
# print("Wall thickness:", Map.Wall.stroke_width)
# print("Building fill color:", Map.Building.fill)

import sys
from pathlib import Path
import chevron
import Map

def render_map(json_file):

    map = Map.Map.LoadFromGeoJson(json_file)

    (x1, y1, x2, y2) = map.bounding_box()

    data = {
        "classes": [Map.Building, Map.District, Map.Road, Map.Wall, Map.Plank, Map.Prism, 
                    Map.Square, Map.Green, Map.Field, Map.Tree, Map.Earth, Map.Water, Map.River],
        "bbox": {
            "x": x1, 
            "y": y1,
            "width": x2 - x1,
            "height": y2 - y1,
        },
        "items": map.items
    }

    output = chevron.render(open("map-template.svg"), data)
    svg_file = str(json_file).replace(".json", ".svg")
    open(svg_file, "w").write(output)
    print(f"Generated {svg_file}")


path = Path(sys.argv[1])
filelists = [file for file in path.iterdir() if file.suffix == ".json"]
for file in filelists:
    render_map(file)
