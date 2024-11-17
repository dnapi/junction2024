import math
import multiprocessing
from collections import defaultdict
from functools import cache
from pathlib import Path

import ifcopenshell
import ifcopenshell.geom


# Find clashes
def _generate_tree(model: ifcopenshell.file) -> ifcopenshell.geom.tree:
    tree = ifcopenshell.geom.tree()
    settings = ifcopenshell.geom.settings()
    iterator = ifcopenshell.geom.iterator(settings, model, multiprocessing.cpu_count())
    if iterator.initialize():
        while True:
            # Use triangulation to build a BVH tree
            tree.add_element(iterator.get())

            # Alternatively, use this code to build an unbalanced binary tree
            # tree.add_element(iterator.get_native())

            if not iterator.next():
                break

    return tree


def _find_clashes(
    model: ifcopenshell.file, pairs: list[set[str]], tolerance: float
) -> list:
    tree = _generate_tree(model)

    clashes = []
    for pair in pairs:
        clashes += list(
            tree.clash_intersection_many(
                model.by_type(pair[0]),
                model.by_type(pair[1]),
                tolerance=tolerance,
                check_all=True,
            )
        )

    return clashes


# Build intersections dictionary
def _get_material(entity: ifcopenshell.entity_instance) -> str:
    material = None
    if entity.HasAssociations:
        for assoc in entity.HasAssociations:
            if assoc.is_a("IfcRelAssociatesMaterial"):
                material = assoc.RelatingMaterial.Name
                break
    return material


@cache
def _get_sizes(entity: ifcopenshell.entity_instance) -> dict:
    if not entity.IsDefinedBy:
        return {}

    sizes = {}
    for definition in entity.IsDefinedBy:
        if definition.is_a(
            "IfcRelDefinesByProperties"
        ) and definition.RelatingPropertyDefinition.is_a("IfcPropertySet"):
            for prop in definition.RelatingPropertyDefinition.HasProperties:
                if prop.is_a("IfcPropertySingleValue") and prop.Name.lower() in [
                    "height",
                    "width",
                    "length",
                    "depth",
                ]:
                    sizes[prop.Name.lower()] = prop.NominalValue.wrappedValue

    return sizes


def _extract_entity(entity: ifcopenshell.entity_instance) -> dict:
    material = _get_material(entity).split("/", 1)
    return {
        "entity": entity.is_a(),
        "guid": entity.GlobalId,
        "material": material[0],
        "spec": material[1],
        "sizes": _get_sizes(entity),
    }


def _convert(
    model: ifcopenshell.file, clashes: list[ifcopenshell.ifcopenshell_wrapper.clash]
) -> dict:
    """Convert ifcopenshell clashes to intersections dictionary"""

    id_to_intersection = {}
    for clash in clashes:
        raw = {}
        raw["coords"] = [
            (lhs + rhs) / 2.0 for lhs, rhs in zip(clash.p1, clash.p2)
        ]  # mean average
        raw["distance"] = clash.distance
        raw["entities"] = [
            _extract_entity(model.by_id(clash.a.id())),
            _extract_entity(model.by_id(clash.b.id())),
        ]
        raw["clash_type"] = {
            ["protrusion", "pierce", "collision", "clearance"][clash.clash_type]
        }
        id_to_intersection["".join([entry["guid"] for entry in raw["entities"]])] = raw

    return id_to_intersection


# Find close intersections
@cache
def _distance(*args) -> float:
    return math.sqrt(sum((lhs - rhs) ** 2 for lhs, rhs in zip(args[0:3], args[3:6])))


def _lookup_closest(id_to_intersection: dict, merge_distance: float) -> set[frozenset]:
    """Lookup closest intersections by merge_distance."""

    closest = set()
    for outer_key, outer in id_to_intersection.items():
        keys = [outer_key]
        for inner_key, inner in id_to_intersection.items():
            if (
                inner_key != outer_key
                and _distance(*outer["coords"], *inner["coords"]) < merge_distance
            ):
                keys.append(inner_key)
        if len(keys) > 1:
            closest.add(frozenset(keys))
    return closest


# Filter intersections out by LxWxH from filter_dimensions
def _filter_by_size(
    filter_dimensions: dict[str, float], is_all: bool, id_to_intersection: dict
) -> None:
    for id, intersection in id_to_intersection.items():
        is_filtered = False
        for entity in intersection["entities"]:
            is_less = [
                entity["sizes"][dim] < filter_dimensions[dim]
                for dim in ["height", "width", "length"]
            ]
            if (is_all and all(is_less)) or (not is_all and any(is_less)):
                is_filtered = True
                break

        if is_filtered:
            del id_to_intersection[id]

def _merge_nearby(closest: set[frozenset], id_to_intersection: dict):
    for keys in closest:
        keys = list(keys)
        for key in keys[1:]:
            current_intersection = id_to_intersection.get(key)
            if current_intersection:
                entities = current_intersection.get("entities", [])
                clash_type = current_intersection.get("clash_type", {})
                if keys[0] in id_to_intersection:
                    id_to_intersection[keys[0]]["entities"].extend(entities)
                    id_to_intersection[keys[0]]["clash_type"].update(clash_type)
                    del id_to_intersection[key]
            else:
                print(f"Key not found: {key}")


# def _merge_nearby(closest: set[frozenset], id_to_intersection: dict):
#     for keys in closest:
#         keys = list(keys)
#         for key in keys[1:]:
#             print(f"Checking key: {key}")
#             if key in id_to_intersection:
#                 print(id_to_intersection[key])
#                 id_to_intersection[keys[0]]["entities"].extend(id_to_intersection[key]["entities"])
#                 id_to_intersection[keys[0]]["clash_type"].update(id_to_intersection[key]["clash_type"])
#                 del id_to_intersection[key]
#             else:
#                 print(f"Key not found: {key}")
#             # print(key)
#             # id_to_intersection[keys[0]]["entities"].extend(
#             #     id_to_intersection.at(key)["entities"]
#             # )
#             # id_to_intersection[keys[0]]["clash_type"].update(
#             #     id_to_intersection[key]["clash_type"]
#             # )
#             # del id_to_intersection[key]


# Group items by the combination of elem_a and elem_b materials
# TODO: STEEL treatment
def _groupby_material(id_to_intersection: dict) -> dict:
    grouped = defaultdict(list)
    for intersection in id_to_intersection.values():
        group = "<->".join(
            sorted([entity["material"] for entity in intersection["entities"]])
        )
        grouped[group].append(intersection)
    return dict(grouped)


def core(
    fpath: Path,
    pairs: list[tuple[str]],
    tolerance: float,  # [mm]
    merge_distance: float,  # [m]
    filter_dimensions: dict[str, float],  # [m]
    is_all: bool,
) -> dict:
    model = ifcopenshell.open(Path(fpath))

    clashes = _find_clashes(model, pairs, tolerance)

    id_to_intersection = _convert(model, clashes)
    # len(id_to_intersection)

    closest = _lookup_closest(id_to_intersection, merge_distance)
    # closest

    _filter_by_size(filter_dimensions, is_all, id_to_intersection)
    # len(id_to_intersection)

    _merge_nearby(closest, id_to_intersection)
    # len(id_to_intersection)

    return _groupby_material(id_to_intersection)


# input = dict(
#     fpath=Path("../ifc_examples_peikko/One_Section.ifc"),
#     pairs=[
#         ("IfcWall", "IfcWall"),
#         ("IfcWall", "IfcBeam"),
#         ("IfcWall", "IfcColumn"),
#         ("IfcBeam", "IfcBeam"),
#         ("IfcBeam", "IfcColumn"),
#         ("IfcColumn", "IfcColumn"),
#     ],
#     tolerance=0.002,  # TODO: Research the tolerance value
#     merge_distance=0.1,  # [m]
#     filter_dimensions={"height": 200e-3, "width": 100e-3, "length": 1.5},
#     is_all=True,
# )
# grouped = core(**input)
# # grouped = {name: len(group) for name, group in dict(grouped).items()}
# grouped

# # %%
# import json


# def set_default(obj):
#     if isinstance(obj, set):
#         return list(obj)
#     raise TypeError

# with open("out.json", "w") as outfile:
#     json.dump(grouped, outfile, default=set_default, indent=2)
