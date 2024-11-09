# %%
import multiprocessing
from collections import defaultdict
from pathlib import Path

import ifcopenshell
import ifcopenshell.geom
import numpy as np
import pandas as pd

# import matplotlib.pyplot as plt

# TODO: Convert to CLI utility

# %% Input data
# TODO: Wrap it up to .yaml or .json input file
fpath = Path("../../ifc_examples_peikko/One_Section.ifc")
pairs = [
    ("IfcWall", "IfcWall"),
    ("IfcWall", "IfcBeam"),
    ("IfcWall", "IfcColumn"),
    ("IfcBeam", "IfcBeam"),
    ("IfcBeam", "IfcColumn"),
    ("IfcColumn", "IfcColumn"),
]
tolerance = 0.002  # TODO: Research the tolerance value


# %%
model = ifcopenshell.open(fpath)
tree = ifcopenshell.geom.tree()
settings = ifcopenshell.geom.settings()
iterator = ifcopenshell.geom.iterator(settings, model, multiprocessing.cpu_count())
if iterator.initialize():
    while True:
        # Use triangulation to build a BVH tree
        tree.add_entity(iterator.get())

        # Alternatively, use this code to build an unbalanced binary tree
        # tree.add_entity(iterator.get_native())

        if not iterator.next():
            break


# %% Find clashes
# TODO: Wrap it up to a function
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


# %% Build DataFrame
def _get_material(entity: ifcopenshell.entity_instance) -> str:
    material = None
    if entity.HasAssociations:
        for assoc in entity.HasAssociations:
            if assoc.is_a("IfcRelAssociatesMaterial"):
                material = assoc.RelatingMaterial.Name
                break
    return material


def _get_sizes(entity: ifcopenshell.entity_instance):
    sizes = {}
    if entity.IsDefinedBy:
        for definition in entity.IsDefinedBy:
            if definition.is_a("IfcRelDefinesByProperties"):
                prop_set = definition.RelatingPropertyDefinition
                if prop_set.is_a("IfcPropertySet"):
                    for prop in prop_set.HasProperties:
                        if prop.is_a("IfcPropertySingleValue") and prop.Name in [
                            "Height",
                            "Width",
                            "Length",
                            "Depth",
                        ]:
                            sizes[prop.Name] = prop.NominalValue.wrappedValue
    return sizes


def extract_entity(entity: ifcopenshell.entity_instance) -> dict:
    material = _get_material(entity).split("/", 1)
    return {
        "entity": entity.is_a(),
        "guid": entity.GlobalId,
        "material": material[0],
        "spec": material[1],
        "sizes": _get_sizes(entity),
    }


# TODO: Filter out by LxWxH
intersections = []
for clash in clashes:
    # Mean average of two points
    raw = {}
    raw["coords"] = [(lhs + rhs) / 2.0 for lhs, rhs in zip(clash.p1, clash.p2)]
    raw["distance"] = clash.distance
    raw["entities"] = [
        extract_entity(model.by_id(clash.a.id())),
        extract_entity(model.by_id(clash.b.id())),
    ]
    raw["clash_type"] = ["protrusion", "pierce", "collision", "clearance"][
        clash.clash_type
    ]
    intersections.append(raw)
intersections

# %%
# TODO: Merge close clashes which fit into the clash_size
clash_size = 0.1  # [m]

# %%
# TODO: Filter intersections out by LxWxH


# %% Group items by the combination of elem_a and elem_b materials
grouped = defaultdict(list)
for intersection in intersections:
    materials = sorted([entity["material"] for entity in intersection["entities"]])
    group = f"{materials[0]}-{materials[1]}"
    grouped[group].append(intersection)
dict(grouped)

# %%
